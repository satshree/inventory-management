# Generated by Django 2.2.7 on 2019-11-18 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20191108_0332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='id',
        ),
        migrations.AlterField(
            model_name='brand',
            name='brand',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='device',
            name='status',
            field=models.BooleanField(choices=[(True, 'Working'), (False, 'Not Working')], default=False),
        ),
    ]
