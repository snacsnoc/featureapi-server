from django.db import models
from django.core.cache import cache

import uuid

import requests

#Decode Github code
import base64

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deployed_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Feature(models.Model):
    feature_hash = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    repository_url = models.TextField() #eg snacsnoc/test-project
    repo_file_path = models.TextField() #eg joke.js
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # Script is in quotes due to circular dependencies
    script_id = models.ForeignKey('Script', on_delete=models.CASCADE, null=True, blank=True)
    commit_hash = models.CharField(max_length=255, default="HEAD", blank=True)


    def save_script(feature):


        repo_url = feature.repository_url
        file_path = feature.repo_file_path
        feature_hash = feature.feature_hash

        if cache.get(feature_hash) is None:
            response = requests.get(f'https://api.github.com/repos/{repo_url}/contents/{file_path}')
            if response.status_code == 200:
                contents = response.json()

                commit_hash = contents['sha']

                code_content = base64.b64decode(contents['content']).decode("utf-8")


                script = Script(repo_url=repo_url, file_path=file_path, commit_hash=commit_hash, feature_hash=feature_hash)
                # Set Feature script ID to newly created script row
                feature.script_id = script

                #save code content into Redis
                cache.set(feature_hash, code_content) #, timeout=None


                script.save()
            else:
                print(f'Failed to fetch file {file_path} from {repo_url}')

    def save(self, *args, **kwargs):


        self.save_script()
        super().save(*args, **kwargs)
        return self.name

class Script(models.Model):
    repo_url = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    commit_hash = models.CharField(max_length=255)
    feature_hash = models.UUIDField(default=uuid.uuid4, editable=False)

    #models.CharField(max_length=200, unique=True,editable=False)
    #feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='scripts')
    # = models.UUIDField(default=uuid.uuid4, editable=False)
    def __str__(self):
        return self.commit_hash
