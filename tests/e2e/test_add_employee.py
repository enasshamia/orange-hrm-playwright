import random
from playwright.sync_api import Page, expect
from pages.add_empolyee import AddEmployee
import pytest
from pathlib import Path

from utils.decorators import pw_trace


def generate_id():
    return str(random.randint(1000, 99999))

# Get the fixture directory path
FIXTURES_DIR = Path(__file__).parent/"fixtures"




@pytest.mark.parametrize(
    "first_name, last_name ,emp_id",
    [  
        ("Rami", "test" , generate_id()),                       # full name search
        ("##$$", "@@test",generate_id()),                             # special characters
        ("rami", "test2",generate_id()),                         # case-insensitive  search
        ("123", "test",generate_id())    ,                   # numeric partial search
        ("FirstNameTest LastNameTest","test",generate_id()) ,                     # numeric exact search 
        ("Nalim" , "test","QA222591")  , 
        ("Nalim" , "test","Employee")  ,    # partial name
  
    ]
)
def test_add_valid_employees(logged_in_page: Page, first_name, last_name, emp_id):
    add_employee = AddEmployee(logged_in_page)
    add_employee.go_to_add_employee_page()
    add_employee.fill_basic_info(
        first_name=first_name, 
        middle_name="", 
        last_name=last_name, 
        emp_id=emp_id
    )
    add_employee.save()
    add_employee.add_employee_ok()
    




@pytest.mark.parametrize(
    "user_name, password, confirm_pass, expected_result",
    [  
        ("admin", "Enas123@#s123", "Enas123@#s123", "Username already exists"),
        ("kjh", "Enas123@#s123", "Enas123@#s123", "Should be at least 5 characters"),
        ("rtkjrithrithrihkryiiuiuiuiruiruriuiuuirtiuit", "Enas123@#s123", "Enas123@#s123", "Should not exceed 40 characters"),
        ("12984", "Enas123@#s123", "Enas123@#s123", "success"),
        ("##ern@", "Enas123@#s123", "Enas123@#s123", "success"),
        ("hjknyfg", "Enas123@#s123", "Enas123@#s123", "success"),
    ]
)


@pw_trace("Add Employee Test")
def test_username_validation(logged_in_page: Page, user_name, password, confirm_pass, expected_result):

    add_employee = AddEmployee(logged_in_page)
    add_employee.go_to_add_employee_page()
    add_employee.fill_basic_info("Enas", "s", "n", generate_id())
    add_employee.enable_login_details(
            username=user_name,
            password=password,
            confirm_password=confirm_pass
        )
    add_employee.save()

    error_locator = logged_in_page.locator(".oxd-input-field-error-message")
    if expected_result == "success":
            add_employee.add_employee_ok()
    else:
            expect(error_locator).to_contain_text(expected_result)

def test_required_fields_validation(logged_in_page: Page):
    add_employee = AddEmployee(logged_in_page)
    add_employee.go_to_add_employee_page()

    add_employee.fill_basic_info("", "", "", "")
    add_employee.enable_login_details("", "", "")
    add_employee.save()
    error_locator = logged_in_page.locator(".oxd-input-field-error-message")

    expect(error_locator).to_have_count(5)
    expect(error_locator).to_have_text([
        "Required",
        "Required",
        "Required",
        "Required",
        "Passwords do not match"
    ])
    
def test_password_mismatch_validation(logged_in_page: Page):
    page = logged_in_page
    
    add_employee = AddEmployee(page)
    add_employee.go_to_add_employee_page()
    add_employee.fill_basic_info("Enas", "k", "n", "")
    add_employee.enable_login_details("kjhg456", "Enas123@#s123", "DifferentPassword")
    add_employee.save()
    expect(page.get_by_text("Passwords do not match")).to_be_visible()

def test_password_length_validation(logged_in_page: Page):
    page = logged_in_page
   
    employee_id = str(random.randint(1000, 99999))
    add_employee = AddEmployee(page)
    add_employee.go_to_add_employee_page()
    add_employee.fill_basic_info("Enas", "k", "n", employee_id)
    add_employee.enable_login_details("kjhg456", "short", "short")
    add_employee.save()
    expect(page.get_by_text("Should have at least 7 characters")).to_be_visible()

def test_password_complexity_validation(logged_in_page: Page):  
    page = logged_in_page
    add_employee = AddEmployee(page)
    add_employee.go_to_add_employee_page()
    add_employee.fill_basic_info("Enas", "k", "n", "")
    add_employee.enable_login_details("kjhg456", "shamiahgf", "shamiahgf")
    add_employee.save()
    expect(page.get_by_text("Your password must contain minimum 1 number")).to_be_visible()


def test_upload_photo_validation(logged_in_page: Page):
    page = logged_in_page
    add_employee = AddEmployee(page)
    add_employee.go_to_add_employee_page()
    add_employee.fill_basic_info("Enas", "k", "n", "")
    add_employee.upload_photo(str(FIXTURES_DIR/"test.pdf"))  # Invalid file type
    expect(page.get_by_text("File type not allowed")).to_be_visible()

def test_upload_photo_size_validation(logged_in_page: Page):
    page = logged_in_page
    add_employee = AddEmployee(page)
    add_employee.go_to_add_employee_page()
    add_employee.fill_basic_info("Enas", "k", "n", "")
    add_employee.upload_photo(str(FIXTURES_DIR/"sunflower2.png"))  # Image larger than allowed size
    expect(page.get_by_text("Attachment Size Exceeded")).to_be_visible()
    
    