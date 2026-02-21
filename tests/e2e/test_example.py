import re
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage

def test_login_to_orangehrm(page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page = LoginPage(page)
    login_page.login("Admin", "admin123")
    expect(page).to_have_title(re.compile("OrangeHRM"))



