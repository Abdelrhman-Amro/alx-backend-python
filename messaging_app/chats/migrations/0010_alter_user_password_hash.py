# Generated by Django 5.1.5 on 2025-02-04 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0009_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password_hash',
            field=models.CharField(default='pbkdf2_sha256$870000$lZqMPY9Fg6azjsbNr1SjDJ$Dg+/0il5qgb7/vts1+ZkMOBch4IRxZ8+MZeY0msRcP4=', max_length=255),
        ),
    ]
