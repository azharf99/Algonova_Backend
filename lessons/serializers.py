from rest_framework import serializers
from lessons.models import Lesson
from students.serializers import StudentSerializer
from groups.serializers import GroupSerializer

class LessonSerializer(serializers.ModelSerializer):
    students_attended_details = StudentSerializer(source='students_attended', many=True, read_only=True)
    group_details = GroupSerializer(source='group', read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'