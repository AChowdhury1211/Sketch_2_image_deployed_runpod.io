import base64
import requests

image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOtI9ZUZI6Be9UC72tuPho3rYVjr_jjYpfBQ&s"
response = requests.get(image_url)
image_data = base64.b64encode(response.content).decode("utf-8")

image_binary = base64.b64decode(image_data)

with open("output_image.jpg", "wb") as f:
    f.write(image_binary)
