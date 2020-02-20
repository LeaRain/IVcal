import pokepy


class APIClient:
    """
    Create a class, which contains the pokepy client, necessary for API calls. This class saves data about already
    fetched pokemon with their stats.
    """

    def __init__(self):
        # Create a client for API calls.
        self.client = pokepy.V2Client()

    def fetch_pokemon_with_stats(self, pokemon_id, stats_as_dict=True):
        """
        Use the pokepy client and a pokemon id as parameter to get the stats of one pokemon. The output format for the
        stats is a dictionary as default, but this function can be disabled.
        """

        # Create a list for saving fetched data. This list will contain two further values: The id of the pokemon and a
        # list with the values. A dictionary is not necessary because only one pokemon is transmitted.
        pokemon_result_list = []

        # Get pokemon based on its id or name.
        pokemon = self.client.get_pokemon(pokemon_id)
        # Get the stats of a pokemon, which are represented in a list.
        stats_container = pokemon.stats

        # The output for the database input can be used better in a dictionary, so this parameter is True. But this can
        # be changed, if necessary, and the result would be a list with a number and a list inside. Now, it is a list
        # with a number and a dictionary.
        if stats_as_dict is True:
            stats_container = self.modify_stats_list(stats_container)

        # Save the id of a pokemon in the list.
        pokemon_result_list.append(pokemon_id)

        # Save the pokemon with its stats in the list.
        pokemon_result_list.append(stats_container)

        return pokemon_result_list

    @staticmethod
    def modify_stats_list(pokemon_stats_list):
        """
        Modify the stat result list of the function fetch_pokemon_with_stats and transform it to a dictionary.
        """

        # Create an empty dictionary
        stats_dict = {}

        for stat in pokemon_stats_list:
            # Get the name of a stat as key and make the related base stat its value.
            stats_dict[stat.stat.name] = stat.base_stat

        return stats_dict
