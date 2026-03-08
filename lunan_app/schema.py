import graphene
from graphene_django import DjangoObjectType

from lunan_app.graphql.account_user.models import UserModel
from .models import User, Address, Patient, Counselor, Diagnostic, Prescription, Assignment
from .mutations import CreateUser, LoginUser


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "contact_no",
            "role",
            "created_at",
        )


class AddressType(DjangoObjectType):
    class Meta:
        model = Address
        fields = (
            "id",
            "user",
            "country",
            "province",
            "city",
            "first_line_address",
            "second_line_address",
            "zip_code",
        )


class PatientType(DjangoObjectType):
    class Meta:
        model = Patient
        fields = (
            "id",
            "user",
            "emergency_contact_person",
            "emergency_contact_no",
            "medical_history",
            "current_medication",
            "gender",
            "marital_status",
            "date_of_birth",
        )


class CounselorType(DjangoObjectType):
    class Meta:
        model = Counselor
        fields = (
            "id",
            "user",
            "specialization",
            "license_no",
        )


class DiagnosticType(DjangoObjectType):
    class Meta:
        model = Diagnostic
        fields = (
            "id",
            "counselor",
            "patient",
            "description",
            "created_at",
        )


class PrescriptionType(DjangoObjectType):
    class Meta:
        model = Prescription
        fields = (
            "id",
            "counselor",
            "patient",
            "prescribed_medicine",
            "created_at",
        )


class AssignmentType(DjangoObjectType):
    class Meta:
        model = Assignment
        fields = (
            "id",
            "counselor",
            "patient",
            "task",
            "status",
            "created_at",
        )


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    user_login = LoginUser.Field()


class Query(graphene.ObjectType):
    users = graphene.List(UserModel)
    user = graphene.Field(UserType, id=graphene.ID())
    addresses = graphene.List(AddressType)
    address = graphene.Field(AddressType, id=graphene.ID())
    patients = graphene.List(PatientType)
    patient = graphene.Field(PatientType, id=graphene.ID())
    counselors = graphene.List(CounselorType)
    counselor = graphene.Field(CounselorType, id=graphene.ID())
    diagnostics = graphene.List(DiagnosticType)
    diagnostic = graphene.Field(DiagnosticType, id=graphene.ID())
    prescriptions = graphene.List(PrescriptionType)
    prescription = graphene.Field(PrescriptionType, id=graphene.ID())
    assignments = graphene.List(AssignmentType)
    assignment = graphene.Field(AssignmentType, id=graphene.ID())

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.filter(pk=id).first()

    def resolve_addresses(self, info, **kwargs):
        return Address.objects.select_related("user").all()

    def resolve_address(self, info, id):
        return Address.objects.filter(pk=id).select_related("user").first()

    def resolve_patients(self, info, **kwargs):
        return Patient.objects.select_related("user").all()

    def resolve_patient(self, info, id):
        return Patient.objects.filter(pk=id).select_related("user").first()

    def resolve_counselors(self, info, **kwargs):
        return Counselor.objects.select_related("user").all()

    def resolve_counselor(self, info, id):
        return Counselor.objects.filter(pk=id).select_related("user").first()

    def resolve_diagnostics(self, info, **kwargs):
        return Diagnostic.objects.select_related("counselor", "patient").all()

    def resolve_diagnostic(self, info, id):
        return Diagnostic.objects.filter(pk=id).select_related("counselor", "patient").first()

    def resolve_prescriptions(self, info, **kwargs):
        return Prescription.objects.select_related("counselor", "patient").all()

    def resolve_prescription(self, info, id):
        return Prescription.objects.filter(pk=id).select_related("counselor", "patient").first()

    def resolve_assignments(self, info, **kwargs):
        return Assignment.objects.select_related("counselor", "patient").all()

    def resolve_assignment(self, info, id):
        return Assignment.objects.filter(pk=id).select_related("counselor", "patient").first()


schema = graphene.Schema(query=Query, mutation=Mutations)