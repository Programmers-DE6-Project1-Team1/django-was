from rest_framework import serializers
from .models import Product, Tag, Label, PromotionTag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name']

class PromotionTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionTag
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    labels = LabelSerializer(many=True, read_only=True)
    promotion_tags = PromotionTagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'price', 'product_description',
            'image_url', 'tags', 'labels', 'promotion_tags'
        ]
