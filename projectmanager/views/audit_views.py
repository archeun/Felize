from django import forms
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.views import generic
from reversion.models import Version

from projectmanager.model_filters.VersionFilter import VersionFilter
from projectmanager.services.audit_service import get_previous_for_version, get_audit_feed_data
from projectmanager.services.list_service import get_audit_list_config


class AuditListView(generic.ListView):
    template_name = 'projectmanager/audit/list.html'
    queryset = Version.objects.all()
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AuditListView, self).get_context_data(**kwargs)

        audit_action_performed_user = forms.ModelChoiceField(queryset=User.objects.all())
        context['audit_action_performed_user_html'] = audit_action_performed_user.widget.render(
            'audit_action_performed_user', self.request.GET.get('audit_action_performed_user'))

        audit_filter = VersionFilter(self.request.GET, queryset=self.get_queryset())
        url_params = self.request.GET.copy()
        if url_params.get('page'):
            del url_params['page']

        audit_list_config = {
            'name': 'Audit List',
            'is_paginated': True,
            'url_encoded_filters': url_params.urlencode(),
        }

        context['audit_list_config'] = get_audit_list_config(audit_list_config)

        filtered_audit_list = audit_filter.qs

        paginator = Paginator(filtered_audit_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            audits = paginator.page(page)
        except PageNotAnInteger:
            audits = paginator.page(1)
        except EmptyPage:
            audits = paginator.page(paginator.num_pages)

        context['audits'] = audits
        context['is_paginated'] = True
        context['audit_filter'] = audit_filter
        context['audit_filter_reset_url'] = reverse('projectmanager:audit_list')
        return context

    def get_queryset(self):
        audit_action_performed_user = self.request.GET.get('audit_action_performed_user')
        if audit_action_performed_user == '' or audit_action_performed_user is None:
            return Version.objects.order_by('-revision__date_created').all()
        else:
            return Version.objects.order_by('-revision__date_created').filter(
                revision__user_id=audit_action_performed_user)


class AuditDetailView(generic.DetailView):
    template_name = 'projectmanager/audit/detail.html'
    model = Version

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AuditDetailView, self).get_context_data(**kwargs)
        post_data = context['version'].serialized_data
        previous = get_previous_for_version(context['version'].object, context['version'].revision.date_created)
        pre_data = "[]"
        if previous is not None:
            pre_data = previous.serialized_data
        context['object_name'] = context['version'].object
        context['changed_date'] = context['version'].revision.date_created
        context['changed_user'] = context['version'].revision.user
        context['entity_type'] = context['version'].content_type
        context['serialized_data'] = context['version'].serialized_data
        context['post_data'] = post_data
        context['pre_data'] = pre_data
        return context


class AuditFeedView(generic.ListView):
    template_name = 'projectmanager/audit/feed.html'
    queryset = Version.objects.order_by('-revision__date_created').all()
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AuditFeedView, self).get_context_data(**kwargs)
        context['audit_feed'] = get_audit_feed_data(context['object_list'])
        return context
