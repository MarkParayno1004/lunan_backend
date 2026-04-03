import graphene
from .enums import RoleEnum


class UserModel(graphene.ObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    contact_no = graphene.String()
    role = graphene.Field(RoleEnum)


class AddressModel(graphene.ObjectType):
    id = graphene.ID()
    user = graphene.Field(UserModel)
    country = graphene.String()
    province = graphene.String()
    city = graphene.String()
    first_line_address = graphene.String()
    second_line_address = graphene.String()
    zip_code = graphene.String()


class PatientModel(graphene.ObjectType):
    id = graphene.ID()
    user = graphene.Field(UserModel)
    emergency_contact_person = graphene.String()
    emergency_contact_no = graphene.String()
    medical_history = graphene.String()
    current_medication = graphene.String()
    gender = graphene.String()
    marital_status = graphene.String()
    date_of_birth = graphene.Date()


class CounselorModel(graphene.ObjectType):
    id = graphene.ID()
    user = graphene.Field(UserModel)
    specialization = graphene.String()
    license_no = graphene.String()


class DiagnosticModel(graphene.ObjectType):
    id = graphene.ID()
    counselor = graphene.Field(CounselorModel)
    patient = graphene.Field(PatientModel)
    description = graphene.String()
    created_at = graphene.DateTime()


class PrescriptionModel(graphene.ObjectType):
    id = graphene.ID()
    counselor = graphene.Field(CounselorModel)
    patient = graphene.Field(PatientModel)
    prescribed_medicine = graphene.String()
    created_at = graphene.DateTime()


class AssignmentModel(graphene.ObjectType):
    id = graphene.ID()
    counselor = graphene.Field(CounselorModel)
    patient = graphene.Field(PatientModel)
    task = graphene.String()
    status = graphene.String()
    created_at = graphene.DateTime()


class CreateUserInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)
    contact_no = graphene.String(required=True)
    role = RoleEnum()


class LoginUserInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
