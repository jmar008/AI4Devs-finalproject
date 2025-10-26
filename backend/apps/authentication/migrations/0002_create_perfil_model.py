# Generated migration to add Perfil model first
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        # Create Perfil model first
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, unique=True, verbose_name='Código')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('activo', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
                'ordering': ['nombre'],
            },
        ),
        # Add fecha_baja to User
        migrations.AddField(
            model_name='user',
            name='fecha_baja',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de baja'),
        ),
        # Add temporary profile_new field as FK to Perfil
        migrations.AddField(
            model_name='user',
            name='profile_new',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='authentication.perfil', verbose_name='Perfil del usuario (nuevo)'),
        ),
    ]
