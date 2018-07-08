from projectmanager.models import Project


def get_projects_for_user(user_id):
    return (Project.objects.filter(project_managers__user__username__exact=user_id) | Project.objects.filter(
        resources__user__username__exact=user_id)).distinct()
