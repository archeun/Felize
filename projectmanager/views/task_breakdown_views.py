from django.db import transaction
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView
from projectmanager.forms.ProjectResourceForm import get_project_resource_tasks_form, ProjectResourceForm
from projectmanager.models import ProjectResource, ProjectManager
from projectmanager.services import project_service


class ProjectResourceTaskCreate(CreateView):
    model = ProjectResource
    form_class = ProjectResourceForm
    template_name = 'projectmanager/task_breakdown/create_project_resource_task_breakdown.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectResourceTaskCreate, self).get_context_data(**kwargs)
        project_manager_obj = ProjectManager.objects.filter(employee__id=self.request.user.employee.id).first()
        is_project_manager = project_manager_obj is not None
        if self.request.POST:
            forms = context['project_resource_tasks'] = get_project_resource_tasks_form(self.get_form(), False,
                                                                                        is_project_manager,
                                                                                        data=self.request.POST)
        else:
            forms = context['project_resource_tasks'] = get_project_resource_tasks_form(self.get_form(), False,
                                                                                        is_project_manager)

        context['project_resource_tasks'] = forms['task_form_set']
        context['form'] = forms['project_resource_form']
        return context

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
    template_name = 'projectmanager/task_breakdown/create_project_resource_task_breakdown.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectResourceTaskUpdate, self).get_context_data(**kwargs)

        project_resource = ProjectResource.objects.filter(id=self.kwargs['pk']).first()
        project = ProjectResource.objects.filter(id=self.kwargs['pk']).first().project
        project_manager_obj = ProjectManager.objects.filter(employee__id=self.request.user.employee.id,
                                                            project_id=project.id).first()
        is_self = project_resource.employee.id == self.request.user.employee.id
        is_project_manager = project_manager_obj is not None

        context['project_name'] = self.object.project.name
        context['employee_name'] = self.object.employee

        if self.request.POST:
            forms = get_project_resource_tasks_form(self.get_form(), is_self, is_project_manager,
                                                    data=self.request.POST,
                                                    instance=self.object)
        else:
            forms = get_project_resource_tasks_form(self.get_form(), is_self, is_project_manager, instance=self.object)

        context['project_resource_tasks'] = forms['task_form_set']
        context['form'] = forms['project_resource_form']

        return context

    def get(self, request, *args, **kwargs):
        project = ProjectResource.objects.filter(id=kwargs['pk']).first().project

        projects_for_user = project_service.get_projects_for_user(request.user.id)
        if not projects_for_user.filter(id=project.id).first():
            return HttpResponse('Unauthorized', status=401)
        return super(ProjectResourceTaskUpdate, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        project_resource_tasks = context['project_resource_tasks']
        with transaction.atomic():
            self.object = form.save()

            if project_resource_tasks.is_valid():
                project_resource_tasks.instance = self.object
                project_resource_tasks.save()
        return super(ProjectResourceTaskUpdate, self).form_valid(form)
