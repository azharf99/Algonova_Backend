from django.db import models
from groups.models import Group
from django.utils import timezone

from students.models import Student

# Create your models here.
class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name='feedbacks', null=True)
    number = models.PositiveBigIntegerField()
    topic = models.CharField(max_length=100, blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    competency = models.TextField(blank=True, null=True)
    tutor_feedback = models.TextField(blank=True, null=True)
    lesson_date = models.DateField(default=timezone.now)
    lesson_time = models.TimeField(default=timezone.now)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback {self.student.fullname} ke-{self.number}"
    
    class Meta:
        ordering = ['student', '-number']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'