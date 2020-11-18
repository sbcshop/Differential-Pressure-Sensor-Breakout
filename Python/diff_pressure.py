import spidev


class DiffPressureClick:
    bus = 0

    def __init__(self, device=0, freq=5000000, mode=0b11):
        # Device is the chip select pin. Set to 0 or 1, depending on the
        # connections
        self.freq = freq
        self.mode = mode
        self.device = device
        self.spi = None
        self.init_spi()

    def init_spi(self):
        self.spi = spidev.SpiDev()

        # Open a connection to a specific bus and device (chip select pin)
        self.spi.open(self.bus, self.device)

        # Set SPI speed and mode
        self.spi.max_speed_hz = self.freq
        self.spi.mode = self.mode
        self.spi.no_cs = False

    def __read_spi(self, n=3):
        return self.spi.readbytes(n)
        # return self.spi.xfer([0, 0, 0])

    def __write_spi(self, data):
        return self.spi.xfer2(data)

    def __read_raw(self):
        buffer = self.__read_spi()
        self.__read_spi()
        # print(buffer)

        result = buffer[0]
        result = (result << 8) | buffer[1]
        result = (result << 8) | buffer[2]

        if not self.__check_status(result):
            return None

        if (buffer[0] & 0x20) >> 5:  # Bit 21 = 1; value is negative
            result = result - 4194304  # for 22 bit resolution

        return result

    @staticmethod
    def __check_status(result):
        if result > 0x400000:
            #  OVH
            return False
        elif result > 0x800000:
            #  OVL
            return False

        return True

    def diff_pressure_kpa(self):
        pressure_digital = self.__read_raw()
        if pressure_digital:
            pressure_kpa = ((pressure_digital / 2097151.0) - .04) / .09
            return pressure_kpa
        return self.__read_raw()

    def diff_pressure_mbar(self):
        """
        :return: Pressure value in mbar
        """
        pressure_kpa = self.diff_pressure_kpa()
        if pressure_kpa:
            pressure_mbar = pressure_kpa * 10
            return pressure_mbar

    @property
    def is_ready(self):
        if self.diff_pressure_kpa():
            return True
        return False


if __name__ == "__main__":
    from time import sleep

    pressureSensor = DiffPressureClick()
    while True:
        p_mbar = pressureSensor.diff_pressure_mbar()
        print(p_mbar)
        sleep(.1)
