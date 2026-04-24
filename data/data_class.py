from dataclasses import dataclass
import random
from faker import Faker

fake = Faker()

@dataclass
class Vacancy:
    name: str
    position_no: int
    manager: str
    description: str
    is_active:bool


def generate_vacancy():
    return Vacancy(
        name=fake.job(),
        position_no=fake.random_int(min=1, max=10),
        manager=fake.name(),
        description=fake.text(max_nb_chars=50),
        is_active=True
    )
    
    
@dataclass
class Candidate:
    first_name: str
    middle_name: str
    last_name: str
    vacancy: str
    email: str
def generate_candidate(vacancy_name: str):
    return Candidate(
        first_name=fake.first_name(),
        middle_name=fake.first_name(),
        last_name=fake.last_name(),
        vacancy=vacancy_name,
        email=fake.email()
    )
    
    
@dataclass
class Employee:
    first_name: str
    middle_name: str
    last_name: str
    id: int
    username: str
    password:str
    
    
    
def generate_employee():

    return Employee(
        first_name=fake.first_name(),
        middle_name=fake.first_name(),
        last_name=fake.last_name(),
        id=fake.random_int(min=1000, max=9999),
        username=fake.name(),
        password=fake.password(),
        
        )
        
    
def generate_job_title():
    titles = ["QA Lead", "Account Assistant", "Database Administrator"]
    return random.choice(titles)