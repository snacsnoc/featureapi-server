from django.core.management.base import BaseCommand

from core.models import Feature

class Command(BaseCommand):
    help = 'Scans the Feature models for features with the commit_hash set to HEAD and updates the cache'

    def handle(self, *args, **options):
        features = Feature.objects.filter(commit_hash='HEAD')
        for feature in features:
            # update the cache for each feature
            print(feature)


