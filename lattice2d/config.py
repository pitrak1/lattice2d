class InnerConfig:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class Config(InnerConfig):
    def __init__(self, data=None):
        super().__init__()
        if data:
            self.command_types = data.get('command_types', [])
            self.log_level = data.get('log_level', -1)

TEST_CONFIG = {
    'command_types': [
        'some_command_type',
        'some_other_command_type'
    ],
    'log_level': -1
}


GRID_WIDTH = 10
GRID_HEIGHT = 10

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
