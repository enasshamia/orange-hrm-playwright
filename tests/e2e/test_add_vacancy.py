
from playwright.sync_api import Page
import pytest
from data.data_class import Employee, Vacancy, generate_employee, generate_job_title, generate_vacancy,generate_candidate
from pages.add_empolyee import AddEmployee
from pages.login_page import LoginPage

from pages.recruitment_page import RecruitmentPage

@pytest.mark.parametrize(
    "employee ,vacancy, job_title",

    [(generate_employee()
      ,generate_vacancy(),generate_job_title() ,
      ) for _ in range(3)]
)
def test_add_vacancies(
    logged_in_page: Page,
    job_title, 
    #cleanup_vacancies, 
    vacancy: Vacancy , 
    employee:Employee , ):
    add_employee = AddEmployee(logged_in_page)
    add_employee.go_to_add_employee_page()
    add_employee.fill_basic_info(employee=employee)
    add_employee.enable_login_details(username=employee.username,
    password=employee.password,)
    add_employee.save()
    add_employee.add_employee_ok()
    hiring_manager_name = f"{employee.first_name} {employee.middle_name} {employee.last_name}"
  
    recruitmentpage = RecruitmentPage(logged_in_page)
    recruitmentpage.go_to_recruitment_page()
    logged_in_page.wait_for_url("**/recruitment/**")
    recruitmentpage.open_vacancies()
    recruitmentpage.click_add()
    recruitmentpage.fill_vacancy_form(
        job_title=job_title,
        vacancy=vacancy,
        manager=hiring_manager_name
    )
    recruitmentpage.save()
    recruitmentpage.assert_success()


    candidate = generate_candidate(vacancy.name)
    recruitmentpage.open_candidate()
    recruitmentpage.click_add()
    recruitmentpage.fill_candidate_form(candidate=candidate )
    recruitmentpage.save()
    loginpage = LoginPage(logged_in_page)
    loginpage.logout()
    logged_in_page.wait_for_url("**/auth/login")
    loginpage.login(employee.username, employee.password)
    recruitmentpage.go_to_recruitment_page()
    recruitmentpage.reject_or_accept_candidate_by_manger(vacancy.name)
    
    #cleanup_vacancies.append(vacancy)

    
    
    
    
   
   
