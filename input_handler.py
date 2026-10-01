# Input Handler Module for Buttons and Potentiometer
import machine
import time
from config import BUTTON_POWER, BUTTON_SELECT, POTENTIOMETER_PIN

class InputHandler:
    """
    Handles button inputs and potentiometer reading for power bank control.
    """
    
    def __init__(self, callback_power=None, callback_select=None):
        self.button_power = machine.Pin(BUTTON_POWER, machine.Pin.IN, machine.Pin.PULL_UP)
        self.button_select = machine.Pin(BUTTON_SELECT, machine.Pin.IN, machine.Pin.PULL_UP)
        self.adc = machine.ADC(machine.Pin(POTENTIOMETER_PIN))
        self.adc.atten(machine.ADC.ATTN_11DB)  # Full range 0-3.3V
        
        self.callback_power = callback_power
        self.callback_select = callback_select
        
        self.last_power_state = 1
        self.last_select_state = 1
        self.last_pot_value = 0
    
    def read_potentiometer(self, smoothing=5):
        """
        Read potentiometer value (0-100) with smoothing.
        
        Args:
            smoothing (int): Number of samples to average
            
        Returns:
            int: 0-100 percent
        """
        readings = []
        for _ in range(smoothing):
            readings.append(self.adc.read())
            time.sleep(0.01)
        
        avg = sum(readings) // len(readings)
        value = (avg / 4095) * 100  # Convert 12-bit ADC to 0-100
        return int(value)
    
    def check_buttons(self):
        """
        Check for button presses (edge detection).
        Returns tuple: (power_pressed, select_pressed)
        """
        power_state = self.button_power.value()
        select_state = self.button_select.value()
        
        power_pressed = False
        select_pressed = False
        
        # Detect falling edge (button press, active low)
        if self.last_power_state == 1 and power_state == 0:
            power_pressed = True
            if self.callback_power:
                self.callback_power()
        
        if self.last_select_state == 1 and select_state == 0:
            select_pressed = True
            if self.callback_select:
                self.callback_select()
        
        self.last_power_state = power_state
        self.last_select_state = select_state
        
        return power_pressed, select_pressed
    
    def get_potentiometer(self):
        """Get current potentiometer value"""
        return self.read_potentiometer(smoothing=3)
