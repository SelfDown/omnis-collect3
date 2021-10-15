from collect.service_imp.model.model_save import ModelSaveService


class EmptyService(ModelSaveService):
    def __init__(self, op_user):
        ModelSaveService.__init__(self, op_user)

        pass

    def result(self, params=None):
        return self.success({})
