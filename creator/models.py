from django.db import models
from django.core.exceptions import ValidationError
from common.mixins.models import BaseModel


class ModelImage(BaseModel):
    model_name = models.CharField(
        'Кодовое имя сущности', max_length=255)
    model_verbose_name = models.CharField(
        'Название сущности', max_length=255)
    model_verbose_name_plural = models.CharField(
        'Название сущности в множественном числе',
        max_length=255)
    has_images = models.BooleanField(
        'Наличие множества картинок', default=False)
    is_instantiated = models.BooleanField(
        'Инициализация', default=False)
    multilingualism = models.BooleanField(
        'Мультиязычность', default=False)
    in_admin_panel = models.BooleanField(
        'Наличие в админке', default=False)
    has_API = models.BooleanField(
        'Наличие API', default=False)

    class Meta:
        verbose_name = 'Образ модели'
        verbose_name_plural = 'Образы моделей'
    
    def __str__(self) -> str:
        return f'{self.model_name} image'

    def clean(self) -> None:
        if not self.model_name.isidentifier():
            error_message = 'Кодовое имя модели некорректно!' +\
                            ' Пример корректного имени: CampingImage'
            raise ValidationError(error_message)
        return super().clean()


class CommonField(BaseModel):
    model_image = models.ForeignKey(
        to=ModelImage, on_delete=models.CASCADE,
        verbose_name='Образ родительской модели')
    field_name = models.CharField(
        'Кодовое имя поля', max_length=255)
    field_verbose_name = models.CharField(
        'Название поля', max_length=255)
    is_required_field = models.BooleanField(
        'Обязательное поле?', default=False)

    class Meta:
        abstract = True
    
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
    is_translatable = models.BooleanField(
        'Переводимое поле?', default=True)
    in_list_display = models.BooleanField(
        'List Display', default=False)
    in_search_fields = models.BooleanField(
        'Search Field', default=False)
    class Meta:
        verbose_name = 'Образ малого текстового поля'
        verbose_name_plural = 'Образы малых текстовых полей'


class TextFieldImage(CommonField):
    is_translatable = models.BooleanField(
        'Переводимое поле', default=True)
    class Meta:
        verbose_name = 'Образ текстового поля'
        verbose_name_plural = 'Образы текстовых полей'


class ImageFieldImage(CommonField):

    class Meta:
        verbose_name = 'Образ поля картинки'
        verbose_name_plural = 'Образы полей картинок'
