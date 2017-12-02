import argparse
import serial
import sys
GOOD = "\033[92mGOOD\033[0m"
BAD = "\033[91mBAD\033[0m"


def checksum1(data):
    data_size = data[2]
    result = data[2]
    for i in range(3, data_size):
        if i != 5 and i != 6:
            result ^= data[i]
    return result & 0xFE


def checksum2(data):
    data_size = data[2]
    result = data[2]
    for i in range(3, data_size):
        if i != 5 and i != 6:
            result ^= data[i]
    return (~result) & 0xFE


def print_packet(label, data, show_calculated_checksums):
    c1 = checksum1(data)
    c2 = checksum2(data)
    if show_calculated_checksums:
        data[5] = c1
        data[6] = c2
    sys.stdout.write("\033[0m")
    sys.stdout.write(label)
    sys.stdout.write("\033[93m")
    for i in range(data[2]):
        if i > 0:
            sys.stdout.write(" ")
        if i == 5:
            if data[5] == c1:
                sys.stdout.write("\033[92m")
            else:
                sys.stdout.write("\033[91m")
            sys.stdout.write("{:02X}".format(c1 if show_calculated_checksums else data[5]))
            sys.stdout.write("\033[93m")
        elif i == 6:
            if data[6] == c2:
                sys.stdout.write("\033[92m")
            else:
                sys.stdout.write("\033[91m")
            sys.stdout.write("{:02X}".format(c2 if show_calculated_checksums else data[6]))
            sys.stdout.write("\033[93m")
        else:
            sys.stdout.write("{:02X}".format(data[i]))
    sys.stdout.write("\033[0m")
    sys.stdout.flush()
    print("")


parser = argparse.ArgumentParser(
    description="Checks HerkuleX servo packet.",
    epilog="Example:\n" +
           "python3 hx.py \"FF FF 07 FE 07 FE 00\"" +
           "\n" +
           "If errors:\n" +
           "sudo apt-get install python3-pil\n" +
           "sudo easy_install -U pyserial",
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    "packet",
    help="packet to check")
parser.add_argument(
    "-r",
    "--run",
    action='store_true',
    help="send to servo and run")
args = parser.parse_args()

packet = bytearray.fromhex(args.packet)

good_length = False
good_cs1 = False
good_cs2 = False

length_output = "—"
cs1_output = "—"
cs2_output = "—"

cs1 = 0
cs2 = 0

good_header = packet[0] == 0xFF and packet[1] == 0xFF
header_output = GOOD if good_header else BAD
if good_header:
    good_length = 7 <= packet[2] <= 223
    length_output = GOOD if good_length else BAD
    if good_length:
        cs1 = checksum1(packet)
        cs2 = checksum2(packet)
        good_cs1 = cs1 == packet[5]
        good_cs2 = cs2 == packet[6]
        cs1_output = GOOD if good_cs1 else BAD
        cs2_output = GOOD if good_cs2 else BAD

print()
print("Header:", header_output)
print("Length:", length_output)
print("Checksum1:", cs1_output)
print("Checksum2:", cs2_output)

if good_header and good_length:
    print()
    print_packet("Source packet: ", packet, False)
    if not good_cs1 or not good_cs2:
        print_packet("Packet with \033[92mGOOD\033[0m checksums: ", packet, True)

print()

if not args.run:
    exit(0)

# Fix the checksums with the calculated values:
if cs1 != packet[5]:
    packet[5] = cs1
if cs2 != packet[6]:
    packet[6] = cs2

with serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
) as ser:

    print_packet("Sending: ", packet, True)
    ser.write(packet)
    received = ser.read(233)
    if len(received) >= 7:
        description = "Received (" + str(len(received)) + " bytes): "
        print_packet(description, received, False)

# TODO: Передавать имя порта параметром.
# TODO: Передавать скорость передачи данных параметром.
