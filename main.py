from fastapi import FastAPI, Depends
from pydantic import BaseModel
import hashlib

from database import engine, Base, SessionLocal
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Schema do Pydantic para validar os dados que chegam do Frontend
class SimulacaoRequest(BaseModel):
    nome: str
    cpf: str
    renda_mensal: float
    valor_solicitado: float
    parcelas: int

# Função para abrir e fechar a conexão com o banco de dados de forma segura
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função de mascarar o CPF
def mascarar_cpf(cpf_original: str) -> str:
    cpf_limpo = cpf_original.replace(".", "").replace("-", "").strip()
    hash_objeto = hashlib.sha256(cpf_limpo.encode('utf-8'))
    return hash_objeto.hexdigest()

@app.post("/simular")
def criar_simulacao(request: SimulacaoRequest, db: Session = Depends(get_db)):
    cpf_criptografado = mascarar_cpf(request.cpf)
    
    # A regra de negócio
    limite_aceitavel = request.renda_mensal * 0.30
    valor_parcela = request.valor_solicitado / request.parcelas
    
    if valor_parcela <= limite_aceitavel:
        status_resultado = "APROVADO"
    else:
        status_resultado = "REPROVADO"
        
    nova_simulacao = models.Simulacao(
        nome=request.nome,
        cpf=cpf_criptografado,  # Salvando o CPF protegido!
        renda_mensal=request.renda_mensal,
        valor_solicitado=request.valor_solicitado,
        parcelas=request.parcelas,
        status=status_resultado
    )
    
    # Grava as informações no banco de dados de verdade
    db.add(nova_simulacao)
    db.commit()
    db.refresh(nova_simulacao)
    
    return {
        "mensagem": "Simulação processada e salva com sucesso!",
        "id": nova_simulacao.id,
        "status": nova_simulacao.status,
        "valor_parcela": round(valor_parcela, 2)
    }