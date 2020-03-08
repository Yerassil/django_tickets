from pytest_factoryboy import register

from django_tickets.tests.factories import UserFactory, TicketFactory


register(UserFactory)
register(TicketFactory)
