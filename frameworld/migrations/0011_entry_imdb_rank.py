# Generated by Django 4.1.7 on 2024-04-30 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frameworld', '0010_entry_cast_entry_description_entry_director_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='imdb_rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]