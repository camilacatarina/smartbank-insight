from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import hashlib
from pydantic import BaseModel

from database import engine, Base, get_db
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

class SimulacaoRequest(BaseModel):
    nome: str
    cpf: str
    renda_mensal: float
    valor_solicitado: float
    parcelas: int

def mascarar_cpf(cpf_original: str) -> str:
    cpf_limpo = cpf_original.replace(".", "").replace("-", "").strip()
    hash_objeto = hashlib.sha256(cpf_limpo.encode('utf-8'))
    return hash_objeto.hexdigest()

@app.post("/simular", status_code=status.HTTP_201_CREATED)
def criar_simulacao(request: SimulacaoRequest, db: Session = Depends(get_db)):
    cpf_criptografado = mascarar_cpf(request.cpf)

    # Regras de Negócio
    limite_parcela = request.renda_mensal * 0.30
    valor_parcela = request.valor_solicitado / request.parcelas
    
    if valor_parcela > limite_parcela:
        status_simulacao = "REPROVADO"
    elif request.valor_solicitado > 50000 or valor_parcela >= (limite_parcela * 0.85):
        # Se pedir mais de 50k ou a parcela comprometer mais de 25.5% da renda, vai para análise humana
        status_simulacao = "EM ANÁLISE"
    else:
        status_simulacao = "APROVADO"

    # Dicas e ofertas personalizadas de acordo com o status
    dicas_e_ofertas = []
    
    if status_simulacao == "APROVADO":
        dicas_e_ofertas = [
            f"Parabéns, {request.nome}! Seu crédito pré-aprovado já está disponível.",
            "Dica Smart: Ative o débito automático das parcelas para nunca atrasar e manter seu Score sempre alto!"
        ]
    elif status_simulacao == "EM ANÁLISE":
        dicas_e_ofertas = [
            f"Olá, {request.nome}. Sua simulação está passando por uma checagem detalhada por nossos analistas.",
            "Dica Smart: Mantenha seus dados cadastrais atualizados no app para acelerar a liberação do seu crédito."
        ]
    else:
        dicas_e_ofertas = [
            "Dica de Crédito: Monitore seu CPF nos órgãos de proteção ao crédito (Serasa) para garantir que não há pendências.",
            "Que tal fazer o seu dinheiro render? Conheça nossos fundos de investimento com rendimento acima da poupança para construir sua reserva."
        ]

    db_simulacao = models.Simulacao(
        nome=request.nome,
        cpf=cpf_criptografado,
        renda_mensal=request.renda_mensal,
        valor_solicitado=request.valor_solicitado,
        parcelas=request.parcelas,
        status=status_simulacao
    )

    try:
        db.add(db_simulacao)
        db.commit()          
        db.refresh(db_simulacao) 
        
    except SQLAlchemyError as e:
        db.rollback()  
        print(f"\nERRO CRÍTICO NO BANCO DE DADOS: {e}\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "erro": "Serviço Temporariamente Indisponível",
                "mensagem": "Não foi possível processar sua simulação devido a uma instabilidade no servidor. Tente novamente em instantes."
            }
        )

    return {
        "mensagem": "Simulação processada e salva com sucesso!",
        "id": db_simulacao.id,              
        "status": db_simulacao.status,      
        "valor_parcela": round(valor_parcela, 2),
        "criado_em": db_simulacao.criado_em,
        "dicas_e_ofertas_do_banco": dicas_e_ofertas
    }