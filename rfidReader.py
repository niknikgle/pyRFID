
import usb.util
import usb.core


from typing import Iterator
import array
from usb.core import Device

class HID:

    HID_MAP = {30: "1", 31: "2", 32: "3", 33: "4", 34: "5", 35: "6", 36: "7", 37: "8", 38: "9", 39: "0"}

    def __init__(self, dev: Device):

        self.dev = dev

        if dev is None:
            raise LookupError("Device not found. Check your Vendor/Product IDs.")
        if dev.is_kernel_driver_active(0):
            try:
                dev.detach_kernel_driver(0)
            except usb.core.USBError as e:
                raise NotImplementedError(f"Could not detach kernel driver: {str(e)}")
            
        dev.set_configuration()
        usb.util.claim_interface(dev, 0)

        self.endpoint = dev[0][(0,0)][0]


    def scan(self) -> Iterator[str]:
        full_string = ""
        while True:
            try:
                raw_data: list[int, int, int, int] = dev.read(self.endpoint.bEndpointAddress, self.endpoint.wMaxPacketSize, timeout=5000)

                data: int = raw_data[2]

                print(raw_data)

                if data == 0:
                    continue

                if data == 40:
                    yield full_string
                    full_string = ""
                
                elif data in self.HID_MAP:
                    full_string += self.HID_MAP[data]

            except usb.core.USBError as e:
                if e.errno == 110 or e.backend_error_code == -7:
                    continue
                else:
                    raise ConnectionError(f"USB Error: {e}")
                    break


dev = usb.core.find(idVendor=0xffff, idProduct=0x0035)
hid = HID(dev)

for code in hid.scan():
    print("New code:", code)

