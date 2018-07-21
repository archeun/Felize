from django.forms import ModelForm, inlineformset_factory, DateField, Textarea, DateInput

from projectmanager.models import Task, ProjectResource


class ProjectResourceForm(ModelForm):
    class Meta:
        model = ProjectResource
        fields = '__all__'
        widgets = {
            'allocation_end_date': DateInput(attrs={'class': 'datepicker'}),
        }


ProjectResourceTaskFormSet = inlineformset_factory(
    ProjectResource, Task,
    fields='__all__',
    extra=1,
    widgets={
        'allocation_end_date': DateInput(attrs={'type': 'date'}),
    }
)
