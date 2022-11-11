# Generated by Django 4.1.3 on 2022-11-10 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "timetracker",
            "0003_alter_screenshot_time_frames_alter_timeframe_session_and_more",
        )
    ]

    operations = [
        migrations.AlterField(
            model_name="timeframe",
            name="start",
            field=models.DateTimeField(auto_now_add=True, verbose_name="start time"),
        ),
        migrations.AlterField(
            model_name="usersession",
            name="start",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="session start time"
            ),
        ),
    ]