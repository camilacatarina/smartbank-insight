import uuid
import enum
from sqlalchemy import Column, String, Float, Integer, DateTime, Enum
from sqlalchemy.sql import func
from database import Base

class StatusSimulacao(str, enum.Enum):
    APROVADO = "APROVADO"
    REPROVADO = "REPROVADO"
    EM_ANALISE = "EM_ANALISE"


class Simulacao(Base):
    __tablename__ = "simulacoes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    renda_mensal = Column(Float, nullable=False)
    valor_solicitado = Column(Float, nullable=False)
    parcelas = Column(Integer, nullable=False)
    
    status = Column(Enum(StatusSimulacao), nullable=False)
    
    criado_em = Column(DateTime(timezone=True), server_default=func.now())