# Generated by Django 4.2.4 on 2023-08-23 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('is_active', models.BooleanField()),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'categories',
            },
        ),
    ]