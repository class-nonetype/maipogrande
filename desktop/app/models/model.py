


class EnvironmentModel:

    attr = {}

    def set_attr(self, **kwargs):
        self.attr.update(
            kwargs
        )

        return self.attr



class Model:

    def __init__(self):
        
        self.EnvironmentModel = EnvironmentModel()
    