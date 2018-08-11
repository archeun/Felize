from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, ModelForm
from projectmanager.models import Task, WorkEntry, ProjectSprint, SprintMilestone


class ProjectSprintForm(ModelForm):
    class Meta:
        model = ProjectSprint
        fields = '__all__'

    def _clean_fields(self):
        pass


def get_sprint_milestones_form(sprint_form, is_project_manager, **kwargs):
    forms = inlineformset_factory(ProjectSprint, SprintMilestone, fields='__all__', extra=1, )(**kwargs)

    if not is_project_manager:
        for field in sprint_form.fields:
            sprint_form.fields[field].widget.attrs['disabled'] = True
            sprint_form.fields[field].required = False
        for form in forms:
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False

    return {'sprint_form': sprint_form, 'sprint_milestones_form_set': forms}
