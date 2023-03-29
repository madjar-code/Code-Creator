import os, random, string
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db.models import Model, ImageField
from django.utils import translation
from rest_framework.request import Request


def slug_unification(input_slug: str, model_class: Model) -> str:
    """
    Function that checks the slug
    and makes it unique if necessary
    """
    letters = string.ascii_letters
    code = random.choice(letters)
    
    if model_class.objects.filter(slug=input_slug).exists():
        new_slug = f'{input_slug}-{code}'
        return slug_unification(new_slug, model_class) 
    return input_slug


def delete_image(input_image: ImageField) -> None:
    """
    Removes image after validation
    """
    if input_image:
        if os.path.isfile(input_image.path):
            os.remove(input_image.path)


def compess(image: File) -> File:
    if not image: return

    _, format = image.name.split('.')
    if format in ('jpg', 'png'):
        # compress image
        im = Image.open(image)
        rgb_im = im.convert('RGB')
        im_io = BytesIO()
        rgb_im.save(im_io, 'JPEG', quality=70)
        new_image = File(im_io, name=image.name)
        return new_image
    # do nothing
    return image


def activate_language_from_request(request: Request) -> None:
    if 'HTTP_ACCEPT_LANGUAGE' in request.META:
        language = request.META['HTTP_ACCEPT_LANGUAGE']
        translation.activate(language)
