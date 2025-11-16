from django.db import models
from groups.models import Group

# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=100)
    module = models.CharField(max_length=50)
    level = models.CharField(max_length=20)
    number = models.PositiveIntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lessons')
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.module} - {self.level}"
    

    class Meta:
        ordering = ['number']
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        indexes = [
            models.Index(fields=['title'], name='lesson_title_idx'),
            models.Index(fields=['module'], name='lesson_module_idx'),
            models.Index(fields=['level'], name='lesson_level_idx'),
        ]