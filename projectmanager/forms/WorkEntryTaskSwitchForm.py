from django import forms

from projectmanager.models import Task


class WorkEntryTaskSwitchForm(forms.Form):
    task = forms.ModelChoiceField(queryset=Task.objects)

    def __init__(self, *args, **kwargs):
        self.user_story_id = kwargs.pop('user_story_id')
        super(WorkEntryTaskSwitchForm, self).__init__(*args, **kwargs)
        self.fields['task'] = forms.ModelChoiceField(queryset=Task.objects.filter(user_story_id=self.user_story_id))
