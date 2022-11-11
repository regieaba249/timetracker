# Generated by Django 4.1.3 on 2022-11-10 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("timetracker", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="screenshot",
            name="time_frames",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="time_frame_screenshots",
                to="timetracker.timeframe",
            ),
        ),
        migrations.AlterField(
            model_name="timeframe",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sessions_time_frames",
                to="timetracker.usersession",
            ),
        ),
        migrations.AlterField(
            model_name="usersession",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_sessions",
                to=settings.AUTH_USER_MODEL,
                to_field="email",
            ),
        ),
    ]
