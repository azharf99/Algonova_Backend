from django.db import models
from groups.models import Group
from django.utils import timezone

from students.models import Student
from utils.constants import ACTIVITY_SCORE, ATTENDANCE_SCORE, TASK_SCORE

# Create your models here.
class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name='feedbacks', null=True)
    group_name = models.CharField(max_length=100, blank=True, null=True)
    number = models.PositiveBigIntegerField()
    topic = models.CharField(max_length=200, blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)
    project_link = models.URLField(blank=True, null=True)
    competency = models.TextField(blank=True, null=True)
    tutor_feedback = models.TextField(blank=True, null=True)
    attendance_score = models.CharField(max_length=1, default=4, choices=ATTENDANCE_SCORE)
    activity_score = models.CharField(max_length=1, default=3, choices=ACTIVITY_SCORE)
    task_score = models.CharField(max_length=1, default=2, choices=TASK_SCORE)
    lesson_date = models.DateField(default=timezone.now)
    lesson_time = models.TimeField(default=timezone.now)
    is_sent = models.BooleanField(default=False)
    url_pdf = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Feedback {self.student.fullname} ke-{self.number}"
    
    
    class Meta:
        ordering = ['student', '-number']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'