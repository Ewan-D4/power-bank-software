# GPS Module for Power Bank Location Tracking
# ==========================================
#
# This module interfaces with a GPS receiver (for example a NEO-6M module) over
# UART serial communication. It reads NMEA sentences from the GPS and extracts
# useful values like latitude, longitude, altitude, and satellite count.
#
# The module is designed for a microcontroller environment (MicroPython), so the
# code uses the `machine` module and the ESP32's UART peripheral.
#
# Typical GPS wiring:
# - NEO-6M VCC -> 3.3V
# - NEO-6M GND -> GND
# - NEO-6M TX -> ESP32 GPIO16 (RX)
# - NEO-6M RX -> ESP32 GPIO17 (TX)

import machine
import time
from config import GPS_UART_NUM, GPS_BAUDRATE, GPS_TX_PIN, GPS_RX_PIN


class GPSModule:
    """
    Interface with a GPS module using UART serial communication.

    The GPS sends NMEA sentences such as $GPRMC and $GPGGA. These messages contain
    position data, fix quality, and satellite information. This class stores the
    latest values and exposes simple methods for reading the location state.
    """

    def __init__(self):
        # Configure the ESP32 UART peripheral for GPS communication.
        # `machine.UART(num, baudrate)` creates a serial instance. The `init()`
        # call sets the TX/RX pins and a timeout so reads can block briefly while
        # waiting for incoming bytes.
        self.uart = machine.UART(GPS_UART_NUM, GPS_BAUDRATE)
        self.uart.init(tx=GPS_TX_PIN, rx=GPS_RX_PIN, timeout=1000)

        # Store the latest decoded GPS information.
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.satellites = 0
        self.fix_type = 0  # 0=no fix, 1=GPS fix, 2=DGPS fix
        self.last_update = 0

    def read_line(self):
        """
        Read one complete line from the GPS module.

        GPS modules send ASCII text lines terminated by a newline character.
        This function reads bytes until it reaches '\n' and returns the message.

        Returns:
            bytes or None: A line of data, or None if no data is received.
        """
        line = b''
        while True:
            char = self.uart.read(1)
            if not char:
                # No data arrived before timeout.
                return None
            if char == b'\n':
                # End of the sentence reached.
                return line
            line += char

    def parse_gprmc(self, sentence):
        """
        Parse a GPRMC sentence.

        GPRMC format example:
        $GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A

        Fields:
        - time
        - status (A=active, V=void)
        - latitude
        - N/S hemisphere
        - longitude
        - E/W hemisphere
        - speed over ground
        - course
        - date

        This method validates the sentence, converts the latitude/longitude into
        decimal degrees, and stores the result as the latest position.
        """
        try:
            parts = sentence.split(',')
            if len(parts) < 9:
                return False

            status = parts[2]  # A=active, V=void
            if status != 'A':
                # The GPS has not produced a valid fix; ignore this sentence.
                return False

            # Parse latitude.
            # Format is degrees + minutes, for example 4807.038 means 48 deg 07.038 min.
            # The first two characters are degrees, the rest are minutes.
            if parts[3]:
                lat = float(parts[3][:2]) + float(parts[3][2:]) / 60
                if parts[4] == 'S':
                    lat = -lat
                self.latitude = lat

            # Parse longitude.
            # Format is degrees + minutes, for example 01131.000 means 11 deg 31.000 min.
            if parts[5]:
                lon = float(parts[5][:3]) + float(parts[5][3:]) / 60
                if parts[6] == 'W':
                    lon = -lon
                self.longitude = lon

            self.fix_type = 1
            self.last_update = time.time()
            return True
        except:
            # Catch malformed or unexpected GPS data and ignore it.
            return False

    def parse_gpgga(self, sentence):
        """
        Parse a GPGGA sentence.

        GPGGA provides fix quality and satellite information, along with altitude.
        Example format:
        $GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47

        Relevant fields:
        - fix quality (field 6)
        - number of satellites (field 7)
        - altitude (field 9)
        """
        try:
            parts = sentence.split(',')
            if len(parts) < 8:
                return False

            self.fix_type = int(parts[6])  # 0=invalid, 1=GPS, 2=DGPS, etc.
            self.satellites = int(parts[7]) if parts[7] else 0
            self.altitude = float(parts[9]) if parts[9] else None

            return self.fix_type > 0
        except:
            return False

    def update(self):
        """
        Read a GPS sentence and parse it.

        The GPS sends many sentences continuously. This method reads one line at a
        time and decides whether it is a GPRMC or GPGGA message before parsing.

        Returns:
            bool: True if a valid sentence was processed, otherwise False.
        """
        line = self.read_line()
        if not line:
            return False

        try:
            sentence = line.decode('utf-8').strip()

            if sentence.startswith('$GPRMC'):
                # GPRMC contains the main location data.
                return self.parse_gprmc(sentence[7:])
            elif sentence.startswith('$GPGGA'):
                # GPGGA contains fix quality, satellites, and altitude.
                return self.parse_gpgga(sentence[7:])
        except:
            # Ignore bad data or unsupported characters.
            pass

        return False

    def get_location(self):
        """
        Get the most recently known GPS position.

        Returns:
            tuple: (latitude, longitude, altitude, satellites, fix_type)
        """
        return (self.latitude, self.longitude, self.altitude, self.satellites, self.fix_type)

    def has_fix(self):
        """Check whether the GPS has a valid fix and usable coordinates."""
        return self.fix_type > 0 and self.latitude is not None

    def get_status_string(self):
        """Return a short human-readable summary of the GPS status."""
        if not self.has_fix():
            return "No GPS Fix"
        return f"Lat: {self.latitude:.4f}, Lon: {self.longitude:.4f}, Sats: {self.satellites}"
