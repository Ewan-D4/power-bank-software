# Power Bank Software Configuration
# =================================
#
# This file centralizes the hardware configuration used by the ESP32 firmware.
# Keeping pin numbers and system limits in one place makes it easier to:
# - wire the hardware correctly
# - adjust LED brightness or power limits
# - change GPIO assignments without editing many files
# - keep the firmware readable and maintainable

# GPIO Pins for LEDs (PWM)
# ------------------------
# The ESP32 can generate PWM signals on many GPIO pins. These are mapped to
# the LED channels used by the lighting system.
LED_PINS = {
    'led1': 25,  # GPIO25
    'led2': 26,  # GPIO26
    'led3': 27,  # GPIO27
    'led4': 14,  # GPIO14
}

# ADC Pin for Potentiometer
# ------------------------
# The potentiometer is read through an analog-to-digital converter (ADC).
# GPIO35 is configured as ADC1 input and is used for user control input.
POTENTIOMETER_PIN = 35  # GPIO35 (ADC1)

# Button Pins
# -----------
# These buttons are configured as active-low inputs. In other words, the GPIO
# reads HIGH (1) when the button is not pressed and LOW (0) when the button is
# pressed because of the internal pull-up resistor.
BUTTON_POWER = 32  # GPIO32 - Main power/mode button
BUTTON_SELECT = 33  # GPIO33 - Selection button

# PWM Settings
# ------------
# PWM is used to control LED brightness. The ESP32 can generate a PWM signal at
# a specific frequency and duty cycle. This project uses 10-bit PWM resolution,
# so values range from 0 to 1023.
PWM_FREQUENCY = 1000  # 1kHz for LED control
PWM_MAX_DUTY = 1023  # 10-bit resolution

# GPS Settings (UART)
# -------------------
# UART (serial communication) is used to read GPS messages from a module such as
# the NEO-6M. TX/RX pins are marked from the ESP32's perspective:
# - ESP32 TX sends data to the GPS RX
# - ESP32 RX receives data from the GPS TX
GPS_UART_NUM = 2  # UART2
GPS_BAUDRATE = 9600
GPS_TX_PIN = 17  # GPIO17
GPS_RX_PIN = 16  # GPIO16

# Battery/Power Settings
# ----------------------
# These values define the electrical thresholds used for battery safety.
# LOW_BATTERY_VOLTAGE is used to decide when the system should stop operation or
# warn the user to avoid damage to the battery.
BAT_ADC_PIN = 34  # GPIO34 - Battery voltage sensing
LOW_BATTERY_VOLTAGE = 3.0  # Volts (cutoff for safety)

# System Settings
# ---------------
# These are overall project limits. They help prevent overloading the power bank
# and keep the software operating in a predictable way.
MAX_LED_POWER = 10  # Watts per LED
TOTAL_LED_POWER = 40  # Watts (4x10W)
UPDATE_INTERVAL = 100  # milliseconds
