from rest_framework import serializers
from groups.models import Group
from students.serializers import StudentSerializer

class GroupSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='students', many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'