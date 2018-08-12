from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.urls import reverse
from django.views.generic.edit import ModelFormMixin

from projectmanager.forms.ProjectForm import ProjectForm, get_project_sprint_form
from projectmanager.model_filters import ProjectFilter
from projectmanager.models import Project, ProjectManager
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
        with transaction.atomic():
            if project_sprints.is_valid():
                project_sprints.instance = self.object
                project_sprints.save()
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
            forms = get_project_sprint_form(self.get_form(), is_project_manager,
                                            data=self.request.POST,
                                            instance=self.object)
        else:
            forms = get_project_sprint_form(self.get_form(), is_project_manager, instance=self.object)

        context['project_sprints'] = forms['sprint_form_set']
        context['form'] = forms['project_form']
        return context


class ProjectCreateView(FelizePermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Project
    fields = '__all__'
    template_name = 'projectmanager/project/detail.html'
    custom_permission_check = 'is_user_project_manager'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        context['is_user_project_manager'] = is_user_project_manager(self.request.user.id)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        project_service.save(self.object, update=False, project_managers=form.cleaned_data['project_managers'],
                             project_resources=form.cleaned_data['resources'])
        messages.success(self.request, 'Successfully Saved')
        return super(ModelFormMixin, self).form_valid(form)
