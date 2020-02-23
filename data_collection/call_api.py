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

    def fetch_pokemon_name_with_id(self, pokemon_id):
        """
        Get the name of a pokemon by its id.
        """

        pokemon_name = None

        try:
            pokemon_name = self.client.get_pokemon(pokemon_id).name

        except Exception as api_error:
            logging.error("An error occurred during the API call (fetch pokemon with id): {}".format(api_error),
                          exc_info=True)

        return pokemon_name

    def fetch_pokemon_id_with_name(self, pokemon_name):
        """
        Get the id of a pokemon by its name as other way around compared with fetch_pokemon_name_with_id
        """

        pokemon_id = None

        try:
            pokemon_id = self.client.get_pokemon(pokemon_name).id

        except Exception as api_error:
            logging.error("An error occurred during the API call (fetch pokemon with name): {}".format(api_error),
                          exc_info=True)

        return pokemon_id

    def fetch_nature_with_status_effect(self, nature_id):
        """
        Get the nature by its id.
        """
        nature_effect_container = None

        # If the nature id is one of those in the list, it is a nature which does not have an effect at the stats of a
        # pokemon.
        if nature_id not in [1, 7, 13, 19, 25]:
            try:
                nature = self.client.get_nature(nature_id)

                # Make the container to a dictionary for more related data.
                nature_effect_container = {"decreased": nature.decreased_stat.name,
                                           "increased": nature.increased_stat.name}

            except Exception as api_error:
                logging.error("An error occurred during the API call (fetch nature wih status effect): "
                              "{}".format(api_error), exc_info=True)

        else:
            # There is not an effect for these natures.
            nature_effect_container = {"decreased": None,
                                       "increased": None}

        return nature_effect_container

    def fetch_nature_name_with_id(self, nature_id):
        """
        Get the name of a nature by its id.
        """

        nature_name = None
        try:
            nature = self.client.get_nature(nature_id)
            nature_name = nature.name

        except Exception as api_error:
            logging.error("An error occurred during the API call (fetch nature with id): {}".format(api_error),
                          exc_info=True)

        return nature_name

    def fetch_nature_id_with_name(self, nature_name):
        """
        Get the name of a nature by its id.
        """

        nature_id = None
        try:
            nature = self.client.get_nature(nature_name)
            nature_id = nature.id

        except Exception as api_error:
            logging.error("An error occurred during the API call (fetch nature with name): {}".format(api_error),
                          exc_info=True)

        return nature_id

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
