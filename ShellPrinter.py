# Text from a terminal can be piped into this funciton to be printed on a connected thermal printer

import sys
import ThermalPrinter

printer = ThermalPrinter.ThermalPrinter("/dev/ttyUSB0")


for line in sys.stdin:
    printer.send_bytes(line)
printer.feed(2)
