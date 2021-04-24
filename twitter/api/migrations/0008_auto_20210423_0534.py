# Generated by Django 3.2 on 2021-04-23 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0007_auto_20210423_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='follows',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='follow',
            name='followed',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
    ]