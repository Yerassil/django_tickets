from rest_framework import serializers

from .models import User, Ticket, Approval


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = ['approver', 'is_approved']


class ApproverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
