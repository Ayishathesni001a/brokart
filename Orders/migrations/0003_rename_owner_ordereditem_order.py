# Generated by Django 5.1.2 on 2024-10-20 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0002_ordereditem_size_alter_order_delete_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ordereditem',
            old_name='owner',
            new_name='order',
        ),
    ]
