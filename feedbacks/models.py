from django.db import models
from students.models import Student

# Create your models here.
class Feedback(models.Model):
    student_name = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='feedbacks')
    number = models.PositiveBigIntegerField()
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback {self.student_name} ({self.number})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'