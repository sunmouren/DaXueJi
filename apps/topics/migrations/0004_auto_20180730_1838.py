# Generated by Django 2.0.7 on 2018-07-30 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_auto_20180730_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='recorded',
            field=models.ManyToManyField(through='topics.RecordArticle', to='writing.Article'),
        ),
    ]
