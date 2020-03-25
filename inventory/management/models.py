from django.db import models

# Create your models here.

class Brand(models.Model):
    brand = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.brand
    
    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

class Device(models.Model):
    CHOICES = [
        (True, 'Working'),
        (False, 'Not Working')
    ]

    brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
    serial_number = models.CharField(max_length=200)
    status = models.BooleanField(default=False, choices=CHOICES)
    location = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    manufactured_date = models.DateField(blank=True, null=True)
    remarks = models.TextField()

    def __str__(self):
        return str(self.serial_number) + " | " + str(self.brand)
    
    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"
        ordering = ['-id']
        # unique_together = ('brand', 'serial_number', 'model')