from django.contrib import admin

from .models import Organization, Employee, Client, Project, ProjectMilestone, ProjectSprint, MilestoneType, \
    MilestoneOwnerType, MilestoneAttachment, ProjectResource, ProjectManager, UserStory, TaskStatus, \
    Task, WorkEntry, ProjectResourceType, Attachment

admin.site.register(Organization)
admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(ProjectMilestone)
admin.site.register(ProjectSprint)
admin.site.register(MilestoneType)
admin.site.register(MilestoneOwnerType)
admin.site.register(MilestoneAttachment)
admin.site.register(ProjectResourceType)
admin.site.register(ProjectResource)
admin.site.register(ProjectManager)
admin.site.register(UserStory)
admin.site.register(TaskStatus)
admin.site.register(Task)
admin.site.register(WorkEntry)
admin.site.register(Attachment)
