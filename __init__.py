from data_collection.save_data import DatabaseHandler
from data_collection.massive_api_call import get_all_pokemon_stats, get_all_pokemon_names

# database_handler = DatabaseHandler()
# data_list = database_handler.get_pokemon_status_data(807)
# database_handler.save_pokemon_status_data(data_list)

get_all_pokemon_stats()
get_all_pokemon_names()
