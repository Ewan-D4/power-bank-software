# Power Bank Software Configuration
# ESP32 Pin Configuration and Settings

# GPIO Pins for LEDs (PWM)
LED_PINS = {
    'led1': 25,  # GPIO25
    'led2': 26,  # GPIO26
    'led3': 27,  # GPIO27
    'led4': 14,  # GPIO14
}

# ADC Pin for Potentiometer
POTENTIOMETER_PIN = 35  # GPIO35 (ADC1)

# Button Pins
BUTTON_POWER = 32  # GPIO32 - Main power/mode button
BUTTON_SELECT = 33  # GPIO33 - Selection button

# PWM Settings
PWM_FREQUENCY = 1000  # 1kHz for LED control
PWM_MAX_DUTY = 1023  # 10-bit resolution

# GPS Settings (UART)
GPS_UART_NUM = 2  # UART2
GPS_BAUDRATE = 9600
GPS_TX_PIN = 17  # GPIO17
GPS_RX_PIN = 16  # GPIO16

# Battery/Power Settings
BAT_ADC_PIN = 34  # GPIO34 - Battery voltage sensing
LOW_BATTERY_VOLTAGE = 3.0  # Volts (cutoff for safety)

# System Settings
MAX_LED_POWER = 10  # Watts per LED
TOTAL_LED_POWER = 40  # Watts (4x10W)
UPDATE_INTERVAL = 100  # milliseconds
