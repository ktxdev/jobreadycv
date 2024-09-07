from datetime import datetime
from pydantic import BaseModel, validator, field_validator
from typing import Optional, List

class Education(BaseModel):
    institution: str
    location: str
    program_name: str
    graduation_date: Optional[datetime] = None
    is_current: Optional[bool] = False

    @classmethod
    @field_validator('graduation_date', mode='before')
    def parse_date(cls, value):
        return format_date(value)

class Achievement(BaseModel):
    description: str

class Position(BaseModel):
    title: str
    achievements: List[Achievement]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: Optional[bool] = False

    @classmethod
    @field_validator('end_date', 'start_date', mode='before')
    def parse_date(cls, value):
        return format_date(value)

class Experience(BaseModel):
    company: str
    location: str
    positions: List[Position]

class Skill(BaseModel):
    name: str

class Resume(BaseModel):
    full_name: str
    phone_number: Optional[str] = ''
    location: Optional[str] = ''
    email: Optional[str] = ''
    linkedin_url: Optional[str] = ''
    education: List[Education] = []
    experience: List[Experience] = []
    skills: List[Skill] = []

def format_date(value):
    # Define a list of possible date formats
    formats = ['%Y-%m-%d', '%Y-%m-%d']  # Add more formats if needed
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ValueError('Invalid date format')
