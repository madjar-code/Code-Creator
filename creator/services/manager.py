import os
from camel_converter import to_snake
from creator.models import ModelImage
# from .run_commands import run_migrations
from .code_generators import\
    ModelCodeGenerator, AdminCodeGenerator,\
    APICodeGenerator, TranslationCodeGenerator


MODELS_PREFIX = 'entities/models'
TRANSLATOR_PREFIX = 'entities/translation'
ADMINS_PREFIX = 'entities/admin'
API_PREFIX = 'entities/api/schema'
GRAPHQL_PATH = 'core/my_graphql.py'

class Manager:
    def __init__(self, image: ModelImage) -> None:
        self.image = image
        self.model_generator = ModelCodeGenerator(image)
        self.translation_generator = TranslationCodeGenerator(image)
        self.admin_generator = AdminCodeGenerator(image)
        self.api_generator = APICodeGenerator(image)

        # module name
        name: str = to_snake(self.image.model_name)

        self.model_init_path = f'{MODELS_PREFIX}/__init__.py'
        self.model_file_path = f'{MODELS_PREFIX}/{name}.py'

        self.translation_init_path = f'{TRANSLATOR_PREFIX}/__init__.py'
        self.translation_file_path = f'{TRANSLATOR_PREFIX}/{name}.py'
        
        self.admin_init_path = f'{ADMINS_PREFIX}/__init__.py'
        self.admin_file_path = f'{ADMINS_PREFIX}/{name}.py'
        
        self.api_init_path = f'{API_PREFIX}/__init__.py'
        self.api_file_path = f'{API_PREFIX}/{name}.py'

        self.importing_string = f'from .{name} import *\n'

    @staticmethod
    def add_line_if_new(new_line: str, file_path: str) -> None:
        need_import = False
        file = open(file_path, 'r')
        if new_line not in file.read():
            need_import = True
        file.close()
        if need_import:
            file = open(file_path, 'a')
            file.write(new_line)
            file.close()

    @staticmethod
    def delete_one_line(deleted_line: str, file_path: str) -> None:
        file = open(file_path, 'r')
        lines = file.readlines()
        file.close()
        new_file = open(file_path, 'w')
        for line in lines:
            if line != deleted_line:
                new_file.write(line)
        new_file.close()

    def create_model(self) -> None:
        model_code: str = self.model_generator.create_model_code()
        Manager.add_line_if_new(self.importing_string,
                                self.model_init_path)
        with open(self.model_file_path,
                  'w', encoding='utf-8') as model_file:
            model_file.write(model_code)
        self.image.is_instantiated = True
        self.image.save()

    def delete_model(self) -> None:
        """
        When deleting a model, the API and admin should
        be deleted
        """
        os.remove(self.model_file_path)
        Manager.delete_one_line(self.importing_string,
                                self.model_init_path)
        if self.image.multilingualism:
            self.delete_translation()
        if self.image.in_admin_panel:
            self.unregister_model_in_adminpanel()
        if self.image.has_API:
            self.delete_API()
        self.image.is_instantiated = False
        self.image.save()

    def translate_model(self) -> None:
        Manager.add_line_if_new(self.importing_string,
                                self.translation_init_path)
        translation_code = self.translation_generator.\
                                create_translation_code()
        with open(self.translation_file_path,
                  'w', encoding='utf-8') as tranlation_file:
            tranlation_file.write(translation_code)
        self.image.multilingualism = True
        self.image.save()

    def delete_translation(self) -> None:
        os.remove(self.translation_file_path)
        Manager.delete_one_line(self.importing_string,
                                self.translation_init_path)
        self.image.multilingualism = False
        self.image.save()

    def register_model_in_adminpanel(self) -> None:
        admin_code = self.admin_generator.create_admin_code()
        Manager.add_line_if_new(self.importing_string,
                                self.admin_init_path)
        with open(self.admin_file_path,
                  'w', encoding='utf-8') as admin_file:
            admin_file.write(admin_code)
        self.image.in_admin_panel = True
        self.image.save()
    
    def unregister_model_in_adminpanel(self) -> None:
        os.remove(self.admin_file_path)
        Manager.delete_one_line(self.importing_string,
                                self.admin_init_path)
        self.image.in_admin_panel = False
        self.image.save()

    def create_API(self) -> None:
        schema_code = self.api_generator.create_object_type()
        Manager.add_line_if_new(self.importing_string,
                                self.api_init_path)
    
        query_name = f'{self.image.model_name}sQuery'
        query_importing_string = f'from apps.entities.api.schema import {query_name}\n'
        inheritance_string = ' '*17 + f'{query_name},\n'

        graphql_file = open(GRAPHQL_PATH, 'r')
        lines = graphql_file.readlines()

        importing_index = lines.index('\n')
        inherit_index = lines.index('                 graphene.ObjectType,):\n')
        if query_importing_string not in lines:
            lines.insert(importing_index, query_importing_string)
        if inheritance_string not in lines:
            lines.insert(inherit_index+1, inheritance_string)

        graphql_file.close()

        new_graphql_file = open(GRAPHQL_PATH, 'w')
        for line in lines:
            new_graphql_file.write(line)
        new_graphql_file.close()

        with open(self.api_file_path,
                  'w', encoding='utf-8') as api_file:
            api_file.write(schema_code)
        self.image.has_API = True
        self.image.save()

    def delete_API(self) -> None:
        os.remove(self.api_file_path)
        Manager.delete_one_line(self.importing_string,
                                self.api_init_path)

        graphql_file = open(GRAPHQL_PATH, 'r')
        query_name = f'{self.image.model_name}sQuery'
        query_importing_string = f'from apps.entities.api.schema import {query_name}\n'
        inheritance_string = ' '*17 + f'{query_name},\n'

        lines = graphql_file.readlines()
        lines.remove(query_importing_string)
        lines.remove(inheritance_string)
        graphql_file.close()
        
        new_graphql_file = open(GRAPHQL_PATH, 'w')
        for line in lines:
            new_graphql_file.write(line)
        new_graphql_file.close()

        self.image.has_API = False
        self.image.save()

    def __str__(self) -> str:
        return f'Manager for {self.image}'
