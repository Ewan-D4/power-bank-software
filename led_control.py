# LED Control Module for 4x10W LEDs via PWM on ESP32
import machine
from config import LED_PINS, PWM_FREQUENCY, PWM_MAX_DUTY

class LEDController:
    """
    Controls 4 high-power LEDs using PWM on ESP32.
    Uses external mosfet/driver circuit for actual power delivery.
    """
    
    def __init__(self):
        self.leds = {}
        self.brightness = 0  # 0-100%
        self.init_pwm()
    
    def init_pwm(self):
        """Initialize PWM on all LED pins"""
        for led_name, pin in LED_PINS.items():
            pwm = machine.PWM(machine.Pin(pin))
            pwm.freq(PWM_FREQUENCY)
            pwm.duty(0)  # Start off
            self.leds[led_name] = pwm
        print("LED PWM initialized for 4 channels")
    
    def set_brightness(self, brightness):
        """
        Set LED brightness 0-100%
        
        Args:
            brightness (int): 0-100 percent
        """
        self.brightness = max(0, min(100, brightness))
        duty_value = int((self.brightness / 100) * PWM_MAX_DUTY)
        
        for led in self.leds.values():
            led.duty(duty_value)
        
        return self.brightness
    
    def get_brightness(self):
        """Get current brightness level"""
        return self.brightness
    
    def pulse(self, duration_ms=1000):
        """
        Simple pulse effect for indication
        """
        import time
        steps = 10
        for i in range(steps):
            self.set_brightness((i / steps) * 100)
            time.sleep(duration_ms / (steps * 2))
        for i in range(steps, 0, -1):
            self.set_brightness((i / steps) * 100)
            time.sleep(duration_ms / (steps * 2))
    
    def all_off(self):
        """Turn all LEDs off"""
        self.set_brightness(0)
    
    def all_on(self):
        """Turn all LEDs to full brightness"""
        self.set_brightness(100)
