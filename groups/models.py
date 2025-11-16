from django.db import models
from students.models import Student
from django.utils.dates import WEEKDAYS

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    day_of_week = models.CharField(max_length=10, choices=WEEKDAYS.items())
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    students = models.ManyToManyField(Student, related_name='groups', blank=True)
    capacity = models.PositiveIntegerField(default=10)
    lesson_count = models.PositiveIntegerField(default=32)
    group_phone = models.CharField(max_length=30, blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)
    recordings_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        indexes = [
            models.Index(fields=['name'], name='group_name_idx'),
        ]

