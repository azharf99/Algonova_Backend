from rest_framework import serializers
from feedbacks.models import Feedback
from students.serializers import StudentSerializer

class FeedbackSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'