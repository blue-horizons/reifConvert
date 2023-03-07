import sys
import binascii
from PIL import Image

def main():
    # Check that the correct number of arguments were passed in
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_file>")
        return

    # Open the image and load its pixels
    with Image.open(sys.argv[1]) as img:
        pixels = img.load()
        width, height = img.size

        # Iterate over each pixel in the image
        hex_text = ""
        for y in range(height):
            for x in range(width):
                # Convert the pixel color to a html color code
                r, g, b = pixels[x, y]
                color_code = '{:02x}{:02x}{:02x}'.format(r, g, b)

                # Ignore black pixels
                if color_code == "000000":
                    continue

                # Convert the html color code to hexadecimal and append it to the text string
                hex_text += color_code

    # Convert the hexadecimal string to binary
    binary_text = binascii.unhexlify(hex_text)

    # Convert each 8 bit binary number to its corresponding ASCII character
    text = "".join([chr(b) for b in binary_text])

    # Save the decoded text to a file
    filename = sys.argv[1].split('.')[0]
    with open(f"{filename}-out.txt", "w") as f:
        f.write(text)

if __name__ == "__main__":
    main()
