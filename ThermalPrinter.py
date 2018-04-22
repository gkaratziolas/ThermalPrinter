kPrinterBaudrate = 19200
kPrinterTimeout  = 2

# use chr to convert to either dec or hex to printable ascii chars


# Constants for thermal printer initiialisation
  # ESC 7 n1 n2 n3 Setting Control Parameter Command
  # n1 = "max heating dots" 0-255 -- max number of thermal print head
  #      elements that will fire simultaneously.  Units = 8 dots (minus 1).
  #      Printer default is 7 (64 dots, or 1/6 of 384-dot width), this code
  #      sets it to 11 (96 dots, or 1/4 of width).
  # n2 = "heating time" 3-255 -- duration that heating dots are fired.
  #      Units = 10 us.  Printer default is 80 (800 us), this code sets it
  #      to value passed (default 120, or 1.2 ms -- a little longer than
  #      the default because we've increased the max heating dots).
  # n3 = "heating interval" 0-255 -- recovery time between groups of
  #      heating dots on line; possibly a function of power supply.
  #      Units = 10 us.  Printer default is 2 (20 us), this code sets it
  #      to 40 (throttled back due to 2A supply).
  # More heating dots = more peak current, but faster printing speed.
  # More heating time = darker print, but slower printing speed and
  # possibly paper 'stiction'.  More heating interval = clearer print,
  # but slower printing speed.

kHeatTime     = 44
kHeatDots     = 80
kHeatInterval = 20

###begin
#timeoutSet(500000L);
#wake();
#reset();
#writeBytes(ASCII_ESC, '7');   // Esc 7 (print settings)
#writeBytes(44, heatTime, 20); // Heating dots, heat time, heat interval

class ThermalPrinter(object):
	def __init__(self, port):
		printer.ser = serial.Serial(port, baudrate=kPrinterBaudrate, timeout=kPrinterTimeout)

	def send_byte(b):
		if type(b) == bytes:

		elif type(b) == str:

		elif type(b) == hex:
