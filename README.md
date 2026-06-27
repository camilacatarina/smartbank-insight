# SmartBank - Motor de Simulação de Crédito API com aplicações de Segurança!

Uma API RESTful robusta desenvolvida em **Python + FastAPI** para simular análises de crédito. O sistema avalia propostas de empréstimo em tempo real, aplicando regras de negócio financeiras, criptografando dados sensíveis (LGPD) e salvando o histórico em um banco de dados relacional.

## Tecnologias Utilizadas

* **Python 3.12+**
* **FastAPI** (Alta performance e documentação automática)
* **PostgreSQL** (Banco de dados relacional)
* **SQLAlchemy** (ORM para modelagem e consultas)
* **Pydantic** (Validação de dados)
* **Uvicorn** (Servidor ASGI)
* **Hashlib** (Criptografia de CPF com SHA-256)

## Regras de Negócio

O sistema classifica as propostas automaticamente em 3 status:
1. 🟢 **APROVADO:** Parcela compromete menos de 25% da renda mensal.
2. 🟡 **EM ANÁLISE:** Valor solicitado acima de R$ 50.000 ou parcela muito próxima do limite (entre 25% e 30% da renda).
3. 🔴 **REPROVADO:** Parcela ultrapassa o limite de 30% da renda mensal.

## Como rodar o projeto na sua máquina

Para rodar este projeto localmente, siga o passo a passo:

**1. Clone o repositório**
```bash
git clone [https://github.com/camilacatarina/smartbank-insight.git](https://github.com/camilacatarina/smartbank-insight.git)
cd smartbank-insight