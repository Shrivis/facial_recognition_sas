# Generated by Django 4.0.3 on 2022-04-20 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='image',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='out_time',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='branch',
            field=models.CharField(default='MCA', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sem',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(),
        ),
    ]
