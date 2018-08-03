from django.urls import path

from projectmanager import views

urlpatterns = [
    path('work_entries/task_id/<int:pk>', views.WorkEntryUpdateView.as_view(),
         name='update_work_entries'),
    path('work_entries/create', views.WorkEntryCreateView.as_view(),
         name='create_work_entries'),
    path('work_entries/list/<int:pk>', views.WorkEntryListView.as_view(),
         name='work_entries_list'),
]
