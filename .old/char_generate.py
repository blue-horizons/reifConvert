import random

def generate_japanese_characters(num_chars):
    characters = []
    for i in range(num_chars):
        # Generate a random integer between 0x3041 and 0x3096, which corresponds to Hiragana characters
        character = chr(random.randint(0x3041, 0x3096))
        characters.append(character)
    return ''.join(characters)

num_chars = int(input("Enter the number of characters you want to generate: "))
filename = input("Enter the name of the file you want to write to: ")

japanese_text = generate_japanese_characters(num_chars)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(japanese_text)

print(f"{num_chars} characters written to {filename}")
