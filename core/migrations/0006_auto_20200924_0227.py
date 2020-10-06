# Generated by Django 3.0.7 on 2020-09-24 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200924_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(choices=[('primary', 'Blue'), ('secondary', 'Grey'), ('danger', 'Red'), ('info', 'Sky Blue'), ('success', 'Green'), ('warning', 'Yellow'), ('dark', 'Black')], max_length=50, null=True),
        ),
    ]