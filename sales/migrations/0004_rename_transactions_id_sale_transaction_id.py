# Generated by Django 5.0.2 on 2024-02-17 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_alter_position_price_alter_sale_total_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='transactions_id',
            new_name='transaction_id',
        ),
    ]