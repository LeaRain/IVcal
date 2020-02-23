from ivcal.calculation.user_communication import UserInteraction, local_data_source_question
from ivcal.data_collection.massive_api_call import get_all_pokemon_names, get_all_pokemon_stats, get_all_nature_names, \
    get_all_nature_stats

from ivcal.calculation.calculator import IVCalculator


def data_collection():
    """
    Get all the data for the database file.
    """

    get_all_pokemon_names()
    get_all_pokemon_stats()
    get_all_nature_names()
    get_all_nature_stats()


def user_information_collection(user_interaction_object):
    """
    Collect the information about the pokemon,
    """

    user_interaction_object.get_pokemon_name()
    user_interaction_object.get_pokemon_level()
    user_interaction_object.get_pokemon_stats()
    user_interaction_object.get_pokemon_ev()
    user_interaction_object.get_pokemon_nature()

    return user_interaction_object.current_pokemon_data, user_interaction_object.current_pokemon_base_data


def main():
    """
    Make all necessary steps as main function and application
    """

    # Get the data source.
    data_source_answer = local_data_source_question()

    # The data source is the local database in this case.
    if data_source_answer is True:
        user_interaction = UserInteraction()

    # The api is used.
    else:
        user_interaction = UserInteraction(data_source="api")

    # Ask for the first usage to collect all necessary data.
    load_massive_data = user_interaction.first_time_question()

    if load_massive_data is True:
        data_collection()

    # Get the necessary user data.
    pokemon_data = user_information_collection(user_interaction)

    # The IV calculator needs the pokemon data and the base data.
    iv_calculator = IVCalculator(pokemon_data[0], pokemon_data[1])

    # Get the IV results.
    iv_result = iv_calculator.calculate_all_iv_values()

    # Show the results to the user.
    user_interaction.show_iv_result(iv_result)
