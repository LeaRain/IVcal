import logging

from .call_api import APIClient
from ivcal.database.database_master import MasterDatabaseClass


class DatabaseAPIHandler(MasterDatabaseClass):
    """
    Create a class for dealing with the sqlite3 database file, while the access is established with its master/parent
    class.
    """

    def __init__(self):
        # Use the init function of its parent class.
        super().__init__()
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

        # Create a table for the nature data and the effect of a nature on the status data.
        self.database_cursor.execute('''CREATE TABLE IF NOT EXISTS nature_status_data (nature_id primary key,
         decrease, increase);''')

        # Create a table for a mapping between the id and the name of a nature.
        self.database_cursor.execute('''CREATE TABLE IF NOT EXISTS nature_id_name_mapping (nature_id primary key,
        nature_name);''')

    def get_pokemon_status_data(self, pokemon_id):
        """
        Use the API client to get the status data of a pokemon and return them in a list.
        """

        pokemon_status_data_list = self.api_client.fetch_pokemon_with_stats(pokemon_id)

        return pokemon_status_data_list

    def get_pokemon_id_name_data(self, pokemon_id):
        """
        Use the API client to get the pokemon name based on its id.
        """

        pokemon_name = self.api_client.fetch_pokemon_name_with_id(pokemon_id)

        return pokemon_id, pokemon_name

    def get_nature_status_data(self, nature_id):
        status_id_dict = self.api_client.fetch_nature_with_status_effect(nature_id)

        return nature_id, status_id_dict

    def get_nature_id_name_data(self, nature_id):
        nature_name = self.api_client.fetch_nature_name_with_id(nature_id)

        return nature_id, nature_name

    def save_pokemon_status_data(self, pokemon_data_list):
        """
        Get a list of data with the pokemon id and the values as parameters and save them in the database file.
        """
        # The first element of the list is a number, containing the id of a pokemon.
        pokemon_id = pokemon_data_list[0]

        # The second element of the list should be a dictionary. If it is None, there has been an API error, which has
        # been logged before.
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

    def save_pokemon_id_name_data(self, pokemon_id_and_name_list):
        """
        Get the pokemon id as parameter in a list and fetch the name of the pokemon with its id. Save both in a
        database.
        """

        pokemon_id = pokemon_id_and_name_list[0]
        pokemon_name = pokemon_id_and_name_list[1]

        # Check for potential errors which will be returned as None.
        if pokemon_name is not None:
            try:
                self.database_cursor.execute('''INSERT INTO pokemon_id_name_mapping (pokemon_id, pokemon_name) 
                VALUES (?, ?);''', (pokemon_id, pokemon_name))

            except Exception as database_error:
                logging.error("Something went wrong while inserting the pokemon id and pokemon name data to the "
                              "database. This error occurred: {}".format(database_error), exc_info=True)

    def save_nature_status_data(self, nature_data_list):
        """
        Get a list of data about the nature and save the id and the decreased and increased value in a database.
        """
        nature_id = nature_data_list[0]

        if isinstance(nature_data_list[1], dict):
            nature_status_container = nature_data_list[1]

            try:
                self.database_cursor.execute('''INSERT INTO nature_status_data (nature_id, decrease, increase) 
                VALUES (?, ?, ?)''', (nature_id,
                                      nature_status_container["decreased"],
                                      nature_status_container["increased"]
                                      ))

            except Exception as database_error:
                logging.error("An exception occurred: {}".format(database_error), exc_info=True)

    def save_nature_id_name_data(self, nature_name_id_data_list):
        """
        Get the pokemon id as a parameter (in a list) and fetch the name of the nature with its id. Save both in a
        database.
        """

        nature_id = nature_name_id_data_list[0]
        nature_name = nature_name_id_data_list[1]

        if nature_name is not None:
            try:
                self.database_cursor.execute('''INSERT INTO nature_id_name_mapping (nature_id, nature_name)
                VALUES (?, ?)''', (nature_id, nature_name))

            except Exception as database_error:
                logging.error("Something went wrong while inserting the pokemon id and pokemon name data to the "
                              "database. This error occurred: {}".format(database_error), exc_info=True)
