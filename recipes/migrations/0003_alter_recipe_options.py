# Generated by Django 4.2.5 on 2023-12-28 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_review_owner_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-vote_ratio', '-vote_total', 'title']},
        ),
    ]
