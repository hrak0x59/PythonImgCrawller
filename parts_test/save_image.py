import requests
import os
def save_image(url,file_path):
    response = requests.get(url,stream=True)
    image_data = response.content
    file_path = url.split('/').pop()
    save_path = os.path.join(url,file_path)
    with open(save_path,'wb') as f:
        f.write(image_data)