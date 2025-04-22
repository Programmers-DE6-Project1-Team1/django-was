from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class PromotionTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    price = models.IntegerField()
    product_description = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True, related_name="products")
    promotion_tags = models.ManyToManyField(PromotionTag, blank=True, related_name="products")
    labels = models.ManyToManyField(Label, blank=True, related_name="products")

    def __str__(self):
        return self.product_name
