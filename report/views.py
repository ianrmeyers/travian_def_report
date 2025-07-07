from django.http import HttpResponse, JsonResponse

from django.shortcuts import render
from django_tables2 import SingleTableView

from datetime import datetime, timedelta
import pytz

from .forms import AttackReportForm, EditNotesForm
from .models import AttackReport
from .tables import AttackReportsTable
from .filters import AttackReportsColumnFilter

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

import csv


def upload_attacks_view(request):
    if request.method == "POST":
        form = AttackReportForm(request.POST)
        if form.is_valid():
            uploaded_attacks = form.cleaned_data['uploaded_attacks']
            print(uploaded_attacks)

            AttackReport.objects.bulk_create(
                [AttackReport(
                    attack_id=attack['id'],
                    attack_type=attack['attack_type'],
                    attacking_player_name=attack['attacker'],
                    attacking_village_name=attack['attacking_village'],
                    attacking_village_coords_x=attack['attacking_village_x'],
                    attacking_village_coords_y=attack['attacking_village_y'],
                    defending_player_name=attack['defender'],
                    defending_village_name=attack['defending_village'],
                    defending_village_coords_x=attack['defending_village_x'],
                    defending_village_coords_y=attack['defending_village_y'],
                    arrival_time=attack['arrival_time'],
                    reported_time=attack['reported_time'],
                    last_checked_time=attack['last_checked_time'],
                    active_flag=attack['active_attack']

                ) for attack in uploaded_attacks]
            )

            return render(request, 'success.html')
    else:
        form = AttackReportForm()

    return render(request, 'report_form.html', {'form': form})


def edit_notes_view(request, attack_id=None):
    if attack_id:
        attack = AttackReport.objects.get(attack_id=attack_id)
    # print(attack_id)
    print("hello")

    if request.method == 'POST':
        print("hello")
        form = EditNotesForm(request.POST)

        if form.is_valid():
            submitter_notes = form.cleaned_data['submitter_notes']
            def_coord_notes = form.cleaned_data['def_coord_notes']

            attack.submitter_notes = submitter_notes
            attack.admin_notes = def_coord_notes
            attack.save()
            return render(request, 'report_list.html')
    else:
        print("hello3")
        form = EditNotesForm()

    print(form)
    return render(request, 'edit_notes_form.html', {'form': form})


class AttackReportsListView(SingleTableMixin, FilterView):
    model = AttackReport
    table_class = AttackReportsTable
    template_name = "report_list.html"

    filterset_class = AttackReportsColumnFilter

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            active_attacks = AttackReport.objects.filter(active_flag=True)
            server_tz = pytz.timezone("UTC")
            # current_time = datetime.now(tz=server_tz) + timedelta(0, 3600)
            current_time = datetime.now(tz=server_tz)
            print(current_time)

            for a in active_attacks:
                arrival_time = getattr(a, "arrival_time")
                if arrival_time.astimezone(server_tz) < current_time:
                    a.active_flag = False
                    a.save()

        return super(AttackReportsListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return AttackReport.objects.filter(active_flag=True)


def generate_csv_view(request):
    server_tz = pytz.timezone("UTC")
    timestamp = datetime.now(tz=server_tz) + timedelta(0, 3600)
    file_name = f"incoming_attacks-{timestamp}.csv"
    response = HttpResponse(content_type="text/csv",)
    response['Content-Disposition'] = f"attachment; filename={file_name}"

    writer = csv.writer(response)
    writer.writerow([
        'Attack ID',
        'Attack Type',
        'Attacker',
        'Attacker Village',
        'Attacker Coords X',
        'Attacker Coords y',
        'Defender',
        'Defender Village',
        'Defender Coords X',
        'Defender Coords Y',
        'Arrival Time',
        'Reported Time',
        'Last Checked Time',
        'Submitter Notes',
        'Defense Coord Notes'
    ])

    attacks = AttackReport.objects.all().values_list('attack_id',
                                                     'attack_type',
                                                     'attacking_player_name',
                                                     'attacking_village_name',
                                                     'attacking_village_coords_x',
                                                     'attacking_village_coords_y',
                                                     'defending_player_name',
                                                     'defending_village_name',
                                                     'defending_village_coords_x',
                                                     'defending_village_coords_y',
                                                     'arrival_time',
                                                     'reported_time',
                                                     'last_checked_time',
                                                     'submitter_notes',
                                                     'admin_notes')

    for attack in attacks:
        writer.writerow(attack)
    return response


def get_data_for_edit_modal(request, attack_id):
    attack = AttackReport.objects.get(attack_id=attack_id)
    response_data = {
        'attack_id': attack.attack_id,
        'submitter_notes': attack.submitter_notes,
        'def_coord_notes': attack.admin_notes
    }
    return JsonResponse(response_data)


def server_time(request):
    now = datetime.now()
    response_data = {'server_time': now.strftime('%H:%M:%S %d.%m')}
    return JsonResponse(response_data)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")