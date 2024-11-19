from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import Exhibit, Exhibition, Employee, Ticket, Restoration, ExhibitionContent
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

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
    exhibition_id: int
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
    employee_id: int
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
    exhibit_id: int
    exhibition_id: int

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
        raise HTTPException(status_code=404, detail="Exhibition not found")

    return exhibitions

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
    return tickets

@app.put("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(ticket_id: int, ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
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
    if restorations is None:
        raise HTTPException(status_code=404, detail="Restoration not found")
    return restorations

@app.put("/restorations/{restoration_id}", response_model=RestorationResponse)
def update_restoration(restoration_id: int, restoration: RestorationCreate, db: Session = Depends(get_db)):
    db_restoration = db.query(Restoration).filter(Restoration.restoration_id == restoration_id).first()
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
@app.post("/exhibition_contents/", response_model=ExhibitionContentResponse)
def create_exhibition_content(content: ExhibitionContentCreate, db: Session = Depends(get_db)):
    new_content = ExhibitionContent(**content.dict())
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
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


@app.get("/exhibition_contents/")
def get_exhibition_content(db: Session = Depends(get_db)):
    contents = db.query(ExhibitionContent).all()
    if contents is None:
        raise HTTPException(status_code=404, detail="Exhibition content not found")
    return contents

@app.delete("/exhibition_contents/{exhibit_id}/{exhibition_id}")
def delete_exhibition_content(exhibit_id: int, exhibition_id: int, db: Session = Depends(get_db)):
    db_content = db.query(ExhibitionContent).filter(
        ExhibitionContent.exhibit_id == exhibit_id,
        ExhibitionContent.exhibition_id == exhibition_id
    ).first()
    if db_content is None:
        raise HTTPException(status_code=404, detail="Exhibition content not found")
    db.delete(db_content)
    db.commit()
    return {"detail": "Exhibition content deleted"}


