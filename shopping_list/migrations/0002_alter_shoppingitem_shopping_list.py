# Generated by Django 5.1.5 on 2025-01-26 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_list', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingitem',
            name='shopping_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_items', to='shopping_list.shoppinglist'),
        ),
    ]
