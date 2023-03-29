from datetime import datetime
from django.db import connection
from django.db.models.base import ModelBase
from django.test import TestCase
from common.mixins.models import BaseModel


class ModelMixinTestCase(TestCase):
    """
    Test Case for abstract mixin models.
    Subclass and set cls.mixin to your desired mixin.
    access your model using cls.model.
    """
    mixin = None
    model = None

    @classmethod
    def setUpClass(cls) -> None:
        # Create a real model from the mixin
        cls.model = ModelBase(
            "__Test" + cls.mixin.__name__,
            (cls.mixin,),
            {'__module__': cls.mixin.__module__}
        )

        # Use schema_editor to create schema
        with connection.schema_editor() as editor:
            editor.create_model(cls.model)

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        # allow the transaction to exit
        super().tearDownClass()

        # Use schema_editor to delete schema
        with connection.schema_editor() as editor:
            editor.delete_model(cls.model)

        # close the connection
        connection.close()


class TestBaseModel(ModelMixinTestCase):
    """Test abstract model."""
    mixin = BaseModel

    def setUp(self) -> None:
        self.object1 = self.model.objects.create(pk=1)
        self.object2 = self.model.objects.create(pk=2)
        self.object2.soft_delete()
    
    def test_soft_deletion(self) -> None:
        object = self.model.objects.get(pk=1)
        self.assertTrue(object.is_active)
        object.soft_delete()
        self.assertFalse(object.is_active)
        object.restore()
        self.assertTrue(object.is_active)

    def test_getting_all_active_objects(self) -> None:
        self.assertEqual(len(self.model.active_objects.all()), 1)
    
    def test_timestamp(self) -> None:
        self.assertEqual(type(self.object1.created_at), datetime)
        self.assertEqual(type(self.object1.updated_at), datetime)
