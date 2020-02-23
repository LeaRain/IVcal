import logging

from ivcal.calculation.calculator_database import DatabaseCalculatorHandler

logging.basicConfig(filename="events.log")


class UserInteraction:
    """
    Create a class for all the interactions with a user.
    """

    def __init__(self, data_source="local"):
        # Define a data source, which should be local as default and has access to the local database.
        self.data_source = data_source

        # The data source can also be defined as api. As a result, the api is used for fetching data, while the local
        # database is not touched.
        if self.data_source == "api":
            from ivcal.data_collection.call_api import APIClient
            self.api_client = APIClient()

        # Save the current pokemon data in a dictionary.
        self.current_pokemon_data = {}
        # Save the current pokemon base data in a dictionary.
        self.current_pokemon_base_data = {}
        # Establish a connection to the database file with a handler.
        self.database_handler = DatabaseCalculatorHandler()

    def first_time_question(self):
        """
        Ask the user, if it's their first time, they run this program. This is necessary, if the data base is local. If
        the data comes from the API, this is irrelevant.
        """

        if self.data_source == "local":
            user_answer = None

            # Initiate a user question process.
            while user_answer is None:
                user_answer = input("Is this the first time you run this program? (Y/n) ").lower()

                # Default answer is yes and True.
                if user_answer in ["y", ""]:
                    print("Please wait a minute (or two, or three, ...). Data collection for the local database in "
                          "progress.")

                    return True

                elif user_answer == "n":
                    return False

                else:
                    user_answer = None

        else:
            return False

    def get_pokemon_name(self):
        """
        Get the name of a pokemon with user interaction.
        """

        # Set the id to None for the next while loop.
        pokemon_id = None

        while pokemon_id is None:
            # Pokemon names are stored in lower case.
            pokemon_user_name = input("What is the name of your pokemon? ").lower()

            # Save the name of the current pokemon.
            self.current_pokemon_data["name"] = pokemon_user_name

            if self.data_source == "local":
                pokemon_id = self.database_handler.get_pokemon_id_by_name(pokemon_user_name)

            else:
                pokemon_id = self.api_client.fetch_pokemon_id_with_name(pokemon_user_name)

            if pokemon_id is None:
                print("Pokemon not found! Please try again.")

        # After leaving the while loop with correct input, the id is stored in the dictionary for pokemon data.
        self.current_pokemon_data["id"] = pokemon_id

        # After saving the correct id, get the base stats for the pokemon.
        self.get_pokemon_base_stats()

    def get_pokemon_level(self):
        """
        Get the level of a pokemon by user interaction.
        """

        # Set the level to None for reaching the loop.
        pokemon_level = None

        while pokemon_level is None:
            pokemon_level = input("What is the level of your pokemon? ")

            # Use a try statement to prevent an error and react with a plausible information.
            try:
                # The level of a pokemon needs to be a number.
                pokemon_level = int(pokemon_level)

                # The level of a pokemon needs to be at least 1 or as a maximum 100.
                if pokemon_level < 0 or pokemon_level > 100:
                    print("The level of your pokemon needs to be between 1 and 100.")
                    pokemon_level = None

            except Exception as error:
                logging.error("An error occurred: {}".format(error))
                print("Your level needs to be a positive number.")
                pokemon_level = None

        # Save the level in the dictionary for the current pokemon.
        self.current_pokemon_data["level"] = pokemon_level

    def get_pokemon_stats(self):
        """
        Get the status values of a pokemon by user interaction.
        """

        # Define the existing status values.
        status_values = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]

        # Get an input for every value.
        for value in status_values:
            value_input = None

            while value_input is None:
                value_input = input("What is the status value for {} of your pokemon? ".format(value))

                try:
                    # The value needs to be an integer number.
                    value_input = int(value_input)

                    # The value needs to be larger than 0.
                    if value_input < 0:
                        print("The status value of your pokemon needs to be larger than 0.")
                        value_input = None

                except Exception as error:
                    logging.error("An error occurred: {}".format(error))
                    print("Your status value needs to be a positive number.")
                    value_input = None

            # Save the data about the pokemon.
            self.current_pokemon_data[value] = value_input

    def get_pokemon_ev(self):
        """
        Get the evs (effort values) of a pokemon by user interaction.
        """

        # Define the existing status values.
        status_values = ["hp_ev", "attack_ev", "defense_ev", "special-attack_ev", "special-defense_ev", "speed_ev"]

        # Define a sum, which only can be 510 or smaller.
        ev_sum = 0

        # Get an input for every value.
        for value in status_values:
            ev_input = None

            while ev_input is None:
                ev_input = input("What is {} (effort value) of your pokemon? ".format(value))

                try:
                    # The value needs to be an integer number.
                    ev_input = int(ev_input)

                    # The value needs to be larger than 0 and smaller than 255.
                    if 0 <= ev_input <= 255:
                        # The sum must be smaller than 511
                        if ev_input + ev_sum <= 510:
                            ev_sum += ev_input

                        else:
                            print("The total sum of your effort values must not be larger than 510.")
                            ev_input = None

                    else:
                        print("The effort value of your pokemon needs to be between 0 and 255.")
                        ev_input = None

                except Exception as error:
                    logging.error("An error occurred: {}".format(error))
                    print("Your status value needs to be a positive number.")
                    ev_input = None

            self.current_pokemon_data[value] = ev_input

    def get_pokemon_nature(self):
        """
        Get the name of the nature of a pokemon by user interaction.
        """
        # Set the id to None for the next while loop.
        nature_id = None

        while nature_id is None:
            # Nature names are stored in lower case.
            nature_name = input("What is the nature of your pokemon? ").lower()

            if self.data_source == "local":
                nature_id = self.database_handler.get_nature_id_by_name(nature_name)

            else:
                nature_id = self.api_client.fetch_nature_id_with_name(nature_name)

            if nature_id is None:
                print("Nature not found! Please try again.")

        # After leaving the while loop with correct input, the id is stored in the dictionary for pokemon data.
        self.current_pokemon_data["nature_id"] = nature_id

        self.get_nature_influence_stats()

    def get_pokemon_base_stats(self):
        """
        Get the base stats of a pokemon by the given method.
        """

        # Use the local method.
        if self.data_source == "local":
            # Use the class for database handling
            base_stats = self.database_handler.get_pokemon_base_stats_by_id(self.current_pokemon_data["id"])

        # Use the api method.
        else:
            # The api function returns a list and only the last part of the list is necessary
            base_stats = self.api_client.fetch_pokemon_with_stats(self.current_pokemon_data["id"])[1]

        # Update the dictionary with pokemon data.
        self.current_pokemon_base_data.update(base_stats)

    def get_nature_influence_stats(self):
        """
        Get the influence of the nature on the status values.
        """

        if self.data_source == "local":
            # Ask the local database.
            nature_effect_result = self.database_handler.get_nature_status_effects(self.current_pokemon_data[
                                                                                       "nature_id"])

        else:
            # Use the api function, which returns a dictionary with a decreased and an increased value.
            nature_effect_dict = self.api_client.fetch_nature_with_status_effect(self.current_pokemon_data["nature_id"])

            # Make a list of potential influenced natures for iterating.
            influenced_natures = ["attack", "defense", "special-attack", "special-defense", "speed"]

            # Make a dictionary for saving the results.
            nature_effect_result = {}

            for nature in influenced_natures:
                # Define the nature effect for its further use in the application and in the dictionary.
                nature_effect = "{}_nature".format(nature)

                # Check for decreased nature.
                if nature == nature_effect_dict["decreased"]:
                    # Set the value to 0.9
                    nature_effect_result[nature_effect] = 0.9

                # Check for increased nature.
                elif nature == nature_effect_dict["increased"]:
                    # Set the value to 1.1
                    nature_effect_result[nature_effect] = 1.1

                else:
                    nature_effect_result[nature_effect] = 1

        # Update the class-wide dictionary with the new data
        self.current_pokemon_data.update(nature_effect_result)

    def show_iv_result(self, iv_calculation_result):
        """
        Show the results of the calculation to the user.
        """

        print("The iv result for your pokemon {} is:\n"
              "hp: {}\n"
              "attack: {}\n"
              "defense: {}\n"
              "special-attack: {}\n"
              "special-defense: {}\n"
              "speed: {}".format(self.current_pokemon_data["name"],
                                 iv_calculation_result["hp"],
                                 iv_calculation_result["attack"],
                                 iv_calculation_result["defense"],
                                 iv_calculation_result["special-attack"],
                                 iv_calculation_result["special-defense"],
                                 iv_calculation_result["speed"]))


def local_data_source_question():
    """
    Ask the user for the data source of the program. This function is not part of the class above, because in a dialog,
    an object of the class for user interaction is created later.
    """

    user_answer = None

    while user_answer is None:
        user_answer = input("Do you want to use the local database as data source? (Y/n) ")

        if user_answer in ["y", ""]:
            return True

        elif user_answer == "n":
            return False

        else:
            user_answer = None
