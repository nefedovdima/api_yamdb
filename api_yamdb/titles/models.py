from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()



class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    # genre = models.ForeignKey(Genre,
    #                           on_delete=models.SET(''),
    #                           related_name='titles')
    # category = models.ForeignKey(Category,
    #                              on_delete=models.SET(''),
    #                              related_name='titles'
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ManyToManyField(Category, through='CategoryTitle')

    def __str__(self):
        return self.name

class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class CategoryTitle(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category} {self.title}'



class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField()


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    score = models.IntegerField()
