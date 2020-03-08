from rest_framework import serializers

from .models import User, Ticket, Approval


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = '__all__'
