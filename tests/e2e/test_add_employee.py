import random
import re
from playwright.sync_api import Page, expect
from pytest_playwright.pytest_playwright import page
from pages.add_empolyee import AddEmployee
from pages.login_page import LoginPage

from pathlib import Path

# Get the fixture directory path
FIXTURES_DIR = Path(__file__).parent / "fixtures"


base_url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
def test_add_employee(page):
    page.goto(base_url)
    login_page = LoginPage(page)
    login_page.login("Admin", "admin123")
    employee_id = str(random.randint(1000, 99999))
    add_employee = AddEmployee(page)
    add_employee.fill_basic_info("Enas", "k", "n", employee_id)
    add_employee.upload_photo(str(FIXTURES_DIR / "sunflower.jpg"))
    add_employee.enable_login_details("kjhsd34", "Enas123@#s123", "Enas123@#s123")
    add_employee.save()
    expect(page.get_by_role("heading", name="Personal Details")).to_be_visible(timeout=15000)

def test_required_fields_validation(page):
    page.goto(base_url)
    login_page = LoginPage(page)
    login_page.login("Admin", "admin123")
    add_employee = AddEmployee(page)
    add_employee.fill_basic_info("", "", "", "")
    add_employee.enable_login_details("", "", "")
    add_employee.save()
    error_locator = page.locator(".oxd-input-field-error-message")
    expect(error_locator).to_have_count(5)  # First Name + Last Name + Employee ID
    expect(error_locator).to_have_text(["Required", "Required", "Required","Required", "Passwords do not match"])


def test_username_uniqueness_validation(page):
    page.goto(base_url)
    login_page = LoginPage(page)
    login_page.login("Admin", "admin123")
    employee_id = str(random.randint(1000, 99999))
    add_employee = AddEmployee(page)
    add_employee.fill_basic_info("Enas", "k", "n", employee_id)
    add_employee.enable_login_details("Admin", "Enas123@#s123", "Enas123@#s123")
    add_employee.save()
    error_locator = page.locator(".oxd-input-field-error-message")
    expect(error_locator).to_have_text("Username already exists")

def test_username_length_validation(page):
    page.goto(base_url)
    login_page = LoginPage(page)
    login_page.login("Admin", "admin123")
    add_employee = AddEmployee(page)
    add_employee.fill_basic_info("Enas", "k", "n", "")
    add_employee.enable_login_details("kjh", "Enas123@#s123", "Enas123@#s123")
    add_employee.save()
    error_locator = page.locator(".oxd-input-field-error-message")  # Username length error
    expect(error_locator).to_have_text("Should be at least 5 characters")

def test_password_mismatch_validation(page):
    page.goto(base_url)
    login_page = LoginPage(page)
    login_page.login("Admin", "admin123")
    add_employee = AddEmployee(page)
    add_employee.fill_basic_info("Enas", "k", "n", "")
    add_employee.enable_login_details("kjhg456", "Enas123@#s123", "DifferentPassword")
    add_employee.save()
    expect(page.get_by_text("Passwords do not match")).to_be_visible()

def test_password_length_validation(page):
    page.goto(base_url)
    login_page = LoginPage(page)
    login_page.login("Admin", "admin123")
    employee_id = str(random.randint(1000, 99999))
    add_employee = AddEmployee(page)
    add_employee.fill_basic_info("Enas", "k", "n", employee_id)
    add_employee.enable_login_details("kjhg456", "short", "short")
    add_employee.save()
    expect(page.get_by_text("Should have at least 7 characters")).to_be_visible()

def test_password_complexity_validation(page):  
    page.goto(base_url)
    login_page = LoginPage(page)
    login_page.login("Admin", "admin123")
    add_employee = AddEmployee(page)
    add_employee.fill_basic_info("Enas", "k", "n", "")
    add_employee.enable_login_details("kjhg456", "shamiahgf", "shamiahgf")
    add_employee.save()
    expect(page.get_by_text("Your password must contain minimum 1 number")).to_be_visible()


def test_upload_photo_validation(page): 
    page.goto(base_url)
    login_page = LoginPage(page)
    login_page.login("Admin", "admin123")
    add_employee = AddEmployee(page)
    add_employee.fill_basic_info("Enas", "k", "n", "")
    add_employee.upload_photo(str(FIXTURES_DIR / "test.pdf"))  # Invalid file type
    expect(page.get_by_text("File type not allowed")).to_be_visible()

def test_upload_photo_size_validation(page):
    page.goto(base_url)
    login_page = LoginPage(page)
    login_page.login("Admin", "admin123")
    add_employee = AddEmployee(page)
    add_employee.fill_basic_info("Enas", "k", "n", "")
    add_employee.upload_photo(str(FIXTURES_DIR / "sunflower2.png"))  # Image larger than allowed size
    expect(page.get_by_text("Attachment Size Exceeded")).to_be_visible()