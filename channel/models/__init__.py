# models.py
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class Brand(models.Model):
    hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

class Channel(models.Model):
    hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")

class Event(models.Model):
    hash = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    brands = models.ManyToManyField(Brand)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    @property
    def brand_hashes(self):
        return self.brands.values_list('hash', flat=True)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
