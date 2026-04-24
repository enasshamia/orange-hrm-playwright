

import allure
from playwright.sync_api import Page, expect
import pytest

from pages.search_employee import SearchEmployee

@allure.title("Search Employee using: {search_text}")
@allure.description("Verify employee search functionality using different search inputs such as empty values, partial names, special characters, and numeric values.")
    
@pytest.mark.parametrize(
    "search_text, expected_text",
    [   ("", ""), # empty search criteria
        ("Rami", "Rami"),                       # full name search
        ("NonExistentName", "No Records Found"), # non-existent employee
        ("##", "##"),                             # special characters
        ("rami", "Rami"),                         # case-insensitive  search
        ("123", "1235")    ,                   # numeric partial search
        ("123","123") ,                     # numeric exact search 
        ("na" , "Nalim")  ,     # partial name
        ("FirstNameTest LastNameTest", "FirstName") ,# full name search
       
    ]
)

def test_search_employee_username(logged_in_page: Page, search_text, expected_text):
    page = logged_in_page
    search_employee = SearchEmployee(page)
    with allure.step("Navigate to Employee List page"):
       search_employee.go_to_employee_list_page()
    with allure.step(f"Search employee using text: {search_text}"):
       search_employee.search_employee(search_text)
    with allure.step("Click Search button"):
       search_employee.save_search_employee()
    with allure.step("Validate search results"):
        if expected_text == "No Records Found":
          expect(page.locator("span:has-text('No Records Found')")).to_be_visible()
        elif  expected_text == "":
            rows = page.locator(".oxd-table-body .oxd-table-row")
            expect(rows.first).to_be_visible()
        else:
            expect(page.locator(".oxd-table-body")).to_contain_text(expected_text)

@pytest.mark.parametrize(
    "employee_id, expected_text",
    [
        ("QA222591", "QA222591"),
        ("0367", "0367"),
        ("ATPValue", "ATPValue"),
        ("Employee", "Employee"),
        ("", ""),
        ("eer", "No Records Found")
    ]
)


def test_employee_id_search(logged_in_page: Page, employee_id, expected_text):
    
    page = logged_in_page
    search_employee = SearchEmployee(page)
    page.context.tracing.group("search about employee with id: {employee_id}")
    search_employee.go_to_employee_list_page()
    search_employee.search_employee(employee_id=employee_id)
    search_employee.save_search_employee()
    rows = page.locator(".oxd-table-body .oxd-table-row")
    if expected_text == "No Records Found":
      SearchEmployee.search_with_id()        
    else: 
        if expected_text == "":
            
            expect(rows.first).to_be_visible()
        else:
            expect(rows).to_have_count(1)
            expect(page.locator(".oxd-table-body")).to_contain_text(expected_text)
            print("Returned Employee ID:", rows.first.text_content())
    page.context.tracing.group_end()



@allure.title("Search employees with empty search criteria")
@allure.description("Verify that the system returns the employee list when no search criteria are provided.")

def test_search_with_empty_fields(logged_in_page: Page):
    page = logged_in_page
    search_employee = SearchEmployee(page)
    search_employee.go_to_employee_list_page()
    search_employee.search_employee()
    search_employee.save_search_employee()
    rows = page.locator(".oxd-table-body .oxd-table-row")
    expect(rows.first).to_be_visible()


@allure.title("Search employee with partial name")
@allure.description("Verify that searching using a partial employee name returns only matching employees.")

def test_search_with_partial_employee_name(logged_in_page: Page):

    page = logged_in_page
    search_employee = SearchEmployee(page)

    with allure.step("Navigate to employee list page"):
        search_employee.go_to_employee_list_page()

    with allure.step("Search employee using partial name 'En'"):
        search_employee.search_employee("En")

    with allure.step("Click search button"):
        search_employee.save_search_employee()

    rows = page.locator(".oxd-table-body .oxd-table-row")

    count = rows.count()

    with allure.step(f"Validate results. Number of rows found: {count}"):

        for i in range(count):
            text = rows.nth(i).text_content().lower()
            assert "en" in text