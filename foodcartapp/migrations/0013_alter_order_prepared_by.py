# Generated by Django 3.2.15 on 2023-07-30 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0012_order_prepared_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='prepared_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='foodcartapp.restaurant', verbose_name='ресторан, принявший заказ'),
        ),
    ]
