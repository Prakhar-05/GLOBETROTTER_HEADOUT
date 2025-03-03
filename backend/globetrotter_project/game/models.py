from django.db import models

class Destination(models.Model):
    city = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True)
    clues = models.JSONField(default=list)
    fun_fact = models.TextField(blank=True)
    trivia = models.JSONField(default=list)
    image_url = models.URLField(blank=True, max_length=500)

    def __str__(self):
        return self.city


