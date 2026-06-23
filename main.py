from fastapi import FastAPI
from pydantic import BaseModel
import hashlib

app = FastAPI()

def mascarar_cpf(cpf_original: str) -> str:
    # 1. Limpamos o CPF (removemos pontos e traços) para o hash ser sempre padrão
    cpf_limpo = cpf_original.replace(".", "").replace("-", "").strip()
    
    # 2. Transformamos o texto em bytes e aplicamos o algoritmo SHA-256
    hash_objeto = hashlib.sha256(cpf_limpo.encode('utf-8'))
    
    # 3. Transformamos o resultado em uma string de letras e números (hexadecimal)
    cpf_escondido = hash_objeto.hexdigest()
    
    return cpf_escondido

# Definição de como os dados devem chegar
class Simulacao(BaseModel):
    nome: str
    cpf: str
    renda: float
    valor_desejado: float
    parcelas: int

@app.get("/")
def home():
    return {"mensagem": "API de Crédito Bancário Online"}

@app.post("/simular")
def analisar_credito(dados: Simulacao):
    # Função de segurança
    cpf_protegido = mascarar_cpf(dados.cpf)
    
    # A lógica de negócio
    limite_parcela = dados.renda * 0.30
    valor_parcela = dados.valor_desejado / dados.parcelas
    
    if valor_parcela <= limite_parcela:
        resultado = "APROVADO"
    else:
        resultado = "REPROVADO"
        
    return {
        "status": resultado,
        "valor_parcela": round(valor_parcela, 2),
        "limite_permitido": limite_parcela,
        "cpf_no_banco_": cpf_protegido 
    }