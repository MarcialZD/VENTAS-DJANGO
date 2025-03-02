# Generated by Django 5.1.6 on 2025-03-02 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Descripcion del producto'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, help_text='Imagen debe ser de 300x300', null=True, upload_to='products'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Si el producto está activo se mostrará en la página principal'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nombre del Producto'),
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(related_name='products', to='shop.tag'),
        ),
    ]
