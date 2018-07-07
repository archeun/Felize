from django.contrib import admin

from .models import Organization, Employee, Client, Project, ProjectResource, UserStory, TaskStatus, Task, WorkEntry

admin.site.register(Organization)
admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(ProjectResource)
admin.site.register(UserStory)
admin.site.register(TaskStatus)
admin.site.register(Task)
admin.site.register(WorkEntry)
