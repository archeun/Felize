from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from projectmanager.forms.ProjectResourceForm import ProjectResourceTaskFormSet, ProjectResourceForm
from projectmanager.models import ProjectResource
from projectmanager.services import project_service


def project_resource_task_breakdown(request, prid):
    projects_for_user = project_service.get_projects_for_user(request.user.id)
    project = projects_for_user.filter(projectresource__id=prid).first()
    if not projects_for_user.filter(projectresource__id=prid).first():
        return HttpResponse('Unauthorized', status=401)
    tasks = project_service.get_tasks_by_project_resource(prid)
    context = {'tasks': tasks, 'project_name': project.name,
               'employee_name': project_service.get_project_resource_by_id(prid).employee}

    return render(request, 'projectmanager/task_breakdown/update_project_resource_task_breakdown.html', context)


class ProjectResourceTaskCreate(CreateView):
    model = ProjectResource
    form_class = ProjectResourceForm
    success_url = reverse_lazy('projectmanager:create_project_resource_task_breakdown')
    template_name = 'projectmanager/task_breakdown/create_project_resource_task_breakdown.html'

    def get_context_data(self, **kwargs):
        data = super(ProjectResourceTaskCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['project_resource_tasks'] = ProjectResourceTaskFormSet(self.request.POST)
        else:
            data['project_resource_tasks'] = ProjectResourceTaskFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        project_resource_tasks = context['project_resource_tasks']
        with transaction.atomic():
            self.object = form.save()

            if project_resource_tasks.is_valid():
                project_resource_tasks.instance = self.object
                project_resource_tasks.save()
        return super(ProjectResourceTaskCreate, self).form_valid(form)


class ProjectResourceTaskUpdate(UpdateView):
    model = ProjectResource
    form_class = ProjectResourceForm
    success_url = reverse_lazy('projectmanager:create_project_resource_task_breakdown')
    template_name = 'projectmanager/task_breakdown/create_project_resource_task_breakdown.html'

    def get_context_data(self, **kwargs):
        data = super(ProjectResourceTaskUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['project_resource_tasks'] = ProjectResourceTaskFormSet(self.request.POST, instance=self.object)
        else:
            data['project_resource_tasks'] = ProjectResourceTaskFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        project_resource_tasks = context['project_resource_tasks']
        with transaction.atomic():
            self.object = form.save()

            if project_resource_tasks.is_valid():
                project_resource_tasks.instance = self.object
                project_resource_tasks.save()
        return super(ProjectResourceTaskUpdate, self).form_valid(form)
