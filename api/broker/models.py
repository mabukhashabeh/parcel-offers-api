from django.db import models


class Broker(models.Model):
    class Type(models.TextChoices):
        AGRICULTURAL = "personal", "Personal"
        RESIDENTIAL = "company", "Company"
        COMMERCIAL = "governmental", "Governmental"

    name = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=Type.choices)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
