# Generated by Django 4.2.7 on 2023-11-24 07:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("example", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="book",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="group",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="label",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="person",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="release",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="song",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
