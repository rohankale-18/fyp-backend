from pydantic import BaseModel
from typing import Optional
from datetime import date as DateType

class MaintenanceLogCreate(BaseModel):
    generator_id: str
    maintenance_detail: str
    status: str
    name_of_person: str
    date: DateType

class MaintenanceLogUpdate(BaseModel):
    log_id: int
    generator_id: Optional[str] = None
    maintenance_detail: Optional[str] = None
    status: Optional[str] = None
    name_of_person: Optional[str] = None
    date: Optional[DateType] = None

class MaintenanceLogDelete(BaseModel):
    log_id: int
