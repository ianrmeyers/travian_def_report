from django.db import models


class AttackReport(models.Model):

    attack_id = models.IntegerField(verbose_name="Attack ID")
    attack_type = models.CharField(verbose_name="Attack Type", max_length=6, default="Attack")
    attacking_player_name = models.CharField(max_length=30, verbose_name="Attacker")
    attacking_village_name = models.CharField(max_length=30, verbose_name="Attacker Village")
    attacking_village_coords_x = models.IntegerField()
    attacking_village_coords_y = models.IntegerField()

    defending_player_name = models.CharField(max_length=30, verbose_name="Defender")
    defending_village_name = models.CharField(max_length=30, verbose_name="Defender Village")
    defending_village_coords_x = models.IntegerField()
    defending_village_coords_y = models.IntegerField()

    arrival_time = models.DateTimeField(verbose_name="Arrival Time")
    reported_time = models.DateTimeField(verbose_name="Reported Time")
    last_checked_time = models.DateTimeField(verbose_name="Last Checked Time", null=True)

    submitter_notes = models.CharField(max_length=100, verbose_name="Submitter Notes")
    admin_notes = models.CharField(max_length=200, verbose_name="Defense Coord Notes")

    active_flag = models.BooleanField(default=True)

    def combine_attacker_coords(self):
        return f"{self.attacking_village_coords_x}|{self.attacking_village_coords_y}"

    def combine_defender_coords(self):
        return f"{self.defending_village_coords_x}|{self.defending_village_coords_y}"
