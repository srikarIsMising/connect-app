import csv
import os
from django.core.management.base import BaseCommand

from apps.home.models import Users

class Command(BaseCommand):
    help = 'Import faculties and users from a CSV File'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing faculty and user data')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'File "{csv_file}" does not exist.'))
            raise FileNotFoundError(f'File "{csv_file}" does not exist.')
        
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Assuming the CSV has columns: institutionId, fullName, email, phoneNumber, userType
                institution_id = row.get('institutionId')
                full_name = row.get('fullName')
                email = row.get('email')
                phone_number = row.get('phoneNumber')
                gender = row.get('gender')
                password = row.get('password')  # Default password if not provided
                user_type = 'faculty'

                if not all([institution_id, full_name, email, phone_number, gender]):
                    self.stdout.write(self.style.ERROR(f'Missing fields in row: {row}'))
                    continue
                
                if Users.objects.filter(institutionId=institution_id).exists():
                    self.stdout.write(self.style.WARNING(f'User with institutionId {institution_id} already exists. Skipping.'))
                    continue

                try:
                    Users.objects.create_user_faculty(
                        institutionId=institution_id,
                        fullName=full_name,
                        email=email,
                        phoneNumber=phone_number,
                        gender=gender,
                        password=password if password else 'password'
                    )
                    self.stdout.write(self.style.SUCCESS(f'Successfully created user for institutionId {institution_id}.'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating user for institutionId {institution_id}: {e}. Skipping.'))
                    continue