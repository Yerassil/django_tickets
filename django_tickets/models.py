from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied


class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)


class Ticket(models.Model):
    author = models.ForeignKey(
        User, related_name='tickets', on_delete=models.CASCADE
    )
    title = models.CharField('Title', max_length=200, null=False)
    description = models.TextField('Description')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    approvers = models.ManyToManyField(
        User, through='Approval', blank=True
    )
    due_date = models.DateField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        User, related_name='assignees', on_delete=models.CASCADE
    )

    STATUS_NEW = 'new'
    STATUS_PENDING = 'pending approval'
    STATUS_APPROVED = 'approved'
    STATUS_INPROGRESS = 'in progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CHANGES_REQUESTED = 'changes requested'
    STATUS_CLOSED = 'closed'

    STATUS_CHOICES = (
        (STATUS_NEW, STATUS_NEW),
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_APPROVED, STATUS_APPROVED),
        (STATUS_INPROGRESS, STATUS_INPROGRESS),
        (STATUS_CHANGES_REQUESTED, STATUS_CHANGES_REQUESTED),
        (STATUS_CLOSED, STATUS_CLOSED)
    )
    completed = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW
    )

    def __str__(self):
        return self.title

    def pending_approval(self):
        return Approval.objects.filter(ticket=self, approved=False)

    def approve(self, user):
        try:
            approval = Approval.objects.get(user=user, ticket=self)
            approval.approved = True
            approval.save()
        except:
            raise PermissionDenied()
        if not self.pending_approval():
            self.status = self.STATUS_INPROGRESS

    def request_changes(self, user):
        if user == self.author:
            self.status = self.STATUS_CHANGES_REQUESTED
        else:
            raise PermissionDenied()

    def complete(self, user):
        if user == self.assigned_to:
            self.status = self.STATUS_COMPLETED
        elif user == self.author:
            self.completed = True
        else:
            raise PermissionDenied()

    def close(self, user):
        if user.is_superuser:
            self.status = self.STATUS_CLOSED
        else:
            raise PermissionDenied()


class Approval(models.Model):
    user = models.ForeignKey(
        User, related_name='approvals', on_delete=models.CASCADE
    )
    ticket = models.ForeignKey(
        Ticket, related_name='tickets', on_delete=models.CASCADE
    )
    approved = models.BooleanField(default=False)
