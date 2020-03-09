import factory
from ..models import Ticket, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('user_name')


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    author = factory.SubFactory(UserFactory)
    assigned_to = factory.SubFactory(UserFactory)
    title = factory.Faker('text')

    @staticmethod
    def pending():
        ticket = TicketFactory()
        user = UserFactory()
        ticket.approvers.add(user)
        return ticket

    @staticmethod
    def in_progress():
        ticket = TicketFactory()
        for user in UserFactory.create_batch(3):
            ticket.approvers.add(user)
            ticket.approve(user)
        return ticket

    @staticmethod
    def completed():
        ticket = TicketFactory.in_progress()
        ticket.complete(ticket.assigned_to)
        return ticket

    @staticmethod
    def changes_requested():
        ticket = TicketFactory.completed()
        ticket.request_changes(ticket.author)
        return ticket
