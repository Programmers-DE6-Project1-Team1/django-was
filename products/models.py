from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    promotion_tag = models.CharField(max_length=100, blank=True, null=True)
    price = models.PositiveIntegerField()
    product_description = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.product_name
