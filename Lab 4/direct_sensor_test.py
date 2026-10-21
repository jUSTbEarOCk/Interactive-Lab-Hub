
import time
from smbus2 import SMBus, i2c_msg

ADDR = 0x60

with SMBus(1) as bus:
    # Read current proximity configuration
    read_cmd = i2c_msg.write(ADDR, [0x03])
    read_data = i2c_msg.read(ADDR, 2)
    bus.i2c_rdwr(read_cmd, read_data)

    data = list(read_data)
    current = data[0] | (data[1] << 8)
    print("Current config:", hex(current))

    # Clear only PS_SD bit (bit 0)
    new_value = current & ~0x0001

    write_data = i2c_msg.write(
        ADDR,
        [0x03, new_value & 0xFF, (new_value >> 8) & 0xFF]
    )

    bus.i2c_rdwr(write_data)
    print("Wrote config:", hex(new_value))

    time.sleep(0.2)

    # Read back configuration
    bus.i2c_rdwr(
        i2c_msg.write(ADDR, [0x03]),
        read_data
    )

    data = list(read_data)
    print("Readback:", hex(data[0] | (data[1] << 8)))

    # Read proximity several times
    for _ in range(20):
        bus.i2c_rdwr(
            i2c_msg.write(ADDR, [0x08]),
            read_data
        )
        data = list(read_data)
        value = data[0] | (data[1] << 8)

        print("Proximity:", value)
        time.sleep(0.3)
