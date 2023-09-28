# Generated by Django 4.2.4 on 2023-09-28 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0006_testimonial_alter_meetup_meetup_speakers'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='profession',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='speaker',
            name='intstagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='speaker',
            name='linkedin',
            field=models.URLField(blank=True, null=True),
        ),
    ]