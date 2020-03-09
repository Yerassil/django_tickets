from pytest_factoryboy import register
import pytest
from django_tickets.tests.factories import UserFactory, TicketFactory
from rest_framework.test import APIClient


register(UserFactory)
register(TicketFactory)


@pytest.fixture
def api_client():
    return APIClient()
