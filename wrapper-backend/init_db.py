from database import engine, Base
from models.db_models import User, Project, ProjectFile, SkillExecution

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
