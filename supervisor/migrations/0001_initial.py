# Generated by Django 4.1 on 2022-09-29 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='orderlist',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('orderId', models.CharField(max_length=250)),
                ('productId', models.IntegerField()),
                ('product_name', models.CharField(max_length=250)),
                ('quantity', models.IntegerField()),
                ('status', models.IntegerField()),
                ('qr', models.IntegerField()),
            ],
            options={
                'db_table': 'orderlist',
            },
        ),
    ]
