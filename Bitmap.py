import math

class Bitmap(object):
    def _init_(self):
        self.raw_data          = b""
        self.signature         = b""
        self.file_size_bytes   = b""
        self.offset            = b""
        self.header_size       = b""
        self.width             = b""
        self.height            = b""
        self.planes            = b""
        self.bits_per_pixel    = b""
        self.compression       = b""
        self.image_size_bytes  = b""
        self.colours           = b""
        self.important_colours = b""
        self.image_data        = b""

    def load_file(self, file):
        with open(file, "rb") as f:
            data = f.read()
        self.raw_data          = data
        self.signature         = int.from_bytes(data[0:2],   byteorder="little")
        self.file_size_bytes   = int.from_bytes(data[2:6],   byteorder="little")
        self.offset            = int.from_bytes(data[10:14], byteorder="little")
        self.header_size       = int.from_bytes(data[14:18], byteorder="little")
        self.width             = int.from_bytes(data[18:22], byteorder="little")
        self.height            = int.from_bytes(data[22:26], byteorder="little")
        self.planes            = int.from_bytes(data[26:28], byteorder="little")
        self.bits_per_pixel    = int.from_bytes(data[28:30], byteorder="little")
        self.compression       = int.from_bytes(data[30:34], byteorder="little")
        self.image_size_bytes  = int.from_bytes(data[34:38], byteorder="little")
        self.colours           = int.from_bytes(data[46:50], byteorder="little")
        self.important_colours = int.from_bytes(data[50:54], byteorder="little")

        self.width_bytes       = math.ceil((self.width * self.bits_per_pixel)/8)

        image_data_start = self.offset
        image_data_end   = self.offset + self.height * self.width_bytes
        self.image_data = data[image_data_start:image_data_end]

if __name__ == "__main__":
    E = Bitmap()
    E.load_file("eye.bmp")