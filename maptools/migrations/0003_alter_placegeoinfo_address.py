# Generated by Django 3.2.15 on 2023-08-20 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maptools', '0002_auto_20230803_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placegeoinfo',
            name='address',
            field=models.CharField(default=0, max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
