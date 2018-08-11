from django import forms

from projectmanager.models import Task, ProjectSprint


class MilestoneSprintSwitchForm(forms.Form):
    task = forms.ModelChoiceField(queryset=ProjectSprint.objects)

    def __init__(self, *args, **kwargs):
        self.project_id = kwargs.pop('project_id')
        super(MilestoneSprintSwitchForm, self).__init__(*args, **kwargs)
        self.fields['sprint'] = forms.ModelChoiceField(queryset=ProjectSprint.objects.filter(project_id=self.project_id))
