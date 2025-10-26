# Migration to replace old profile field with new FK field
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0003_populate_perfiles'),
    ]

    operations = [
        # Remove old profile CharField
        migrations.RemoveField(
            model_name='user',
            name='profile',
        ),
        # Rename profile_new to profile
        migrations.RenameField(
            model_name='user',
            old_name='profile_new',
            new_name='profile',
        ),
    ]
