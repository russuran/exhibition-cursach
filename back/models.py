from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

class Exhibit(Base):
    __tablename__ = 'Exhibit'
    
    exhibit_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    year_created = Column(Integer, CheckConstraint('year_created > 0'), nullable=False)
    country_of_origin = Column(String(50), nullable=False)
    material = Column(String(50), nullable=False)

class Exhibition(Base):
    __tablename__ = 'Exhibition'
    
    exhibition_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    title = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    start_date = Column(String(10), nullable=False)
    end_date = Column(String(10))
    working_schedule = Column(String(50), nullable=False, default='С 10:00 до 20:00')

    employee = relationship("Employee", back_populates="exhibitions")

class Employee(Base):
    __tablename__ = 'Employee'
    
    employee_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), nullable=False)
    position = Column(String(50), nullable=False)
    phone_number = Column(Integer, unique=True, nullable=False)
    salary = Column(Integer, nullable=False)

    exhibitions = relationship("Exhibition", back_populates="employee")

class Ticket(Base):
    __tablename__ = 'Ticket'
    
    ticket_id = Column(Integer, primary_key=True, index=True)
    exhibition_id = Column(Integer, ForeignKey('Exhibition.exhibition_id'), nullable=False)
    ticket_type = Column(String(8), nullable=False, default='Adult')
    date = Column(String(10), nullable=False)
    price = Column(Integer, CheckConstraint('price >= 0'), nullable=False)
    payment_method = Column(String(8), nullable=False, default='Card')

class Restoration(Base):
    __tablename__ = 'Restoration'
    
    restoration_id = Column(Integer, primary_key=True, index=True)
    exhibit_id = Column(Integer, ForeignKey('Exhibit.exhibit_id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    start_date = Column(String(10), nullable=False)
    end_date = Column(String(10))
    restoration_reason = Column(String(50), nullable=False)

class ExhibitionContent(Base):
    __tablename__ = 'ExhibitionContent'
    
    exhibit_id = Column(Integer, ForeignKey('Exhibit.exhibit_id'), primary_key=True)
    exhibition_id = Column(Integer, ForeignKey('Exhibition.exhibition_id'), primary_key=True)
