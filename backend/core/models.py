from django.db import models
from utils.model_abstracts import UuidModel
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleDescriptionModel,
)


class Contact(TimeStampedModel, ActivatorModel, TitleDescriptionModel, UuidModel):
    class Meta:
        verbose_name_plural = "Contacts"

    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return f"{self.title}"
