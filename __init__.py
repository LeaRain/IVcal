"""
Right now, this file is a hell of testing area.
"""

from data_collection.api_database import DatabaseAPIHandler
from data_collection.massive_api_call import get_all_pokemon_stats, get_all_pokemon_names, get_all_nature_stats, \
    get_all_nature_names
from data_collection.call_api import APIClient
from calculation.calculator_database import DatabaseCalculatorHandler
from calculation.user_communication import UserInteraction

# database_handler = DatabaseHandler()
# data_list = database_handler.get_pokemon_status_data(807)
# database_handler.save_pokemon_status_data(data_list)

# get_all_pokemon_stats()
# get_all_pokemon_names()

# api_client = APIClient()
# print(api_client.fetch_nature_with_status_effect(4))

# get_all_nature_stats()
# get_all_nature_names()

# database_handler = DatabaseCalculatorHandler()
# print(database_handler.get_nature_status_effects(1))

user_interaction = UserInteraction(data_source="local")
user_interaction.get_pokemon_nature()
