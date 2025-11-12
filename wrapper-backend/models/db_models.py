from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, unique=True, index=True, nullable=False)
    institution = Column(String, nullable=False)
    position = Column(String, nullable=False)
    current_stage = Column(String, default="created")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for migration

    owner = relationship("User", back_populates="projects")
    files = relationship("ProjectFile", back_populates="project")
    executions = relationship("SkillExecution", back_populates="project")

class ProjectFile(Base):
    __tablename__ = "project_files"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String)  # json, md, pdf, docx
    file_path = Column(String, nullable=False)
    size_bytes = Column(Integer)
    version = Column(Integer, default=1)
    file_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="files")

class SkillExecution(Base):
    __tablename__ = "skill_executions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    skill_name = Column(String, nullable=False)
    prompt = Column(String)
    status = Column(String, default="running")  # running, completed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    duration_seconds = Column(Integer)
    success = Column(Boolean)
    stdout = Column(String)
    stderr = Column(String)
    returncode = Column(Integer)

    project = relationship("Project", back_populates="executions")
