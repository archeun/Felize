from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, ModelForm
from projectmanager.models import Task, WorkEntry


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def _clean_fields(self):
        for name, field in self.fields.items():
            if name == 'title' or name == 'description' or name == 'owner':
                continue
            elif field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            try:
                value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError as e:
                print(name, e)
                self.add_error(name, e)


def get_work_entry_form(task_form, is_self, is_project_manager, **kwargs):
    forms = inlineformset_factory(Task, WorkEntry, fields='__all__', extra=1, )(**kwargs)

    for form in forms:
        if not is_self and not is_project_manager:
            for field in form.fields:
                form.fields[field].widget.attrs['disabled'] = True
                form.fields[field].required = False

    if is_self or (not is_self and not is_project_manager):
        for field in task_form.fields:
            task_form.fields[field].widget.attrs['disabled'] = True
            task_form.fields[field].required = False

    return {'task_form': task_form, 'work_entries_form_set': forms}
