from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File as FastAPIFile
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import Project
from schemas import ProjectCreate, ProjectUpdate, SectionDataUpdate, SectionEnableUpdate
from export.word_export import export_word
from export.excel_export import export_excel
import os
import uuid

router = APIRouter(prefix="/api")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)


# ── File upload ──

@router.post("/upload")
async def upload_file(file: UploadFile = FastAPIFile(...)):
    allowed_exts = {'.png','.jpg','.jpeg','.pdf','.doc','.docx','.xls','.xlsx'}
    ext = os.path.splitext(file.filename or '')[1].lower()
    if ext not in allowed_exts:
        raise HTTPException(400, f"不支持的文件格式: {ext}")
    # 10MB limit
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "文件大小不能超过10MB")
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = os.path.join(UPLOAD_DIR, unique_name)
    with open(save_path, "wb") as f:
        f.write(contents)
    return JSONResponse({"url": f"/api/uploads/{unique_name}", "filename": file.filename, "size": len(contents)})


@router.get("/uploads/{filename}")
def serve_upload(filename: str):
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.isfile(filepath):
        raise HTTPException(404, "文件不存在")
    return FileResponse(filepath)


# ── Project CRUD ──

@router.get("/projects")
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.updated_at.desc()).all()
    return [p.to_dict() for p in projects]


@router.post("/projects")
def create_project(proj: ProjectCreate, db: Session = Depends(get_db)):
    p = Project(name=proj.name, company_name=proj.company_name, system_name=proj.system_name)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p.to_dict()


@router.get("/projects/{proj_id}")
def get_project(proj_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == proj_id).first()
    if not p:
        raise HTTPException(404, "项目不存在")
    return p.to_dict()


@router.put("/projects/{proj_id}")
def update_project(proj_id: int, proj: ProjectUpdate, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == proj_id).first()
    if not p:
        raise HTTPException(404, "项目不存在")
    if proj.name is not None:
        p.name = proj.name
    if proj.company_name is not None:
        p.company_name = proj.company_name
    if proj.system_name is not None:
        p.system_name = proj.system_name
    db.commit()
    db.refresh(p)
    return p.to_dict()


@router.delete("/projects/{proj_id}")
def delete_project(proj_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == proj_id).first()
    if not p:
        raise HTTPException(404, "项目不存在")
    db.delete(p)
    db.commit()
    return {"ok": True}


# ── Section data ──

@router.put("/projects/{proj_id}/section")
def save_section(proj_id: int, body: SectionDataUpdate, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == proj_id).first()
    if not p:
        raise HTTPException(404, "项目不存在")
    if body.section_num < 1 or body.section_num > 6:
        raise HTTPException(400, "section_num must be 1-6")
    p.set_section_data(body.section_num, body.data)
    db.commit()
    return {"ok": True}


@router.put("/projects/{proj_id}/section/enable")
def toggle_section(proj_id: int, body: SectionEnableUpdate, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == proj_id).first()
    if not p:
        raise HTTPException(404, "项目不存在")
    if body.section_num < 2 or body.section_num > 6:
        raise HTTPException(400, "section_num must be 2-6")
    setattr(p, f"section{body.section_num}_enabled", 1 if body.enabled else 0)
    db.commit()
    return {"ok": True}


# ── Export ──

@router.get("/projects/{proj_id}/export/word")
def download_word(proj_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == proj_id).first()
    if not p:
        raise HTTPException(404, "项目不存在")
    output_path = export_word(p)
    return FileResponse(output_path, filename=f"{p.name}_测评调研表.docx",
                        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


@router.get("/projects/{proj_id}/export/excel")
def download_excel(proj_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == proj_id).first()
    if not p:
        raise HTTPException(404, "项目不存在")
    output_path = export_excel(p)
    return FileResponse(output_path, filename=f"{p.name}_测评调研表.xlsx",
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
