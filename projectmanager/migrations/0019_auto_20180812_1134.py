# Generated by Django 2.0.7 on 2018-08-12 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0018_auditrecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auditrecord',
            name='performed_user',
        ),
        migrations.DeleteModel(
            name='AuditRecord',
        ),
    ]
