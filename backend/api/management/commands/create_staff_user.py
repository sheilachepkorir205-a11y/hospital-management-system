from getpass import getpass

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError

from api.models import Role, User


class Command(BaseCommand):
    help = 'Create a staff user in the existing users table with a secure password hash.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True, help='Unique staff username.')
        parser.add_argument('--email', required=True, help='Staff email address.')
        parser.add_argument('--first-name', required=True, help='Staff first name.')
        parser.add_argument('--last-name', required=True, help='Staff last name.')
        parser.add_argument('--role-id', required=True, type=int, help='Existing roles.role_id value.')

    def handle(self, *args, **options):
        username = options['username'].strip()
        email = options['email'].strip().lower()
        first_name = options['first_name'].strip()
        last_name = options['last_name'].strip()
        role_id = options['role_id']

        if not username or len(username) > 50:
            raise CommandError('Username must contain 1 to 50 characters.')
        if not email or len(email) > 100:
            raise CommandError('Email must contain 1 to 100 characters.')
        if not first_name or len(first_name) > 50:
            raise CommandError('First name must contain 1 to 50 characters.')
        if not last_name or len(last_name) > 50:
            raise CommandError('Last name must contain 1 to 50 characters.')
        if User.objects.filter(username=username).exists():
            raise CommandError('That username already exists.')
        if User.objects.filter(email=email).exists():
            raise CommandError('That email already exists.')

        try:
            role = Role.objects.get(role_id=role_id)
        except Role.DoesNotExist as exc:
            raise CommandError(f'No existing role was found for role_id={role_id}.') from exc

        password = getpass('Password: ')
        confirmation = getpass('Password (again): ')
        if not password:
            raise CommandError('Password cannot be empty.')
        if password != confirmation:
            raise CommandError('The two passwords did not match.')

        User.objects.create(
            username=username,
            email=email,
            password_hash=make_password(password),
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=True,
        )
        self.stdout.write(self.style.SUCCESS(f'Staff user {username!r} created with role {role.role_name!r}.'))