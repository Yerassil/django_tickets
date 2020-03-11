from .models import Ticket, User
from .serializers import (TicketSerializer,
                          ApproverSerializer,
                          ApprovalSerializer)
# from rest_framework import permissions
# from .permissions import IsAuthorOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework_extensions.mixins import NestedViewSetMixin


# class TicketViewSet(viewsets.ModelViewSet):
#     #  This viewset automatically provides 'list', 'create', 'retrieve',
#     #  'update' and 'destroy' actions.
#     #  Additionally we also provide an extra 'description' action.

#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#     #                       IsAuthorOrReadOnly]

#     @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
#     def description(self, request, *args, **kwargs):
#         ticket = self.get_object()
#         return Response(ticket.description)

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        ticket = self.get_object()
        ticket.approve(request.user)
        approval = ticket.approvals.get(approver=request.user)
        return Response(
            ApprovalSerializer(approval).data,
            status=status.HTTP_200_OK
        )


# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     #  this viewset automatically provides 'list' and 'detail' actions.
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class ApproverViewSet(NestedViewSetMixin,
                      RetrieveModelMixin,
                      ListModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = ApproverSerializer
    queryset = User.objects.all()

    def _get_ticket_and_user(self, user_id):
        ticket_id = self.get_parents_query_dict()['tickets_for_approval']
        ticket = Ticket.objects.get(id=ticket_id)
        user = User.objects.get(id=user_id)
        return ticket, user

    def create(self, request, *args, **kwargs):
        ticket, user = self._get_ticket_and_user(request.data['id'])
        ticket.approvers.add(user)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        ticket, user = self._get_ticket_and_user(self.kwargs['pk'])
        ticket.approvers.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
