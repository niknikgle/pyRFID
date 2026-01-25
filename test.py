import usb.core
import usb.util

# Mapping HID scan codes to numbers
HID_MAP = {
    30: "1",
    31: "2",
    32: "3",
    33: "4",
    34: "5",
    35: "6",
    36: "7",
    37: "8",
    38: "9",
    39: "0",
}

dev = usb.core.find(idVendor=0xFFFF, idProduct=0x0035)
endpoint = dev[0][(0, 0)][0]

uid_string = ""
print("Waiting for card scan...")

while True:
    try:
        data = dev.read(endpoint.bEndpointAddress, 8, timeout=5000)
        scan_code = data[2]  # The 3rd byte holds the key

        if scan_code == 40:  # Enter key (End of UID)
            print(f"Full UID Captured: {uid_string}")
            uid_string = ""  # Reset for next card
        elif scan_code in HID_MAP:
            uid_string += HID_MAP[scan_code]

    except usb.core.USBError:
        continue
