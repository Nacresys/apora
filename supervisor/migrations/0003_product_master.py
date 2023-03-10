# Generated by Django 4.1.2 on 2022-10-20 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supervisor', '0002_orderlist_address_city_orderlist_customer_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='product_master',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False)),
                ('product', models.CharField(max_length=250)),
                ('Batch', models.CharField(max_length=250)),
                ('row', models.IntegerField()),
                ('rack', models.IntegerField()),
                ('shelf', models.IntegerField()),
                ('stock_qty', models.IntegerField()),
            ],
            options={
                'db_table': 'product_master',
            },
        ),
    ]
