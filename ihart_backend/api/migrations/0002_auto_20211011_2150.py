# Generated by Django 3.2.5 on 2021-10-11 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='schedule_id',
            new_name='schedule',
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='diagnosis',
            old_name='appointment_id',
            new_name='appointment',
        ),
        migrations.RenameField(
            model_name='emergency',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='medicalcertificate',
            old_name='diagnosis_id',
            new_name='diagnosis',
        ),
        migrations.RenameField(
            model_name='medicalcertificate',
            old_name='document_id',
            new_name='document',
        ),
        migrations.RenameField(
            model_name='medicalhistory',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='prescription',
            old_name='diagnosis_id',
            new_name='diagnosis',
        ),
        migrations.RenameField(
            model_name='prescription',
            old_name='inventory_id',
            new_name='inventory',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='inventory_id',
            new_name='inventory',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='prescription_id',
            new_name='prescription',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='photo_id',
            new_name='photo',
        ),
    ]