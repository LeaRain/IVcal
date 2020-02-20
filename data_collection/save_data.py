import sqlite3
import logging

from .call_api import APIClient


class DatabaseHandling:
    """
    Create a class for dealing with the sqlite3 database file.
    """

    def __init__(self):
        # Initialize a connection and if this file does not exist, it is created in this step. The isolation level is
        # set to None, so autocommit is possible. 
        database_connection = sqlite3.connect("pokemon.db", isolation_level=None)

        # Use a cursor as class object, so every function has access to the database.
        self.database_cursor = database_connection.cursor()

        # Get a client for API calls.
        self.api_client = APIClient()

        self.init_database()

    def init_database(self):
        """
        Initialize tables in the database file, if they are not there already.
        """

        # Create a table for the pokemon status data.
        self.database_cursor.execute('''CREATE TABLE IF NOT EXISTS pokemon_status_data (pokemon_id primary key, 
        pokemon_hp, pokemon_attack, pokemon_defense, pokemon_sp_attack, pokemon_sp_defense, pokemon_speed);''')

        # Create a table for a mapping between the id and the name of a pokemon.
        self.database_cursor.execute('''CREATE TABLE IF NOT EXISTS pokemon_id_name_mapping (pokemon_id primary key, 
        pokemon_name);''')

    def get_pokemon_status_data(self, pokemon_id):
        """
        Use the API client to get the status data of a pokemon and return them in a list.
        """

        pokemon_status_data_list = self.api_client.fetch_pokemon_with_stats(pokemon_id)

        return pokemon_status_data_list

    def save_pokemon_status_data(self, pokemon_data_list):
        """
        Get a list of data with the pokemon id and the values and save them in the database file.
        """

        # The first element of the list is a number, containing the id of a pokemon.
        pokemon_id = pokemon_data_list[0]
        # The second element of the list should be a dictionary

        if isinstance(pokemon_data_list[1], dict):
            pokemon_status_container = pokemon_data_list[1]

            try:
                self.database_cursor.execute('''INSERT INTO pokemon_status_data (pokemon_id, pokemon_hp, pokemon_attack, 
                    pokemon_defense, pokemon_sp_attack, pokemon_sp_defense, pokemon_speed) 
                    VALUES (?, ?, ?, ?, ?, ?, ?);''', (pokemon_id,
                                                       pokemon_status_container["hp"],
                                                       pokemon_status_container["attack"],
                                                       pokemon_status_container["defense"],
                                                       pokemon_status_container["special-attack"],
                                                       pokemon_status_container["special-defense"],
                                                       pokemon_status_container["speed"]
                                                       ))

            except Exception as database_error:
                logging.error("An exception occurred: {}".format(database_error), exc_info=True)

        else:
            logging.warning("The second item of the data list is not a dictionary, it has the type"
                            " {}.".format(type(pokemon_data_list[1])))
