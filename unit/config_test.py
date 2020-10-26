import pytest
import os
import copy

from lattice2d.config import Config, ConfigurationError
from config import CONFIG

class TestConfig:
	class TestWindowDimensions:
		def test_window_dimensions_are_required(self):
			config = copy.deepcopy(CONFIG)
			del(config['window_dimensions'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_window_dimensions_must_be_a_tuple(self):
			config = copy.deepcopy(CONFIG)
			config['window_dimensions'] = [800, 600]
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_window_dimensions_must_be_of_length_2(self):
			config = copy.deepcopy(CONFIG)
			config['window_dimensions'] = (800, 600, 150)
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_window_dimension_entries_must_be_ints(self):
			config = copy.deepcopy(CONFIG)
			config['window_dimensions'] = ('800', '600')
			with pytest.raises(ConfigurationError):
				Config(config)

	@pytest.mark.skip(reason='the "network" entry in the config must be uncommented to run these')
	class TestNetwork:
		def test_network_is_optional(self):
			config = copy.deepcopy(CONFIG)
			del(config['network'])
			Config(config)

		def test_network_must_be_a_dict(self):
			config = copy.deepcopy(CONFIG)
			config['network'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_network_ip_address_is_required(self):
			config = copy.deepcopy(CONFIG)
			del(config['network']['ip_address'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_network_ip_address_must_be_a_string(self):
			config = copy.deepcopy(CONFIG)
			config['network']['ip_address'] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_network_port_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['network']['port'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_network_port_must_be_an_int(self):
			config = copy.deepcopy(CONFIG)
			config['network']['port'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

	class TestLogging:
		def test_logging_is_required(self):
			config = copy.deepcopy(CONFIG)
			del(config['logging'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_logging_must_be_a_dict(self):
			config = copy.deepcopy(CONFIG)
			config['logging'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_logging_values_must_be_colors(self):
			config = copy.deepcopy(CONFIG)
			config['logging'] = ['not_a_color']
			with pytest.raises(ConfigurationError):
				Config(config)

	class TestRendering:
		def test_rendering_is_required(self):
			config = copy.deepcopy(CONFIG)
			del(config['rendering'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_rendering_must_be_a_dict(self):
			config = copy.deepcopy(CONFIG)
			config['rendering'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_rendering_layers_is_required(self):
			config = copy.deepcopy(CONFIG)
			del(config['rendering']['layers'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_rendering_layers_must_be_a_list(self):
			config = copy.deepcopy(CONFIG)
			config['rendering']['layers'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_rendering_layer_must_be_a_string(self):
			config = copy.deepcopy(CONFIG)
			config['rendering']['layers'][0] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_rendering_groups_per_layer_is_required(self):
			config = copy.deepcopy(CONFIG)
			del(config['rendering']['groups_per_layer'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_rendering_groups_per_layer_must_be_a_list(self):
			config = copy.deepcopy(CONFIG)
			config['rendering']['groups_per_layer'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

	class TestGrid:
		def test_grid_is_required(self):
			config = copy.deepcopy(CONFIG)
			del(config['grid'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_grid_must_be_a_dict(self):
			config = copy.deepcopy(CONFIG)
			config['grid'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_grid_width_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['grid']['width'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_grid_width_must_be_an_int(self):
			config = copy.deepcopy(CONFIG)
			config['grid']['width'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_grid_height_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['grid']['height'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_grid_height_must_be_an_int(self):
			config = copy.deepcopy(CONFIG)
			config['grid']['height'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_grid_size_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['grid']['size'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_grid_size_must_be_an_int(self):
			config = copy.deepcopy(CONFIG)
			config['grid']['size'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

	class TestCommandTypes:
		def test_command_types_is_required(self):
			config = copy.deepcopy(CONFIG)
			del(config['command_types'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_command_types_must_be_a_list(self):
			config = copy.deepcopy(CONFIG)
			config['command_types'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_command_type_must_be_a_string(self):
			config = copy.deepcopy(CONFIG)
			config['command_types'] = [1]
			with pytest.raises(ConfigurationError):
				Config(config)

	class TestPlayerClass:
		def test_player_class_is_required(self):
			config = copy.deepcopy(CONFIG)
			del(config['player_class'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_player_class_must_be_a_class(self):
			config = copy.deepcopy(CONFIG)
			config['player_class'] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

	class TestEmptyTileClass:
		def test_empty_tile_class_is_required(self):
			config = copy.deepcopy(CONFIG)
			del(config['empty_tile_class'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_empty_tile_class_must_be_a_class(self):
			config = copy.deepcopy(CONFIG)
			config['empty_tile_class'] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

	class TestClientStates:
		def test_client_states_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['client_states'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_client_states_must_be_a_dict(self):
			config = copy.deepcopy(CONFIG)
			config['client_states'] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_starting_state_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['client_states']['starting_state'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_starting_state_must_be_a_class(self):
			config = copy.deepcopy(CONFIG)
			config['client_states']['starting_state'] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_states_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['client_states']['states'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_states_must_be_a_list(self):
			config = copy.deepcopy(CONFIG)
			config['client_states']['states'] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_state_transitions_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['client_states']['states'][0]['transitions'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_state_transitions_must_be_a_dict(self):
			config = copy.deepcopy(CONFIG)
			config['client_states']['states'][0]['transitions'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_state_transition_must_be_a_class(self):
			config = copy.deepcopy(CONFIG)
			config['client_states']['states'][0]['transitions']['to_other_state'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

	class TestServerStates:
		def test_server_states_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['server_states'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_server_states_must_be_a_dict(self):
			config = copy.deepcopy(CONFIG)
			config['server_states'] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_starting_state_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['server_states']['starting_state'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_starting_state_must_be_a_class(self):
			config = copy.deepcopy(CONFIG)
			config['server_states']['starting_state'] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_states_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['server_states']['states'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_states_must_be_a_list(self):
			config = copy.deepcopy(CONFIG)
			config['server_states']['states'] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_state_transitions_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['server_states']['states'][0]['transitions'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_state_transitions_must_be_a_dict(self):
			config = copy.deepcopy(CONFIG)
			config['server_states']['states'][0]['transitions'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_state_transition_must_be_a_class(self):
			config = copy.deepcopy(CONFIG)
			config['server_states']['states'][0]['transitions']['to_other_state'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

	class TestAssets:
		def test_assets_is_required(self):
			config = copy.deepcopy(CONFIG)
			del(config['assets'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_assets_must_be_a_dict(self):
			config = copy.deepcopy(CONFIG)
			config['assets'] = 'something'
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_assets_path_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['assets']['path'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_assets_path_must_be_a_string(self):
			config = copy.deepcopy(CONFIG)
			config['assets']['path'] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_assets_resources_is_required(self):
			config = copy.deepcopy(CONFIG)
			del (config['assets']['resources'])
			with pytest.raises(ConfigurationError):
				Config(config)

		def test_assets_path_must_be_a_list(self):
			config = copy.deepcopy(CONFIG)
			config['assets']['resources'] = {}
			with pytest.raises(ConfigurationError):
				Config(config)

		class TestAssetsResources:
			def test_must_be_a_dict(self):
				config = copy.deepcopy(CONFIG)
				config['assets']['resources'][0] = 'something'
				with pytest.raises(ConfigurationError):
					Config(config)

			def test_key_is_required(self):
				config = copy.deepcopy(CONFIG)
				del(config['assets']['resources'][0]['key'])
				with pytest.raises(ConfigurationError):
					Config(config)

			def test_key_must_be_a_string(self):
				config = copy.deepcopy(CONFIG)
				config['assets']['resources'][0]['key'] = {}
				with pytest.raises(ConfigurationError):
					Config(config)

			def test_location_is_required(self):
				config = copy.deepcopy(CONFIG)
				del (config['assets']['resources'][0]['location'])
				with pytest.raises(ConfigurationError):
					Config(config)

			def test_location_must_be_a_string(self):
				config = copy.deepcopy(CONFIG)
				config['assets']['resources'][0]['location'] = {}
				with pytest.raises(ConfigurationError):
					Config(config)

			def test_type_is_required(self):
				config = copy.deepcopy(CONFIG)
				del (config['assets']['resources'][0]['type'])
				with pytest.raises(ConfigurationError):
					Config(config)

			def test_type_must_be_a_string(self):
				config = copy.deepcopy(CONFIG)
				config['assets']['resources'][0]['type'] = {}
				with pytest.raises(ConfigurationError):
					Config(config)

			def test_type_must_be_single_gif_or_grid(self):
				config = copy.deepcopy(CONFIG)
				config['assets']['resources'][0]['type'] = 'something'
				with pytest.raises(ConfigurationError):
					Config(config)

			class TestTypeGrid:
				def test_rows_is_required(self):
					config = copy.deepcopy(CONFIG)
					del (config['assets']['resources'][4]['rows'])
					with pytest.raises(ConfigurationError):
						Config(config)

				def test_rows_must_be_an_int(self):
					config = copy.deepcopy(CONFIG)
					config['assets']['resources'][4]['rows'] = {}
					with pytest.raises(ConfigurationError):
						Config(config)

				def test_columns_is_required(self):
					config = copy.deepcopy(CONFIG)
					del (config['assets']['resources'][4]['columns'])
					with pytest.raises(ConfigurationError):
						Config(config)

				def test_columns_must_be_an_int(self):
					config = copy.deepcopy(CONFIG)
					config['assets']['resources'][4]['columns'] = {}
					with pytest.raises(ConfigurationError):
						Config(config)

				def test_resources_is_optional(self):
					config = copy.deepcopy(CONFIG)
					del (config['assets']['resources'][4]['resources'])
					Config(config)

				def test_resources_must_be_a_list(self):
					config = copy.deepcopy(CONFIG)
					config['assets']['resources'][4]['resources'] = {}
					with pytest.raises(ConfigurationError):
						Config(config)

				class TestWithResources:
					def test_must_be_a_dict(self):
						config = copy.deepcopy(CONFIG)
						config['assets']['resources'][4]['resources'][0] = 'something'
						with pytest.raises(ConfigurationError):
							Config(config)

					def test_key_is_required(self):
						config = copy.deepcopy(CONFIG)
						del (config['assets']['resources'][4]['resources'][0]['key'])
						with pytest.raises(ConfigurationError):
							Config(config)

					def test_key_must_be_a_string(self):
						config = copy.deepcopy(CONFIG)
						config['assets']['resources'][4]['resources'][0]['key'] = {}
						with pytest.raises(ConfigurationError):
							Config(config)

					def test_index_is_required(self):
						config = copy.deepcopy(CONFIG)
						del (config['assets']['resources'][4]['resources'][0]['index'])
						with pytest.raises(ConfigurationError):
							Config(config)

					def test_index_must_be_an_int(self):
						config = copy.deepcopy(CONFIG)
						config['assets']['resources'][4]['resources'][0]['index'] = 'something'
						with pytest.raises(ConfigurationError):
							Config(config)