from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class NGOMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    ngo_name = models.CharField(max_length=255)
    ngo_website = models.URLField(blank=True, null=True)
    services = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    matched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ngo_name}"

class MatcherHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    results = models.JSONField()  # Requires Django 3.1+ and PostgreSQL or SQLite
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.query[:30]}"
