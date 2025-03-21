# Generated by Django 5.1.7 on 2025-03-17 07:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoPrice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('symbol', models.CharField(max_length=10)),
                ('price', models.DecimalField(decimal_places=10, max_digits=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('org_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crypto_prices', to='organizations.organization')),
            ],
        ),
    ]
