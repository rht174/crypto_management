# Generated by Django 5.1.7 on 2025-03-17 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organization_owner'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='organization',
        ),
        migrations.AddField(
            model_name='user',
            name='organizations',
            field=models.ManyToManyField(blank=True, related_name='member_users', to='organizations.organization'),
        ),
    ]
