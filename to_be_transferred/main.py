
import board
import bitbangio
import time
import json

import adafruit_bme280.basic as adafruit_bme280
import adafruit_ina219
import adafruit_bh1750

from bmi270 import BMI270

i2c = bitbangio.I2C(
    scl=board.GP9,
    sda=board.GP10
)



def initialise_sensor(constructor):
    try:
        return constructor()
    except (OSError, ValueError, RuntimeError) as error:
        print("Sensor initialisation failed:", error)
        return None


def read_sensor(sensor, attribute):
    if sensor is None:
        return None, "unavailable"

    try:
        return getattr(sensor, attribute), "ok"
    except (OSError, ValueError, RuntimeError):
        return None, "read_error"



bme280 = initialise_sensor(
    lambda: adafruit_bme280.Adafruit_BME280_I2C(i2c)
)

ina219 = initialise_sensor(
    lambda: adafruit_ina219.INA219(i2c)
)

bh1750 = initialise_sensor(
    lambda: adafruit_bh1750.BH1750(i2c)
)

bmi270 = initialise_sensor(
    lambda: BMI270(i2c)
)


while True:


    temperature, temperature_status = read_sensor(
        bme280, "temperature"
    )

    humidity, humidity_status = read_sensor(
        bme280, "relative_humidity"
    )

    pressure, pressure_status = read_sensor(
        bme280, "pressure"
    )


    bus_voltage, bus_voltage_status = read_sensor(
        ina219, "bus_voltage"
    )

    shunt_voltage, shunt_voltage_status = read_sensor(
        ina219, "shunt_voltage"
    )

    current, current_status = read_sensor(
        ina219, "current"
    )

    power, power_status = read_sensor(
        ina219, "power"
    )


    light_lux, light_status = read_sensor(
        bh1750, "lux"
    )


    acceleration, acceleration_status = read_sensor(
        bmi270, "acceleration"
    )

    gyro, gyro_status = read_sensor(
        bmi270, "gyro"
    )


    data = {
        "timestamp": time.monotonic(),

        "sensors": {
            "bme280": {
                "temperature": temperature,
                "humidity": humidity,
                "pressure": pressure
            },

            "ina219": {
                "bus_voltage": bus_voltage,
                "shunt_voltage": shunt_voltage,
                "current": current,
                "power": power
            },

            "bh1750": {
                "light_lux": light_lux
            },

            "bmi270": {
                "acceleration": acceleration,
                "gyro": gyro
            }
        },

        "status": {
            "bme280": (
                "ok" if bme280 is not None
                else "unavailable"
            ),

            "ina219": (
                "ok" if ina219 is not None
                else "unavailable"
            ),

            "bh1750": (
                "ok" if bh1750 is not None
                else "unavailable"
            ),

            "bmi270": (
                "ok" if bmi270 is not None
                else "unavailable"
            )
        },

        "reading_status": {
            "temperature": temperature_status,
            "humidity": humidity_status,
            "pressure": pressure_status,

            "bus_voltage": bus_voltage_status,
            "shunt_voltage": shunt_voltage_status,
            "current": current_status,
            "power": power_status,

            "light_lux": light_status,

            "acceleration": acceleration_status,
            "gyro": gyro_status
        }
    }


    print(json.dumps(data))

    time.sleep(1)
