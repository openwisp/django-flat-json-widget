from django import forms
from django.contrib import admin

from flat_json_widget.widgets import FlatJsonWidget

from .models import JsonDocument


class JsonDocumentForm(forms.ModelForm):
    class Meta:
        widgets = {'content': FlatJsonWidget}


@admin.register(JsonDocument)
class JsonDocumentAdmin(admin.ModelAdmin):
    list_display = ['name']
    form = JsonDocumentForm
