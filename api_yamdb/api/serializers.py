import base64
from rest_framework import serializers
from django.core.files.base import ContentFile
from titles.models import (Title, Category, Genre,
                           Review, Comment)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    # genre = GenreSerializer(many=True)
    # category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'

    # def create(self, validated_data):
    #     print(validated_data)
    #     genres = validated_data.pop('genre')
    #     category = validated_data.pop('category')
    #     title = Title.objects.create(**validated_data)
    #     for genre in genres:

    #         current_genre, status = Genre.objects.get_or_create(
    #             **genre)

    #         GenreTitle.objects.create(
    #             genre=current_genre, tilte=tilte)
        
    #     current_category, status = Category.objects.get_or_create(**category)
    #     CategoryTitle.objects.create(category=current_category, tilte=tilte)
    #     return title

    def to_representation(self, instance):
        representation = TitleRetrieveSerializer(instance).data
        return representation

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['genre'] = GenreSerializer(
    #         instance=instance.genre,
    #         many=True
    #     ).data
    #     representation['category'] = CategorySerializer(
    #         instance=instance.category,
    #     ).data
    #     return representation
    

class TitleRetrieveSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(
        many=True)
    category = CategorySerializer()
    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['author', 'title']




