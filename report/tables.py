import django_tables2 as tables
from .models import AttackReport
from django_tables2 import A


style = {'class': 'table table-hover table-striped table-light'}
lowercase = {'td': {'style': 'text-transform:lowercase'}}


class DateTimeColumn(tables.Column):
    def render(self, value):
        return value.strftime("%H:%M:%S %d.%m")


class NotesColumn(tables.Column):
    def render(self, value):
        return value


class AttackReportsTable(tables.Table):

    table = tables.Table

    attacker_coords_column = tables.Column(accessor='combine_attacker_coords', verbose_name="Attacker Coords")
    defender_coords_column = tables.Column(accessor='combine_defender_coords', verbose_name="Defender Coords")
    arrival_time = DateTimeColumn()
    reported_time = DateTimeColumn()
    last_checked_time = DateTimeColumn()
    submitter_notes = NotesColumn()
    admin_notes = NotesColumn()
    edit = tables.TemplateColumn(verbose_name="Edit",
                                 template_name='edit_button.html',
                                 orderable=False)

    class Meta:
        model = AttackReport
        fields = ['attack_id',
                  'attack_type',
                  'attacking_player_name',
                  'attacking_village_name',
                  'attacker_coords_column',
                  'defending_player_name',
                  'defending_village_name',
                  'defender_coords_column',
                  'arrival_time',
                  'reported_time',
                  'last_checked_time',
                  'submitter_notes',
                  'admin_notes']
        exclude = ('id', 'attacking_village_coords_x', 'attacking_village_coords_y', 'defending_village_coords_x', 'defending_village_coords_y')
        attrs = style
        order_by = 'attack_id'
        row_attrs = {
            "data-id": lambda record: record.attack_id
        }
