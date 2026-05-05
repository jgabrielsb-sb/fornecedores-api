from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class FornecedoresSchema(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    cnpj = Column(String(32), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)


class FornecedorOnProteusSchema(Base):
    __tablename__ = "fornecedor_on_proteus"

    id = Column(Integer, primary_key=True, index=True)
    id_fornecedor = Column(
        Integer,
        ForeignKey("fornecedores.id"),
        nullable=False,
        index=True,
    )
    cep = Column(String, nullable=True)
    version = Column(Integer, nullable=False, default=0, server_default=text("0"))
    to_update = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )
    protheus_synced_version = Column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0"),
    )
    protheus_last_synced_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
