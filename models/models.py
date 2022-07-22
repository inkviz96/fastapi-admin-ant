from sqlalchemy import Column, VARCHAR, Integer, Boolean, Text
from database.database_connection import Base




class User(Base):
    __tablename__ = 'admin_user'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    password = Column(Text, nullable=False)
