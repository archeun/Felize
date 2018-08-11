from django.urls import path

from projectmanager import views

urlpatterns = [
    path('milestones/sprint_id/<int:pk>', views.SprintMilestonesUpdateView.as_view(),
         name='update_sprint_milestones'),
]
