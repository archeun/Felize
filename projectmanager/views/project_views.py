from projectmanager.models import Project
from django.views import generic

from projectmanager.services.project_service import get_projects_for_user


class ProjectListView(generic.ListView):
    template_name = 'projectmanager/project/index.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return get_projects_for_user(self.request.user)


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'projectmanager/project/detail.html'
