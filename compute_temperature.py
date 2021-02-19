def compute_temperature_no_greenhouse(albedo):
    
    solar_insolation = 1361
    stefan_boltzmann_constant = 5.6704 * (10 ** (-8))
    absorbed_energy = solar_insolation * (1 - albedo)
    temperature = (absorbed_energy / (4 * stefan_boltzmann_constant)) ** 0.25
    return (absorbed_energy, temperature)


def convert_kelvin_to_celsius(kelvin):
    return kelvin - 273.15
