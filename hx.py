import argparse

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


def print_packet(label, data, c1, c2):
    sys.stdout.write("\033[0m")
    sys.stdout.write(label)
    sys.stdout.write("\033[93m")
    for i in range(data[2]):
        if i > 0:
            sys.stdout.write(" ")
        if i == 5:
            sys.stdout.write("\033[95m")
            sys.stdout.write("{:02X}".format(c1))
            sys.stdout.write("\033[93m")
        elif i == 6:
            sys.stdout.write("\033[95m")
            sys.stdout.write("{:02X}".format(c2))
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
           "sudo apt-get install python3-pil",
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    "packet",
    help="packet to check")
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

if good_header and good_length and (not good_cs1 or not good_cs2):
    print()
    print_packet("Source packet: ", packet, packet[5], packet[6])
    print_packet("Packet with \033[92mGOOD\033[0m checksums: ", packet, cs1, cs2)

print()
