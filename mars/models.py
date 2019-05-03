from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)


class Review(models.Model):
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1),
                                                                    MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)


class Job(models.Model):
    owner = models.ForeignKey(User, null=False, related_name='job_owner', on_delete=models.PROTECT)
    worker = models.ForeignKey(User, null=True, blank=True, related_name='job_worker', on_delete=models.PROTECT)

    post_time = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    assign_time = models.DateTimeField(null=True, blank=True)

    owner_review = models.ForeignKey(Review, null=True, blank=True, related_name='job_owner_review', on_delete=models.CASCADE)
    worker_review = models.ForeignKey(Review, null=True, blank=True, related_name='job_worker_review', on_delete=models.CASCADE)

    category = models.ForeignKey(Category, null=False, blank=False, related_name='job_category', on_delete=models.PROTECT)


class JobImage(models.Model):
    job = models.ForeignKey(Job, null=False, on_delete=models.PROTECT)
    image = models.ImageField(upload_to=settings.IMAGE_STORE)


class Dispute(models.Model):
    NEW = 'N'
    PROGRESS = 'P'
    RESOLVED = 'R'
    UNRESOLVED = 'U'

    DISPUTE_STATES = (
        (NEW, 'New'),
        (PROGRESS, 'In Progress'),
        (RESOLVED, 'Resolved'),
        (UNRESOLVED, 'Unresolved')
    )

    job = models.ForeignKey(Job, null=False, on_delete=models.PROTECT)
    state = models.CharField(max_length=1, choices=DISPUTE_STATES, default=NEW)



