class IVCalculator:
    """
    Create a class for calculating the IV (individual values) of a pokemon with its specific data and the base data for
    its pokemon type.
    """

    def __init__(self, pokemon_input_data_dict, pokemon_base_data_dict):
        # Make the parameters class-wide accessible.
        self.pokemon_input_data = pokemon_input_data_dict
        self.pokemon_base_data = pokemon_base_data_dict

    def calculate_all_iv_values(self):
        """
        Calculate all iv values and return them in a dictionary.
        """

        # Create an empty dictionary for the results
        iv_result_dictionary = {}

        # Define the values, which should be calculated for iterating over them.
        values_to_calculate = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]

        for value in values_to_calculate:
            # Define a string for the ev value and the nature value of a specific status value.
            ev_value = "{}_ev".format(value)
            nature_value = "{}_nature".format(value)

            # Standard calculation is for status values which are not the HP value.
            if value != "hp":
                iv_value = self.calculate_single_iv_value(value, ev_value, nature_value)

            else:
                iv_value = self.calculate_hp_iv_value()

            iv_value = self.round_iv_value(iv_value)

            # Save the result in the dictionary.
            iv_result_dictionary[value] = iv_value

        return iv_result_dictionary

    def calculate_single_iv_value(self, specific_value, specific_value_ev, nature_effect):
        """
        Calculate one single IV value for one status value with the value and nature references to the class wide
        dictionaries. This function works for all values except HP.
        """

        # Use one hell of formula for IV calculation.
        single_iv_value = ((((self.pokemon_input_data[specific_value] / self.pokemon_input_data[nature_effect]) - 5)
                            * 100) / self.pokemon_input_data["level"]) - 2 * self.pokemon_base_data[specific_value] \
                          - 0.25 * self.pokemon_input_data[specific_value_ev]

        return single_iv_value

    def calculate_hp_iv_value(self):
        """
        Calculate the HP IV value with its specific formula.
        """

        # Use one hell of formula for IV calculation.
        hp_iv_value = (((self.pokemon_input_data["hp"] - self.pokemon_input_data["level"] - 10) * 100) /
                       self.pokemon_input_data["level"]) - 2 * self.pokemon_base_data["hp"] - 0.25 * \
                      self.pokemon_input_data["hp_ev"]

        return hp_iv_value

    @staticmethod
    def round_iv_value(iv_value):
        """
        Round the IV value to a "realistic" value. Every IV value can be an integer number between 0 and 31.
        """

        # If a value is smaller than 0, it is a calculation issue.
        if iv_value < 0:
            iv_value = 0

        # If a value is larger than 0, it is a calculation issue.
        if iv_value > 31:
            iv_value = 31

        # Round to the smaller integer number.
        rounded_iv_value = int(iv_value)

        return rounded_iv_value

