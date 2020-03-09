from django_tickets.models import Ticket, User


def test_users_list(db, api_client, user_factory):
    users = user_factory.create_batch(3)
    response = api_client.get('/api/users/')
    assert response.status_code == 200
    response = response.json()
    assert len(response) == len(User.objects.all())
    assert len(User.objects.all()) == 3


def test_tickets_list(db, api_client, ticket_factory):
    tickets = ticket_factory.create_batch(3)
    response = api_client.get('/api/tickets/')
    assert response.status_code == 200
    response = response.json()
    assert len(response) == len(Ticket.objects.all())
    assert len(Ticket.objects.all()) == 3
