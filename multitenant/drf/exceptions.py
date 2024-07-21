class MissingTenant(Exception):
    def __init__(self):
        super().__init__("Missing tenant at request")
