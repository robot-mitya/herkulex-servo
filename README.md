# herkulex-servo
Python scripts for smart servos HerkuleX DRS-0101 and DRS-0201

# Some useful commands
## Reboot
python3 hx.py -r "FF FF 07 FD 09 F2 0C"
## Stat
FF FF 07 FE 07 FE 00

## Move
### Torque On
FF FF 0A FD 03 A0 5E 34 01 60
### Move 10°
FF FF 0C FD 05 20 DE 1E 02 08 FD 3C
### Move 90°
FF FF 0C FD 05 26 D8 14 03 04 FD 3C

## Read position
FF FF 09 FD 04 C8 36 3A 02
### Answer 10°
FF FF 0D FD 44 B2 4C 3A 02 1F 62 00 42
### Answer 90°
FF FF 0D FD 44 BE 40 3A 02 13 63 00 42

## LED
### LED on (green color)
FF FF 0A FD 03 C0 3E 35 01 01
### LED off
FF FF 0A FD 03 C0 3E 35 01 00
