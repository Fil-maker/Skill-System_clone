import base64
import binascii
import datetime
import hashlib
import os
from io import BytesIO

from PIL import Image


def generate_photo_filename(unique_id):
    user_id_hash = hashlib.md5(str(unique_id).encode("utf-8")).digest()
    datetime_hash = hashlib.md5(str(datetime.datetime.now()).encode("utf-8")).digest()
    return hashlib.sha1(user_id_hash + datetime_hash).hexdigest() + ".jpeg"


def save_photo(photo_base64, filename):
    try:
        img = Image.open(BytesIO(base64.b64decode(photo_base64.split(",")[1])))
    except (IndexError, binascii.Error):
        try:
            img = Image.open(BytesIO(base64.b64decode(photo_base64)))
        except binascii.Error:
            raise ValueError("Invalid base64 data")
    img = crop_image(img)
    img.save(os.path.join(os.path.dirname(__file__), "..", "..", "user-images", filename))
    return True


def crop_image(img: Image.Image):
    w, h = img.size
    if w > h:
        area = ((w - h) / 2, 0, (w + h) / 2, h)
    elif w < h:
        area = (0, (h - w) / 2, w, (h + w) / 2)
    else:
        return img
    return img.crop(area)
