# Generated by Django 3.2.9 on 2022-02-04 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0004_profiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='price_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
