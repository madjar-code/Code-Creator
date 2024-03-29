from django.contrib import admin, messages
from creator.services.manager import Manager
from .models import *


class CharFieldImageInline(admin.StackedInline):
    model: CharFieldImage = CharFieldImage
    extra: int = 1


class TextFieldImageInline(admin.StackedInline):
    model: TextFieldImage = TextFieldImage
    extra: int = 1


class ImageFieldImageInline(admin.StackedInline):
    model: ImageFieldImage = ImageFieldImage
    extra: int = 1


@admin.register(ModelImage)
class ModelImageAdmin(admin.ModelAdmin):
    inlines: tuple = (
        CharFieldImageInline,
        TextFieldImageInline,
        ImageFieldImageInline,
    )
    search_fields: tuple = ('model_verbose_name',)
    ordering: tuple = ('-created_at',)
    list_display: tuple = (
        'model_name',
        'model_verbose_name',
        'created_at',
        'is_instantiated',
        'multilingualism',
        'in_admin_panel',
        'has_API',
        'is_active',
    )
    readonly_fields: tuple = (
        'is_instantiated',
        'multilingualism',
        'in_admin_panel',
        'has_API',
    )
    actions: tuple = (
        'instantiate_an_image',
        'register_in_admin',
        'create_API_by_model_image',
        'unregister_an_image',
        'unregister_in_admin',
        'delete_API',
    )
    
    @admin.action(description='Model Creation by Image')
    def instantiate_an_image(modeladmin, request, queryset) -> None:
        for image in queryset:
            manager = Manager(image)
            manager.create_model()
            manager.translate_model()

    @admin.action(description='Model Deletion')
    def unregister_an_image(modeladmin, request, queryset) -> None:
        for image in queryset:
            if image.is_instantiated:
                manager = Manager(image)
                manager.delete_model()
            msg: str = f'Модель с именем {image.model_name} была удалена из кодовой базы'
            messages.add_message(request, messages.SUCCESS, msg)

    @admin.action(description='Admin Creation')
    def register_in_admin(modeladmin, request, queryset) -> None:
        for image in queryset:
            manager = Manager(image)
            manager.register_model_in_adminpanel()

    @admin.action(description='Admin Deletion')
    def unregister_in_admin(modeladmin, request, queryset) -> None:
        for image in queryset:
            if image.in_admin_panel:
                manager = Manager(image)
                manager.unregister_model_in_adminpanel()
            msg: str = f'Модель с именем {image.model_name} была удалена из панели администратора'
            messages.add_message(request, messages.SUCCESS, msg)

    @admin.action(description='API Creation')
    def create_API_by_model_image(modeladmin, request, queryset) -> None:
        for image in queryset:
            manager = Manager(image)
            manager.create_API()

    @admin.action(description='API Deletion')
    def delete_API(modeladmin, request, queryset) -> None:
        for image in queryset:
            if image.has_API:
                manager = Manager(image)
                manager.delete_API()
            msg: str = f'Модель с именем {image.model_name} была удалена из API'
            messages.add_message(request, messages.SUCCESS, msg)

    def delete_queryset(self, request, queryset) -> None:
        for image in queryset:
            if image.is_instantiated:
                manager = Manager(image)
                manager.delete_model()
            return super().delete_queryset(request, queryset)
