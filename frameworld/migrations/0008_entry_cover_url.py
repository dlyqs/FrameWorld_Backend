# Generated by Django 4.1.7 on 2024-04-16 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frameworld', '0007_likerecord_delete_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='cover_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]