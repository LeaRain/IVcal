import pokepy
import logging


class APIClient:
    """
    Create a class, which contains the pokepy client, necessary for API calls. This class saves data about already
    fetched pokemon with their stats.
    """

    def __init__(self):
        # Create a client for API calls.
        self.client = pokepy.V2Client()

    def fetch_pokemon_with_stats(self, pokemon_id):
        """
        Use the pokepy client and a pokemon id as parameter to get the stats of one pokemon. The output format for the
        stats is a dictionary as default.
        """

        # Create a list for saving fetched data. This list will contain two further values: The id of the pokemon and a
        # list with the values. A dictionary is not necessary because only one pokemon is transmitted.
        pokemon_result_list = []

        # Initialize as None for a potential error case, overwrite in a try part.
        status_container = None

        try:
            # Get pokemon based on its id or name.
            pokemon = self.client.get_pokemon(pokemon_id)
            # Get the stats of a pokemon, which are represented in a list.
            status_container = pokemon.stats

            # This function is only for one pokemon, so the return value should contain, in the best case, a number as
            # pokemon id and a dictionary with the status values of the pokemon.
            status_container = self.modify_status_list(status_container)

        except Exception as api_error:
            logging.error("An error occurred during the API call (get pokemon by id): {}".format(api_error),
                          exc_info=True)

        # Save the id of a pokemon in the list.
        pokemon_result_list.append(pokemon_id)

        # Save the pokemon with its stats in the list.
        pokemon_result_list.append(status_container)

        return pokemon_result_list

    def fetch_pokemon_with_name(self, pokemon_id):
        """
        Get the name of a pokemon by its id.
        """

        pokemon_name = None

        try:
            pokemon_name = self.client.get_pokemon(pokemon_id).name

        except Exception as api_error:
            logging.error("An error occurred during the API call (get pokemon by id): {}".format(api_error),
                          exc_info=True)

        return pokemon_name

    @staticmethod
    def modify_status_list(pokemon_stats_list):
        """
        Modify the stat result list of the function fetch_pokemon_with_stats and transform it to a dictionary.
        """

        # Create an empty dictionary
        stats_dict = {}

        for stat in pokemon_stats_list:
            # Get the name of a stat as key and make the related base stat its value.
            stats_dict[stat.stat.name] = stat.base_stat

        return stats_dict
