from rest_framework import serializers
from feedbacks.models import Feedback
from groups.serializers import GroupSerializer

class FeedbackSerializer(serializers.ModelSerializer):
    group_details = GroupSerializer(source='group', read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'