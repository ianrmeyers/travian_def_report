from django.urls import path

from . import views

urlpatterns = [
    path("", views.upload_attacks_view, name="upload-attacks"),
    path("attacks/", views.AttackReportsListView.as_view(), name="incoming-attacks"),
    path("exportHistory/", views.generate_csv_view, name="export-history"),
    path("editNotes/<int:attack_id>", views.edit_notes_view, name='edit-notes'),
    path('server-time/', views.server_time, name="server_time"),
]