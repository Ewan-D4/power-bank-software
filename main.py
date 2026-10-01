# Main Power Bank Control Software
# ESP32 with 4x10W LEDs, Potentiometer control, GPS tracking, Button input

import time
import machine
from led_control import LEDController
from input_handler import InputHandler
from gps_module import GPSModule

class PowerBankController:
    """
    Main controller for power bank with LED lights and GPS tracking.
    """
    
    def __init__(self):
        print("\n=== Power Bank Software Initializing ===")
        self.led_controller = LEDController()
        self.gps = GPSModule()
        self.input_handler = InputHandler(
            callback_power=self.on_power_button,
            callback_select=self.on_select_button
        )
        
        self.mode = 'manual'  # manual, auto, gps_track
        self.is_running = True
        self.last_gps_update = 0
        self.gps_update_interval = 5  # seconds
        
        print("Power Bank Controller Ready!")
        print("Modes: 'manual' (pot control), 'auto' (button control), 'gps_track'")
    
    def on_power_button(self):
        """Callback for power button press"""
        print("Power button pressed")
        self.is_running = not self.is_running
        if not self.is_running:
            self.led_controller.all_off()
            print("Power Bank OFF")
        else:
            print("Power Bank ON")
    
    def on_select_button(self):
        """Callback for select button press"""
        modes = ['manual', 'auto', 'gps_track']
        current_idx = modes.index(self.mode)
        self.mode = modes[(current_idx + 1) % len(modes)]
        print(f"Mode switched to: {self.mode}")
        
        if self.mode == 'gps_track':
            self.led_controller.pulse(duration_ms=500)
    
    def handle_manual_mode(self):
        """Manual brightness control via potentiometer"""
        brightness = self.input_handler.get_potentiometer()
        self.led_controller.set_brightness(brightness)
        return brightness
    
    def handle_auto_mode(self):
        """Auto mode - brightness increases with each press"""
        current = self.led_controller.get_brightness()
        new_brightness = (current + 25) % 125  # 0, 25, 50, 75, 100
        self.led_controller.set_brightness(new_brightness)
        return new_brightness
    
    def handle_gps_mode(self):
        """GPS tracking mode - LEDs fade based on signal strength"""
        if time.time() - self.last_gps_update > self.gps_update_interval:
            # Try to read GPS data
            for _ in range(10):  # Try a few times
                if self.gps.update():
                    self.last_gps_update = time.time()
                    break
        
        # Set brightness based on number of satellites
        if self.gps.has_fix():
            brightness = min(100, (self.gps.satellites / 12) * 100)
            self.led_controller.set_brightness(brightness)
            return brightness, self.gps.get_status_string()
        else:
            self.led_controller.all_off()
            return 0, "Searching for GPS..."
    
    def run(self):
        """Main control loop"""
        loop_count = 0
        
        while True:
            try:
                # Check buttons
                power_pressed, select_pressed = self.input_handler.check_buttons()
                
                if not self.is_running:
                    time.sleep(0.1)
                    continue
                
                # Handle different modes
                if self.mode == 'manual':
                    brightness = self.handle_manual_mode()
                    if loop_count % 50 == 0:  # Print every 5 seconds
                        print(f"[Manual] Brightness: {brightness}%")
                
                elif self.mode == 'auto':
                    if power_pressed:
                        brightness = self.handle_auto_mode()
                        print(f"[Auto] Brightness: {brightness}%")
                
                elif self.mode == 'gps_track':
                    result = self.handle_gps_mode()
                    if isinstance(result, tuple):
                        brightness, status = result
                        if loop_count % 20 == 0:  # Print less frequently
                            print(f"[GPS] {status}")
                
                loop_count += 1
                time.sleep(0.1)  # 100ms loop
            
            except KeyboardInterrupt:
                print("\nShutting down...")
                self.led_controller.all_off()
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)

if __name__ == '__main__':
    controller = PowerBankController()
    controller.run()
