from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class FornecedoresSchema(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(32), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    
