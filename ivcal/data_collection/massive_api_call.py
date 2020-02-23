"""
An option for the calculator is the usage of a local pokemon database. This data needs to be created and so, there is
a file for all the API calls.
"""

from .api_database import DatabaseAPIHandler


def get_all_pokemon_stats():
    """
    Get all the pokemon and their stats by an API call.
    """

    database_handler = DatabaseAPIHandler()

    # There are 807 pokemon callable in the API.
    for pokemon_number in range(1, 808):
        pokemon_status_data = database_handler.get_pokemon_status_data(pokemon_number)
        database_handler.save_pokemon_status_data(pokemon_status_data)


def get_all_pokemon_names():
    """
    Similar function like get_all_pokemon_stats, but uses names.
    """

    database_handler = DatabaseAPIHandler()

    for pokemon_number in range(1, 808):
        pokemon_number_id_data = database_handler.get_pokemon_id_name_data(pokemon_number)
        database_handler.save_pokemon_id_name_data(pokemon_number_id_data)


def get_all_nature_stats():
    """
    Similar to functions above.
    """
    database_handler = DatabaseAPIHandler()

    for nature_number in range(1, 26):
        nature_status_data = database_handler.get_nature_status_data(nature_number)
        database_handler.save_nature_status_data(nature_status_data)


def get_all_nature_names():
    """
    Similar to functions above.
    """

    database_handler = DatabaseAPIHandler()

    for nature_number in range(1, 26):
        nature_id_data = database_handler.get_nature_id_name_data(nature_number)
        database_handler.save_nature_id_name_data(nature_id_data)
