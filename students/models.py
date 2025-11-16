from django.db import models

# Create your models here.
class Student(models.Model):
    fullname = models.CharField(max_length=150)
    surname = models.CharField(max_length=50)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    parent_name = models.CharField(max_length=60, blank=True, null=True)
    parent_contact = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.fullname} ({self.username})"
    
    class Meta:
        ordering = ['fullname']
        verbose_name = "Student"
        verbose_name_plural = "Students"
    