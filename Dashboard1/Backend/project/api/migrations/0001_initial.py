# Generated by Django 4.2.2 on 2023-06-20 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('Empcode', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('Name', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Attandance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(null=True)),
                ('InTime', models.TimeField(null=True)),
                ('OutTime', models.TimeField(null=True)),
                ('WorkingHour', models.TimeField(null=True)),
                ('OverTime', models.TimeField(null=True)),
                ('Status', models.CharField(max_length=10)),
                ('Remark', models.CharField(max_length=20, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.employee')),
            ],
            options={
                'unique_together': {('employee', 'Date')},
            },
        ),
    ]
