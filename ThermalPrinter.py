import time
import serial
import Bitmap

# ASCII codes used by some of the printer config commands:
ASCII_TAB = '\t' # Horizontal tab
ASCII_LF  = '\n' # Line feed
ASCII_FF  = '\f' # Form feed
ASCII_CR  = '\r' # Carriage return
ASCII_DC2 =  18  # Device control 2
ASCII_ESC =  27  # Escape
ASCII_FS  =  28  # Field separator
ASCII_GS  =  29  # Group separator

kPrinterBaudrate = 19200
kPrinterTimeout  = 20

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
kHeatInterval = 100


  # Print density description from manual:
  # DC2 # n Set printing density
  # D4..D0 of n is used to set the printing density.  Density is
  # 50% + 5% * n(D4-D0) printing density.
  # D7..D5 of n is used to set the printing break time.  Break time
  # is n(D7-D5)*250us.
  # (Unsure of the default value for either -- not documented)

kPrintDensity   = 10 # 100% (? can go higher, text is darker but fuzzy)
kPrintBreakTime = 2 # 500 uS


kDotPrintTime   = 30000; # See comments near top of file for
kDotFeedTime    =  2100; # an explanation of these values.
kMaxChunkHeight =   255;

def not_byte(n):
    not_n = 256 - n - 1
    return (not_n).to_bytes(1, "little")

class ThermalPrinter(object):
    def __init__(self, port):
        self.ser = serial.Serial(port, baudrate=kPrinterBaudrate, timeout=kPrinterTimeout)

        self.previous_byte = ""
        self.column        = 0
        self.maxColumn     = 0
        self.charHeight    = 0
        self.lineSpacing   = 0
        self.barcodeHeight = 0

        self.wake()
        self.reset()
        self.send_bytes(ASCII_ESC, '7');   # Esc 7 (print settings)
        self.send_bytes(kHeatDots, kHeatTime, kHeatInterval); # Heating dots, heat time, heat interval
        self.send_bytes(ASCII_DC2, '#', (kPrintBreakTime << 5) | kPrintDensity);

        self.previous_byte = "\n"

    def send_byte(self, b):
        if type(b) == bytes:
            data = b
        elif type(b) == str:
            data = b.encode("utf-8")
        elif type(b) == hex:
            data = (b).to_bytes(1, "little")
        elif type(b) == float:
            b = int(b)
        elif type(b) == int:
            data = (b).to_bytes(1, "little")

        self.ser.write(data)

    def send_bytes(self, *bs):
        for b in bs:
            if type(b) == str:
                for c in list(b):
                    self.send_byte(c)
            else:
                self.send_byte(b)
                self.prevByte = b;

    def wake(self):
        self.send_bytes(255) # Wake from low-energy state
        time.sleep(0.05)
        self.send_bytes(ASCII_ESC, '8', 0, 0) # Sleep off

    def reset(self):
        self.send_bytes(ASCII_ESC, "@") # Init command

        self.previous_byte = "\n"       # Treat as if prior line is blank
        self.column        = 0
        self.maxColumn     = 32
        self.charHeight    = 24
        self.lineSpacing   = 6
        self.barcodeHeight = 50

        # Configure tab stops
        self.send_bytes(ASCII_ESC, 'D') # Set tab stops...
        self.send_bytes( 4,  8, 12, 16) # ...every 4 columns,
        self.send_bytes(20, 24, 28,  0) # 0 marks end-of-list.

    def feed(self, n):
        self.send_bytes(ASCII_ESC, 'd', n)
        #timeoutSet(dotFeedTime * charHeight)
        self.prevByte = '\n';
        self.column   =    0;

    def flush(self):
        self.send_bytes(ASCII_FF)

    def print_row(self, data):
        self.send_bytes(ASCII_DC2, '*', 1, len(row))
        for b in row:
            self.send_byte(not_byte(b))

    def print_bitmap(self, bitmap):
        #for i in range(bitmap.height):
        # can only send upto 256 bytes at a time
        chunk_height_limit = 256 // bitmap.width_bytes

        for row in range(bitmap.height):
            self.send_bytes(ASCII_DC2, '*', 1, bitmap.width_bytes)

            for b in bitmap.image_data[row*bitmap.width_bytes: (row+1)*bitmap.width_bytes]:
                self.send_byte(not_byte(b))


#        for row in range(bitmap.height-chunk_height_limit, -1, -1*chunk_height_limit):
#            print("a")
#            self.send_bytes(ASCII_DC2, '*', chunk_height_limit, bitmap.width_bytes)
#            for b in bitmap.image_data[row*bitmap.width_bytes: (row+chunk_height_limit)*bitmap.width_bytes]:
#                self.send_byte(not_byte(b))



if __name__ == "__main__":
    printer = ThermalPrinter("/dev/ttyUSB0")
    printer.feed(2)
    image = Bitmap.Bitmap()
    image.load_file("demo.bmp")
    printer.print_bitmap(image)
    printer.send_bytes("Choggy Carrots - 2018")
    time.sleep(0.5)
    printer.feed(3)
