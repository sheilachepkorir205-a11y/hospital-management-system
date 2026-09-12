from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .auth import staff_login_required
from .forms import DepartmentForm, DoctorForm, InsuranceProviderForm, NurseForm, PatientForm
from .models import Department, Doctor, InsuranceProvider, Nurse, Patient


@staff_login_required
def patient_list(request):
	query = request.GET.get('q', '').strip()
	patients = Patient.objects.select_related('insurance_provider').order_by('last_name', 'first_name')
	if query:
		patients = patients.filter(
			Q(first_name__icontains=query)
			| Q(last_name__icontains=query)
			| Q(phone__icontains=query)
			| Q(insurance_member_number__icontains=query)
		)

	return render(request, 'patients/patient_list.html', {'patients': patients, 'query': query})


@staff_login_required
def patient_detail(request, patient_id):
	patient = get_object_or_404(
		Patient.objects.select_related('insurance_provider'),
		patient_id=patient_id,
	)
	return render(request, 'patients/patient_detail.html', {'patient': patient})


@staff_login_required
def patient_create(request):
	if request.method == 'POST':
		form = PatientForm(request.POST)
		if form.is_valid():
			patient = form.save()
			messages.success(request, 'Patient registered successfully.')
			return redirect('patient-detail', patient_id=patient.patient_id)
	else:
		form = PatientForm()

	return render(request, 'patients/patient_form.html', {'form': form, 'page_title': 'Register patient'})


@staff_login_required
def patient_update(request, patient_id):
	patient = get_object_or_404(Patient, patient_id=patient_id)
	if request.method == 'POST':
		form = PatientForm(request.POST, instance=patient)
		if form.is_valid():
			form.save()
			messages.success(request, 'Patient details updated successfully.')
			return redirect('patient-detail', patient_id=patient.patient_id)
	else:
		form = PatientForm(instance=patient)

	return render(
		request,
		'patients/patient_form.html',
		{'form': form, 'patient': patient, 'page_title': 'Edit patient'},
	)


@staff_login_required
def doctor_list(request):
	return staff_list(request, Doctor, 'Doctors')


@staff_login_required
def nurse_list(request):
	return staff_list(request, Nurse, 'Nurses')


def staff_list(request, model, staff_label):
	query = request.GET.get('q', '').strip()
	staff = model.objects.select_related('department').order_by('last_name', 'first_name')
	if query:
		staff = staff.filter(
			Q(first_name__icontains=query)
			| Q(last_name__icontains=query)
			| Q(phone__icontains=query)
			| Q(email__icontains=query)
			| Q(department__department_name__icontains=query)
		)
	return render(request, 'staff/staff_list.html', {
		'staff': staff,
		'staff_label': staff_label,
		'query': query,
		'is_doctor': model is Doctor,
	})


@staff_login_required
def doctor_detail(request, doctor_id):
	return staff_detail(request, Doctor, doctor_id, 'doctor_id', 'Doctor')


@staff_login_required
def nurse_detail(request, nurse_id):
	return staff_detail(request, Nurse, nurse_id, 'nurse_id', 'Nurse')


def staff_detail(request, model, staff_id, lookup_field, staff_label):
	staff_member = get_object_or_404(
		model.objects.select_related('department'),
		**{lookup_field: staff_id},
	)
	return render(request, 'staff/staff_detail.html', {
		'staff_member': staff_member,
		'staff_label': staff_label,
		'is_doctor': model is Doctor,
	})


@staff_login_required
def doctor_create(request):
	return staff_create(request, DoctorForm, 'doctor', 'doctor-detail', 'doctor_id')


@staff_login_required
def nurse_create(request):
	return staff_create(request, NurseForm, 'nurse', 'nurse-detail', 'nurse_id')


def staff_create(request, form_class, staff_label, detail_url, id_field):
	if request.method == 'POST':
		form = form_class(request.POST)
		if form.is_valid():
			staff_member = form.save()
			messages.success(request, f'{staff_label.capitalize()} added successfully.')
			return redirect(detail_url, **{id_field: staff_member.pk})
	else:
		form = form_class()
	return render(request, 'staff/staff_form.html', {
		'form': form,
		'page_title': f'Add {staff_label}',
	})


@staff_login_required
def doctor_update(request, doctor_id):
	return staff_update(request, Doctor, DoctorForm, doctor_id, 'doctor_id', 'doctor', 'doctor-detail')


@staff_login_required
def nurse_update(request, nurse_id):
	return staff_update(request, Nurse, NurseForm, nurse_id, 'nurse_id', 'nurse', 'nurse-detail')


def staff_update(request, model, form_class, staff_id, lookup_field, staff_label, detail_url):
	staff_member = get_object_or_404(model, **{lookup_field: staff_id})
	if request.method == 'POST':
		form = form_class(request.POST, instance=staff_member)
		if form.is_valid():
			form.save()
			messages.success(request, f'{staff_label.capitalize()} details updated successfully.')
			return redirect(detail_url, **{lookup_field: staff_member.pk})
	else:
		form = form_class(instance=staff_member)
	return render(request, 'staff/staff_form.html', {
		'form': form,
		'staff_member': staff_member,
		'page_title': f'Edit {staff_label}',
	})


@staff_login_required
def department_list(request):
	query = request.GET.get('q', '').strip()
	departments = Department.objects.order_by('department_name')
	if query:
		departments = departments.filter(
			Q(department_name__icontains=query) | Q(description__icontains=query)
		)
	return render(request, 'directory/directory_list.html', {
		'items': departments,
		'item_label': 'Departments',
		'query': query,
		'kind': 'department',
	})


@staff_login_required
def department_detail(request, department_id):
	department = get_object_or_404(Department, department_id=department_id)
	return render(request, 'directory/directory_detail.html', {
		'item': department,
		'item_label': 'Department',
		'kind': 'department',
	})


@staff_login_required
def department_create(request):
	return directory_create(request, DepartmentForm, 'department', 'department-detail', 'department_id')


@staff_login_required
def department_update(request, department_id):
	return directory_update(request, Department, DepartmentForm, department_id, 'department_id', 'department', 'department-detail')


@staff_login_required
def provider_list(request):
	query = request.GET.get('q', '').strip()
	providers = InsuranceProvider.objects.order_by('provider_name')
	if query:
		providers = providers.filter(
			Q(provider_name__icontains=query)
			| Q(phone__icontains=query)
			| Q(email__icontains=query)
		)
	return render(request, 'directory/directory_list.html', {
		'items': providers,
		'item_label': 'Insurance providers',
		'query': query,
		'kind': 'provider',
	})


@staff_login_required
def provider_detail(request, provider_id):
	provider = get_object_or_404(InsuranceProvider, insurance_provider_id=provider_id)
	return render(request, 'directory/directory_detail.html', {
		'item': provider,
		'item_label': 'Insurance provider',
		'kind': 'provider',
	})


@staff_login_required
def provider_create(request):
	return directory_create(request, InsuranceProviderForm, 'insurance provider', 'provider-detail', 'provider_id')


@staff_login_required
def provider_update(request, provider_id):
	return directory_update(request, InsuranceProvider, InsuranceProviderForm, provider_id, 'insurance_provider_id', 'insurance provider', 'provider-detail')


def directory_create(request, form_class, item_label, detail_url, id_field):
	if request.method == 'POST':
		form = form_class(request.POST)
		if form.is_valid():
			item = form.save()
			messages.success(request, f'{item_label.capitalize()} added successfully.')
			return redirect(detail_url, **{id_field: item.pk})
	else:
		form = form_class()
	return render(request, 'directory/directory_form.html', {
		'form': form,
		'page_title': f'Add {item_label}',
		'item_label': item_label,
	})


def directory_update(request, model, form_class, item_id, lookup_field, item_label, detail_url):
	item = get_object_or_404(model, **{lookup_field: item_id})
	if request.method == 'POST':
		form = form_class(request.POST, instance=item)
		if form.is_valid():
			form.save()
			messages.success(request, f'{item_label.capitalize()} updated successfully.')
			return redirect(detail_url, **{lookup_field.removesuffix('_id') + '_id': item.pk})
	else:
		form = form_class(instance=item)
	return render(request, 'directory/directory_form.html', {
		'form': form,
		'item': item,
		'page_title': f'Edit {item_label}',
		'item_label': item_label,
	})
