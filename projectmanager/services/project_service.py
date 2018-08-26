from projectmanager.models import Project, ProjectManager, ProjectResource, Task


def get_projects_for_user(user_id):
    """
    Returns the list of projects accessible to the user who has the given user_id

    :param user_id:
    :return:
    """
    return (Project.objects.filter(project_managers__user__id=user_id) | Project.objects.filter(
        resources__user__id=user_id)).distinct()


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

    project.save()

    if update:
        for project_manager in project.project_managers.all():
            pm_employee_id = project_manager.id
            should_delete = True
            for saved_project_manager in project_managers:
                if saved_project_manager.id == pm_employee_id:
                    should_delete = False
            if should_delete:
                pm_to_delete = ProjectManager.objects.get(project_id=project.id, employee_id=pm_employee_id)
                pm_to_delete.delete()

        for project_resource in project.resources.all():
            pr_employee_id = project_resource.id
            should_delete = True
            for saved_project_resource in project_resources:
                if saved_project_resource.id == pr_employee_id:
                    should_delete = False
            if should_delete:
                pr_to_delete = ProjectResource.objects.get(project_id=project.id, employee_id=pr_employee_id)
                pr_to_delete.delete()

    if project_managers is not None:
        for person in project_managers:
            if ProjectManager.objects.filter(project_id=project.id, employee_id=person.id).first() is None:
                project_manager = ProjectManager()
                project_manager.project = project
                project_manager.employee = person
                project_manager.save()

    if project_resources is not None:
        for person in project_resources:
            if ProjectResource.objects.filter(project_id=project.id, employee_id=person.id).first() is None:
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


def get_project_resources_for_project(project_id):
    """

    Returns the ProjectResource set in the Project for the given project_id
    :param project_id:
    :return:
    """
    return ProjectResource.objects.filter(project_id=project_id)


def get_prepared_work_entries_for_date_range(tasks, project_dates):
    """

    Returns the dict of work entries for each day thoughout the project duration
    :param tasks:
    :param project_dates:
    :return:
    """
    task_work_entries = {}
    for task in tasks:
        task_work_entries[task.id] = {'total_work_hours': 0}
        total_work_hours = 0
        for work_entry in task.workentry_set.all():
            duration = work_entry.duration
            total_work_hours += duration
            for project_day in project_dates:
                if project_day not in task_work_entries[task.id]:
                    task_work_entries[task.id][project_day] = ''
                if project_day == work_entry.worked_date.strftime('%Y-%m-%d'):
                    if task_work_entries[task.id][project_day] == '':
                        task_work_entries[task.id][project_day] = work_entry.duration
                    else:
                        task_work_entries[task.id][project_day] += work_entry.duration
        task_work_entries[task.id]['total_work_hours'] = total_work_hours
        task_work_entries[task.id]['learning_hours'] = total_work_hours - min(task.estimated_time, total_work_hours)
    return task_work_entries
