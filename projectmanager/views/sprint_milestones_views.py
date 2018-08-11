from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import UpdateView

from projectmanager.forms.MilestoneSprintSwitchForm import MilestoneSprintSwitchForm
from projectmanager.forms.SprintMilestones import get_sprint_milestones_form, ProjectSprintForm
from projectmanager.models import ProjectManager, Task, ProjectSprint
from projectmanager.services import project_service


class SprintMilestonesUpdateView(UpdateView):
    model = ProjectSprint
    form_class = ProjectSprintForm
    template_name = 'projectmanager/sprint_milestones/detail.html'

    def get_context_data(self, **kwargs):
        context = super(SprintMilestonesUpdateView, self).get_context_data(**kwargs)

        sprint = ProjectSprint.objects.filter(id=self.kwargs['pk']).first()
        project = sprint.project
        project_manager_obj = ProjectManager.objects.filter(employee__id=self.request.user.employee.id,
                                                            project_id=project.id).first()
        is_project_manager = project_manager_obj is not None

        context['sprint_milestone_switch_form'] = MilestoneSprintSwitchForm(project_id=project.id)
        context['project_name'] = project.name
        context['sprint'] = sprint

        if self.request.POST:
            forms = get_sprint_milestones_form(self.get_form(), is_project_manager,
                                               data=self.request.POST,
                                               instance=self.object)
        else:
            forms = get_sprint_milestones_form(self.get_form(), is_project_manager, instance=self.object)

        context['sprint_milestones'] = forms['sprint_milestones_form_set']
        context['exclude_milestone_form_fields'] = ['comment', 'owner_type', 'assigned_to']
        context['form'] = forms['sprint_form']

        return context

    def get(self, request, *args, **kwargs):
        project = ProjectSprint.objects.filter(id=self.kwargs['pk']).first().project

        projects_for_user = project_service.get_projects_for_user(request.user.id)
        if not projects_for_user.filter(id=project.id).first():
            return HttpResponse('Unauthorized', status=401)
        return super(SprintMilestonesUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST and 'switch-sprint-btn' in request.POST:
            switched_sprint = ProjectSprint.objects.get(id=request.POST['sprint'])
            return redirect(switched_sprint)
        return super(SprintMilestonesUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        work_entries = context['sprint_milestones']
        with transaction.atomic():
            self.object = form.save()

            if work_entries.is_valid():
                work_entries.instance = self.object
                work_entries.save()
        return super(SprintMilestonesUpdateView, self).form_valid(form)
