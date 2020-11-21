import base64
import binascii
import datetime
import hashlib
import os
from io import BytesIO
from threading import Thread

import boto3
from PIL import Image


def generate_photo_filename(unique_id):
    user_id_hash = hashlib.md5(str(unique_id).encode("utf-8")).digest()
    datetime_hash = hashlib.md5(str(datetime.datetime.now()).encode("utf-8")).digest()
    return hashlib.sha1(user_id_hash + datetime_hash).hexdigest() + ".jpg"


def save_photo(photo_base64, directory, filename):
    try:
        img = Image.open(BytesIO(base64.b64decode(photo_base64.split(",")[1])))
    except (IndexError, binascii.Error):
        try:
            img = Image.open(BytesIO(base64.b64decode(photo_base64)))
        except binascii.Error:
            raise ValueError("Invalid base64 data")
    img = img.convert("RGB")
    img = crop_image(img)
    create_and_upload_thumbnail(img, 128, directory, filename)
    create_and_upload_thumbnail(img, 256, directory, filename)
    create_and_upload_thumbnail(img, 512, directory, filename)
    upload_to_s3(img, directory + "/init", filename)
    return True


def upload_to_s3(img: Image.Image, directory, obj_name):
    bytes_io = BytesIO()
    img.save(bytes_io, "JPEG")
    bytes_io.seek(0)

    s3 = boto3.client("s3")
    s3.upload_fileobj(bytes_io, os.environ.get("S3_BUCKET_NAME"), directory + "/" + obj_name)
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


def create_thumbnail(img: Image.Image, size):
    img = img.copy()
    img.thumbnail((size, size))
    return img


def create_and_upload_thumbnail(img: Image.Image, size, directory, obj_name):
    return Thread(target=_async_create_and_upload_thumbnail, args=(img, size, directory, obj_name)).start()


def _async_create_and_upload_thumbnail(img: Image.Image, size, directory, obj_name):
    img = create_thumbnail(img, size)
    upload_to_s3(img, directory + "/" + str(size), obj_name)


def delete_photo(directory, obj_name):
    return Thread(target=_delete_async_photo, args=(directory, obj_name)).start()


def _delete_async_photo(directory, obj_name):
    s3 = boto3.resource("s3")
    for d in ("128", "256", "512", "init"):
        obj = s3.Object(os.environ.get("S3_BUCKET_NAME"), f"{directory}/{d}/{obj_name}")
        obj.delete()
