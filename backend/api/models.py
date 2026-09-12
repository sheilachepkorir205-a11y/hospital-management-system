from django.db import models


class Role(models.Model):
	role_id = models.AutoField(primary_key=True, db_column='role_id')
	role_name = models.CharField(max_length=50)
	description = models.CharField(max_length=255, null=True, blank=True)

	class Meta:
		managed = False
		db_table = 'roles'


class User(models.Model):
	user_id = models.AutoField(primary_key=True, db_column='user_id')
	username = models.CharField(max_length=50)
	email = models.EmailField(max_length=100)
	password_hash = models.CharField(max_length=255)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	role = models.ForeignKey(
		Role,
		db_column='role_id',
		on_delete=models.DO_NOTHING,
		related_name='users',
	)
	is_active = models.BooleanField(null=True)
	created_at = models.DateTimeField(null=True)

	class Meta:
		managed = False
		db_table = 'users'


class Department(models.Model):
	department_id = models.AutoField(primary_key=True, db_column='department_id')
	department_name = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(null=True)

	class Meta:
		managed = False
		db_table = 'departments'


class InsuranceProvider(models.Model):
	insurance_provider_id = models.AutoField(primary_key=True, db_column='insurance_provider_id')
	provider_name = models.CharField(max_length=100)
	phone = models.CharField(max_length=20, null=True, blank=True)
	email = models.EmailField(max_length=100, null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	created_at = models.DateTimeField(null=True)

	class Meta:
		managed = False
		db_table = 'insurance_providers'


class Patient(models.Model):
	patient_id = models.AutoField(primary_key=True, db_column='patient_id')
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	date_of_birth = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=20, null=True, blank=True)
	phone = models.CharField(max_length=20, null=True, blank=True)
	address = models.CharField(max_length=255, null=True, blank=True)
	blood_group = models.CharField(max_length=5, null=True, blank=True)
	created_at = models.DateTimeField(null=True)
	insurance_provider = models.ForeignKey(
		InsuranceProvider,
		db_column='insurance_provider_id',
		null=True,
		blank=True,
		on_delete=models.DO_NOTHING,
		related_name='patients',
	)
	insurance_member_number = models.CharField(max_length=100, null=True, blank=True)
	updated_at = models.DateTimeField(null=True)

	class Meta:
		managed = False
		db_table = 'patients'


class Doctor(models.Model):
	doctor_id = models.AutoField(primary_key=True, db_column='doctor_id')
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	specialization = models.CharField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=20, null=True, blank=True)
	email = models.EmailField(max_length=100, null=True, blank=True)
	created_at = models.DateTimeField(null=True)
	department = models.ForeignKey(
		Department,
		db_column='department_id',
		null=True,
		blank=True,
		on_delete=models.DO_NOTHING,
		related_name='doctors',
	)
	updated_at = models.DateTimeField(null=True)

	class Meta:
		managed = False
		db_table = 'doctors'


class Nurse(models.Model):
	nurse_id = models.AutoField(primary_key=True, db_column='nurse_id')
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=20, null=True, blank=True)
	email = models.EmailField(max_length=100, null=True, blank=True)
	department = models.ForeignKey(
		Department,
		db_column='department_id',
		null=True,
		blank=True,
		on_delete=models.DO_NOTHING,
		related_name='nurses',
	)
	created_at = models.DateTimeField(null=True)

	class Meta:
		managed = False
		db_table = 'nurses'
