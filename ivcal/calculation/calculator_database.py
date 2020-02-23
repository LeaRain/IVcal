import logging

from ivcal.database.database_master import MasterDatabaseClass

logging.basicConfig(filename="events.log")


class DatabaseCalculatorHandler(MasterDatabaseClass):
    """
    Create a database class for access while dealing with the IV calculator.
    """

    def __init__(self):
        # Use the init function of its parent class.
        super().__init__()

    def get_pokemon_id_by_name(self, pokemon_name):
        """
        Get the id of a pokemon by its name.
        """

        # Execute a query with the name of the pokemon to get its id for further usage.
        pokemon_id_query_result = self.database_cursor.execute("""SELECT pokemon_id FROM pokemon_id_name_mapping 
        WHERE pokemon_name=?;""", (pokemon_name,))

        # The result of fetchone is a tuple, if it was successful. If the result does not contain an item, it is None.
        pokemon_id = pokemon_id_query_result.fetchone()

        # Check if the result is not None, because this can happen, if the result is empty.
        if pokemon_id is not None:
            # Set the pokemon id to the one and only element in the result tuple.
            pokemon_id = pokemon_id[0]

        else:
            logging.error("Pokemon {} was not found in the database.".format(pokemon_name))

        return pokemon_id

    def get_pokemon_base_stats_by_id(self, pokemon_id):
        """
        Get the base stats of a pokemon by its id.
        """

        # Execute a query with all necessary base status parameters.
        pokemon_stats_query_result = self.database_cursor.execute("""SELECT pokemon_hp, pokemon_attack, pokemon_defense, 
        pokemon_sp_attack, pokemon_sp_defense, pokemon_speed FROM pokemon_status_data WHERE pokemon_id=?;""",
                                                                  (pokemon_id,))

        # Get the result in a tuple. The variable is not a tuple if the result is None.
        pokemon_status_result = pokemon_stats_query_result.fetchone()

        if pokemon_status_result is not None:
            # Create a dictionary with all base status values.
            status_dictionary = {
                "hp": pokemon_status_result[0],
                "attack": pokemon_status_result[1],
                "defense": pokemon_status_result[2],
                "special-attack": pokemon_status_result[3],
                "special-defense": pokemon_status_result[4],
                "speed": pokemon_status_result[5]
            }

        else:
            # Set the dictionary to None, if the query result is empty.
            status_dictionary = None
            logging.error("Pokemon with id {} was not found in the database.".format(pokemon_id))

        return status_dictionary

    def get_nature_id_by_name(self, nature_name):
        """
        Get the id of a nature by its name.
        """

        # Execute the query for the nature id based on the parameter name.
        nature_id_query_result = self.database_cursor.execute("""SELECT nature_id FROM nature_id_name_mapping 
        WHERE nature_name=?;""", (nature_name,))

        # Get the result, which is a tuple, if the result query is empty.
        nature_id_result = nature_id_query_result.fetchone()

        if nature_id_result is not None:
            nature_id_result = nature_id_result[0]

        else:
            logging.error("Nature name {} was not found in the database.".format(nature_name))

        return nature_id_result

    def get_nature_status_effects(self, nature_id):
        """
        Get the status effects of a pokemon's nature by the nature id. For every status value as key, a new value is
        defined in a dictionary.
        """

        # Execute the necessary query.
        nature_effect_query_result = self.database_cursor.execute("""SELECT decrease, increase FROM nature_status_data
        WHERE nature_id=?;""", (nature_id,))

        # Get the result of the query. This will be a tuple, if it is not None.
        nature_effect_result = nature_effect_query_result.fetchone()

        # If the result is not None, the results of the query are not empty.
        if nature_effect_result is not None:
            # Define the different status values.
            status_values = ["attack", "defense", "special-attack", "special-defense", "speed"]
            # Create a dictionary for saving the results.
            nature_effect_dictionary = {}

            # Check the effect of the nature on every value.
            for value in status_values:
                # Prepare a key for compatibility with the IV calculator.
                nature_key = "{}_nature".format(value)

                # This value is the decreased one.
                if value == nature_effect_result[0]:
                    # Set the effect to 0.9 as decreased value.
                    nature_effect_dictionary[nature_key] = 0.9

                # This value is the increased one.
                elif value == nature_effect_result[1]:
                    # Set the effect to 1.1 as increased value.
                    nature_effect_dictionary[nature_key] = 1.1

                # If a value is not decreased or increased, there is no effect.
                else:
                    nature_effect_dictionary[nature_key] = 1

        else:
            # If the nature id is not found, the return value will be None.
            nature_effect_dictionary = None
            logging.error("Nature id {} was not found in the database.".format(nature_id))

        return nature_effect_dictionary
