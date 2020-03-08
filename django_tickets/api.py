from rest_framework.viewsets import ModelViewSet
from rest_framework import routers

from .models import User, Ticket, Approval

from .serializers import UserSerializer, TicketSerializer, ApprovalSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


class ApprovalViewSet(ModelViewSet):
    serializer_class = ApprovalSerializer
    queryset = Approval.objects.all()


router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'approvals', ApprovalViewSet)
api_urls = router.urls
