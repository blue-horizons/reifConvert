import sys, os
import binascii
from math import ceil, sqrt
from PIL import Image

global remove_file
global copy_file
global clear

def commands():
    if "win" in sys.platform:
        remove_file = "del"
        copy_file = "copy"
        clear = "cls"
    else:
        remove_file = "rm"
        copy_file = "cp"
        clear = "cls"


def remove_control_characters(filename, binary_data):
    # Remove control characters
    binary_data.join(filter(lambda x: x >= ' ', binary_data))

    # Write the cleaned data back to the file
    with open(filename, 'w') as f:
        f.write(binary_data)

    # os.system(remove_file + " tmp")

def encode(filename):
    # Read in the input file as binary data
    with open(filename, "rb") as f:
        data = f.read()

    # Convert each byte to an 8-bit binary string and concatenate them
    binary_data = "".join([format(byte, "08b") for byte in data])

    # Pad the binary data with zeros so its length is a multiple of 24 bits
    padding_length = 24 - len(binary_data) % 24
    binary_data += "0" * padding_length

    # Split the binary data into groups of 24 bits, convert each group to a hex string, and concatenate them
    hex_data = "".join([hex(int(binary_data[i:i+24], 2))[2:].zfill(6) for i in range(0, len(binary_data), 24)])

    # Determine the width and height of the image based on the length of the hex data
    num_pixels = ceil(sqrt(len(hex_data) // 6))
    width = height = num_pixels

    # Create a new image with the calculated dimensions
    img = Image.new("RGB", (width, height), color="black")

    # Draw each pixel in the image
    for i in range(0, len(hex_data), 6):
        # Extract the RGB values from the hex color code
        r, g, b = tuple(int(hex_data[i:i+2], 16) for i in range(i, i+6, 2))

        # Calculate the x and y coordinates of the pixel
        x = (i // 6) % width
        y = (i // 6) // width

        # Set the pixel color in the image
        img.putpixel((x, y), (r, g, b))

    # Save the image to a file
    img.save(f"{filename}.bmp")

def decode(filename):
    # Open the image and load its pixels
    with Image.open(filename) as img:
        pixels = img.load()
        width, height = img.size

        # Iterate over each pixel in the image
        hex_data = ""
        for y in range(height):
            for x in range(width):
                # Convert the pixel color to a html color code
                r, g, b = pixels[x, y]
                color_code = '{:02x}{:02x}{:02x}'.format(r, g, b)

                # Ignore black pixels
                if color_code == "000000":
                    continue

                # Convert the html color code to hexadecimal and append it to the hex data string
                hex_data += color_code

    # Convert the hexadecimal string to binary
    binary_data = binascii.unhexlify(hex_data)
    # binary_data.replace("\x00","")

    

    remove_control_characters(f"{filename}.txt")


if __name__ == "__main__":
    # Check that the correct number of arguments were passed in
    if len(sys.argv) != 3:
        print("Usage: python convert.py <filename> <encode|decode>")
    else:
        commands()
        # Determine whether to encode or decode the file
        filename = sys.argv[2]
        mode = sys.argv[1]
        if mode == "encode":
            encode(filename)
        elif mode == "decode":
            decode(filename)
        else:
            print("Invalid mode")