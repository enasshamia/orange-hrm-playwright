import random
from playwright.sync_api import Page, expect
from pages.add_empolyee import AddEmployee

from pathlib import Path


# Get the fixture directory path
FIXTURES_DIR = Path(__file__).parent/"fixtures"


def test_add_employee(logged_in_page: Page):
    add_employee = AddEmployee(logged_in_page)
    employee_id = str(random.randint(1000, 99999))
    add_employee.go_to_add_employee_page()
    add_employee.fill_basic_info("Enas", "k", "n", employee_id)
    add_employee.upload_photo(str(FIXTURES_DIR/"sunflower.jpg"))
    add_employee.enable_login_details("test39", "Enas123@#s123", "Enas123@#s123")
    add_employee.save()
    expect(logged_in_page.get_by_role("heading", name="Personal Details")).to_be_visible(timeout=15000)

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

def test_username_uniqueness_validation(logged_in_page: Page):
    employee_id = str(random.randint(1000, 99999))
    add_employee = AddEmployee(logged_in_page)
    add_employee.go_to_add_employee_page()

    add_employee.fill_basic_info("Enas", "k", "n", employee_id)
    add_employee.enable_login_details("admin", "Enas123@#s123", "Enas123@#s123")
    add_employee.save()
    error_locator = logged_in_page.locator(".oxd-input-field-error-message")
    expect(error_locator).to_have_text("Username already exists")

def test_username_length_validation(logged_in_page: Page):
    page = logged_in_page
    add_employee = AddEmployee(page)
    add_employee.go_to_add_employee_page()
    add_employee.fill_basic_info("Enas", "k", "n", "")
    add_employee.enable_login_details("kjh", "Enas123@#s123", "Enas123@#s123")
    add_employee.save()
    error_locator = page.locator(".oxd-input-field-error-message") 
    expect(error_locator).to_have_text("Should be at least 5 characters")

    def test_username_length(logged_in_page: Page):
        page = logged_in_page
        add_employee = AddEmployee(page)
        add_employee.go_to_add_employee_page()
        add_employee.fill_basic_info("it657yghgjftiyiytrichiuu9rtickkhcbcbcbt", "k", "n", "")
        add_employee.save()
        error_locator = page.locator(".oxd-input-field-error-message") 
        expect(error_locator).to_have_text("Should not exceed 30 characters")

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