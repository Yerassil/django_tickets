import pytest

from django.core.exceptions import PermissionDenied
from django_tickets.models import Ticket


def test_ticket_new_ok(db, ticket_factory):
    #  new status when a ticket is created
    ticket = ticket_factory()
    assert ticket.status == Ticket.STATUS_NEW


def test_ticket_pending_ok(db, ticket_factory):
    #  if the ticket has approvers, then status changes to Pending
    ticket = ticket_factory.pending()
    assert ticket.status == Ticket.STATUS_PENDING


def test_ticket_pending_approvers_ok(db, ticket_factory, user_factory):
    #  after one approval the list of approvers shall contain everybody
    #  but the one that already approved
    ticket = ticket_factory()
    approvers = user_factory.create_batch(3)
    for user in approvers:
        ticket.approvers.add(user)
    assert len(ticket.pending_approval()) == 3
    ticket.approve(ticket.pending_approval()[0].user)
    assert len(ticket.pending_approval()) == 2
    ticket.approve(ticket.pending_approval()[0].user)
    assert len(ticket.pending_approval()) == 1


def test_ticket_inprogress_ok(db, ticket_factory):
    #  once the ticket is approved by everyone
    #  the assignee changes ticket status to in progress
    ticket = ticket_factory.in_progress()
    assert ticket.status == Ticket.STATUS_INPROGRESS


def test_ticket_completed_ok(db, ticket_factory):
    ticket = ticket_factory.completed()
    assert ticket.status == Ticket.STATUS_COMPLETED


def test_ticket_changes_requested_ok(db, ticket_factory):
    #  ticket author checks the work and requests changes
    ticket = ticket_factory.changes_requested()
    assert ticket.status == Ticket.STATUS_CHANGES_REQUESTED


def test_ticket_changes_requested_complete_again_ok(db, ticket_factory):
    #  the assigned person processes the ticket again
    ticket = ticket_factory.changes_requested()
    ticket.complete(ticket.assigned_to)
    assert ticket.status == Ticket.STATUS_COMPLETED


def test_ticket_closed_ok(db, ticket_factory, user_factory):
    #  at the end only a superuser can close the ticket
    ticket = ticket_factory.completed()
    superuser = user_factory(is_superuser=True)
    ticket.close(superuser)
    assert ticket.status == ticket.STATUS_CLOSED


def test_ticket_approval_not_by_approver_permision_denied(
    db, ticket_factory, user_factory
):
    ticket = ticket_factory.pending()
    user = user_factory()
    with pytest.raises(PermissionDenied):
        ticket.approve(user)


def test_ticket_completion_not_by_assignee_permision_denied(
    db, ticket_factory, user_factory
):
    ticket = ticket_factory.in_progress()
    user = user_factory()
    with pytest.raises(PermissionDenied):
        ticket.complete(user)


def test_ticket_changes_requested_by_not_author_permission_denied(
    db, ticket_factory, user_factory
):
    ticket = ticket_factory.completed()
    user = user_factory()
    with pytest.raises(PermissionDenied):
        ticket.request_changes(user)


def test_ticket_close_not_by_superuser_permision_denied(
    db, ticket_factory, user_factory
):
    ticket = ticket_factory.completed()
    user = user_factory()
    with pytest.raises(PermissionDenied):
        ticket.close(user)
