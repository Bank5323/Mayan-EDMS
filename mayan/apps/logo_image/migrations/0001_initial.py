# Generated by Django 2.2.24 on 2022-02-26 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='A short text logo name.', max_length=128, verbose_name='name')),
            ],
            options={
                'verbose_name': 'name',
                'verbose_name_plural': 'name',
            },
        ),
    ]
