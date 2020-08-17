from django.contrib import admin
from django import forms
from .models import JsonDocument

from flat_json_widget.widgets import FlatJsonWidget


class JsonDocumentForm(forms.ModelForm):
    class Meta:
        widgets = {
            'content': FlatJsonWidget
        }


@admin.register(JsonDocument)
class JsonDocumentAdmin(admin.ModelAdmin):
    list_display = ['name']
    form = JsonDocumentForm
