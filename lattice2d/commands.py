WINDOW_COMMAND_TYPES = [
	'key_press',
	'text',
	'text_motion',
	'text_motion_select',
	'mouse_press',
	'mouse_drag',
	'mouse_scroll'
]

NETWORK_COMMAND_TYPES = []

COMMAND_TYPES = [
	'client_redraw',
	'client_mouse_press',
	'client_mouse_drag',
	'client_mouse_scroll',
	'client_key_press',
	'client_text_entered',
	'client_text_motion',
	'client_text_motion_selected',
	'client_select',
	'server_broadcast_players',
	'server_destroy_game',
	'network_create_player',
	'network_create_game',
	'network_leave_game',
	'network_get_players_in_game',
	'network_get_games',
	'network_join_game',
	'network_logout',
	'network_start_game',
	'network_get_player_order',
	'network_confirm_player_order',
	'network_get_available_characters',
	'network_get_current_player',
	'network_select_character',
	'network_all_characters_selected',
	'network_get_character_selections',
	'network_confirm_character_selections',
	'network_get_player_positions'
]

class Command():
	def __init__(self, type_, data={}):
		self.type = type_
		self.data = data

class NetworkCommand(Command):
	def __init__(self, type_, data={}, status=None, connection=None):
		super().__init__(type_, data)
		self.status = status
		self.connection = connection
