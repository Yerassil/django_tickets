import os

os.system("rm db.sqlite3")
os.system("")

# django project name is adleads, replace adleads with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_tickets.settings")
import django
django.setup()
from django.core.management import call_command
call_command("migrate", interactive=False)


from django_tickets.models import Ticket
from django_tickets.models import User
author = User.objects.create_user(username='author', password="author")
assignee = User.objects.create_user(username='assignee', password="assignee")
approver = User.objects.create_user(username='approver', password="approver")
superuser = User.objects.create_user(
	username='superuser', password="superuser", is_superuser=True
)
ticket = Ticket.objects.create(
	author=author, assigned_to=assignee, title='first', description='desc'
)
ticket.approvers.add(approver)
ticket2 = Ticket.objects.create(
	author=author, assigned_to=assignee, title='second', description='desc'
)
ticket2.approvers.add(approver)
