# Generated by Django 4.2.5 on 2023-10-01 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_ad_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pettypes',
            name='pet_breed',
        ),
        migrations.AddField(
            model_name='petbreeds',
            name='pet_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.pettypes'),
        ),
    ]
