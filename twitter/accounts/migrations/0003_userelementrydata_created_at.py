# Generated by Django 3.2.6 on 2021-08-30 17:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userelementrydata_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='userelementrydata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
