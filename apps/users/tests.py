from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.core.files.base import ContentFile
import requests
from PIL import Image
from io import BytesIO
from django.conf import settings

# Create your tests here.
img_src = 'http://tvax3.sinaimg.cn/crop.0.0.664.664.50/005y0IGvly8fq09xw676cj30ig0ig3zc.jpg'

response = requests.get(img_src)
avatar_name = img_src.split('/')[-1]
avatar_io = BytesIO(response.content)
if response.status_code == 200:
    image = Image.open(avatar_io)
    avatar_file = InMemoryUploadedFile(
        file=avatar_io,
        field_name=None,
        name=avatar_name,
        content_type=image.format,
        size=image.size,
        charset=None
    )
    print(avatar_file)
