import base64
import os
import hashlib


def _get_content_path(url, folder_path) -> str:
    hashed = hashlib.md5(url.encode()).hexdigest()
    return f"{folder_path}/{hashed}.txt"

def _get_image_path(url, folder_path) -> str:
    hashed = hashlib.md5(url.encode()).hexdigest()
    return f"{folder_path}/{hashed}.png"

def load_previous_content(url, folder_path) -> str:
    path = _get_content_path(url, folder_path)
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return ""

def save_current_version(url, content, folder_path) -> str:
    os.makedirs(folder_path, exist_ok=True)
    path = _get_content_path(url, folder_path)
    with open(path, "w") as f:
        f.write(content)
    return path

def save_image(url, base64_encoded_image, folder_path) -> str:
    os.makedirs(folder_path, exist_ok=True)
    path = _get_image_path(url, folder_path)
    with open(path, "w") as image_file:
        image_file.write(base64.b64decode(base64_encoded_image))
    return path
