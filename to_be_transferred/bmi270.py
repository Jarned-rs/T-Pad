
# bmi270.py
# CircuitPython BMI270 driver for T-Pad
# Based on the register/configuration approach in the
# MIT-licensed MicroPython BMI270 community driver.
#
# Supports acceleration in m/s^2 and gyro in degrees/second.

import time
from config_file import bmi270_config_file


class BMI270:
    CHIP_ID_REG = 0x00
    ERROR_REG = 0x02
    ACC_DATA_REG = 0x0C
    INTERNAL_STATUS_REG = 0x21

    ACC_CONF_REG = 0x40
    ACC_RANGE_REG = 0x41
    GYR_CONF_REG = 0x42
    GYR_RANGE_REG = 0x43

    INIT_CTRL_REG = 0x59
    INIT_ADDR_0_REG = 0x5B
    INIT_ADDR_1_REG = 0x5C
    INIT_DATA_REG = 0x5E

    POWER_CONF_REG = 0x7C
    POWER_CTRL_REG = 0x7D
    COMMAND_REG = 0x7E

    EXPECTED_CHIP_ID = 0x24
    GRAVITY = 9.80665

    # Default ranges: accelerometer +/-2g,
    # gyroscope +/-250 degrees/second.
    ACCEL_SCALE = 16384
    GYRO_SCALE = 131.2

    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address

        chip_id = self._read_register(self.CHIP_ID_REG)

        if chip_id != self.EXPECTED_CHIP_ID:
            raise RuntimeError(
                "BMI270 not found at address 0x{:02X}; "
                "chip ID was 0x{:02X}".format(address, chip_id)
            )

        self._load_config()

        status = self._read_register(self.INTERNAL_STATUS_REG)
        if status != 0x01:
            error = self._read_register(self.ERROR_REG)
            raise RuntimeError(
                "BMI270 configuration failed. "
                "Status=0x{:02X}, error=0x{:02X}".format(
                    status, error
                )
            )

        # Disable advanced power saving and enable
        # accelerometer and gyroscope.
        self._write_register(self.POWER_CONF_REG, 0x02)
        time.sleep(0.01)

        self._write_register(self.POWER_CTRL_REG, 0x0E)
        self._write_register(self.ACC_CONF_REG, 0xA8)
        self._write_register(self.GYR_CONF_REG, 0xA9)

        # Accelerometer range: +/-2g.
        self._write_register(self.ACC_RANGE_REG, 0x00)

        # Gyroscope range: +/-250 degrees/second.
        self._write_register(self.GYR_RANGE_REG, 0x03)

        time.sleep(0.1)

    def _read_register(self, register):
        result = bytearray(1)

        while not self.i2c.try_lock():
            pass

        try:
            self.i2c.writeto(
                self.address,
                bytes([register]),
                stop=False
            )
            self.i2c.readfrom_into(self.address, result)
        finally:
            self.i2c.unlock()

        return result[0]

    def _write_register(self, register, value):
        payload = bytes([register, value])

        while not self.i2c.try_lock():
            pass

        try:
            self.i2c.writeto(self.address, payload)
        finally:
            self.i2c.unlock()

    def _write_block(self, register, data):
        payload = bytes([register]) + bytes(data)

        while not self.i2c.try_lock():
            pass

        try:
            self.i2c.writeto(self.address, payload)
        finally:
            self.i2c.unlock()

    def _read_block(self, register, length):
        result = bytearray(length)

        while not self.i2c.try_lock():
            pass

        try:
            self.i2c.writeto(
                self.address,
                bytes([register]),
                stop=False
            )
            self.i2c.readfrom_into(self.address, result)
        finally:
            self.i2c.unlock()

        return result

    def _load_config(self):
        config = bmi270_config_file

        # The configuration must contain 8192 bytes.
        if len(config) != 8192:
            raise RuntimeError(
                "Incorrect BMI270 configuration length: "
                "{} bytes; expected 8192".format(len(config))
            )

        # Stop power saving before uploading configuration.
        self._write_register(self.POWER_CONF_REG, 0x00)
        time.sleep(0.001)

        self._write_register(self.INIT_CTRL_REG, 0x00)

        # Upload 256 blocks of 32 bytes.
        for block in range(256):
            self._write_register(self.INIT_ADDR_0_REG, 0x00)
            self._write_register(self.INIT_ADDR_1_REG, block)

            start = block * 32
            chunk = config[start:start + 32]

            self._write_block(self.INIT_DATA_REG, chunk)
            time.sleep(0.0001)

        self._write_register(self.INIT_CTRL_REG, 0x01)
        time.sleep(0.025)

    @staticmethod
    def _signed_16(low, high):
        value = low | (high << 8)

        if value & 0x8000:
            value -= 0x10000

        return value

    @property
    def acceleration(self):
        """Return X, Y, Z acceleration in m/s^2."""
        raw = self._read_block(self.ACC_DATA_REG, 6)

        x = self._signed_16(raw[0], raw[1])
        y = self._signed_16(raw[2], raw[3])
        z = self._signed_16(raw[4], raw[5])

        scale = self.GRAVITY / self.ACCEL_SCALE

        return (
            x * scale,
            y * scale,
            z * scale
        )

    @property
    def gyro(self):
        """Return X, Y, Z angular velocity in degrees/second."""
        raw = self._read_block(self.ACC_DATA_REG + 6, 6)

        x = self._signed_16(raw[0], raw[1])
        y = self._signed_16(raw[2], raw[3])
        z = self._signed_16(raw[4], raw[5])

        return (
            x / self.GYRO_SCALE,
            y / self.GYRO_SCALE,
            z / self.GYRO_SCALE
        )
