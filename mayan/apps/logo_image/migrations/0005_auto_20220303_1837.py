# Generated by Django 2.2.24 on 2022-03-03 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logo_image', '0004_auto_20220302_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logo',
            name='id',
        ),
        migrations.AlterField(
            model_name='logo',
            name='logo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='converter.Asset'),
        ),
    ]
