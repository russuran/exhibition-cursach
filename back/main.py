from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import Exhibit, Exhibition, Employee, Ticket, Restoration, ExhibitionContent
from pydantic import BaseModel
from typing import List, Optional, Any
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    # Создание тестовых данных
    db: Session = next(get_db())
    
    first_names = ["Иван", "Павел", "Мария", "Анна", "Сергей", "Елена", "Дмитрий", "Алексей", "Ольга", "Татьяна"]
    last_names = ["Петров", "Иванов", "Сидоров", "Кузнецов", "Смирнов", "Попов", "Лебедев", "Ковалев", "Зайцев", "Морозов"]

    # Создание тестовых сотрудников
    employees = []
    for i in range(10):
        employee = Employee(
            full_name=f"{random.choice(first_names)} {random.choice(last_names)}",
            position=random.choice(["Куратор", "Менеджер", "Эксперт"]),
            phone_number=random.randint(1000000000, 9999999999),
            salary=random.randint(40000, 80000)
        )
        employees.append(employee)
    
    db.add_all(employees)
    db.commit()
    for employee in employees:
        db.refresh(employee)

    # Создание тестовых экспонатов
    exhibit_titles = [
        "Мона Лиза", "Звёздная ночь", "Тайная вечеря", "Сотворение Адама",
        "Крик", "Девушка с жемчужной серёжкой", "Ночной дозор", "Сад земных наслаждений",
        "Герника", "Сон разума рождает чудовищ"
    ]
    
    exhibits = []
    for i in range(10):
        exhibit = Exhibit(
            title=exhibit_titles[i],
            description=f"Описание экспоната: {exhibit_titles[i]}",
            author=f"Автор {i + 1}",
            year_created=random.randint(1500, 2023),
            country_of_origin=random.choice(["Италия", "Франция", "Нидерланды", "Россия"]),
            material=random.choice(["Масло", "Акварель", "Графика", "Скульптура"])
        )
        exhibits.append(exhibit)
    
    db.add_all(exhibits)
    db.commit()
    for exhibit in exhibits:
        db.refresh(exhibit)

    # Создание тестовых выставок
    exhibition_titles = [
        "Искусство Ренессанса", "Импрессионизм", "Современное искусство",
        "Классическая живопись", "Скульптура XX века", "Фотография как искусство",
        "Авангард", "Модернизм", "Барокко", "Романтизм"
    ]
    
    exhibitions = []
    for i in range(10):
        exhibition = Exhibition(
            employee_id=random.choice(employees).employee_id,
            title=exhibition_titles[i],
            description=f"Описание выставки: {exhibition_titles[i]}",
            start_date=f"2023-01-{random.randint(1, 28):02d}",
            end_date=f"2023-02-{random.randint(1, 28):02d}",
            working_schedule="С 10:00 до 20:00"
        )
        exhibitions.append(exhibition)
    
    db.add_all(exhibitions)
    db.commit()
    for exhibition in exhibitions:
        db.refresh(exhibition)

    # Создание тестовых билетов
    tickets = []
    for i in range(10):
        ticket = Ticket(
            exhibition_id=random.choice(exhibitions).exhibition_id,
            ticket_type=random.choice(["Взрослый", "Детский"]),
            date=f"2023-01-{random.randint(1, 28):02d}",
            price=random.randint(10, 50),
            payment_method=random.choice(["Карта", "Наличные"])
        )
        tickets.append(ticket)
    
    db.add_all(tickets)
    db.commit()
    for ticket in tickets:
        db.refresh(ticket)

    # Создание тестовых восстановлений
    restorations = []
    for i in range(10):
        restoration = Restoration(
            exhibit_id=random.choice(exhibits).exhibit_id,
            employee_id=random.choice(employees).employee_id,
            start_date=f"2023-02-{random.randint(1, 28):02d}",
            end_date=f"2023-02-{random.randint(1, 28):02d}",
            restoration_reason=random.choice(["Чистка", "Ремонт", "Консервация"])
        )
        restorations.append(restoration)
    
    db.add_all(restorations)
    db.commit()
    for restoration in restorations:
        db.refresh(restoration)

    # Создание тестового содержания выставки
    exhibition_contents = []
    for exhibit in exhibits:
        for exhibition in exhibitions:
            exhibition_content = ExhibitionContent(
                exhibit_id=exhibit.exhibit_id,
                exhibition_id=exhibition.exhibition_id
            )
            exhibition_contents.append(exhibition_content)
    
    db.add_all(exhibition_contents)
    db.commit()
    for exhibition_content in exhibition_contents:
        db.refresh(exhibition_content)

    print("Тестовые данные успешно созданы!")



# Pydantic модели для валидации входящих данных
class ExhibitBase(BaseModel):
    title: str
    description: str
    author: str
    year_created: int
    country_of_origin: str
    material: str

class ExhibitCreate(ExhibitBase):
    pass

class ExhibitResponse(ExhibitBase):
    exhibit_id: int

    class Config:
        orm_mode = True

class ExhibitionBase(BaseModel):
    employee_id: int
    title: str
    description: str
    start_date: str
    end_date: Optional[str] = None
    working_schedule: str

class ExhibitionCreate(ExhibitionBase):
    pass

class ExhibitionResponse(ExhibitionBase):
    exhibition_id: int

    class Config:
        orm_mode = True

class EmployeeBase(BaseModel):
    full_name: str
    position: str
    phone_number: int
    salary: int

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    employee_id: int

    class Config:
        orm_mode = True

class TicketBase(BaseModel):
    exhibition_id: Any
    ticket_type: str
    date: str
    price: int
    payment_method: str

class TicketCreate(TicketBase):
    pass

class TicketResponse(TicketBase):
    ticket_id: int

    class Config:
        orm_mode = True

class RestorationBase(BaseModel):
    exhibit_id: int
    employee_id: Any
    start_date: str
    end_date: Optional[str] = None
    restoration_reason: str

class RestorationCreate(RestorationBase):
    pass

class RestorationResponse(RestorationBase):
    restoration_id: int

    class Config:
        orm_mode = True

class ExhibitionContentBase(BaseModel):
    exhibit_id: Any
    exhibition_id: Any

class ExhibitionContentCreate(ExhibitionContentBase):
    pass

class ExhibitionContentResponse(ExhibitionContentBase):
    class Config:
        orm_mode = True

# CRUD для Exhibit
@app.post("/exhibits/", response_model=ExhibitResponse)
def create_exhibit(exhibit: ExhibitCreate, db: Session = Depends(get_db)):
    new_exhibit = Exhibit(**exhibit.dict())
    db.add(new_exhibit)
    db.commit()
    db.refresh(new_exhibit)
    return new_exhibit

@app.get("/exhibits/{exhibit_id}", response_model=ExhibitResponse)
def read_exhibit(exhibit_id: int, db: Session = Depends(get_db)):
    exhibit = db.query(Exhibit).filter(Exhibit.exhibit_id == exhibit_id).first()
    if exhibit is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    return exhibit


@app.get("/exhibits/")
def get_exhibits(db: Session = Depends(get_db)):
    exhibits = db.query(Exhibit).all()
    if exhibits is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")

    return exhibits


@app.put("/exhibits/{exhibit_id}", response_model=ExhibitResponse)
def update_exhibit(exhibit_id: int, exhibit: ExhibitCreate, db: Session = Depends(get_db)):
    db_exhibit = db.query(Exhibit).filter(Exhibit.exhibit_id == exhibit_id).first()
    if db_exhibit is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    for key, value in exhibit.dict().items():
        setattr(db_exhibit, key, value)
    db.commit()
    return db_exhibit

@app.delete("/exhibits/{exhibit_id}")
def delete_exhibit(exhibit_id: int, db: Session = Depends(get_db)):
    db_exhibit = db.query(Exhibit).filter(Exhibit.exhibit_id == exhibit_id).first()
    if db_exhibit is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    db.delete(db_exhibit)
    db.commit()
    return {"detail": "Exhibit deleted"}

# CRUD для Exhibition
@app.post("/exhibitions/", response_model=ExhibitionResponse)
def create_exhibition(exhibition: ExhibitionCreate, db: Session = Depends(get_db)):
    new_exhibition = Exhibition(**exhibition.dict())
    db.add(new_exhibition)
    db.commit()
    db.refresh(new_exhibition)
    return new_exhibition

@app.get("/exhibitions/{exhibition_id}", response_model=ExhibitionResponse)
def read_exhibition(exhibition_id: int, db: Session = Depends(get_db)):
    exhibition = db.query(Exhibition).filter(Exhibition.exhibition_id == exhibition_id).first()
    if exhibition is None:
        raise HTTPException(status_code=404, detail="Exhibition not found")
    return exhibition

@app.get("/exhibitions/")
def read_exhibition(db: Session = Depends(get_db)):
    exhibitions = db.query(Exhibition).all()
    if exhibitions is None:
        raise HTTPException(status_code=404, detail="Exhibitions not found")

    exhibition_list = []
    for exhibition in exhibitions:
        employee = db.query(Employee).filter(Employee.employee_id == exhibition.employee_id).first()
        exhibition_list.append({
            "exhibition_id": exhibition.exhibition_id,
            "title": exhibition.title,
            "description": exhibition.description,
            "start_date": exhibition.start_date,
            "end_date": exhibition.end_date,
            "working_schedule": exhibition.working_schedule,
            "employee_id": employee.full_name if employee else "Неизвестный сотрудник"
        })

    return exhibition_list

@app.put("/exhibitions/{exhibition_id}", response_model=ExhibitionResponse)
def update_exhibition(exhibition_id: int, exhibition: ExhibitionCreate, db: Session = Depends(get_db)):
    db_exhibition = db.query(Exhibition).filter(Exhibition.exhibition_id == exhibition_id).first()
    if db_exhibition is None:
        raise HTTPException(status_code=404, detail="Exhibition not found")
    for key, value in exhibition.dict().items():
        setattr(db_exhibition, key, value)
    db.commit()
    return db_exhibition

@app.delete("/exhibitions/{exhibition_id}")
def delete_exhibition(exhibition_id: int, db: Session = Depends(get_db)):
    db_exhibition = db.query(Exhibition).filter(Exhibition.exhibition_id == exhibition_id).first()
    if db_exhibition is None:
        raise HTTPException(status_code=404, detail="Exhibition not found")
    db.delete(db_exhibition)
    db.commit()
    return {"detail": "Exhibition deleted"}

# CRUD для Employee
@app.post("/employees/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.get("/employees/")
def read_employee(db: Session = Depends(get_db)):
    employee = db.query(Employee).all()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in employee.dict().items():
        setattr(db_employee, key, value)
    db.commit()
    return db_employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(db_employee)
    db.commit()
    return {"detail": "Employee deleted"}

# CRUD для Ticket
@app.post("/tickets/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = Ticket(**ticket.dict())
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.get("/tickets/")
def get_ticket(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    if tickets is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    for ticket in tickets:
        exhibition = db.query(Exhibition).filter(Exhibition.exhibition_id == ticket.exhibition_id).first()
        ticket.exhibition_id = exhibition.title if exhibition else "Неизвестная выставка"

    return tickets

@app.put("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    
    if type(ticket.exhibition_id) == str:
        ticket.exhibition_id = db.query(Exhibition).filter(Exhibition.title == ticket.exhibition_id).first().exhibition_id
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    for key, value in ticket.dict().items():
        setattr(db_ticket, key, value)
    db.commit()
    return db_ticket

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(db_ticket)
    db.commit()
    return {"detail": "Ticket deleted"}

# CRUD для Restoration
@app.post("/restorations/", response_model=RestorationResponse)
def create_restoration(restoration: RestorationCreate, db: Session = Depends(get_db)):
    new_restoration = Restoration(**restoration.dict())
    db.add(new_restoration)
    db.commit()
    db.refresh(new_restoration)
    return new_restoration

@app.get("/restorations/{restoration_id}", response_model=RestorationResponse)
def read_restoration(restoration_id: int, db: Session = Depends(get_db)):
    restoration = db.query(Restoration).filter(Restoration.restoration_id == restoration_id).first()
    if restoration is None:
        raise HTTPException(status_code=404, detail="Restoration not found")
    return restoration

@app.get("/restorations/")
def get_restoration(db: Session = Depends(get_db)):
    restorations = db.query(Restoration).all()
    for restoration in restorations:
        employee = db.query(Employee).filter(Employee.employee_id == restoration.employee_id).first()
        restoration.employee_id = employee.full_name if employee else "Неизвестный сотрудник"

        exhibit = db.query(Exhibit).filter(Exhibit.exhibit_id == restoration.exhibit_id).first()
        restoration.exhibit_id = exhibit.title if exhibit else "Неизвестная выставка"


    if restorations is None:
        raise HTTPException(status_code=404, detail="Restoration not found")
    return restorations

@app.put("/restorations/{restoration_id}", response_model=RestorationResponse)
def update_restoration(restoration_id: int, restoration: RestorationCreate, db: Session = Depends(get_db)):
    db_restoration = db.query(Restoration).filter(Restoration.restoration_id == restoration_id).first()
    if type(restoration.employee_id) == str:
        restoration.employee_id = db.query(Employee).filter(Employee.full_name == restoration.employee_id).first().employee_id

    if db_restoration is None:
        raise HTTPException(status_code=404, detail="Restoration not found")
    for key, value in restoration.dict().items():
        setattr(db_restoration, key, value)
    db.commit()
    return db_restoration

@app.delete("/restorations/{restoration_id}")
def delete_restoration(restoration_id: int, db: Session = Depends(get_db)):
    db_restoration = db.query(Restoration).filter(Restoration.restoration_id == restoration_id).first()
    if db_restoration is None:
        raise HTTPException(status_code=404, detail="Restoration not found")
    db.delete(db_restoration)
    db.commit()
    return {"detail": "Restoration deleted"}

# CRUD для ExhibitionContent
@app.post("/exhibition_contents/")
def create_exhibition_content(content: ExhibitionContentCreate, db: Session = Depends(get_db)):
    try:
        new_content = ExhibitionContent(**content.dict())
        db.add(new_content)
        db.commit()
        db.refresh(new_content)
    except Exception as e:
        print(123)
        return {"error": str(e)}

    return new_content

@app.get("/exhibition_contents/{exhibit_id}/{exhibition_id}", response_model=ExhibitionContentResponse)
def read_exhibition_content(exhibit_id: int, exhibition_id: int, db: Session = Depends(get_db)):
    content = db.query(ExhibitionContent).filter(
        ExhibitionContent.exhibit_id == exhibit_id,
        ExhibitionContent.exhibition_id == exhibition_id
    ).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Exhibition content not found")
    return content


@app.put("/exhibition_contents/{id}/")
def read_exhibition_content(id: int, data: ExhibitionContentCreate, db: Session = Depends(get_db)):
    content = db.query(ExhibitionContent).filter(ExhibitionContent.id == id).first()
    
    if type(data.exhibit_id) == str:
        data.exhibit_id = db.query(Exhibit).filter(Exhibit.title == data.exhibit_id).first().exhibit_id
    if type(data.exhibition_id) == str:
        data.exhibition_id = db.query(Exhibition).filter(Exhibition.title == data.exhibition_id).first().exhibition_id  

    if content is None:
        raise HTTPException(status_code=404, detail="Exhibition content not found")
    
    for key, value in data.dict().items():
        setattr(content, key, value)
    db.commit()

    print(content)
    return content


@app.get("/exhibition_contents/")
def get_exhibition_content(db: Session = Depends(get_db)):
    contents = db.query(ExhibitionContent).all()
    for content in contents:
        exhibit = db.query(Exhibit).filter(Exhibit.exhibit_id == content.exhibit_id).first()
        content.exhibit_id = exhibit.title if exhibit else "Неизвестный экспонат"

        exhibition = db.query(Exhibition).filter(Exhibition.exhibition_id == content.exhibition_id).first()
        content.exhibition_id = exhibition.title if exhibition else "Неизвестная выставка"
    if contents is None:
        raise HTTPException(status_code=404, detail="Exhibition content not found")
    return contents

@app.delete("/exhibition_contents/{id}/")
def delete_exhibition_content(id: int, db: Session = Depends(get_db)):
    db_content = db.query(ExhibitionContent).filter(ExhibitionContent.id == id).first()

    if db_content is None:
        raise HTTPException(status_code=404, detail="Exhibition content not found")
    db.delete(db_content)
    db.commit()
    return {"detail": "Exhibition content deleted"}


@app.get("/exhibitions_list/")
def exhibitions_list(db: Session = Depends(get_db)):
    contents = db.query(Exhibition).all()

    return [{ 'id': content.exhibition_id, 'name': content.title } for content in contents]


@app.get("/employee_list/")
def employee_list(db: Session = Depends(get_db)):
    contents = db.query(Employee).all()

    return [{ 'id': employee.employee_id, 'name': employee.full_name } for employee in contents]


@app.get("/exhibit_list/")
def exhibit_list(db: Session = Depends(get_db)):
    contents = db.query(Exhibit).all()

    return [{ 'id': exhibit.exhibit_id, 'name': exhibit.title } for exhibit in contents]

