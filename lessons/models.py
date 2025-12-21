from django.db import models
from groups.models import Group
from django.utils import timezone
from students.models import Student

# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True, null=True)
    module = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons')
    description = models.TextField(blank=True, null=True)
    date_start = models.DateField(default=timezone.now)
    time_start = models.TimeField(default=timezone.now)
    meeting_link = models.URLField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    students_attended = models.ManyToManyField(Student, related_name='attended_lessons', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.module} - {self.level} - {self.group}"
    

    class Meta:
        ordering = ['group__name', 'number']
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        indexes = [
            models.Index(fields=['title'], name='lesson_title_idx'),
            models.Index(fields=['module'], name='lesson_module_idx'),
            models.Index(fields=['level'], name='lesson_level_idx'),
        ]