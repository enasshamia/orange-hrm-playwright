from email.mime import image
from operator import ge
from playwright.sync_api import expect
from pytest_playwright.pytest_playwright import page


class AddEmployee :
    def __init__(self, page):
        self.page = page
    def fill_basic_info(self, first_name, middle_name, last_name, emp_id):
        self.page.get_by_role("link", name="PIM").click()
        self.page.get_by_role("button", name=" Add").click()    
        self.page.get_by_role("textbox", name="First Name").click()
        self.page.get_by_role("textbox", name="First Name").fill(first_name)
        self.page.get_by_role("textbox", name="Middle Name").click()
        self.page.get_by_role("textbox", name="Middle Name").fill(middle_name)
        self.page.get_by_role("textbox", name="Last Name").click()
        self.page.get_by_role("textbox", name="Last Name").fill(last_name)
        self.page.get_by_role("textbox").nth(4).click()
        self.page.get_by_role("textbox").nth(4).fill(emp_id)
    
    def enable_login_details(self, username, password, confirm_password):
        self.page.locator(".oxd-switch-input").click()
       
        self.page.get_by_role("textbox").nth(5).click()
        self.page.get_by_role("textbox").nth(5).fill(username)
        self.page.locator("input[type=\"password\"]").first.click()
        self.page.locator("input[type=\"password\"]").first.fill(password)
        self.page.locator("input[type=\"password\"]").nth(1).click()
        self.page.locator("input[type=\"password\"]").nth(1).fill(confirm_password)
        self.page.get_by_text("Disabled").click()
    
    def upload_photo(self, image_path=None):
        
        self.page.get_by_role("button").nth(4).click()
        if image_path: self.page.get_by_role("button", name="Choose File").set_input_files(image_path)
        self.page.wait_for_timeout(2000)


    # ================
    # ===========
    # 4️⃣ حفظ الموظف
    # ===========================
    def save(self):
        self.page.get_by_role("button", name="Save").click()

       

