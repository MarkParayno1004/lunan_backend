from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    first_line_address  = models.CharField(max_length=255)
    second_line_address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emergency_contact_person = models.CharField(max_length=255)
    emergency_contact_no = models.CharField(max_length=255)
    medical_history = models.CharField(max_length=255)
    current_medication = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    marital_status = models.CharField(max_length=255)
    date_of_birth = models.DateField()


class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)
    license_no = models.CharField(max_length=255)


class Diagnostic(models.Model):
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Prescription(models.Model):
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescribed_medicine = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Assignment(models.Model):
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    task = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)