import inspect

class ConfigurationError(AssertionError):
	pass

class InnerConfig:
	_shared_state = {}

	def __init__(self):
		self.__dict__ = self._shared_state


class Config(InnerConfig):
	def __init__(self, data=None):
		super().__init__()
		if data:
			self.__validate_window_dimensions(data)
			self.__validate_network(data)
			self.__validate_rendering(data)
			self.__validate_grid(data)
			self.__validate_command_types(data)
			self.__validate_player_class(data)
			self.__validate_empty_tile_class(data)
			self.__validate_client_states(data)
			self.__validate_server_states(data)
			self.__validate_assets(data)
			self.data = data
			self.data['command_types'] = self.data['command_types'] + FULL_COMMAND_TYPES

	def __validate_window_dimensions(self, data):
		if not 'window_dimensions' in data.keys():
			raise ConfigurationError('"window_dimensions" is not present')
		if not isinstance(data['window_dimensions'], tuple):
			raise ConfigurationError('"window_dimensions" is not a tuple')
		if len(data['window_dimensions']) != 2:
			raise ConfigurationError('"window_dimensions" is not length 2')
		for item in data['window_dimensions']:
			if not isinstance(item, int):
				raise ConfigurationError('"window_dimension" is not an int')

	def __validate_network(self, data):
		if 'network' in data.keys():
			if not isinstance(data['network'], dict):
				raise ConfigurationError('"network" is not a dict')

			if not 'ip_address' in data['network'].keys():
				raise ConfigurationError('"network.ip_address" is not present')
			if not isinstance(data['network']['ip_address'], str):
				raise ConfigurationError('"network.ip_address" is not a string')

			if not 'port' in data['network'].keys():
				raise ConfigurationError('"network.port" is not present')
			if not isinstance(data['network']['port'], int):
				raise ConfigurationError('"network.port" is not an int')

	def __validate_rendering(self, data):
		if not 'rendering' in data.keys():
			raise ConfigurationError('"rendering" is not present')
		if not isinstance(data['rendering'], dict):
			raise ConfigurationError('"rendering" is not a dict')

		if not 'layers' in data['rendering'].keys():
			raise ConfigurationError('"rendering.layers" is not present')
		if not isinstance(data['rendering']['layers'], list):
			raise ConfigurationError('"rendering.layers" is not a list')

		for layer in data['rendering']['layers']:
			if not isinstance(layer, str):
				raise ConfigurationError('"rendering.layer" is not a string')

		if not 'groups_per_layer' in data['rendering'].keys():
			raise ConfigurationError('"rendering.groups_per_layer" is not present')
		if not isinstance(data['rendering']['groups_per_layer'], int):
			raise ConfigurationError('"rendering.groups_per_layer" is not an int')

	def __validate_grid(self, data):
		if not 'grid' in data.keys():
			raise ConfigurationError('"grid" is not present')
		if not isinstance(data['grid'], dict):
			raise ConfigurationError('"grid" is not a dict')

		if not 'width' in data['grid'].keys():
			raise ConfigurationError('"grid.width" is not present')
		if not isinstance(data['grid']['width'], int):
			raise ConfigurationError('"grid.width" is not an int')

		if not 'height' in data['grid'].keys():
			raise ConfigurationError('"grid.height" is not present')
		if not isinstance(data['grid']['height'], int):
			raise ConfigurationError('"grid.height" is not an int')

		if not 'size' in data['grid'].keys():
			raise ConfigurationError('"grid.size" is not present')
		if not isinstance(data['grid']['size'], int):
			raise ConfigurationError('"grid.size" is not an int')

	def __validate_command_types(self, data):
		if not 'command_types' in data.keys():
			raise ConfigurationError('"command_types" is not present')
		if not isinstance(data['command_types'], list):
			raise ConfigurationError('"command_types" is not a list')

		for command_type in data['command_types']:
			if not isinstance(command_type, str):
				raise ConfigurationError('"command_type" is not a string')

	def __validate_player_class(self, data):
		if not 'player_class' in data.keys():
			raise ConfigurationError('"player_class" is not present')
		if not inspect.isclass(data['player_class']):
			raise ConfigurationError('"player_class" is not a class')

	def __validate_empty_tile_class(self, data):
		if not 'empty_tile_class' in data.keys():
			raise ConfigurationError('"empty_tile_class" is not present')
		if not inspect.isclass(data['empty_tile_class']):
			raise ConfigurationError('"empty_tile_class" is not a class')

	def __validate_client_states(self, data):
		if not 'client_states' in data.keys():
			raise ConfigurationError('"client_states" is not present')

		self.__validate_states(data['client_states'], 'client')

	def __validate_server_states(self, data):
		if not 'server_states' in data.keys():
			raise ConfigurationError('"server_states" is not present')

		self.__validate_states(data['server_states'], 'server')

	def __validate_states(self, data, key):
		if not isinstance(data, dict):
			raise ConfigurationError(f'"{key}_states" is not a dict')

		if not 'starting_state' in data.keys():
			raise ConfigurationError(f'"{key}_states.starting_state" is not present')
		if not inspect.isclass(data['starting_state']):
			raise ConfigurationError(f'"{key}_states.starting_state" is not a class')

		if not 'states' in data.keys():
			raise ConfigurationError(f'"{key}_states.states" is not present')
		if not isinstance(data['states'], list):
			raise ConfigurationError(f'"{key}_states.states" is not a list')

		for state in data['states']:
			if not isinstance(state, dict):
				raise ConfigurationError(f'"{key}_states.state" is not a dict')

			if not 'state' in state.keys():
				raise ConfigurationError(f'"{key}_states.state.state" is not present')
			if not inspect.isclass(state['state']):
				raise ConfigurationError(f'"{key}_states.state.state" is not a class')

			if not 'transitions' in state.keys():
				raise ConfigurationError(f'"{key}_states.state.transitions" is not present')
			if not isinstance(state['transitions'], dict):
				raise ConfigurationError(f'"{key}_states.state.transitions" is not a dict')

			for transition_state in state['transitions'].values():
				if not inspect.isclass(transition_state):
					raise ConfigurationError(f'"{key}_states.state.transition" is not a class')



	def __validate_assets(self, data):
		if not 'assets' in data.keys():
			raise ConfigurationError('"assets" is not present')
		if not isinstance(data['assets'], dict):
			raise ConfigurationError('"assets" is not a dict')

		if not 'path' in data['assets'].keys():
			raise ConfigurationError('"assets.path" is not present')
		if not isinstance(data['assets']['path'], str):
			raise ConfigurationError('"assets.path" is not a string')

		if not 'resources' in data['assets'].keys():
			raise ConfigurationError('"assets.resources" is not present')
		if not isinstance(data['assets']['resources'], list):
			raise ConfigurationError('"assets.resources" is not a list')

		for resource in data['assets']['resources']:
			if not isinstance(resource, dict):
				raise ConfigurationError('"assets.resources" is not a dict')

			if not 'key' in resource.keys():
				raise ConfigurationError('"assets.resources" does not have "key"')
			if not isinstance(resource['key'], str):
				raise ConfigurationError('"assets.resource.key" is not a string')

			if not 'location' in resource.keys():
				raise ConfigurationError('"assets.resources" does not have "location"')
			if not isinstance(resource['location'], str):
				raise ConfigurationError('"assets.resource.location" is not a string')

			if not 'type' in resource.keys():
				raise ConfigurationError('"assets.resources" does not have "type"')
			if not isinstance(resource['type'], str):
				raise ConfigurationError('"assets.resource.type" is not a string')
			if resource['type'] not in ['single', 'gif', 'grid']:
				raise ConfigurationError('"assets.resources" does not have "type" of "single", "gif", or "grid"')

			if resource['type'] == 'grid':
				if 'rows' not in resource.keys():
					raise ConfigurationError('"assets.resources" of "type" "grid" does not have "rows"')
				if not isinstance(resource['rows'], int):
					raise ConfigurationError('"assets.resource.rows" is not an int')

				if 'columns' not in resource.keys():
					raise ConfigurationError('"assets.resources" of "type" "grid" does not have "columns"')
				if not isinstance(resource['columns'], int):
					raise ConfigurationError('"assets.resource.columns" is not an int')

				if 'resources' in resource.keys():
					if not isinstance(resource['resources'], list):
						raise ConfigurationError('"assets.resource.resources" is not a list')
					for grid_resource in resource['resources']:
						if not isinstance(grid_resource, dict):
							raise ConfigurationError('"assets.resource.resource" is not a dict')
						if 'key' not in grid_resource.keys():
							raise ConfigurationError('"assets.resource.resource" does not have "key"')
						if not isinstance(grid_resource['key'], str):
							raise ConfigurationError('"assets.resource.resource.key" is not a string')
						if 'index' not in grid_resource.keys():
							raise ConfigurationError('"assets.resource.resource" does not have "index"')
						if not isinstance(grid_resource['index'], int):
							raise ConfigurationError('"assets.resource.resource.index" is not an int')

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

