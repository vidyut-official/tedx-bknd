from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    ticket_rate = models.IntegerField(blank=False,null=False,default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name