from django.db import models
from django.core.exceptions import ValidationError
from common.mixins.models import BaseModel


class ModelImage(BaseModel):
    model_name: str = models.CharField(max_length=255)
    model_verbose_name: str = models.CharField(max_length=255)
    model_verbose_name_plural: str = models.CharField(max_length=255)
    has_images: bool = models.BooleanField(default=False)
    is_instantiated: bool = models.BooleanField(default=False)
    multilingualism: bool = models.BooleanField(default=False)
    in_admin_panel: bool = models.BooleanField(default=False)
    has_API: bool = models.BooleanField(default=False)

    class Meta:
        verbose_name: str = 'Model Image'
        verbose_name_plural: str = 'Model Images'
    
    def __str__(self) -> str:
        return f'{self.model_name} image'

    def clean(self) -> None:
        if not self.model_name.isidentifier():
            error_message = 'Кодовое имя модели некорректно!' +\
                            ' Пример корректного имени: CampingImage'
            raise ValidationError(error_message)
        return super().clean()


class CommonField(BaseModel):
    model_image: ModelImage = models.ForeignKey(
        to=ModelImage, on_delete=models.CASCADE)
    field_name: str = models.CharField(max_length=255)
    field_verbose_name: str = models.CharField(max_length=255)
    is_required_field: bool = models.BooleanField(default=False)

    class Meta:
        abstract: bool = True
    
    def __str__(self) -> str:
        return self.field_verbose_name

    def clean(self) -> None:
        if not self.field_name.isidentifier():
            error_message = f'Кодовое имя поля "{self.field_verbose_name}" ' +\
                             'некорректно! Примеры корректных имён: name, ' +\
                             'short_descrtiption'
            raise ValidationError(error_message)
        return super().clean()


class CharFieldImage(CommonField):
    is_translatable: bool = models.BooleanField(default=True)
    in_list_display: bool = models.BooleanField(default=False)
    in_search_fields: bool = models.BooleanField(default=False)
    class Meta:
        verbose_name: str = 'CharField Image'
        verbose_name_plural: str = 'Images of CharFields'


class TextFieldImage(CommonField):
    is_translatable = models.BooleanField(default=True)
    class Meta:
        verbose_name: str = 'TextField Image'
        verbose_name_plural: str = 'Images of TextFields'


class ImageFieldImage(CommonField):
    class Meta:
        verbose_name: str = 'ImageField Image'
        verbose_name_plural: str = 'Images of ImageFields'
