import compute_light_directions
import compute_albedo_map
import compute_albedo


if __name__ == "__main__":
    compute_light_directions.compute("images/image.png")
    compute_albedo_map.compute("images/image.png")
    print(compute_albedo.compute("images/image.png"))
    print(compute_albedo.compute("output_albedos/image.png"))