from django.db import models

class TYPE(models.TextChoices):
        ln = 'ln', "link"
        sm = 'sm', "system"
        st = 'st', "static"
