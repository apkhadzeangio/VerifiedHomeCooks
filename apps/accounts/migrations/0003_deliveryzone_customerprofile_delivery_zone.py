from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customerprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('city', models.CharField(default='Tbilisi', max_length=120)),
                ('description', models.TextField(blank=True)),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='delivery_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customers', to='accounts.deliveryzone'),
        ),
    ]
