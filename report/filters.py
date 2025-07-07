# from django_filters.views import FilterView
# from django_tables2.views import SingleTableMixin
from django_filters import FilterSet, CharFilter
from .models import AttackReport


class AttackReportsColumnFilter(FilterSet):

    attack_type = CharFilter(label="Attack Type", lookup_expr="icontains")
    attacking_player_name = CharFilter(label="Attacker", lookup_expr="icontains")
    attacking_village_name = CharFilter(label="Attacker Village", lookup_expr="icontains")
    defending_player_name = CharFilter(label="Defender", lookup_expr="icontains")
    defending_village_name = CharFilter(label="Defender Village", lookup_expr="icontains")

    class Meta:
        model = AttackReport
        fields = {

        }

    # def __init__(self, *args, **kwargs):
    #     super(AttackReportsColumnFilter, self).__init__(*args, **kwargs)
    #     self.filters['attack_id'].label="Attack ID"
    #     self.filters['attack_type'].label = "Attack Type"
