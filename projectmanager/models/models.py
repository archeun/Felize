import json

import reversion
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core import serializers


class BaseFelizeModel(models.Model):
    MODEL_DIFF_NEWLY_CREATED = 'NEW'
    MODEL_DIFF_NO_CHANGE = 'NO_CHANGE'
    MODEL_DIFF_CHANGE_TYPE_CREATED = 'Created'
    MODEL_DIFF_CHANGE_TYPE_CHANGED = 'Changed'
    MODEL_DIFF_FEED_ENTRY_ICON = 'pencil'

    class Meta:
        abstract = True

    def reversion_diff(self, old):
        current = json.loads(serializers.serialize("json", [self, ]))[0]['fields']
        diff = self.MODEL_DIFF_NEWLY_CREATED
        if old is not None:
            diff = {}
            for x in current:
                prepared_key = x
                if x not in old and x + '_id' in old:
                    prepared_key = x + '_id'
                if current[x] != old[prepared_key]:
                    diff[x] = {'current': current[x], 'old': old[prepared_key]}
        if diff == {}:
            return self.MODEL_DIFF_NO_CHANGE
        return diff

    def get_diff_feed_entry(self, old):
        entry = {}
        reversion_diff = self.reversion_diff(old)

        if reversion_diff == BaseFelizeModel.MODEL_DIFF_NO_CHANGE:
            return entry

        entry['object'] = self.__str__()
        entry['entry_icon'] = self.MODEL_DIFF_FEED_ENTRY_ICON
        entry['object_type_name'] = self._meta.verbose_name
        entry['object_url'] = self.get_absolute_url()
        entry['changed_attrs'] = []
        entry['changed_attr_values'] = []
        if reversion_diff == self.MODEL_DIFF_NEWLY_CREATED:
            entry['change_type'] = self.MODEL_DIFF_CHANGE_TYPE_CREATED
        else:
            entry['change_type'] = self.MODEL_DIFF_CHANGE_TYPE_CHANGED
            entry['changed_attrs'] = ", ".join(
                list(map(lambda field_name: self._meta.get_field(field_name).verbose_name, [*reversion_diff])))
            entry['changed_attr_values'] = ", ".join(map(str, [reversion_diff[k]['old'] for k in reversion_diff]))
        return entry

    def get_absolute_url(self):
        return None


class Organization(BaseFelizeModel):
    name = models.CharField(max_length=1000, blank=False, verbose_name='Name')

    class Meta:
        ordering = ('name',)
        verbose_name = "Organization"

    def __str__(self):
        return self.name


class Employee(BaseFelizeModel):
    employee_id = models.CharField(max_length=100, blank=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=False)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ('employee_id',)
        verbose_name = "Employee"

    def __str__(self):
        return self.get_full_name() + " (" + self.user.username + ")"

    def get_full_name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name


class Client(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name = "Client"

    def __str__(self):
        return self.name


@reversion.register()
class Project(BaseFelizeModel):
    MODEL_DIFF_FEED_ENTRY_ICON = 'building outline'

    code = models.CharField(max_length=10, blank=False, unique=True, verbose_name='Code')
    name = models.CharField(max_length=255, blank=False, verbose_name='Name')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Client')
    start_date = models.DateField(null=True, blank=True, verbose_name='Start Date')
    end_date = models.DateField(null=True, blank=True, verbose_name='End Date')
    approved_work_days = models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True,
                                             verbose_name='No. of Approved Days')
    ACTIVE = 'ACT'
    CLOSED = 'CLS'
    PROJECT_STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    )
    status = models.CharField(
        max_length=3,
        choices=PROJECT_STATUS_CHOICES,
        default=ACTIVE,
        verbose_name='Status'
    )
    project_managers = models.ManyToManyField(
        Employee,
        related_name='project_manager',
        through='ProjectManager',
        blank=True
    )
    resources = models.ManyToManyField(
        Employee,
        related_name='project_resource',
        through='ProjectResource',
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = "Project"

    def __str__(self):
        return "<" + self.client.name + "> " + self.code + " : " + self.name

    def get_absolute_url(self):
        return reverse("projectmanager:update_project", args=[self.id])


class ProjectResourceType(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=False, verbose_name='Name')

    class Meta:
        ordering = ('name',)
        verbose_name = "Resource Type"

    def __str__(self):
        return self.name


@reversion.register()
class ProjectSprint(BaseFelizeModel):
    MODEL_DIFF_FEED_ENTRY_ICON = 'stopwatch'

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Project')
    name = models.CharField(max_length=255, blank=False, verbose_name='Name')
    start_date = models.DateField(null=False, blank=False, verbose_name='Start Date')
    end_date = models.DateField(null=False, blank=False, verbose_name='End Date')
    ACTIVE = 'ACT'
    COMPLETED = 'CMP'
    PROJECT_SPRINT_STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
    )
    status = models.CharField(
        max_length=3,
        choices=PROJECT_SPRINT_STATUS_CHOICES,
        default=ACTIVE,
        verbose_name='Status'
    )

    class Meta:
        verbose_name = "Sprint"

    def __str__(self):
        return self.project.name + " : " + self.name

    def get_absolute_url(self):
        return reverse('projectmanager:update_sprint_milestones', kwargs={'pk': self.id})


class Attachment(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=True, verbose_name='Name')
    description = models.TextField(max_length=2048, blank=False, verbose_name='Description')
    url = models.CharField(max_length=2048, blank=True, verbose_name='url')
    file_path = models.CharField(max_length=2048, blank=True, verbose_name='File Path')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "Attachment"


class MilestoneType(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=False, verbose_name='Name')

    class Meta:
        verbose_name = "Milestone Type"


class MilestoneOwnerType(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=False, verbose_name='Name')

    class Meta:
        verbose_name = "Milestone Owner Type"


@reversion.register()
class SprintMilestone(BaseFelizeModel):
    MODEL_DIFF_FEED_ENTRY_ICON = 'certificate'

    sprint = models.ForeignKey(ProjectSprint, on_delete=models.CASCADE, verbose_name='Sprint')
    name = models.CharField(max_length=255, blank=False, verbose_name='Name')
    due_date = models.DateField(verbose_name='Due Date')
    type = models.ForeignKey(MilestoneType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Type')
    owner_type = models.ForeignKey(MilestoneOwnerType, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name='Owner Type')
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name='Assigned Employee')
    comment = models.TextField(max_length=2048, blank=True, verbose_name='Comment')

    PENDING = 'PND'
    IN_PROGRESS = 'INP'
    COMPLETED = 'CMP'
    PROJECT_MILESTONE_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In-Progress'),
        (COMPLETED, 'Completed'),
    )
    status = models.CharField(
        max_length=3,
        choices=PROJECT_MILESTONE_STATUS_CHOICES,
        default=PENDING,
        verbose_name='Status'
    )

    class Meta:
        verbose_name = "Milestone"

    def __str__(self):
        return self.sprint.__str__() + " : " + self.name


class MilestoneAttachment(BaseFelizeModel):
    milestone = models.ForeignKey(SprintMilestone, on_delete=models.CASCADE, verbose_name='Milestone')
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE, verbose_name='Attachment')

    class Meta:
        verbose_name = "Milestone Attachment"


@reversion.register()
class ProjectResource(BaseFelizeModel):
    MODEL_DIFF_FEED_ENTRY_ICON = 'users'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Employee')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Project')
    resource_type = models.ForeignKey(ProjectResourceType, on_delete=models.SET_NULL, null=True, verbose_name='Type')
    allocation_start_date = models.DateField(null=True, blank=True, verbose_name='Allocation Start Date')
    allocation_end_date = models.DateField(null=True, blank=True, verbose_name='Allocation Start Date')
    work_hours_per_day = models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True,
                                             verbose_name='Work Hrs./Day')

    class Meta:
        verbose_name = "Resource"

    def __str__(self):
        if self.resource_type:
            return self.employee.first_name + " : {" + self.project.__str__() + ": [" + self.resource_type.name + "]}"
        else:
            return self.employee.first_name + " : {" + self.project.__str__() + "}"

    def get_absolute_url(self):
        return reverse('projectmanager:update_project_resource', kwargs={'pk': self.id})


class ProjectManager(BaseFelizeModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Employee')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Project')

    class Meta:
        verbose_name = "Project Manager"

    def __str__(self):
        return self.employee.first_name + " : {" + self.project.__str__() + "}"


@reversion.register()
class UserStory(BaseFelizeModel):
    MODEL_DIFF_FEED_ENTRY_ICON = 'address card outline'

    title = models.CharField(max_length=1000, blank=False, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Project')

    class Meta:
        verbose_name = "User Story"

    def __str__(self):
        return self.project.name + " : " + self.title


class TaskStatus(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=False, verbose_name='Name')

    class Meta:
        ordering = ('name',)
        verbose_name = "Task Status"

    def __str__(self):
        return self.name


@reversion.register()
class Task(BaseFelizeModel):
    MODEL_DIFF_FEED_ENTRY_ICON = 'tasks'

    title = models.CharField(max_length=1000, blank=False, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE, verbose_name='User Story')
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, verbose_name='Status')
    owner = models.ForeignKey(ProjectResource, on_delete=models.CASCADE, default=None, null=True, verbose_name='Owner')
    estimated_time = models.IntegerField(verbose_name='Estimated Time')

    class Meta:
        verbose_name = "Task"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projectmanager:update_work_entries', kwargs={'pk': self.id})


@reversion.register()
class WorkEntry(BaseFelizeModel):
    MODEL_DIFF_FEED_ENTRY_ICON = 'pen square'

    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Task')
    worked_date = models.DateField(verbose_name='Worked Date')
    duration = models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True, verbose_name='Duration')
    comment = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Comment')

    class Meta:
        ordering = ('worked_date',)
        verbose_name = "Work Entry"

    def __str__(self):
        return self.task.title
