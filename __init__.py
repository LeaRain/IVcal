from data_collection.save_data import DatabaseHandling

database_handler = DatabaseHandling()
data_list = database_handler.get_pokemon_status_data(1)

database_handler.save_pokemon_status_data(data_list)

