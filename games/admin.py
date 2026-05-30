from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Game
admin.site.register(Game)
# Register your models here.
