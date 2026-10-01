# GPS Module for Power Bank Location Tracking
# Uses NEO-6M GPS module (cheapest option ~$5-10)
import machine
import time
from config import GPS_UART_NUM, GPS_BAUDRATE, GPS_TX_PIN, GPS_RX_PIN

class GPSModule:
    """
    Interface with NEO-6M GPS module via UART.
    Cheapest GPS option: NEO-6M (~$5-10 on AliExpress)
    
    Connection:
    - NEO-6M VCC -> 3.3V
    - NEO-6M GND -> GND
    - NEO-6M TX -> ESP32 GPIO16 (RX)
    - NEO-6M RX -> ESP32 GPIO17 (TX)
    """
    
    def __init__(self):
        self.uart = machine.UART(GPS_UART_NUM, GPS_BAUDRATE)
        self.uart.init(tx=GPS_TX_PIN, rx=GPS_RX_PIN, timeout=1000)
        
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.satellites = 0
        self.fix_type = 0  # 0=no fix, 1=GPS fix, 2=DGPS fix
        self.last_update = 0
    
    def read_line(self):
        """Read a line from GPS module"""
        line = b''
        while True:
            char = self.uart.read(1)
            if not char:
                return None
            if char == b'\n':
                return line
            line += char
    
    def parse_gprmc(self, sentence):
        """
        Parse GPRMC (Recommended Minimum) sentence.
        Format: $GPRMC,time,status,lat,lat_dir,lon,lon_dir,speed,course,date,...
        """
        try:
            parts = sentence.split(',')
            if len(parts) < 9:
                return False
            
            status = parts[2]  # A=active, V=void
            if status != 'A':
                return False
            
            # Parse latitude
            if parts[3]:
                lat = float(parts[3][:2]) + float(parts[3][2:]) / 60
                if parts[4] == 'S':
                    lat = -lat
                self.latitude = lat
            
            # Parse longitude
            if parts[5]:
                lon = float(parts[5][:3]) + float(parts[5][3:]) / 60
                if parts[6] == 'W':
                    lon = -lon
                self.longitude = lon
            
            self.fix_type = 1
            self.last_update = time.time()
            return True
        except:
            return False
    
    def parse_gpgga(self, sentence):
        """
        Parse GPGGA (Fix Data) sentence.
        Format: $GPGGA,time,lat,lat_dir,lon,lon_dir,fix_quality,num_sats,hdop,alt,...
        """
        try:
            parts = sentence.split(',')
            if len(parts) < 8:
                return False
            
            self.fix_type = int(parts[6])  # 0=invalid, 1=GPS, 2=DGPS, etc
            self.satellites = int(parts[7]) if parts[7] else 0
            self.altitude = float(parts[9]) if parts[9] else None
            
            return self.fix_type > 0
        except:
            return False
    
    def update(self):
        """Read and parse GPS data"""
        line = self.read_line()
        if not line:
            return False
        
        try:
            sentence = line.decode('utf-8').strip()
            
            if sentence.startswith('$GPRMC'):
                return self.parse_gprmc(sentence[7:])
            elif sentence.startswith('$GPGGA'):
                return self.parse_gpgga(sentence[7:])
        except:
            pass
        
        return False
    
    def get_location(self):
        """
        Get last known location.
        Returns: (latitude, longitude, altitude, satellites, fix_type)
        """
        return (self.latitude, self.longitude, self.altitude, self.satellites, self.fix_type)
    
    def has_fix(self):
        """Check if GPS has a valid fix"""
        return self.fix_type > 0 and self.latitude is not None
    
    def get_status_string(self):
        """Get human-readable GPS status"""
        if not self.has_fix():
            return "No GPS Fix"
        return f"Lat: {self.latitude:.4f}, Lon: {self.longitude:.4f}, Sats: {self.satellites}"
