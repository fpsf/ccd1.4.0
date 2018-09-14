import serial
from src.utils.Leitura_portas import serial_ports

'''
Microcontroller Serial Commands:
Open Shutter; CHARS 235, 144, 86, 1, 46; SENDS: "ëV."
Close Shutter; CHARS: 235, 144, 214, 1, 174 SENDS: "ëÖ®"
Get Status; CHARS: 235, 144, 2, 1, 130 SENDS: "ë‚"
In Python, Must be Written as: ser.write(bytes([nums, you, want, to, send]))
'''


def shutter_control(cont):
    ret = 25, "???"
    print("Searching Devices...\n")
    try:
        ser = serial.Serial(serial_ports()[len(serial_ports()) - 1], 9600,
                            bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, timeout=20)
        if cont is True:
            send = bytes([235, 144, 86, 1, 46])
            ser.write(send)
            frame = list(ser.read(5))
            processa_frame(frame)
        elif cont is False:
            send = bytes([235, 144, 214, 1, 174])
            ser.write(send)
            frame = list(ser.read(5))
            processa_frame(frame)
        else:
            send = bytes([235, 144, 2, 1, 90])
            ser.write(send)
            frame = list(ser.read(8))
            ret = processa_frame(frame)
    except serial.serialutil.SerialException:
        print("An Error Occured...")
        return "An Error Occured..."
    finally:
        return ret


def processa_frame(frame):
    if frame[2] == 5:
        print("STATUS\n")
        return processa_status(frame)
    elif frame[2] == 17:
        print("MSG RECEIVED\n")
        print(frame)
    elif frame[2] == 6:
        print("SHUTTER ERROR\n")
    else:
        print("UNKNOWN TYPE\n")


def processa_status(frame):
    temp = 8.0036 * (0.001221 * (frame[4] + (256 * frame[5])))
    print("Temperature: " + "{0:.2f}".format(temp))
    print("\n")
    if frame[6] == 1:
        print("Shutter: Open.")
    elif frame[6] == 2 or frame[6] == 3:
        print("Shutter: Closed.")
    else:
        print("Shutter: ???")
    return temp, frame[6]


# shutter_control(None)
