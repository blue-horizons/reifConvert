import sys
import binascii
from math import ceil, sqrt
from PIL import Image

def main():
    # Check that the correct number of arguments were passed in
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        return

    # Open the input file and read its contents
    with open(sys.argv[1], "r") as f:
        text = f.read()

    # Convert each letter to an 8 bit binary number
    binary_text = ''.join(format(ord(c), '08b') for c in text)

    # Convert each 8 bit binary number to hexadecimal
    hex_text = format(int(binary_text, 2), 'x')

    # Add padding to the hexadecimal string if necessary
    if len(hex_text) % 6 != 0:
        hex_text += '0' * (6 - (len(hex_text) % 6))

    # Convert every six hex characters to a html color code and add it to a list
    color_codes = [hex_text[i:i+6] for i in range(0, len(hex_text), 6)]

    # Calculate the width and height of the image based on the number of color codes
    num_pixels = len(color_codes)
    width = int(ceil(sqrt(num_pixels)))
    height = int(ceil(num_pixels / width))

    # Add black color codes to the end of the list if necessary to complete the image
    if len(color_codes) < width * height:
        num_missing = width * height - len(color_codes)
        color_codes += ['000000'] * num_missing

    # Create a new image with the appropriate dimensions
    img = Image.new('RGB', (width, height), "black")
    pixels = img.load()

    # Convert each html color code to a pixel and add it to the image
    for i in range(num_pixels):
        color = tuple(int(color_codes[i][j:j+2], 16) for j in (0, 2, 4))
        x = i % width
        y = i // width
        pixels[x, y] = color

    # Save the image
    filename = sys.argv[1].split('.')[0]
    img.save(f"{filename}.bmp")

    print(f"""Input File {sys.argv[0]} converted to {filename}.bmp which is a {width} x {height} px 
image with {num_missing} missing pixels.""")

if __name__ == "__main__":
    main()
