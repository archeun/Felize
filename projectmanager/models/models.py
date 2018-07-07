from django.contrib.auth.models import User
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=1000, blank=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Employee(models.Model):
    employee_id = models.CharField(max_length=100, blank=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=False)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ('employee_id',)

    def __str__(self):
        return self.first_name + " : " + self.last_name + " (" + self.user.username + ")"


class Client(models.Model):
    name = models.CharField(max_length=255, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Project(models.Model):
    code = models.CharField(max_length=5, blank=False, unique=True)
    name = models.CharField(max_length=255, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project_managers = models.ManyToManyField(
        Employee,
        related_name='project_manager',
        through='ProjectManager',
    )
    resources = models.ManyToManyField(
        Employee,
        related_name='project_resource',
        through='ProjectResource',
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "<" + self.client.name + "> " + self.code + " : " + self.name


class ProjectResource(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.first_name + " : {" + self.project.__str__() + "}"


class ProjectManager(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.employee.first_name + " : {" + self.project.__str__() + "}"


class UserStory(models.Model):
    title = models.CharField(max_length=1000, blank=False)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.name + " : " + self.title


class TaskStatus(models.Model):
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=1000, blank=False)
    description = models.TextField()
    user_story = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE)
    owner = models.ForeignKey(ProjectResource, on_delete=models.CASCADE, default=None, null=True)
    estimated_time = models.IntegerField()

    def __str__(self):
        return self.title


class WorkEntry(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    worked_date = models.DateField()
    duration = models.IntegerField()

    class Meta:
        ordering = ('worked_date',)

    def __str__(self):
        return self.task.title
