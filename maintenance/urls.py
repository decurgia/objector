from django.urls import path
from . import views

app_name = "maintenance"

urlpatterns = [
    path("task/", views.TaskFilterView.as_view(), name="task-list"),
    path(
        "task/add/",
        views.TaskCreateView.as_view(),
        name="task-create",
    ),
    path(
        "task/<int:pk>/",
        views.TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "task/<int:pk>/change/",
        views.TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "task/<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="task-delete",
    ),
    path("journal/", views.JournalFilterView.as_view(), name="journal-list"),
    path(
        "journal/add",
        views.JournalCreate.as_view(),
        name="journal-create",
    ),
    path(
        "journal/<int:pk>/",
        views.JournalDetailView.as_view(),
        name="journal-detail",
    ),
    path(
        "journal/<int:pk>/change/",
        views.JournalUpdateView.as_view(),
        name="journal-update",
    ),
    path(
        "journal/<int:pk>/delete/",
        views.JournalDeleteView.as_view(),
        name="journal-delete",
    ),
    path(
        "trigger/add",
        views.TriggerCreateView.as_view(),
        name="trigger-create",
    ),
    path(
        "trigger/<int:pk>/",
        views.TriggerDetailView.as_view(),
        name="trigger-detail",
    ),
    path(
        "trigger/<int:pk>/change/",
        views.TriggerUpdateView.as_view(),
        name="trigger-update",
    ),
    path(
        "trigger/<int:pk>/delete/",
        views.TriggerDeleteView.as_view(),
        name="trigger-delete",
    ),
]
