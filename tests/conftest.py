import pytest
import allure

from pages.login_page import LoginPage
from playwright.sync_api import Page
from pages.recruitment_page import RecruitmentPage

@pytest.fixture
def logged_in_page(page: Page):
    login_page = LoginPage(page)

    with allure.step("Open OrangeHRM login page"):
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    with allure.step("Login with Admin credentials"):
        LoginPage(page).login("Admin", "admin123")
    yield page  # 👉 test runs here

    # 🔹 Teardown (logout)
    login_page.logout()
    return page

@pytest.fixture
def logged_by_manger(page: Page ,username:str , password:str):
    with allure.step("Open OrangeHRM login page"):
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    with allure.step("Login with manger credentials"):
        LoginPage(page).login(username=username,password=password)

    return page

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("logged_in_page")
        if page:
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="failure-screenshot",
                attachment_type=allure.attachment_type.PNG
            )

@pytest.fixture
def cleanup_vacancies(logged_in_page):
    created = []  
    yield created  
    recruitment = RecruitmentPage(logged_in_page)
    recruitment.open_vacancies()
    for vacancy in created:
        try:
          recruitment.delete_vacancy(vacancy)
          recruitment.success_delete()
        except Exception:
            print(f"Failed to delete vacancy: {vacancy.name}")