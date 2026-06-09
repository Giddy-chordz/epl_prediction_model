#======SETUP DATABASE MODELS======
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key = True, nullable = False)

    HomeTeam = Column(String, nullable = False)
    AwayTeam = Column(String, nullable = False)

    FTHG = Column(Integer, nullable = False)
    FTAG = Column(Integer, nullable = False)

    UtcDate = Column(String, nullable = False)