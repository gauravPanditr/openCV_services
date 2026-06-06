import cv2
from PIL import Image, ImageChops
import io

def ela_score(pil_img):

    buffer = io.BytesIO()

    pil_img.save(buffer, "JPEG", quality=90)

    buffer.seek(0)

    compressed = Image.open(buffer)

    diff = ImageChops.difference(pil_img, compressed)

    extrema = diff.getextrema()

    return max([e[1] for e in extrema])

def analyze(img, pil_img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    brightness = float(img.mean())

    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    ela = ela_score(pil_img)

    edited = ela > 20

    damage = "HIGH" if blur_score > 1000 else "LOW"

    fraud_score = 0.0

    if edited:
        fraud_score += 0.5

    return {
        "ela_score": ela,
        "edited": edited,
        "damage": damage,
        "fraud_score": fraud_score
    }