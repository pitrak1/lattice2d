class InnerConfig:
	_shared_state = {}

	def __init__(self):
		self.__dict__ = self._shared_state


class Config(InnerConfig):
	def __init__(self, data=None):
		super().__init__()
		if data:
			self.data = data
			self.data['command_types'] = self.data['command_types'] + FULL_COMMAND_TYPES

	def __getitem__(self, key):
		return self.data[key]


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

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
