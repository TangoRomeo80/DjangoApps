# Generated by Django 4.0.2 on 2022-02-14 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20220212_1705'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='customer',
            name='store_custo_last_na_e6a359_idx',
        ),
        migrations.AlterModelTable(
            name='customer',
            table=None,
        ),
    ]