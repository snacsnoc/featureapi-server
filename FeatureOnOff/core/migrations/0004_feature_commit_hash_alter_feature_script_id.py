# Generated by Django 4.1.6 on 2023-02-04 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_feature_script_id_alter_script_feature_hash"),
    ]

    operations = [
        migrations.AddField(
            model_name="feature",
            name="commit_hash",
            field=models.CharField(blank=True, default="HEAD", max_length=255),
        ),
        migrations.AlterField(
            model_name="feature",
            name="script_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.script",
            ),
        ),
    ]