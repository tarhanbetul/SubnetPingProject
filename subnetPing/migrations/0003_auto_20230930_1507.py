# Generated by Django 3.2.9 on 2023-09-30 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subnetPing', '0002_pingresult'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='pingresult',
            table='PingResult',
        ),
        migrations.AlterModelTable(
            name='subnet',
            table='Subnet',
        ),
    ]
