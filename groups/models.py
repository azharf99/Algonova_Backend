from django.db import models
from students.models import Student
from django.utils.translation import gettext_lazy as _

GROUP_TYPES = (
    ("Group", _("Group")),
    ("Private", _("Private")),
)

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    students = models.ManyToManyField(Student, related_name='groups', blank=True)
    type = models.CharField(max_length=10, choices=GROUP_TYPES, default="Group")
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

