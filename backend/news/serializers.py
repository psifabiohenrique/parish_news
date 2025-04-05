from rest_framework import serializers
from .models import Category, News, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'caption', 'order']
        read_only_fields = ['id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']
        read_only_fields = ['id']

class NewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.get_full_name')
    category = CategorySerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'content', 'summary',
            'category', 'author', 'cover_image', 'is_published',
            'featured', 'created_at', 'updated_at', 'published_at',
            'images'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

class NewsCreateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    
    class Meta:
        model = News
        fields = [
            'title', 'content', 'summary', 'category',
            'cover_image', 'is_published', 'featured', 'images'
        ]
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        news = News.objects.create(**validated_data)
        
        for image_data in images_data:
            Image.objects.create(news=news, **image_data)
        
        return news

class NewsUpdateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    
    class Meta:
        model = News
        fields = [
            'title', 'content', 'summary', 'category',
            'cover_image', 'is_published', 'featured', 'images'
        ]
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        
        # Atualiza os campos da notícia
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Atualiza as imagens
        if images_data:
            # Mantém apenas as imagens que são arquivos novos
            new_images = []
            for image_data in images_data:
                if isinstance(image_data.get('image'), str):
                    # Se for uma string (URL), é uma imagem existente, então mantém
                    continue
                new_images.append(image_data)
            
            # Adiciona novas imagens
            for image_data in new_images:
                Image.objects.create(news=instance, **image_data)
        
        return instance 