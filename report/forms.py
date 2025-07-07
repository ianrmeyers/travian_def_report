from django import forms
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import AttackReport
import pytz

import re


class EditNotesForm(forms.Form):
    attack_id = forms.IntegerField(label="Test")
    submitter_notes = forms.CharField(label="Test1")
    def_coord_notes = forms.CharField(label="Test2")

    def clean(self):
        self.cleaned_data['attack_id'] = self.attack_id
        self.cleaned_data['submitter_notes'] = self.submitter_notes
        self.cleaned_data['def_coord_notes'] = self.def_coord_notes


class AttackReportForm(forms.Form):
    page_source = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Paste Page Source Here',
                                                                         'class': 'upload-box-ta'}))
    last_checked_time = forms.DateTimeField(label="Last Checked Time", widget=DateTimePickerInput(
        format='%Y-%m-%d %H:%M',
        options={
            'format': 'YYYY-MM-DD HH:mm:ss',
            'showTodayButton': True,
            'sideBySide': True,
        }))

    # TODO: Input sanitation
    def clean(self):
        uploaded_attacks = self.process_html(self.cleaned_data.get('page_source'), self.cleaned_data.get('last_checked_time'))
        self.cleaned_data['uploaded_attacks'] = uploaded_attacks

    @staticmethod
    def process_html(html, last_checked_time):
        soup = BeautifulSoup(html, "html.parser")
        attacks = []

        attack_tables = soup.find_all(class_="troop_details inAttack")
        attack_tables += soup.find_all(class_="troop_details inRaid")

        defending_player_name = soup.find(class_="playerName").getText()

        defending_village_coords = None
        defending_village_name = None

        reported_time = int(soup.find(counting="up").get("value"))

        javascript_tags = soup.find_all("script")
        timezone_offset = 0
        for x in javascript_tags:
            if "Travian.Game.timezoneOffsetToUTC" in x.getText():
                timezone_offset = int(x.getText().split("=")[1].replace(";", "").strip())
                break

        server_tz = pytz.timezone("Europe/London")
        current_time = datetime.now(tz=server_tz)

        reported_time = datetime.utcfromtimestamp(reported_time - timezone_offset)

        for attack in attack_tables:
            arrival_countdown = int(attack.find(counting="down").get("value"))
            arrival_time = reported_time + timedelta(0, arrival_countdown)
            arrival_time_l = server_tz.localize(arrival_time)

            attack_id = attack.find_next(class_="markAttack").find_next("img").get("id").split("_")[1]

            # If Attack ID has been uploaded already, we skip this attack for upload
            if AttackReport.objects.filter(attack_id=attack_id).exists():
                continue

            attacker_village = attack.find_next(class_="role").find_next("a")
            attacker_village_name = attacker_village.getText()
            attacker_village_id = int(attacker_village.get("href").split("?d=")[1])
            attacker_village_x = int(attacker_village_id % 401 - 201)
            attacker_village_y = int(200 - (attacker_village_id - attacker_village_id % 401) / 401)
            attacker_coords = (attacker_village_x, attacker_village_y)
            attack_desc_text = attack.find_next(class_="markAttack").find_next_sibling().getText()

            pattern = re.compile(r"\b\sraids\s\b", re.IGNORECASE)
            if pattern.search(attack_desc_text):
                attack_type = "Raid"
                attack_desc = attack.find_next(class_="markAttack").find_next_sibling().getText().split("raids")
            else:
                attack_type = "Attack"
                attack_desc = attack.find_next(class_="markAttack").find_next_sibling().getText().split("attacks")

            attacking_player_name = attack_desc[0].strip()

            if defending_village_name:
                pass
            else:
                defending_village_name = attack_desc[1].strip()

            if defending_village_coords:
                pass
            else:
                defending_village_id = int(
                    attack.find_next(class_="markAttack").find_next_sibling().get("href").split("?d=")[1])
                defending_village_x = int(defending_village_id % 401 - 201)
                defending_village_y = int(200 - (defending_village_id - defending_village_id % 401) / 401)
                defending_village_coords = (defending_village_x, defending_village_y)

            attack = {
                'id': attack_id,
                'attack_type': attack_type,
                'attacker': attacking_player_name,
                'attacking_village': attacker_village_name,
                'attacking_village_x': attacker_coords[0],
                'attacking_village_y': attacker_coords[1],
                'defender': defending_player_name,
                'defending_village': defending_village_name,
                'defending_village_x': defending_village_coords[0],
                'defending_village_y': defending_village_coords[1],
                'arrival_time': arrival_time,
                'reported_time': reported_time,
                'last_checked_time': last_checked_time,
                'active_attack': True if current_time < arrival_time_l else False
            }
            attacks.append(attack)

        return attacks
