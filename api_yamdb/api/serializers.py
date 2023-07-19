from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("id",)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("id",)
        model = Genre


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", many=False, queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "category",
            "genre",
        )


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "category",
            "genre",
            "rating",
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, data):
        if self.context["request"].method == "POST":
            user = self.context["request"].user
            title_id = self.context["view"].kwargs.get("title_id")
            if Review.objects.filter(
                author_id=user.id, title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    "Отзыв можно оставить только один раз"
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLES, default="user")

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
            "bio",
        )


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError(
                'Имя me недоступно для регистрации'
            )
        return value


class CreateTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )
    confirmation_code = serializers.CharField(required=True)
