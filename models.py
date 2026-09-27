import json

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///analysis.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    algo = Column(String, nullable=False)
    step = Column(Integer, nullable=False)
    n_max = Column(Integer, nullable=False)

    sizes_json = Column(String, nullable=False)
    steps_taken_json = Column(String, nullable=False)

    image_base64 = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def to_dict(self):
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
    Base.metadata.create_all(engine)
