from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from projectmanager.model_filters import ProjectFilter
from projectmanager.models import Project
from django.views import generic

from projectmanager.services.list_service import get_project_list_config
from projectmanager.services.project_service import get_projects_for_user


class ProjectListView(generic.ListView):
    template_name = 'projectmanager/project/list.html'
    queryset = []
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        project_filter = ProjectFilter(self.request.GET, queryset=get_projects_for_user(self.request.user))
        url_params = self.request.GET.copy()
        if url_params.get('page'):
            del url_params['page']
        context['project_list_config'] = get_project_list_config({
            'name': 'Projects List',
            'is_paginated': True,
            'url_encoded_filters': url_params.urlencode()
        })
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
        project_filter = ProjectFilter(self.request.GET, queryset=get_projects_for_user(self.request.user))
        return project_filter.qs


class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'projectmanager/project/detail.html'
