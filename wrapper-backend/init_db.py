from database import engine, Base
from models.db_models import User, Project, ProjectFile, SkillExecution
import logging

logger = logging.getLogger(__name__)

def init_db():
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")

if __name__ == "__main__":
    # Configure basic logging for standalone script
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    init_db()
