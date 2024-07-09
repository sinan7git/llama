from django.db import models

class TimeStampedModel(models.Model):
    """
    An abstract model for the common fields 'created' and 'last_modified'.
    """
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True