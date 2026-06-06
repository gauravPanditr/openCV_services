import imagehash
from PIL import Image

def generate_hash(img: Image.Image):
    return str(imagehash.phash(img))