from django import forms
from django.forms import inlineformset_factory

from projectmanager.models import Project, ProjectSprint


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

    def _clean_fields(self):
        super(ProjectForm, self)._clean_fields()
        for name, field in self.fields.items():
            if self.instance and self.instance.pk:
                return getattr(self.instance, name)
            else:
                return self.cleaned_data[name]


def get_project_sprint_form(project_form, is_project_manager, **kwargs):
    sprint_forms = inlineformset_factory(Project, ProjectSprint, fields='__all__', extra=1, )(**kwargs)

    if not is_project_manager:
        for field in project_form.fields:
            project_form.fields[field].widget.attrs['disabled'] = True
            project_form.fields[field].required = False
        for form in sprint_forms:
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False

    return {'project_form': project_form, 'sprint_form_set': sprint_forms}
