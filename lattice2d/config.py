class InnerConfig:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

class Config(InnerConfig):
    def __init__(self, data=None):
        super().__init__()
        if data:
            self.command_types = data.get('command_types', [])
            self.log_level = data.get('log_level', 0)
            self.ip_address = data.get('ip_address', '0.0.0.0')
            self.port = data.get('port', 8080)

            full_solution = data.get('full_solution', False)
            if full_solution != False:
                self.command_types = self.command_types + FULL_COMMAND_TYPES
                self.group_count = full_solution.get('group_count', 6)
                self.network = full_solution.get('network', False)
                self.minimum_players = full_solution.get('minimum_players', 2)

FULL_COMMAND_TYPES = [
    'adjust_grid_position',
    'adjust_grid_scale',
    'broadcast_players_in_game',
    'leave_game',
    'get_current_player',
    'redraw',
    'destroy_game',
    'create_player',
    'create_game',
    'get_games',
    'join_game',
    'logout',
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

GRID_WIDTH = 10
GRID_HEIGHT = 10
GRID_SIZE = 512

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
