# Generated by Django 4.0.3 on 2022-03-06 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='u_phn',
            new_name='u_contact',
        ),
    ]
