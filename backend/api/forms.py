from django import forms

from .models import Department, Doctor, InsuranceProvider, Nurse, Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'phone',
            'address',
            'blood_group',
            'insurance_provider',
            'insurance_member_number',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return phone.strip() if phone else phone

    def clean_insurance_member_number(self):
        member_number = self.cleaned_data.get('insurance_member_number')
        return member_number.strip() if member_number else member_number


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialization', 'phone', 'email', 'department']

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return phone.strip() if phone else phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.strip().lower() if email else email


class NurseForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = ['first_name', 'last_name', 'phone', 'email', 'department']

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return phone.strip() if phone else phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.strip().lower() if email else email


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'description']

    def clean_department_name(self):
        return self.cleaned_data['department_name'].strip()


class InsuranceProviderForm(forms.ModelForm):
    class Meta:
        model = InsuranceProvider
        fields = ['provider_name', 'phone', 'email', 'address']

    def clean_provider_name(self):
        return self.cleaned_data['provider_name'].strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email.strip().lower() if email else email