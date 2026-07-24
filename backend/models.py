import json
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    company_name = Column(String(200), default="")
    system_name = Column(String(200), default="")
    # Sections 1-6 stored as JSON text
    section1_data = Column(Text, default="{}")   # 单位及系统基本信息
    section2_data = Column(Text, default="{}")   # 云计算
    section3_data = Column(Text, default="{}")   # 大数据
    section4_data = Column(Text, default="{}")   # 工控
    section5_data = Column(Text, default="{}")   # 物联网
    section6_data = Column(Text, default="{}")   # 移动互联
    # Section enable flags
    section2_enabled = Column(Integer, default=0)
    section3_enabled = Column(Integer, default=0)
    section4_enabled = Column(Integer, default=0)
    section5_enabled = Column(Integer, default=0)
    section6_enabled = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def get_section_data(self, section_num):
        attr = f"section{section_num}_data"
        return json.loads(getattr(self, attr, "{}"))

    def set_section_data(self, section_num, data):
        attr = f"section{section_num}_data"
        setattr(self, attr, json.dumps(data, ensure_ascii=False))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "company_name": self.company_name,
            "system_name": self.system_name,
            "section1_data": self.get_section_data(1),
            "section2_data": self.get_section_data(2),
            "section3_data": self.get_section_data(3),
            "section4_data": self.get_section_data(4),
            "section5_data": self.get_section_data(5),
            "section6_data": self.get_section_data(6),
            "section2_enabled": bool(self.section2_enabled),
            "section3_enabled": bool(self.section3_enabled),
            "section4_enabled": bool(self.section4_enabled),
            "section5_enabled": bool(self.section5_enabled),
            "section6_enabled": bool(self.section6_enabled),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
