# Generated by Django 4.1.7 on 2024-03-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_message_message_type_message_user_embeddingdocument_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='source_page',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
