from django.db.models.signals import m2m_changed
from .models import Ticket, Approval


def approvers_changed(sender, instance, **kwargs):
    instance.status = Ticket.STATUS_PENDING
    instance.save()


m2m_changed.connect(approvers_changed, sender=Approval)
