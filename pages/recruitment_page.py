import random
from playwright.sync_api import  expect
from data.data_class import Candidate, Vacancy
class RecruitmentPage:

    def __init__(self, page):
        self.page = page

    def go_to_recruitment_page(self):
     link = self.page.get_by_role("link", name="Recruitment")
     link.wait_for(state="visible")
     link.click()
    def open_vacancies(self):
        self.page.get_by_role("link", name="Vacancies").click()

    def click_add(self):
        self.page.get_by_role("button", name="Add").click()

    def fill_vacancy_form(self, job_title:str ,  vacancy:Vacancy, manager: str):
        self.page.get_by_role("textbox").nth(1).fill(vacancy.name)
        self.page.get_by_text("-- Select --").click()
        self.page.get_by_text(job_title).click()
        self.page.get_by_role("textbox", name="Type description here").fill(vacancy.description)
        self.page.get_by_role("textbox", name="Type for hints...").fill(manager)
        self.page.get_by_text(manager).click()
        self.page.get_by_role("textbox").nth(4).fill(str(vacancy.position_no))

    def save(self):
        self.page.get_by_role("button", name="Save").click()

    def assert_success(self):
        expect(self.page.get_by_text("Edit Vacancy")).to_be_visible(timeout=10000)
        
      
    def delete_vacancy(self, vacancy:Vacancy):
     vacancy_name = vacancy.name.strip()
     print("Trying to delete:", vacancy_name)
     row = self.page.locator("div[role='row']", has_text=vacancy_name)
     row.locator("button:has(i.bi-trash)").click()    
     self.page.get_by_role("button", name=" Yes, Delete ").click()
     
    def success_delete (self):
        expect(self.page.get_by_text("Successfully Deleted")).to_be_visible()
        
    def open_candidate(self):
        self.page.get_by_role("link", name="Candidates").click()
        
    def fill_candidate_form(self,  candidate:Candidate,):
        self.page.get_by_role("textbox", name="First Name").fill(candidate.first_name)
        self.page.get_by_role("textbox", name="Middle Name").fill(candidate.middle_name)
        self.page.get_by_role("textbox", name="Last Name").fill(candidate.last_name)
        dropdown = self.page.locator(".oxd-select-text").first
        dropdown.click()
        options = self.page.locator(".oxd-select-dropdown")
        options.wait_for()
        options.get_by_text(candidate.vacancy).click()

        self.page.get_by_role("textbox", name="Type here").first.fill(candidate.email)
        
    def reject_or_accept_candidate_by_manger(self , manger_name):
        row = self.page.locator(".oxd-table-row").filter(has_text=manger_name)
        row.get_by_role("button").nth(0).click()
        action = random.choice(["Shortlist", "Reject"])
        self.page.get_by_role("button", name=action).click()
        self.page.get_by_role("textbox", name="Type here").fill("Auto decision")
        self.page.get_by_role("button", name="Save").click()

        

          
        