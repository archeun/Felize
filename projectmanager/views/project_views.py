import time
from datetime import timedelta, datetime, date

from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.urls import reverse
from django.views.generic.edit import ModelFormMixin

from projectmanager.forms.ProjectForm import ProjectForm, get_project_inline_forms
from projectmanager.model_filters import ProjectFilter
from projectmanager.models import Project, ProjectManager, WorkEntry, Task
from django.views import generic
from projectmanager.authorization.authorization_service import FelizePermissionRequiredMixin, is_user_project_manager, \
    is_entity_accessible
from projectmanager.services.list_service import get_project_list_config
import projectmanager.services.project_service as project_service
from django.contrib import messages
from reversion.views import RevisionMixin


class ProjectListView(generic.ListView):
    template_name = 'projectmanager/project/list.html'
    queryset = []
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        project_filter = ProjectFilter(self.request.GET,
                                       queryset=project_service.get_projects_for_user(self.request.user.id))
        url_params = self.request.GET.copy()
        if url_params.get('page'):
            del url_params['page']

        project_list_config = {
            'name': 'Projects List',
            'is_paginated': True,
            'url_encoded_filters': url_params.urlencode(),
        }

        is_project_manager = is_user_project_manager(self.request.user.id)
        if is_project_manager:
            project_list_config['add_object'] = {"url": reverse("projectmanager:create_project"),
                                                 "button_tooltip": "Add Project"}

        context['project_list_config'] = get_project_list_config(project_list_config)

        filtered_project_list = project_filter.qs

        paginator = Paginator(filtered_project_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            projects = paginator.page(page)
        except PageNotAnInteger:
            projects = paginator.page(1)
        except EmptyPage:
            projects = paginator.page(paginator.num_pages)

        context['projects'] = projects
        context['is_paginated'] = True
        context['project_filter'] = project_filter
        context['project_filter_reset_url'] = reverse('projectmanager:project_list')
        return context

    def get_queryset(self):
        project_filter = ProjectFilter(self.request.GET,
                                       queryset=project_service.get_projects_for_user(self.request.user.id))
        return project_filter.qs


class ProjectUpdateView(SuccessMessageMixin, RevisionMixin, generic.UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = 'projectmanager/project/detail.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not is_entity_accessible(self.object, self.request.user, 'edit'):
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        project_service.save(self.object, update=True, project_managers=form.cleaned_data['project_managers'],
                             project_resources=form.cleaned_data['resources'])

        messages.success(self.request, 'Successfully Updated')
        context = self.get_context_data()
        project_sprints = context['project_sprints']
        user_stories = context['user_stories']
        with transaction.atomic():
            if project_sprints.is_valid():
                project_sprints.instance = self.object
                project_sprints.save()
            if user_stories.is_valid():
                user_stories.instance = self.object
                user_stories.save()
        return super(ModelFormMixin, self).form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)

        is_project_resource = project_service.get_project_resource_for_user(self.request.user,
                                                                            context['project'].id)

        project_manager_obj = ProjectManager.objects.filter(employee__id=self.request.user.employee.id,
                                                            project_id=context['project'].id).first()
        is_project_manager = project_manager_obj is not None

        context['can_edit'] = is_entity_accessible(context['project'], self.request.user, 'edit')
        if is_project_resource:
            context['project_resource_task_breakdown_url'] = reverse(
                'projectmanager:update_project_resource', kwargs={'pk': is_project_resource.id}
            )
        if self.request.POST:
            forms = get_project_inline_forms(self.get_form(), is_project_manager,
                                             data=self.request.POST,
                                             instance=self.object)
        else:
            forms = get_project_inline_forms(self.get_form(), is_project_manager, instance=self.object)

        context['project_sprints'] = forms['sprint_form_set']
        context['user_stories'] = forms['user_story_form_set']
        context['form'] = forms['project_form']
        return context


class ProjectCreateView(FelizePermissionRequiredMixin, SuccessMessageMixin, RevisionMixin, generic.CreateView):
    model = Project
    fields = '__all__'
    template_name = 'projectmanager/project/detail.html'
    custom_permission_check = 'is_project_manager'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context['can_edit'] = context['is_user_project_manager'] = is_user_project_manager(self.request.user.id)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        project_service.save(self.object, update=False, project_managers=form.cleaned_data['project_managers'],
                             project_resources=form.cleaned_data['resources'])
        messages.success(self.request, 'Successfully Saved')
        return super(ModelFormMixin, self).form_valid(form)


class ProjectWorksheetView(generic.ListView):
    template_name = 'projectmanager/project/worksheet.html'
    queryset = []
    filters = {
        'start_date': date(2018, 7, 17),
        'end_date': date(2018, 8, 31),
        'employee_ids': ['10', '12'],
        'user_story_ids': ['4', '5', '6'],
        'status_ids': ['1', '2', '3', '4', '5', '6'],
        'resource_type_ids': ['1', '2', '3', '4', '5'],
        'due_date': date(2018, 8, 25),
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectWorksheetView, self).get_context_data(**kwargs)
        project = Project.objects.filter(id=self.kwargs['pk']).first()
        start_date = self.filters['start_date']
        if project.start_date > self.filters['start_date']:
            start_date = project.start_date
        end_date = self.filters['end_date']
        if project.end_date < self.filters['end_date']:
            end_date = project.end_date
        project_duration = end_date - start_date
        context['project_name'] = project.name
        context['project_days'] = []
        context['today'] = date.today()
        for i in range(project_duration.days + 1):
            context['project_days'].append((start_date + timedelta(i)).strftime('%Y-%m-%d'))

        context['task_work_entries'] = project_service.get_prepared_work_entries_for_date_range(
            context['task_list'], context['project_days'])
        return context

    def get_queryset(self):
        wo_filters = Task.objects.filter()
        # w_filters = Task.objects.filter(
        #     user_story__project_id=self.kwargs['pk'],
        #     workentry__worked_date__gte=self.filters['start_date'],
        #     workentry__worked_date__lte=self.filters['end_date'],
        #     owner__employee_id__in=self.filters['employee_ids'],
        #     user_story_id__in=self.filters['user_story_ids'],
        #     status_id__in=self.filters['status_ids'],
        #     owner__resource_type_id__in=self.filters['resource_type_ids'],
        #     due_date=self.filters['due_date']
        # ).distinct()
        return wo_filters
