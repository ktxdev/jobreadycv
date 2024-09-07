from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class Education(BaseModel):
    institution: str
    location: str
    program_name: str
    graduation_date: Optional[datetime] = None
    is_current: Optional[bool] = False

class Achievement(BaseModel):
    description: str

class Position(BaseModel):
    title: str
    achievements: List[Achievement]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: Optional[bool] = False

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


