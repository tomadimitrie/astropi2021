import csv
from pathlib import Path

import compute_light_directions
import compute_albedo_map
import compute_albedo
import compute_temperature

if __name__ == "__main__":
    light_directions = compute_light_directions.compute("images/image.png")
    compute_albedo_map.compute("images/image.png", light_directions)
    albedo = compute_albedo.compute("images/image.png")
    energy, temperature = compute_temperature.compute_temperature_no_greenhouse(albedo)
    optimized_albedo = compute_albedo.compute("output_albedos/image.png")
    optimized_energy, optimized_temperature = compute_temperature.compute_temperature_no_greenhouse(optimized_albedo)
    
    dir_path = Path(__file__).parent.resolve()
    data_file = dir_path / "data01.csv"

    with open(data_file, 'w') as file:
        writer = csv.writer(file)
        header = (
            "file name", "light directions", "albedo", "optimized albedo", "temperature", "optimized temperature",
            "energy",
            "optimized energy")
        writer.writerow(header)
        writer.writerow(("image.png", light_directions, albedo, optimized_albedo,
                         compute_temperature.convert_kelvin_to_celsius(temperature),
                         compute_temperature.convert_kelvin_to_celsius(optimized_temperature),
                         energy, optimized_energy))
