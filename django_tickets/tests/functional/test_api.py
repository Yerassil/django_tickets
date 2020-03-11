from django_tickets.models import Ticket, User


def test_tickets_list_ok(db, api_client, ticket_factory):
    tickets = ticket_factory.create_batch(3)
    assert len(tickets) == 3
    response = api_client.get('/api/tickets/')
    assert response.status_code == 200
    response = response.json()
    assert len(response) == len(Ticket.objects.all())


def test_ticket_details_ok(db, api_client, user_factory, ticket_factory):
    user = user_factory()
    ticket = ticket_factory(author=user)
    response = api_client.get('/api/tickets/1/')
    assert response.status_code == 200
    response = response.json()
    assert response['title'] == ticket.title


def test_ticket_new(db, api_client, user_factory):
    author = user_factory()
    assignee = user_factory()
    response = api_client.post(
        '/api/tickets/', {
            'author': author.id, 'title': 'test',
            'assigned_to': assignee.id, 'description': 'test'}
    )
    assert response.status_code == 201
    assert response.json()['id'] == 1


def test_ticket_add_approver(db, api_client, user_factory, ticket_factory):
    ticket = ticket_factory()
    approver = user_factory()
    response = api_client.post('/api/tickets/1/approvers/', {'id': approver.id})
    assert response.status_code == 201
    assert approver in ticket.approvers.all()


def test_ticket_list_approvers(db, api_client, user_factory, ticket_factory):
    ticket = ticket_factory.in_progress()
    response = api_client.get('/api/tickets/1/approvers/')
    assert response.status_code == 200
    assert len(response.json()) == len(ticket.approvers.all())


def test_ticket_delete_approvers(db, api_client, user_factory, ticket_factory):
    ticket = ticket_factory.in_progress()
    approver = ticket.approvers.all()[0]
    len_before = len(ticket.approvers.all())
    response = api_client.delete(
        '/api/tickets/1/approvers/{}/'.format(approver.id)
    )
    assert response.status_code == 204
    assert len(ticket.approvers.all()) == len_before - 1


def test_ticket_approve(db, api_client, ticket_factory):
    ticket = ticket_factory.in_progress()
    print(ticket.author)
    print(ticket.approvers.first())
    api_client.force_authenticate(user=ticket.approvers.first())
    response = api_client.post('/api/tickets/1/approve/')
    print(response)
    assert response.status_code == 200
    assert response.json()['approver'] == ticket.approvers.first().id
    assert response.json()['is_approved'] is True
    assert ticket.approvals.first().is_approved
    #  get status fresh from db
    assert Ticket.objects.get(id=ticket.id).status == Ticket.STATUS_INPROGRESS


def test_ticket_complete(db, api_client, ticket_factory):
    ticket = ticket_factory.in_progress()
    api_client.force_authenticate(user=ticket.assigned_to)
    response = api_client.post('/api/tickets/1/complete/')
    assert response.status_code == 200
    #  get fresh status from db
    assert Ticket.objects.get(id=ticket.id).status == Ticket.STATUS_COMPLETED


def test_ticket_changes_requested(db, api_client, ticket_factory):
    ticket = ticket_factory.completed()
    api_client.force_authenticate(user=ticket.author)
    response = api_client.post('/api/tickets/1/changes/')
    assert response.status_code == 200
    # get fresh status from db
    assert Ticket.objects.get(id=ticket.id).status == Ticket.STATUS_CHANGES_REQUESTED


def test_ticket_changes_requested_complete_again(db, api_client, ticket_factory):
    ticket = ticket_factory.changes_requested()
    api_client.force_authenticate(user=ticket.assigned_to)
    response = api_client.post('/api/tickets/1/complete/')
    assert response.status_code == 200
    # get fresh status from db
    assert Ticket.objects.get(id=ticket.id).status == Ticket.STATUS_COMPLETED


def test_ticket_closed(db, api_client, ticket_factory, user_factory):
    ticket = ticket_factory.completed()
    superuser = user_factory(is_superuser=True)
    api_client.force_authenticate(user=superuser)
    response = api_client.post('/api/tickets/1/close/')
    assert response.status_code == 200
    # get fresh status from db
    assert Ticket.objects.get(id=ticket.id).status == Ticket.STATUS_CLOSED
