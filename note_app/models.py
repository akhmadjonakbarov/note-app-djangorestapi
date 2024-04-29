from django.db import models


# Create your models here.
class Note(models.Model):
    topic = models.CharField(max_length=250, blank=False, null=False)
    info = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic
