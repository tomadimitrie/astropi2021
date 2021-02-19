import csv
import datetime
import time
from enum import Enum
from pathlib import Path
import ephem
import math
import reverse_geocoder
from logzero import logger, logfile
import picamera

import compute_light_directions
import compute_albedo_map
import compute_albedo
import compute_temperature

TWILIGHT_ANGLE = math.radians(-6)


class TimePeriod(Enum):
    DAY = 0
    NIGHT = 1


def get_time_period(iss):
    """
    Returns whether the photographed area is during the day or the night
    :param iss: the ISS object
    :return: TimePeriod
    """
    observer = ephem.Observer()

    observer.lat = iss.sublat
    observer.long = iss.sublong

    observer.elevation = 0
    sun = ephem.Sun()
    sun.compute(observer)
    sun_angle = math.degrees(sun.alt)

    return TimePeriod.DAY if sun_angle > TWILIGHT_ANGLE else TimePeriod.NIGHT


if __name__ == "__main__":
    try:
        dir_path = Path(__file__).parent.resolve()

        # setup headers and logfile
        logfile(str(dir_path / "program.log"))
        with open(str(dir_path / "data01.csv"), "w") as file:
            writer = csv.writer(file)
            writer.writerow((
                "file name",
                "light directions",
                "albedo",
                "optimized albedo",
                "temperature",
                "optimized temperature",
                "energy",
                "optimized energy"
            ))
        with open(str(dir_path / "data02.csv"), "w") as file:
            csv.writer(file).writerow(("image", "latitude", "longitude", "location", "time"))

        name = "ISS (ZARYA)"
        line1 = "1 25544U 98067A   21050.35666428  .00001943  00000-0  43448-4 0  9992"
        line2 = "2 25544  51.6441 205.5251 0003032  33.1814  49.2099 15.48980511270331"
        iss = ephem.readtle(name, line1, line2)

        # setup the camera
        cam = picamera.PiCamera()
        cam.resolution = (400, 300)

        # Create a datetime variable to store the start time
        start_time = datetime.datetime.now()
        # Create a datetime variable to store the current time
        now_time = datetime.datetime.now()
        computed_photo_count = 0
        photo_count = 0

        while now_time < start_time + datetime.timedelta(minutes=170):
            iss.compute()
            # Get the country below ISS at the moment.
            pos = (iss.sublat / ephem.degree, iss.sublong / ephem.degree)
            location = reverse_geocoder.search(pos)
            time_period = get_time_period(iss)

            if time_period == TimePeriod.DAY:
                # capture the photo and write info about it in the csv
                cam.capture(str(dir_path / "images" / (str(photo_count) + ".png")), format="png")
                with open(str(dir_path / "data02.csv"), "a") as file:
                    csv.writer(file).writerow((photo_count, iss.sublat, iss.sublong, location, now_time))
                logger.info(
                    "took photo with index " + str(photo_count) + " started at " + str(
                        now_time) + " and ended at " + str(datetime.datetime.now())
                )
                time.sleep(2 * 60)
                photo_count += 1
            else:
                if computed_photo_count <= photo_count and photo_count != 0:
                    # compute the data
                    light_directions = compute_light_directions.compute(
                        str(dir_path / "images" / (str(str(computed_photo_count) + ".png")))
                    )
                    logger.info(
                        "computed light directions with index " + str(computed_photo_count) + " started at " + str(
                            now_time) + " and ended at " + str(datetime.datetime.now())
                    )
                    if light_directions is not None:
                        compute_albedo_map.compute(
                            str(dir_path / "images" / (str(computed_photo_count) + ".png")),
                            light_directions
                        )
                        logger.info(
                            "computed albedo map with index " + str(computed_photo_count) + " started at " + str(
                                now_time) + " and ended at " + str(datetime.datetime.now())
                        )
                        albedo = compute_albedo.compute(dir_path / "images" / (str(computed_photo_count) + ".png"))
                        energy, temperature = compute_temperature.compute_temperature_no_greenhouse(albedo)
                        optimized_albedo = compute_albedo.compute(
                            str(dir_path / "output_albedos" / (str(computed_photo_count) + ".png"))
                        )
                        optimized_energy, optimized_temperature = compute_temperature.compute_temperature_no_greenhouse(
                            optimized_albedo
                        )

                        # write info in the csv
                        with open(str(dir_path / "data01.csv"), 'a') as file:
                            writer = csv.writer(file)
                            writer.writerow((
                                computed_photo_count,
                                light_directions,
                                albedo,
                                optimized_albedo,
                                compute_temperature.convert_kelvin_to_celsius(temperature),
                                compute_temperature.convert_kelvin_to_celsius(optimized_temperature),
                                energy, optimized_energy
                            ))
                    logger.info(
                        "computed image with index " + str(computed_photo_count) + " started at " + str(
                            now_time) + " and ended at " + str(datetime.datetime.now())
                    )
                    computed_photo_count += 1
            now_time = datetime.datetime.now()
    except Exception as ex:
        logger.error(ex)