from projectmanager.models import Project, ProjectManager, ProjectResource, Task


def get_projects_for_user(user_id):
    """
    Returns the list of projects accessible to the user who has the given user_id

    :param user_id:
    :return:
    """
    return (Project.objects.filter(project_managers__user__id=user_id) | Project.objects.filter(
        resources__user__username__exact=user_id)).distinct()


def get_project_resource_for_user(user, project_id):
    """
    Returns the ProjectResource for the given User and Project.id, if any exists. Otherwise false.
    :param user:
    :param project_id:
    :return ProjectResource:
    """
    return ProjectResource.objects.filter(employee_id=user.employee.id, project_id=project_id).first()


def save(project, update=True, project_managers=None, project_resources=None):
    """
    Saves or updates the given project object

    :param Project project:
    :param bool update:
    :param dict project_managers:
    :param dict project_resources:
    :return Project project:
    """

    if update:
        project.project_managers.clear()
        project.resources.clear()

    project.save()

    if project_managers is not None:
        for person in project_managers:
            project_manager = ProjectManager()
            project_manager.project = project
            project_manager.employee = person
            project_manager.save()

    if project_resources is not None:
        for person in project_resources:
            project_resource = ProjectResource()
            project_resource.project = project
            project_resource.employee = person
            project_resource.save()
    return project


def get_tasks_by_project_resource(prid):
    return Task.objects.filter(owner_id=prid).all()


def get_project_resource_by_id(prid):
    """

    Returns the ProjectResource having the given primary key
    :param prid:
    :return:
    :rtype: ProjectResource
    """
    return ProjectResource.objects.filter(id=prid).first()
