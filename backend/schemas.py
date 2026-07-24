from pydantic import BaseModel
from typing import Optional, Dict, Any


class ProjectCreate(BaseModel):
    name: str
    company_name: str = ""
    system_name: str = ""


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    company_name: Optional[str] = None
    system_name: Optional[str] = None


class SectionDataUpdate(BaseModel):
    section_num: int   # 1-6
    data: Dict[str, Any] = {}


class SectionEnableUpdate(BaseModel):
    section_num: int   # 2-6
    enabled: bool


class ProjectResponse(BaseModel):
    id: int
    name: str
    company_name: str
    system_name: str
    section1_data: Dict[str, Any]
    section2_data: Dict[str, Any]
    section3_data: Dict[str, Any]
    section4_data: Dict[str, Any]
    section5_data: Dict[str, Any]
    section6_data: Dict[str, Any]
    section2_enabled: bool
    section3_enabled: bool
    section4_enabled: bool
    section5_enabled: bool
    section6_enabled: bool
    created_at: Optional[str]
    updated_at: Optional[str]
