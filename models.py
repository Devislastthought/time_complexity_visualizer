"""
This file sets up the database using SQLAlchemy — no raw SQL needed.

SQLAlchemy lets us describe a database table as a normal Python class
(this is called an "ORM" — Object Relational Mapper). Then we can save
and load rows just by creating/reading Python objects.

We're using SQLite here because it needs zero setup — the whole
database is just one file (analysis.db) that gets created automatically.
"""

import json

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Database connection ---
DATABASE_URL = "sqlite:///analysis.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Analysis(Base):
    """One row = one saved analysis result from the /analyze endpoint."""

    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    algo = Column(String, nullable=False)
    step = Column(Integer, nullable=False)
    n_max = Column(Integer, nullable=False)

    # Lists can't be stored directly in a normal column, so we store
    # them as JSON text and convert them back to Python lists when reading.
    sizes_json = Column(String, nullable=False)
    steps_taken_json = Column(String, nullable=False)

    image_base64 = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
        """Convert this database row into a plain dictionary for JSON responses."""
        return {
            "id": self.id,
            "algo": self.algo,
            "step": self.step,
            "n_max": self.n_max,
            "sizes": json.loads(self.sizes_json),
            "steps_taken": json.loads(self.steps_taken_json),
            "image_base64": self.image_base64,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def init_db():
    """Create the analyses table if it doesn't already exist."""
    Base.metadata.create_all(engine)
