from django.core.management.base import BaseCommand
import requests
import base64
from core.models import Feature, Script
from django.core.cache import cache


class Command(BaseCommand):
    help = "Scans the Feature models for features with the commit_hash set to HEAD and updates the cache"

    def handle(self, *args, **options):
        features = Feature.objects.filter(commit_hash="HEAD")
        for feature in features:
            print("Feature to update: ", feature.feature_hash)
            scripts = Script.objects.filter(feature_hash=feature.feature_hash)
            for script in scripts:

                response = requests.get(
                    f"https://api.github.com/repos/{script.repo_url}/contents/{script.file_path}"
                )
                if response.status_code == 200:
                    contents = response.json()

                    commit_hash = contents["sha"]
                    print("New commit hash: ", commit_hash)
                    code_content = base64.b64decode(contents["content"]).decode("utf-8")

                    script.commit_hash = commit_hash

                    # save code content into Redis
                    cache.set(feature.feature_hash, code_content)  # , timeout=None

                    script.save()
