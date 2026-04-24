
from playwright.sync_api import  expect

class SearchEmployee:
    def __init__(self, page):
        self.page = page
    def go_to_employee_list_page(self):
        self.page.get_by_role("link", name="PIM").click()
        self.page.get_by_role("link", name="Employee List").click()

    def search_employee(self, employee_name = None, employee_id=None):
    
        if employee_name:
           self.page.get_by_role("textbox", name="Type for hints...").first.fill(employee_name)
        if employee_id:
            self.page.get_by_role("textbox").nth(2).click()
            self.page.get_by_role("textbox").nth(2).fill(employee_id)


    def save_search_employee(self):
        
        self.page.get_by_role("button", name="Search").click()

    
    def search_with_id (self):
       expect(self.page.get_by_text("No Records Found")).to_be_visible(timeout=10000)
    