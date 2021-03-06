# Generated by Django 3.1.7 on 2021-04-13 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realbeast', '0008_auto_20210319_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='contains',
            name='size',
            field=models.CharField(default='L', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='brand',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='realbeast.product'),
        ),
        migrations.AlterField(
            model_name='color',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='realbeast.product'),
        ),
        migrations.AlterField(
            model_name='contains',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contains', to='realbeast.order'),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_type', to='realbeast.product'),
        ),
        migrations.AlterField(
            model_name='size',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='realbeast.product'),
        ),
        migrations.AlterField(
            model_name='size',
            name='store_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store', to='realbeast.store'),
        ),
    ]
