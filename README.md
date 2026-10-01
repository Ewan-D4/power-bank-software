# Power Bank Software

MicroPython firmware for an ESP32-based power bank with 4x10W high-power LEDs, GPS tracking, potentiometer brightness control, and button inputs.

## Hardware Requirements

### Core Components
- **Microcontroller**: ESP32 (30 pins recommended)
- **LEDs**: 4x 10W High-Power LEDs (or compatible)
- **LED Driver**: MOSFET/PWM driver circuit for high-power switching (e.g., IRF540N)
- **Potentiometer**: 10kΩ variable resistor for brightness control
- **Buttons**: 2x Tactile buttons (Power, Mode Select)
- **GPS Module**: NEO-6M GPS receiver (~$5-10)
- **Power Supply**: LiPo battery pack (suitable for 40W total LED power)

### GPS Module (Cheapest Option)
- **NEO-6M GPS Module** (~$5-10 on AliExpress/Alibaba)
- Advantages:
  - Very affordable
  - Low power consumption (~60mA)
  - Compact size
  - Widely available
  - Standard UART interface (easy to integrate)
- Connection: Simple UART on GPIO16 (RX) and GPIO17 (TX)

### Wiring Diagram

```
ESP32 GPIO Assignments:
- GPIO25, 26, 27, 14  -> LED PWM Control (via MOSFET driver)
- GPIO35 (ADC1)       -> Potentiometer (0-3.3V)
- GPIO32              -> Power Button
- GPIO33              -> Mode Select Button
- GPIO16              -> GPS RX (from NEO-6M TX)
- GPIO17              -> GPS TX (to NEO-6M RX)
- GPIO34 (ADC)        -> Battery Voltage Sensing (optional)

NEO-6M GPS:
- VCC -> 3.3V
- GND -> GND
- TX  -> ESP32 GPIO16
- RX  -> ESP32 GPIO17
```

## Features

### Operating Modes

1. **Manual Mode** (Default)
   - Potentiometer directly controls LED brightness (0-100%)
   - Real-time adjustment
   - Great for hands-on control

2. **Auto Mode**
   - Button cycles through brightness levels: 0% → 25% → 50% → 75% → 100% → 0%
   - One press = one step
   - Useful for preset lighting levels

3. **GPS Tracking Mode**
   - LED brightness increases with number of satellites locked
   - Useful for navigation and signal strength indication
   - Shows current location (latitude, longitude, altitude)
   - Requires NEO-6M GPS module

### Controls
- **Power Button (GPIO32)**: Toggle power on/off
- **Mode Button (GPIO33)**: Cycle through manual → auto → gps_track modes
- **Potentiometer (GPIO35)**: Adjust brightness in manual mode (0-100%)

## Installation

1. **Flash MicroPython** to ESP32:
   ```bash
   # Download ESP32 MicroPython firmware from micropython.org
   esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
   esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-version.bin
   ```

2. **Upload Files** to ESP32:
   ```bash
   # Using ampy tool
   ampy --port /dev/ttyUSB0 put config.py
   ampy --port /dev/ttyUSB0 put led_control.py
   ampy --port /dev/ttyUSB0 put input_handler.py
   ampy --port /dev/ttyUSB0 put gps_module.py
   ampy --port /dev/ttyUSB0 put main.py
   ```

3. **Configure** in `config.py`:
   - Adjust GPIO pin numbers to match your wiring
   - Set PWM frequency and ADC sensitivity
   - Customize battery voltage thresholds

4. **Run**:
   ```
   # Connect via serial monitor and it will auto-run main.py
   # Or manually:
   import main
   ```

## File Structure

- **config.py** - All configuration settings (pins, frequencies, thresholds)
- **led_control.py** - LED PWM control (4 channels)
- **input_handler.py** - Button and potentiometer input handling
- **gps_module.py** - NEO-6M GPS module interface (UART-based)
- **main.py** - Main control loop and mode management
- **README.md** - This file

## Power Consumption

- **ESP32**: ~80-100mA (active)
- **4x10W LEDs**: ~3.3A @ full brightness (on external power)
- **NEO-6M GPS**: ~60mA (average)
- **Total System**: Variable (depends on LED brightness)

## Performance Tips

1. **Reduce GPS Update Rate**: Modify `gps_update_interval` to lower power draw
2. **PWM Frequency**: Higher frequency = smoother dimming but more current draw
3. **Smooth Potentiometer Reads**: Adjust `smoothing` parameter for noise rejection
4. **Battery Monitoring**: Implement low-battery cutoff in main.py

## Troubleshooting

### GPS Not Working
- Check UART baud rate (default 9600)
- Verify TX/RX are not swapped
- GPS needs clear sky view for initial fix (5-10 minutes typical)
- Check NEO-6M power supply voltage

### LEDs Not Responding
- Verify MOSFET driver connections
- Check PWM frequency in config.py
- Test individual LED pins with simple PWM test script

### Button Input Not Working
- Verify GPIO pins in config.py
- Check pull-up/pull-down resistor wiring
- Increase button debounce time if needed

## Future Enhancements

- [ ] Battery voltage monitoring and low-battery alerts
- [ ] Data logging to SD card
- [ ] Web interface for remote control
- [ ] Wireless connectivity (WiFi/Bluetooth)
- [ ] Temperature monitoring for thermal protection
- [ ] GPS data logging and track recording

## License

MIT License - Feel free to modify and use as needed!

## References

- [MicroPython Documentation](https://docs.micropython.org/)
- [ESP32 Pinout](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/)
- [NEO-6M GPS Module Guide](https://learn.sparkfun.com/tutorials/gps-basics)
