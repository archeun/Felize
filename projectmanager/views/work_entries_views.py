from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView
from projectmanager.forms.TaskForm import get_work_entry_form, TaskForm
from projectmanager.model_filters.ProjectResourceFilter import ProjectResourceFilter
from projectmanager.models import WorkEntry, ProjectManager, Task
from projectmanager.services import project_service
from projectmanager.services.list_service import get_project_resource_list_config


class WorkEntryCreateView(CreateView):
    model = WorkEntry
    form_class = TaskForm
    template_name = 'projectmanager/work_entries/detail.html'

    def get_context_data(self, **kwargs):
        context = super(WorkEntryCreateView, self).get_context_data(**kwargs)
        project_manager_obj = ProjectManager.objects.filter(employee__id=self.request.user.employee.id).first()
        is_project_manager = project_manager_obj is not None
        if self.request.POST:
            forms = context['project_resource_tasks'] = get_work_entry_form(self.get_form(), False,
                                                                            is_project_manager,
                                                                            data=self.request.POST)
        else:
            forms = context['project_resource_tasks'] = get_work_entry_form(self.get_form(), False,
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
        return super(WorkEntryCreateView, self).form_valid(form)


class WorkEntryUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'projectmanager/work_entries/detail.html'

    def get_context_data(self, **kwargs):
        context = super(WorkEntryUpdateView, self).get_context_data(**kwargs)

        task = Task.objects.filter(id=self.kwargs['pk']).first()
        project = task.owner.project
        project_manager_obj = ProjectManager.objects.filter(employee__id=self.request.user.employee.id,
                                                            project_id=project.id).first()
        is_self = task.owner.employee.id == self.request.user.employee.id
        is_project_manager = project_manager_obj is not None

        context['project_name'] = project.name
        context['employee_name'] = self.request.user.employee.get_full_name()

        if self.request.POST:
            forms = get_work_entry_form(self.get_form(), is_self, is_project_manager,
                                        data=self.request.POST,
                                        instance=self.object)
        else:
            forms = get_work_entry_form(self.get_form(), is_self, is_project_manager, instance=self.object)

        context['work_entries'] = forms['work_entries_form_set']
        context['form'] = forms['task_form']

        return context

    def get(self, request, *args, **kwargs):
        project = Task.objects.filter(id=self.kwargs['pk']).first().owner.project

        projects_for_user = project_service.get_projects_for_user(request.user.id)
        if not projects_for_user.filter(id=project.id).first():
            return HttpResponse('Unauthorized', status=401)
        return super(WorkEntryUpdateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        work_entries = context['work_entries']
        with transaction.atomic():
            self.object = form.save()

            if work_entries.is_valid():
                work_entries.instance = self.object
                work_entries.save()
        return super(WorkEntryUpdateView, self).form_valid(form)


class WorkEntryListView(ListView):
    template_name = 'projectmanager/work_entries/list.html'
    queryset = []
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkEntryListView, self).get_context_data(**kwargs)
        project_resource_filter = ProjectResourceFilter(self.request.GET,
                                                        queryset=project_service.get_project_resources_for_project(
                                                            self.kwargs['pk']))
        url_params = self.request.GET.copy()
        if url_params.get('page'):
            del url_params['page']
        context['project_resource_list_config'] = get_project_resource_list_config({
            'name': 'Project Resources',
            'is_paginated': True,
            'url_encoded_filters': url_params.urlencode(),
            'add_object': {"url": reverse("projectmanager:create_project_resource"),
                           "button_tooltip": "Add Project Resource"}
        })
        filtered_project_resource_list = project_resource_filter.qs

        paginator = Paginator(filtered_project_resource_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            project_resources = paginator.page(page)
        except PageNotAnInteger:
            project_resources = paginator.page(1)
        except EmptyPage:
            project_resources = paginator.page(paginator.num_pages)
        context['project_resources'] = project_resources
        context['is_paginated'] = True
        context['project_resource_filter'] = project_resource_filter
        context['project_resource_filter_reset_url'] = reverse('projectmanager:project_resource_list',
                                                               kwargs={'pk': self.kwargs['pk']})
        return context

    def get_queryset(self):
        project_resources_filter = ProjectResourceFilter(self.request.GET,
                                                         queryset=project_service.get_project_resources_for_project(
                                                             self.kwargs['pk']))
        return project_resources_filter.qs
