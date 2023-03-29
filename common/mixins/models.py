import uuid
from uuid import UUID
from datetime import datetime
from django.db import models
from django.db.models import Manager
from .managers import SoftDeletionManager


class SoftDeletionModel(models.Model):
    """Abstract model with soft deletion"""
    is_active: bool = models.BooleanField(
        default=True, verbose_name='Активность')

    objects: Manager = models.Manager()
    active_objects: Manager = SoftDeletionManager()

    class Meta:
        abstract: bool = True

    def soft_delete(self) -> None:
        self.is_active = False
        self.save()
    
    def restore(self) -> None:
        self.is_active = True
        self.save()


class UUIDModel(models.Model):
    """Abstract model for uuid"""
    id: UUID = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        db_index = True,
        editable = False
    )

    class Meta:
        abstract: bool = True


class TimeStampModel(models.Model):
    """Abstract model with timestamp"""
    created_at: datetime = models.DateTimeField(
        auto_now_add=True, null=True,
        verbose_name='Дата создания')
    updated_at: datetime = models.DateTimeField(
        auto_now=True, null=True,
        verbose_name='Дата последнего редактирования')

    class Meta:
        abstract: bool = True


class BaseModel(UUIDModel,
                TimeStampModel,
                SoftDeletionModel):
    """Base model for inheritance"""
    class Meta:
        abstract: bool = True

