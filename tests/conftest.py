import pytest
import allure

from pages.login_page import LoginPage
from playwright.sync_api import Page


@pytest.fixture
def logged_in_page(page: Page):
    with allure.step("Open OrangeHRM login page"):
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    with allure.step("Login with Admin credentials"):
        LoginPage(page).login("Admin", "admin123")

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