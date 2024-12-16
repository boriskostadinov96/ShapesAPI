from sqlalchemy import Column, Integer, String, JSON, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./shapes.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class ShapeRequest(Base):
    __tablename__ = "shape_requests"
    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(String, unique=True, index=True)
    shape_type = Column(String, nullable=False)
    area_values = Column(JSON, nullable=False)


class ShapeResult(Base):
    __tablename__ = "shape_results"
    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(String, unique=True, index=True)
    result = Column(Float)


Base.metadata.create_all(bind=engine)
