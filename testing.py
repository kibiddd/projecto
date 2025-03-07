import json
import base64

# read test.txt
with open('test.txt', 'r', encoding='utf-8') as file:  # Specify the encoding
    content = file.read()

content = json.loads(content)

data = content['data']

content = data['content']
screenshot = data['screenShots']
screenshot = screenshot[0]
screenshot = screenshot['image']
# Decode the Base64 string
header, base64_data = screenshot.split(",", 1)

# Decode the Base64 data
image_data = base64.b64decode(base64_data)

# Save it as a PNG file
with open("output_image.png", "wb") as image_file:
    image_file.write(image_data)

print("Image has been saved as output_image.png")
