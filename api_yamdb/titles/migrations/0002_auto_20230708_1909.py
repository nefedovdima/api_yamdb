# Generated by Django 3.2 on 2023-07-08 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(on_delete=models.SET(''), related_name='titles', to='titles.category'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ForeignKey(on_delete=models.SET(''), related_name='titles', to='titles.genre'),
        ),
    ]
