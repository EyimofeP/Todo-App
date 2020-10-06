# Generated by Django 3.0.7 on 2020-09-29 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200924_0427'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ['-start_date']},
        ),
        migrations.AlterField(
            model_name='todo',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Optional', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Category'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='description',
            field=models.TextField(blank=True, help_text='Optional', null=True, verbose_name='To-Do Description'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='name',
            field=models.CharField(help_text='Please Type your Todo', max_length=300, null=True, verbose_name='To-Do Name'),
        ),
    ]