# Generated by Django 5.1.1 on 2024-10-05 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_alter_avocadoavenue_grn'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='avocadoavenue',
            name='sheet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='analytics.sheet'),
            preserve_default=False,
        ),
    ]
