from serial.tools.list_ports import comports
import platform
import usb
import os
from .port import Port
import sys

    
def find_motor(ser_no):
    if platform.system() != 'Linux':
        raise NotImplementedError("Your operating system is not supported. "
            "PyStage_APT only works on Linux.")

    # Use comports() for both VID/PID and serial number matching.
    # pyusb serial_number access fails in 1.3.x when ftdi_sio has claimed the device,
    # but comports() reads from sysfs and works regardless of kernel driver state.
    for port_info in comports():
        hwid = dict(y.split('=', 1) for y in port_info[2].split(' ') if '=' in y)
        if hwid.get('VID:PID', '').upper() != '0403:FAF0':
            continue
        if hwid.get('SER', None) != ser_no:
            continue

        p = Port.create(port_info[0], ser_no)
        for stage in p.get_stages().values():
            yield stage
            
     
        # Example device:
        # Manufacturer                1. Thorlabs
        # Product                     2. APT DC Motor Controller
        # Serial No.                  3. 83844171
        
if __name__ == '__main__':
    args = sys.argv[1:]
    ser_no = args[0]
    find_motor(ser_no)
    # print(list(find_stages()))


