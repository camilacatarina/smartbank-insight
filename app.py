# Simulação de entrada de dados (O que viria do Frontend)
nome = "Maria"
cpf = "123.456.789-00"
renda_mensal = 4000.00
valor_solicitado = 15000.00
parcelas = 12

# Regra de Negócio: A parcela não pode ser > 30% da renda
limite_aceitavel = renda_mensal * 0.30
valor_parcela = valor_solicitado / parcelas

print(f"--- Analisando Crédito para: {nome} ---")
print(f"Limite de Parcela: R$ {limite_aceitavel}")
print(f"Valor da Parcela Proposta: R$ {valor_parcela:.2f}")

if valor_parcela <= limite_aceitavel:
    status = "APROVADO"
    cor = "Verde"
else:
    status = "REPROVADO"
    cor = "Vermelho"

print(f"Resultado Final: {status}")