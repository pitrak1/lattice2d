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
            self.ip_address = data.get('ip_address', '0.0.0.0')
            self.port = data.get('port', 8080)

            full_solution = data.get('full_solution')
            if full_solution:
                self.command_types = self.command_types + FULL_COMMAND_TYPES
                self.window_width = full_solution.get('window_width', 1280)
                self.window_height = full_solution.get('window_height', 720)
                self.client_starting_state = full_solution['client_starting_state']
                self.server_starting_state = full_solution.get('server_starting_state', None)
                self.group_count = full_solution.get('group_count', 6)
                self.network = full_solution.get('network', False)

FULL_COMMAND_TYPES = [
    'broadcast_players_in_game',
    'redraw',
    'activate',
    'close',
    'context_lost',
    'context_state_lost',
    'deactivate',
    'expose',
    'hide',
    'key_press',
    'key_release',
    'mouse_drag',
    'mouse_enter',
    'mouse_leave',
    'mouse_motion',
    'mouse_press',
    'mouse_release',
    'mouse_scroll',
    'move',
    'resize',
    'show',
    'text',
    'text_motion',
    'text_motion_select'
]

TEST_CONFIG = {
    'command_types': [
        'some_command_type',
        'some_other_command_type'
    ]
}

BUILT_IN_ASSETS = {
    'grey_panel': { 'location': 'lattice2d/panels/grey_panel.png', 'type': '9-tile' }
}

GRID_WIDTH = 10
GRID_HEIGHT = 10

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
