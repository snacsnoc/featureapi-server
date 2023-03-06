from django.contrib import admin
from .models import Project, Feature, Script


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "deployed_url",
        "created_at",
        "updated_at",
    )


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "created_at",
        "updated_at",
        "state",
        "project",
        "repository_url",
        "feature_hash",
    )


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ("id", "feature_hash", "file_path", "commit_hash")
