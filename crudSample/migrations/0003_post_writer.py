# Generated by Django 3.2.5 on 2021-07-23 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudSample', '0002_remove_post_writer'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='writer',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]