def compute_temperature_no_greenhouse(albedo):
    """
    Function that calculates the raw theoretical temperature (no greenhouse effect) and the surface absorbed energy
    :param albedo: the albedo of the photographed area
    :return: a tuple which contains the absorbed energy from the Sun by the surface and also the theoretical temperature
    """
    solar_insolation = 1361 # solar insolation(solar constant) in watts per square meter
    stefan_boltzmann_constant = 5.6704 * (10 ** (-8)) # the Stefan-Boltzmann constant in watts / m^2 K^2
    absorbed_energy = solar_insolation * (1 - albedo) # absorbed energy from the Sun by the photographed surface
    temperature = (absorbed_energy / (4 * stefan_boltzmann_constant)) ** 0.25 # Stefan-Boltzmann law
    return (absorbed_energy, temperature)


def convert_kelvin_to_celsius(kelvin):
    """
    Function that converts a Kelvin-valued temperature into Celsius degrees
    :param kelvin: the number of kelvins
    :return: the value of temperature in Celsius degrees (float)
    """
    return kelvin - 273.15
