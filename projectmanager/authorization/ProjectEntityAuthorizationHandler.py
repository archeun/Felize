from django.contrib.auth.models import User, Permission

from projectmanager.authorization.FelizeEntityAuthorizationHandler import FelizeEntityAuthorizationHandler
from projectmanager.models import Project


class ProjectEntityAuthorizationHandler(FelizeEntityAuthorizationHandler):

    def can_read(self, entity, user, **kwargs):
        return super(ProjectEntityAuthorizationHandler, self).can_read()

    def can_create(self, entity, user, **kwargs):
        return super().can_create(entity, user, **kwargs)

    def can_edit(self, entity, user, **kwargs):
        """

        :param Project entity:
        :param User user:
        :param kwargs:
        :return:
        """
        is_project_manager_of_project = Project.objects.filter(project_managers__user__id=user.id).count() > 0
        has_static_change_project_permissions = user.has_perm('projectmanager.change_project')
        return is_project_manager_of_project or has_static_change_project_permissions

    def can_delete(self, entity, user, **kwargs):
        return super().can_delete(entity, user, **kwargs)
