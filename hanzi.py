from PIL import Image, ImageDraw, ImageFont

def create_bitmap(character, font_path, size):
    # Load the font
    font = ImageFont.truetype(font_path, size)

    # Create an image with white background
    image = Image.new('1', (size, size), color=1)
    draw = ImageDraw.Draw(image)

    # Get size of the rendered character
    text_width, text_height = draw.textsize(character, font=font)

    text_x = (size) / 2
    text_y = (size) / 2

    # Render the character
    draw.text((text_x, text_y), character,  font=font, anchor="mm", fill=0)

    return image

sans_path = 'C:\\Users\\meisg\\OneDrive\\Desktop\\Noto_Sans_SC\\static\\NotoSansSC-Medium.ttf'
serif_path = 'C:\\Users\\meisg\\OneDrive\\Desktop\\Noto_Serif_SC\\NotoSerifSC-Medium.otf'
kaiti_path = "C:\\Windows\\Fonts\\simkai.ttf"

# Example usage
bitmap = create_bitmap("家", kaiti_path, 1000).show()
bitmap = create_bitmap("狗", kaiti_path, 1000).show()
