from rest_framework import serializers
from .models import Product, Tag, PromotionTag, Label

class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    promotion_tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    labels = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Product
        fields = '__all__'
