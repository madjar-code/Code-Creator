from jinja2 import Environment, FileSystemLoader
from camel_converter import to_snake
from creator.models import *
from common.queryset import QuerySetChain


TEMPLATES_PREFIX = 'apps/creator/services/code_templates'

def get_field_images_by_model_image(model_image: ModelImage,
                                    *field_image_classes):
    result_querysets = []
    for image_class in field_image_classes:
        queryset = image_class.active_objects.\
            filter(model_image=model_image)
        result_querysets.append(queryset)
    return result_querysets


def connect_to_template(template_name: str):
    file_loader = FileSystemLoader(searchpath=TEMPLATES_PREFIX)
    env = Environment(loader=file_loader)
    return env.get_template(template_name)


class ModelCodeGenerator:
    """Generating model code"""
    def __init__(self, model_image: ModelImage) -> None:
        self.model_image = model_image
        self.char_field_images, self.text_field_images,\
        self.image_field_images = get_field_images_by_model_image(
            model_image, CharFieldImage, TextFieldImage, ImageFieldImage
        )
        self.template = connect_to_template('models.txt')

    def create_model_code(self) -> str:
        model_name_snake_case = to_snake(self.model_image.model_name)
        output = self.template.render({
            'id': self.model_image.id,
            'model_has_images': self.model_image.has_images,
            'model_name': self.model_image.model_name,
            'model_name_snake_case': model_name_snake_case,
            'char_field_images': self.char_field_images,
            'text_field_images': self.text_field_images,
            'image_field_images': self.image_field_images,
            'verbose_name': self.model_image.model_verbose_name,
            'verbose_name_plural': self.model_image.model_verbose_name_plural
        })
        return output

    def __str__(self) -> str:
        return f'Model code generator with {self.model_image}'


class TranslationCodeGenerator:
    """
    Generating code for translation model
    fields
    """
    def __init__(self, model_image: ModelImage) -> None:
        self.model_image = model_image        
        char_field_images = CharFieldImage.active_objects.\
                                filter(model_image=self.model_image)
        text_field_images = TextFieldImage.active_objects.\
                                filter(model_image=self.model_image)
        self.all_field_images = QuerySetChain(char_field_images, text_field_images)

        self.template = connect_to_template('translation.txt')

    def create_translation_code(self,) -> str:
        output = self.template.render({
            'id': self.model_image.id,
            'all_field_images': self.all_field_images,
            'model_name': self.model_image.model_name,
        })
        return output


class AdminCodeGenerator:
    """
    Generating code for registering models
    in the admin panel
    """
    def __init__(self, model_image: ModelImage) -> None:
        self.model_image = model_image
        self.char_field_images = CharFieldImage.\
                                    active_objects.\
                                    filter(model_image=self.model_image)
        self.model_name = model_image.model_name
        self.template = connect_to_template('admin.txt')

    def create_admin_code(self) -> str:
        if self.model_image.multilingualism:
            stacked_inline_class = 'TranslationStackedInline'
            model_admin_class = 'TranslationAdmin'
        else:
            stacked_inline_class = 'StackedInline'
            model_admin_class = 'ModelAdmin'
            
        output = self.template.render({
            'id': self.model_image.id,
            'model_has_images': self.model_image.has_images,
            'model_name': self.model_image.model_name,
            'char_field_images': self.char_field_images,
            'stacked_inline_class': stacked_inline_class,
            'model_admin_class': model_admin_class,
        })
        return output

    def __str__(self) -> str:
        return f'Admin code generator with {self.model_image}'


class APICodeGenerator:
    """
    Generator for API (graphql). We have to create endpoints
    to get one object and to get all.
    """
    def __init__(self, model_image: ModelImage) -> None:
        self.model_image = model_image
        self.model_name = model_image.model_name
        self.template = connect_to_template('schema.txt')

    def create_object_type(self) -> str:
        output = self.template.render({
            'id': self.model_image.id,
            'model_name': self.model_image.model_name,
            'model_has_images': self.model_image.has_images,
            'all_objects_name': f'all_{to_snake(self.model_name)}s',
            'one_object_name': f'{to_snake(self.model_name)}_by_id'
        })
        return output

