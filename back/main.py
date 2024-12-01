from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.future import select
import asyncio
from database import get_db, Base, engine
from models import Exhibit, Exhibition, Employee, Ticket, Restoration, ExhibitionContent, Base
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
async def startup(db: AsyncSession = Depends(get_db)):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


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
    exhibit_id: Any

    class Config:
        orm_mode = True

class ExhibitionBase(BaseModel):
    employee_id: Any
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
    exhibit_id: Any
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
async def create_exhibit(exhibit: ExhibitCreate, db: AsyncSession = Depends(get_db)):
    new_exhibit = Exhibit(**exhibit.dict())

    db.add(new_exhibit)
    await db.commit()
    await db.refresh(new_exhibit)
    return new_exhibit

@app.get("/exhibits/{exhibit_id}", response_model=ExhibitResponse)
async def read_exhibit(exhibit_id: int, db: AsyncSession = Depends(get_db)):
    exhibit = await db.execute(select(Exhibit).where(Exhibit.exhibit_id == exhibit_id))
    exhibit = exhibit.scalars().first()
    if exhibit is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    return exhibit


@app.get("/exhibits/")
async def get_exhibits(db: AsyncSession = Depends(get_db)):
    exhibits = await db.execute(select(Exhibit))
    exhibits = exhibits.scalars().all()

    if exhibits is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")

    return exhibits


@app.put("/exhibits/{exhibit_id}", response_model=ExhibitResponse)
async def update_exhibit(exhibit_id: int, exhibit: ExhibitCreate, db: AsyncSession = Depends(get_db)):
    db_exhibit = await db.execute(select(Exhibit).where(Exhibit.exhibit_id == exhibit_id))
    db_exhibit = db_exhibit.scalars().first()
    if db_exhibit is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    for key, value in exhibit.dict().items():
        setattr(db_exhibit, key, value)
    await db.commit()
    return db_exhibit

@app.delete("/exhibits/{exhibit_id}")
async def delete_exhibit(exhibit_id: int, db: AsyncSession = Depends(get_db)):
    db_exhibit = await db.execute(select(Exhibit).where(Exhibit.exhibit_id == exhibit_id))
    db_exhibit = db_exhibit.scalars().first()
    if db_exhibit is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    
    await db.execute(text("CALL remove_exhibit(:e_id)"), {"e_id": exhibit_id})

    await db.commit()

    # await db.delete(db_exhibit)
    # await db.commit()
    return {"status": "ok"}

# CRUD для Exhibition
@app.post("/exhibitions/", response_model=ExhibitionResponse)
async def create_exhibition(exhibition: ExhibitionCreate, db: AsyncSession = Depends(get_db)):
    new_exhibition = Exhibition(**exhibition.dict())
    db.add(new_exhibition)
    await db.commit()
    await db.refresh(new_exhibition)
    return new_exhibition

@app.get("/exhibitions/{exhibition_id}", response_model=ExhibitionResponse)
async def read_exhibition(exhibition_id: int, db: AsyncSession = Depends(get_db)):
    exhibition = await db.execute(select(Exhibition).where(Exhibition.exhibition_id == exhibition_id))
    exhibition = exhibition.scalars().first()
    if exhibition is None:
        raise HTTPException(status_code=404, detail="Exhibition not found")
    return exhibition

@app.get("/exhibitions/")
async def read_exhibition(db: AsyncSession = Depends(get_db)):
    exhibitions = await db.execute(select(Exhibition))
    exhibitions = exhibitions.scalars().all()
    if exhibitions is None:
        raise HTTPException(status_code=404, detail="Exhibitions not found")

    exhibition_list = []
    for exhibition in exhibitions:
        employee = await db.execute(select(Employee).where(Employee.employee_id == exhibition.employee_id))
        employee = employee.scalars().first()
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
async def update_exhibition(exhibition_id: int, exhibition: ExhibitionCreate, db: AsyncSession = Depends(get_db)):
    db_exhibition = await db.execute(select(Exhibition).where(Exhibition.exhibition_id == exhibition_id))
    db_exhibition = db_exhibition.scalars().first()

    print(333, exhibition)

    if type(exhibition.employee_id) == str:
        employee_id = await db.execute(select(Employee).where(Employee.full_name == exhibition.employee_id))
        exhibition.employee_id = employee_id.scalars().first().employee_id


    if db_exhibition is None:
        raise HTTPException(status_code=404, detail="Exhibition not found")
    for key, value in exhibition.dict().items():
        setattr(db_exhibition, key, value)
    await db.commit()
    return db_exhibition

@app.delete("/exhibitions/{exhibition_id}")
async def delete_exhibition(exhibition_id: int, db: AsyncSession = Depends(get_db)):
    db_exhibition = await db.execute(select(Exhibition).where(Exhibition.exhibition_id == exhibition_id))
    db_exhibition = db_exhibition.scalars().first()
    if db_exhibition is None:
        raise HTTPException(status_code=404, detail="Exhibition not found")
    await db.delete(db_exhibition)
    await db.commit()

    return {"status": "ok"}

# CRUD для Employee
@app.post("/employees/", response_model=EmployeeResponse)
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):\
    
    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    await db.commit()
    await db.refresh(new_employee)
    return new_employee

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def read_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    employee = await db.execute(select(Employee).where(Employee.employee_id == employee_id))
    employee = employee.scalars().first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.get("/employees/")
async def read_employee(db: AsyncSession = Depends(get_db)):
    employee = await db.execute(select(Employee))
    employee = employee.scalars().all()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee(employee_id: int, employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    db_employee = await db.execute(select(Employee).where(Employee.employee_id == employee_id))
    db_employee = db_employee.scalars().first()

    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in employee.dict().items():
        setattr(db_employee, key, value)
    await db.commit()
    return db_employee

@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    db_employee = await db.execute(select(Employee).where(Employee.employee_id == employee_id))
    db_employee = db_employee.scalars().first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    await db.delete(db_employee)
    await db.commit()
    return {"status": "ok"}

# CRUD для Ticket
@app.post("/tickets/", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate, db: AsyncSession = Depends(get_db)):

    if ticket.price <= 0:
        raise HTTPException(status_code=301, detail="Price must be greater than 0")


    new_ticket = Ticket(**ticket.dict())
    db.add(new_ticket)
    await db.commit()
    await db.refresh(new_ticket)
    return new_ticket

@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
async def read_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    ticket = await db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id))
    ticket = ticket.scalars().first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.get("/tickets/")
async def get_ticket(db: AsyncSession = Depends(get_db)):
    tickets = await db.execute(select(Ticket))
    tickets = tickets.scalars().all()
    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets found")

    for ticket in tickets:
        print(33333, ticket.exhibition_id)
        exhibition = await db.execute(select(Exhibition).where(Exhibition.exhibition_id == ticket.exhibition_id))
        exhibition = exhibition.scalars().first()
        
        ticket.exhibition_title = exhibition.title if exhibition else "Неизвестная выставка"

    return tickets

@app.put("/tickets/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: int, ticket: TicketCreate, db: AsyncSession = Depends(get_db)):
    db_ticket = await db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id))
    db_ticket = db_ticket.scalars().first()
    
    if type(ticket.exhibition_id) == str:
        ticket.exhibition_id = await db.execute(select(Exhibition).where(Exhibition.title == ticket.exhibition_id))
        ticket.exhibition_id = ticket.exhibition_id.scalars().first().exhibition_id
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    for key, value in ticket.dict().items():
        setattr(db_ticket, key, value)
    await db.commit()
    return db_ticket

@app.delete("/tickets/{ticket_id}")
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    db_ticket = await db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id))
    db_ticket = db_ticket.scalars().first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    await db.execute(text("CALL remove_ticket(:ticket_id)"), {"ticket_id": ticket_id})

    await db.commit()
    return {"status": "ok"}

# CRUD для Restoration
@app.post("/restorations/", response_model=RestorationResponse)
async def create_restoration(restoration: RestorationCreate, db: AsyncSession = Depends(get_db)):


    if type(restoration.employee_id) == str:
        employee = await db.execute(select(Employee).where(Employee.full_name == restoration.employee_id))
        restoration.employee_id = employee.scalars().first().employee_id


    new_restoration = Restoration(**restoration.dict())
    db.add(new_restoration)
    await db.commit()
    await db.refresh(new_restoration)
    return new_restoration

@app.get("/restorations/{restoration_id}", response_model=RestorationResponse)
async def read_restoration(restoration_id: int, db: AsyncSession = Depends(get_db)):
    restoration = await db.execute(select(Restoration).where(Restoration.restoration_id == restoration_id))
    restoration = restoration.scalars().first()
    if restoration is None:
        raise HTTPException(status_code=404, detail="Restoration not found")
    return restoration

@app.get("/restorations/")
async def get_restoration(db: AsyncSession = Depends(get_db)):
    # Fetch all restorations
    restorations = await db.execute(select(Restoration))
    restorations = restorations.scalars().all()

    if not restorations:
        return []

    employee_ids = {restoration.employee_id for restoration in restorations}
    exhibit_ids = {restoration.exhibit_id for restoration in restorations}

    employees = await db.execute(select(Employee).where(Employee.employee_id.in_(employee_ids)))
    employees_dict = {employee.employee_id: employee.full_name for employee in employees.scalars()}

    exhibits = await db.execute(select(Exhibit).where(Exhibit.exhibit_id.in_(exhibit_ids)))
    exhibits_dict = {exhibit.exhibit_id: exhibit.title for exhibit in exhibits.scalars()}

    for restoration in restorations:
        restoration.employee_id = employees_dict.get(restoration.employee_id, "Неизвестный сотрудник")
        restoration.exhibit_id = exhibits_dict.get(restoration.exhibit_id, "Неизвестная выставка")

    return restorations

@app.put("/restorations/{restoration_id}", response_model=RestorationResponse)
async def update_restoration(restoration_id: int, restoration: RestorationCreate, db: AsyncSession = Depends(get_db)):
    db_restoration = await db.execute(select(Restoration).where(Restoration.restoration_id == restoration_id))
    db_restoration = db_restoration.scalars().first()

    if type(restoration.employee_id) == str:
        employee = await db.execute(select(Employee).where(Employee.full_name == restoration.employee_id))
        restoration.employee_id = employee.scalars().first().employee_id

    if type(restoration.exhibit_id) == str:
        exhibit = await db.execute(select(Exhibit).where(Exhibit.title == restoration.exhibit_id))
        restoration.exhibit_id = exhibit.scalars().first().exhibit_id

    if db_restoration is None:
        raise HTTPException(status_code=404, detail="Restoration not found")
        
    for key, value in restoration.dict().items():
        setattr(db_restoration, key, value)
    await db.commit()
    return db_restoration

@app.delete("/restorations/{restoration_id}")
async def delete_restoration(restoration_id: int, db: AsyncSession = Depends(get_db)):
    db_restoration = await db.execute(select(Restoration).where(Restoration.restoration_id == restoration_id))
    db_restoration = db_restoration.scalars().first()
    if db_restoration is None:
        raise HTTPException(status_code=404, detail="Restoration not found")
    await db.delete(db_restoration)
    await db.commit()
    return {"status": "ok"}

# CRUD для ExhibitionContent
@app.post("/exhibition_contents/")
async def create_exhibition_content(content: ExhibitionContentCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_content = ExhibitionContent(**content.dict())
        db.add(new_content)
        await db.commit()
        await db.refresh(new_content)
    except Exception as e:
        print(123)
        return {"error": str(e)}

    return new_content

@app.get("/exhibition_contents/{exhibit_id}/{exhibition_id}", response_model=ExhibitionContentResponse)
async def read_exhibition_content(exhibit_id: int, exhibition_id: int, db: AsyncSession = Depends(get_db)):
    content = await db.execute(select(ExhibitionContent).where(
        ExhibitionContent.exhibit_id == exhibit_id,
        ExhibitionContent.exhibition_id == exhibition_id
    ))
    content = content.scalars().first()
    if content is None:
        raise HTTPException(status_code=404, detail="Exhibition content not found")
    return content


@app.put("/exhibition_contents/{id}/")
async def read_exhibition_content(id: int, data: ExhibitionContentCreate, db: AsyncSession = Depends(get_db)):
    content = await db.execute(select(ExhibitionContent).where(ExhibitionContent.id == id))
    content = content.scalars().first()
    
    if type(data.exhibit_id) == str:
        data.exhibit_id = await db.execute(select(Exhibit).where(Exhibit.title == data.exhibit_id))
        data.exhibit_id = data.exhibit_id.scalars().first().exhibit_id
    if type(data.exhibition_id) == str:
        data.exhibition_id = await db.execute(select(Exhibition).where(Exhibition.title == data.exhibition_id))
        data.exhibition_id = data.exhibition_id.scalars().first().exhibition_id  

    if content is None:
        raise HTTPException(status_code=404, detail="Exhibition content not found")
    
    for key, value in data.dict().items():
        setattr(content, key, value)
    await db.commit()

    print(content)
    return content


@app.get("/exhibition_contents/")
async def get_exhibition_content(db: AsyncSession = Depends(get_db)):
    contents = await db.execute(select(ExhibitionContent))
    contents = contents.scalars().all()

    if not contents:  # Проверяем, пуст ли список
        raise HTTPException(status_code=404, detail="Exhibition content not found")

    r_list = []

    for content in contents:
        exhibit = await db.execute(select(Exhibit).where(Exhibit.exhibit_id == content.exhibit_id))
        exhibit = exhibit.scalars().first()

        exhibition = await db.execute(select(Exhibition).where(Exhibition.exhibition_id == int(content.exhibition_id)))
        exhibition = exhibition.scalars().first()

        r_list.append({
            "id": content.id,
            "exhibit_id": exhibit.title if exhibit else "Неизвестный экспонат",
            "exhibition_id": exhibition.title if exhibition else "Неизвестная выставка"
        })
    
    return r_list


@app.delete("/exhibition_contents/{id}/")
async def delete_exhibition_content(id: int, db: AsyncSession = Depends(get_db)):
    db_content = await db.execute(select(ExhibitionContent).where(ExhibitionContent.id == id))
    db_content = db_content.scalars().first()

    if db_content is None:
        raise HTTPException(status_code=404, detail="Exhibition content not found")
    
    await db.execute(text("CALL remove_exhibition_contents(:e_id)"), {"e_id": id})

    await db.commit()


    return {"status": "ok"}


@app.get("/exhibitions_list/")
async def exhibitions_list(db: AsyncSession = Depends(get_db)):
    contents = await db.execute(select(Exhibition))
    contents = contents.scalars().all()

    return [{ 'id': content.exhibition_id, 'name': content.title } for content in contents]


@app.get("/employee_list/")
async def employee_list(db: AsyncSession = Depends(get_db)):
    contents = await db.execute(select(Employee))
    contents = contents.scalars().all()

    return [{ 'id': employee.employee_id, 'name': employee.full_name } for employee in contents]


@app.get("/exhibit_list/")
async def exhibit_list(db: AsyncSession = Depends(get_db)):
    contents = await db.execute(select(Exhibit))
    contents = contents.scalars().all()

    return [{ 'id': exhibit.exhibit_id, 'name': exhibit.title } for exhibit in contents]

