"""
An option for the calculator is the usage of a local pokemon database. This data needs to be created and so, there is
a file for all the API calls.
"""

from .save_data import DatabaseHandler


def get_all_pokemon_stats():
    """
    Get all the pokemon and their stats by an API call.
    """

    database_handler = DatabaseHandler()

    # There are 807 pokemon callable in the API.
    for pokemon_number in range(1, 808):
        pokemon_status_data = database_handler.get_pokemon_status_data(pokemon_number)
        database_handler.save_pokemon_status_data(pokemon_status_data)


def get_all_pokemon_names():
    """
    Similar function like get_all_pokemon_stats, but uses names.
    """

    database_handler = DatabaseHandler()

    for pokemon_number in range(1, 808):
        database_handler.get_pokemon_id_name_data(pokemon_number)
        database_handler.save_pokemon_id_name_data(pokemon_number)
