from django.db import models

class BaseQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_active=False)

class DeleteManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model).filter(is_active=True)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class DeleteModel(models.Model):
    is_active = models.BooleanField(default=True)

    objects = DeleteManager()
    all_objects = models.Manager()


    class Meta:
        abstract = True
# Create your models here.
