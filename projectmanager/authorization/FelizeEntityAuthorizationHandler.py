class FelizeEntityAuthorizationHandler:
    def can_read(self, entity, user, **kwargs):
        return True

    def can_create(self, entity, user, **kwargs):
        return True

    def can_edit(self, entity, user, **kwargs):
        return True

    def can_delete(self, entity, user, **kwargs):
        return True
