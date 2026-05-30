from django.db.models.signals import post_delete
from django.dispatch import receiver

from games.models import Game

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='delete_game.log', filemode='a+')


@receiver(post_delete, sender=Game)
def delete_games(sender, instance, **kwargs):
    # with open('delete_game.log', 'a+') as f:
    #     f.write(str(instance.title, 'utf-8'))
    print(instance)
    logging.info(f'deleting game {instance.title} {instance.genre}')