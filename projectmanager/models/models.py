import reversion
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core import serializers


class BaseFelizeModel(models.Model):
    class Meta:
        abstract = True

    def diff(self, old):
        return serializers.serialize("json", [self, ])


class Organization(BaseFelizeModel):
    name = models.CharField(max_length=1000, blank=False)

    class Meta:
        ordering = ('name',)

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

    def __str__(self):
        return self.get_full_name() + " (" + self.user.username + ")"

    def get_full_name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name


class Client(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


@reversion.register()
class Project(BaseFelizeModel):
    code = models.CharField(max_length=10, blank=False, unique=True)
    name = models.CharField(max_length=255, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    approved_work_days = models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)
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

    def __str__(self):
        return "<" + self.client.name + "> " + self.code + " : " + self.name

    def get_absolute_url(self):
        return reverse("projectmanager:update_project", args=[self.id])

    # def diff(self, old):
    #     return {
    #         'name': {'old': old['name'], 'new': self.name},
    #         'start_date': {'old': old['start_date'], 'new': self.start_date},
    #         'end_date': {'old': old['end_date'], 'new': self.end_date},
    #         'status': {'old': old['status'], 'new': self.status},
    #         'approved_work_days': {'old': old['approved_work_days'], 'new': self.approved_work_days},
    #     }


class ProjectResourceType(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


@reversion.register()
class ProjectSprint(BaseFelizeModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
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
    )

    def __str__(self):
        return self.project.name + " : " + self.name

    def get_absolute_url(self):
        return reverse('projectmanager:update_sprint_milestones', kwargs={'pk': self.id})

    # def diff(self, old):
    #     return {
    #         'name': {'old': old['name'], 'new': self.name},
    #         'start_date': {'old': old['start_date'], 'new': self.start_date},
    #         'end_date': {'old': old['end_date'], 'new': self.end_date},
    #         'status': {'old': old['status'], 'new': self.status},
    #     }


class Attachment(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=2048, blank=False)
    url = models.CharField(max_length=2048, blank=True)
    file_path = models.CharField(max_length=2048, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class MilestoneType(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=False)


class MilestoneOwnerType(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=False)


@reversion.register()
class SprintMilestone(BaseFelizeModel):
    sprint = models.ForeignKey(ProjectSprint, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    due_date = models.DateField()
    type = models.ForeignKey(MilestoneType, on_delete=models.SET_NULL, null=True, blank=True)
    owner_type = models.ForeignKey(MilestoneOwnerType, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(max_length=2048, blank=True)

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
    )

    def __str__(self):
        return self.sprint.__str__() + " : " + self.name

    # def diff(self, old):
    #     return {
    #         'name': {'old': old['name'], 'new': self.name},
    #         'due_date': {'old': old['due_date'], 'new': self.due_date},
    #         'type': {'old': old['type_id'], 'new': self.type},
    #         'owner_type': {'old': old['owner_type_id'], 'new': self.owner_type},
    #         'assigned_to': {'old': old['assigned_to_id'], 'new': self.assigned_to},
    #         'comment': {'old': old['comment'], 'new': self.comment},
    #         'status': {'old': old['status'], 'new': self.status},
    #     }


class MilestoneAttachment(BaseFelizeModel):
    milestone = models.ForeignKey(SprintMilestone, on_delete=models.CASCADE)
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)


@reversion.register()
class ProjectResource(BaseFelizeModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    resource_type = models.ForeignKey(ProjectResourceType, on_delete=models.SET_NULL, null=True)
    allocation_start_date = models.DateField(null=True, blank=True)
    allocation_end_date = models.DateField(null=True, blank=True)
    work_hours_per_day = models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)

    def __str__(self):
        if self.resource_type:
            return self.employee.first_name + " : {" + self.project.__str__() + ": [" + self.resource_type.name + "]}"
        else:
            return self.employee.first_name + " : {" + self.project.__str__() + "}"

    def get_absolute_url(self):
        return reverse('projectmanager:update_project_resource', kwargs={'pk': self.id})

    # def diff(self, old):
    #     return {
    #         'resource_type': {'old': old['resource_type'], 'new': self.resource_type},
    #         'allocation_start_date': {'old': old['allocation_start_date'], 'new': self.allocation_start_date},
    #         'allocation_end_date': {'old': old['allocation_end_date'], 'new': self.allocation_end_date},
    #         'work_hours_per_day': {'old': old['work_hours_per_day'], 'new': self.work_hours_per_day}
    #     }


class ProjectManager(BaseFelizeModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.first_name + " : {" + self.project.__str__() + "}"


@reversion.register()
class UserStory(BaseFelizeModel):
    title = models.CharField(max_length=1000, blank=False)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.name + " : " + self.title


class TaskStatus(BaseFelizeModel):
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


@reversion.register()
class Task(BaseFelizeModel):
    title = models.CharField(max_length=1000, blank=False)
    description = models.TextField()
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE)
    owner = models.ForeignKey(ProjectResource, on_delete=models.CASCADE, default=None, null=True)
    estimated_time = models.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projectmanager:update_work_entries', kwargs={'pk': self.id})

    # def diff(self, old):
    #     return {
    #         'title': {'old': old['title'], 'new': self.title},
    #         'description': {'old': old['description'], 'new': self.description},
    #         'status': {'old': old['status'], 'new': self.status},
    #         'owner': {'old': old['owner'], 'new': self.owner},
    #         'estimated_time': {'old': old['estimated_time'], 'new': self.estimated_time}
    #     }


@reversion.register()
class WorkEntry(BaseFelizeModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    worked_date = models.DateField()
    duration = models.DecimalField(null=True, max_digits=6, decimal_places=2, blank=True)
    comment = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        ordering = ('worked_date',)

    def __str__(self):
        return self.task.title

    # def diff(self, old):
    #     return {
    #         'worked_date': {'old': old['worked_date'], 'new': self.worked_date},
    #         'duration': {'old': old['duration'], 'new': self.duration},
    #         'comment': {'old': old['comment'], 'new': self.comment},
    #         'owner': {'old': old['owner'], 'new': self.owner}
    #     }
