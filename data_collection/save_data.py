import sqlite3
import logging

from .call_api import APIClient


class DatabaseHandling:
    def __init__(self):
        database_connection = sqlite3.connect("pokemon.db")
        self.database_cursor = database_connection.cursor()

        self.api_client = APIClient()

        self.init_database()

    def init_database(self):
        self.database_cursor.execute('''CREATE TABLE IF NOT EXISTS pokemon_value_data (pokemon_id primary key, 
        pokemon_hp, pokemon_attack, pokemon_defense, pokemon_sp_attack, pokemon_sp_defense, pokemon_speed);''')

        self.database_cursor.execute('''CREATE TABLE IF NOT EXISTS pokemon_id_name_mapping (pokemon_id, 
        pokemon_name);''')

    def get_pokemon_data(self, pokemon_id):
        pokemon_value_data_list = self.api_client.fetch_pokemon_with_stats(pokemon_id)

        return pokemon_value_data_list

    def save_pokemon_data(self, pokemon_data_list):
        pokemon_id = pokemon_data_list[0]
        pokemon_stat_container = pokemon_data_list[1]

        try:
            self.database_cursor.execute('''INSERT INTO pokemon_value_data (pokemon_id, pokemon_hp, pokemon_attack, 
                pokemon_defense, pokemon_sp_attack, pokemon_sp_defense, pokemon_speed) VALUES (?, ?, ?, ?, ?, ?, ?);''',
                                         (pokemon_id,
                                          pokemon_stat_container["hp"],
                                          pokemon_stat_container["attack"],
                                          pokemon_stat_container["defense"],
                                          pokemon_stat_container["special-attack"],
                                          pokemon_stat_container["special-defense"],
                                          pokemon_stat_container["speed"]
                                          ))

        except Exception as database_error:
            logging.error("An exception occurred: {}".format(database_error), exc_info=True)
