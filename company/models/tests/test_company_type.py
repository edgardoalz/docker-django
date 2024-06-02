from django.core.exceptions import ValidationError
from django.db.models.fields import Field
from django.test import TestCase

from ...constants import CompanyTypeCodes
from ..company_type import CompanyType


class CompanyTypeTestCase(TestCase):
    def test_str(self):
        company_type = CompanyType.objects.get(code=CompanyTypeCodes.employee)
        self.assertEqual(str(company_type), "Employee")

    def test_create_invalid_code(self):
        error_message = Field().error_messages["invalid_choice"] % dict(value="Test")
        with self.assertRaisesMessage(ValidationError, error_message):
            CompanyType.objects.create(code="Test", name="Test")

    def test_create_derives_name_from_code(self):
        # We can't create a company_type with the same code, so we delete the existing one
        CompanyType.objects.filter(code=CompanyTypeCodes.employee).delete()

        company_type = CompanyType.objects.create(
            code=CompanyTypeCodes.employee, name="Test"
        )
        self.assertEqual(company_type.name, CompanyTypeCodes.employee.label)

    def test_update_invalid_code(self):
        company_type = CompanyType.objects.get(code=CompanyTypeCodes.employee)
        company_type.code = "Test"

        error_message = Field().error_messages["invalid_choice"] % dict(value="Test")
        with self.assertRaisesMessage(ValidationError, error_message):
            company_type.save()

    def test_update_name_ignored_deriving_from_code(self):
        company_type = CompanyType.objects.get(code=CompanyTypeCodes.employee)
        company_type.name = "Test"
        company_type.save()
        self.assertEqual(company_type.name, CompanyTypeCodes.employee.label)

    def test_company_type_codes_exist(self):
        company_types = CompanyType.objects.all()
        self.assertEqual(len(company_types), len(CompanyTypeCodes.values))
        for company_type in company_types:
            self.assertIn(company_type.code, CompanyTypeCodes.values)
