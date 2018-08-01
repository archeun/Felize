from django.forms import inlineformset_factory, ModelForm
from projectmanager.models import Task, ProjectResource


class ProjectResourceForm(ModelForm):
    class Meta:
        model = ProjectResource
        fields = '__all__'

    def _clean_fields(self):
        super(ProjectResourceForm, self)._clean_fields()
        for name, field in self.fields.items():
            if self.instance and self.instance.pk:
                return getattr(self.instance, name)
            else:
                return self.cleaned_data[name]


def get_project_resource_tasks_form(project_resource_form, is_self, is_project_manager, **kwargs):
    forms = inlineformset_factory(ProjectResource, Task, fields='__all__', extra=1, )(**kwargs)

    for form in forms:
        if 'instance' in kwargs:
            form.fields['user_story'].queryset = kwargs['instance'].project.userstory_set.all()
        if not is_self and not is_project_manager:
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False

    if is_self or (not is_self and not is_project_manager):
        for field in project_resource_form.fields:
            project_resource_form.fields[field].widget.attrs['disabled'] = True
            project_resource_form.fields[field].required = False

    return {'project_resource_form': project_resource_form, 'task_form_set': forms}
