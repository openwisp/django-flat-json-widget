from django.db import models


class JsonDocument(models.Model):
    name = models.CharField(max_length=64, unique=True)
    content = models.JSONField()
