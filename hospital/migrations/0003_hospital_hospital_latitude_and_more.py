# Generated by Django 4.1.4 on 2022-12-12 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospital", "0002_auto_20221211_1715"),
    ]

    operations = [
        migrations.AddField(
            model_name="hospital",
            name="hospital_latitude",
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hospital",
            name="hospital_longitude",
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="hospital",
            name="hospital_address",
            field=models.CharField(default="", max_length=200),
        ),
    ]
