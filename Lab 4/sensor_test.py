import time
import qwiic_proximity

sensor = qwiic_proximity.QwiicProximity()

if not sensor.connected:
    print("Sensor not connected!")
    raise SystemExit

sensor.begin()

# Configure stronger proximity detection
sensor.set_led_current(200)
sensor.set_prox_integration_time(8)
sensor.power_on_proximity()

print("Sensor ready!")
print("Move your finger close to the sensor.")

while True:
    value = sensor.get_proximity()
    print("Proximity:", value)
    time.sleep(0.5)
