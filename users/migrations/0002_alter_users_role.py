# Generated by Django 4.1.3 on 2022-12-02 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='role',
            field=models.CharField(choices=[('moderator', 'moderator'), ('admin', 'admin'), ('member', 'member'), ('unknown', 'unknown')], default='unknown', max_length=40, null=True),
        ),
    ]