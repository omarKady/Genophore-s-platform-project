from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import bleach
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .constants import TYPE

# Create your models here.

class Protein(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amino_acid_seq = models.TextField()
    dna_seq = models.TextField()

    def clean(self):
        if len(self.dna_seq) != 3*len(self.amino_acid_seq):
            raise ValidationError("DNA seq always 3 times Amino Acid seq")

    def __str__(self):
        return f'Protein num: {self.id} author: {self.author}'


class Document(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def bleach_content(self):
        self.content = bleach.clean(self.content)
        return self.content

    def save(self, *args, **kwargs):
        self.bleach_content()
        return super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return f'Document num: {self.id} author: {self.author}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    # add Generic Foreign Key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    def __str__(self):
        return f'Comment num: {self.id} author: {self.author}'


class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=3, choices=TYPE.choices)
    link = models.URLField(max_length=250, null=True, blank=True)
    icon = models.CharField(max_length=250)
    # Add Generic Foreign Key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def clean(self):
        if self.notification_type == 'ln' and self.link is None:
            raise ValidationError("Enter link value")

    def bleach_message(self):
        self.message = bleach.clean(self.message)
        return self.message

    def save(self, *args, **kwargs):
        self.full_clean()
        self.bleach_message()
        return super(Notification, self).save(*args, **kwargs)

    def __str__(self):
        return f'Notification num: {self.id} Type: {self.notification_type}'
