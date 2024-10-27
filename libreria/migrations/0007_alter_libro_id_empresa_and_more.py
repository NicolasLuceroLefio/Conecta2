# Generated by Django 5.0.6 on 2024-07-25 02:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0006_empresa_evaluadores_libro_id_empresa_evaluaciones_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='id_empresa',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='libreria.empresa'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='id_evaluadoresEmpresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='libros', to='libreria.evaluadores'),
        ),
    ]