from django.db import models

from common.models import BaseModel, DeleteModel
from accounts.models import User
from django.utils.translation import gettext_lazy as _

class Status(models.TextChoices):
    PUBLISHED = 'published', 'Published'
    DRAFT = 'draft', 'Draft'


class Genre(models.TextChoices):
    PVP = 'pvp', 'PvP'
    PVE = 'pve', 'PvE'
    RPG = 'rpg', 'RPG'
    FPS = 'fps', 'FPS'
    MMO = 'mmo', 'MMO'
    ADVENTURE = 'adventure', 'Adventure'
    STRATEGY = 'strategy', 'Strategy'
    SIMULATION = 'simulation', 'Simulation'
    SPORTS = 'sports', 'Sports'
    RACING = 'racing', 'Racing'
    MULTIPLAYER = 'multiplayer', 'Multiplayer'


class Game(BaseModel, DeleteModel):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    genre = models.CharField(max_length=50, choices=Genre.choices, default=Genre.PVP, verbose_name=_('Genre'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name=_('Status'))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Created by'))


    def __str__(self):
        return self.title