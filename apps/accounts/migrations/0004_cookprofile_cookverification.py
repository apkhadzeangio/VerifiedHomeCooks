from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_deliveryzone_customerprofile_delivery_zone'),
    ]

    operations = [
        migrations.CreateModel(
            name='CookProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=150)),
                ('bio', models.TextField(blank=True)),
                ('profile_image', models.ImageField(blank=True, upload_to='cook_profiles/')),
                ('phone_number', models.CharField(max_length=20)),
                ('kitchen_address', models.TextField()),
                ('verification_status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('SUSPENDED', 'Suspended')], default='PENDING', max_length=20)),
                ('is_available', models.BooleanField(default=False)),
                ('average_rating', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('review_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('delivery_zone', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cooks', to='accounts.deliveryzone')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cook_profile', to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='CookVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('personal_id_number', models.CharField(blank=True, max_length=100)),
                ('id_document_image', models.ImageField(blank=True, upload_to='cook_verification/id_documents/')),
                ('kitchen_photo', models.ImageField(upload_to='cook_verification/kitchen_photos/')),
                ('additional_kitchen_photo', models.ImageField(blank=True, upload_to='cook_verification/kitchen_photos/')),
                ('cooking_experience', models.TextField(blank=True)),
                ('food_safety_notes', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('SUSPENDED', 'Suspended')], default='PENDING', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('admin_comment', models.TextField(blank=True)),
                ('cook', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verification', to='accounts.cookprofile')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_cook_verifications', to='accounts.user')),
            ],
        ),
    ]
