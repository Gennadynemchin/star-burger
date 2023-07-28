# Generated by Django 3.2.15 on 2023-07-28 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0006_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('RC', 'RECEIVED'), ('PR', 'PREPARING'), ('DL', 'DELIVERING'), ('FN', 'FINISHED')], db_index=True, default='RECEIVED', max_length=20),
        ),
    ]