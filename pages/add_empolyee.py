    
from playwright.sync_api import  expect

from data.data_class import Employee
class AddEmployee :
    def __init__(self, page):
        self.page = page

    def go_to_add_employee_page(self):
        self.page.get_by_role("link", name="PIM").click()
        self.page.get_by_role("button", name=" Add").click()   
        
        
    def fill_basic_info(self, employee:Employee):
    
        self.page.get_by_role("textbox", name="First Name").click()
        self.page.get_by_role("textbox", name="First Name").fill(employee.first_name)
        self.page.get_by_role("textbox", name="Middle Name").click()
        self.page.get_by_role("textbox", name="Middle Name").fill(employee.middle_name)
        self.page.get_by_role("textbox", name="Last Name").click()
        self.page.get_by_role("textbox", name="Last Name").fill(employee.last_name)
        self.page.get_by_role("textbox").nth(4).click()
        self.page.get_by_role("textbox").nth(4).clear()

        self.page.get_by_role("textbox").nth(4).fill(str(employee.id))
    
    def enable_login_details(self, username, password,):
        self.page.locator(".oxd-switch-input").click()
       
        self.page.get_by_role("textbox").nth(5).click()
        self.page.get_by_role("textbox").nth(5).fill(username)
        self.page.locator("input[type=\"password\"]").first.click()
        self.page.locator("input[type=\"password\"]").first.fill(password)
        self.page.locator("input[type=\"password\"]").nth(1).click()
        self.page.locator("input[type=\"password\"]").nth(1).fill(password)
    
    def upload_photo(self, image_path=None):
        self.page.get_by_role("button").nth(4).click()
        if image_path:
           self.page.get_by_role("button", name="Choose File").set_input_files(image_path)
        self.page.wait_for_timeout(2000)            


    def save(self):
        self.page.get_by_role("button", name="Save").click()
        
        
    def add_employee_ok (self):
       expect(self.page.get_by_text("Successfully Saved")).to_be_visible(timeout=10000)
    

       

