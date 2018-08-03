from functools import reduce

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Model

from projectmanager.models import Project
from projectmanager.utils.felize import felize_module_import


class FelizePermissionRequiredMixin(PermissionRequiredMixin):
    custom_permission_check = None

    def has_permission(self):
        has_static_permission = False
        has_runtime_permission = False

        if self.permission_required is not None:
            has_static_permission = super(FelizePermissionRequiredMixin, self).has_permission()
        if self.custom_permission_check is not None:
            check_permission_function = getattr(self, self.custom_permission_check)
            has_runtime_permission = check_permission_function()

        return has_static_permission or has_runtime_permission

    def is_project_manager(self):
        return is_user_project_manager(self.request.user.id)


def is_user_project_manager(user_id):
    """

    Returns true if the User given by the user_id is assigned as a Project Manager to at least one Project
    :param user_id:
    :return:
    """
    return Project.objects.filter(project_managers__user__id=user_id).count() > 0


def is_entity_accessible(entity, user, access_type='read'):
    """

    Returns True if the given user has edit permissions to the given Entity. It checks for both static and dynamic
    permissions
    :param access_type:
    :param Model entity:
    :param User user:
    :return:
    """

    is_accessible = False

    class_name = '{0}EntityAuthorizationHandler'.format(entity.__class__.__name__)

    auth_handler = felize_module_import('projectmanager.authorization'.format(class_name))
    auth_handler_class = getattr(auth_handler, class_name)
    auth_handler_instance = auth_handler_class()

    if access_type == 'read':
        is_accessible = auth_handler_instance.can_read(entity, user)
    elif access_type == 'create':
        is_accessible = auth_handler_instance.can_create(entity, user)
    elif access_type == 'edit':
        is_accessible = auth_handler_instance.can_edit(entity, user)
    elif access_type == 'delete':
        is_accessible = auth_handler_instance.can_delete(entity, user)

    return is_accessible
