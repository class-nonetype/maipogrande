# Generated by Django 4.1 on 2022-09-06 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maipogrande', '0004_remove_contact_id_contact_id_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='id_request',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]