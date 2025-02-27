import matplotlib.pyplot as plt
import pandas as pd

# Dados de Crescimento de Membros (Agregado Mensal) - INCLUÍDOS DIRETAMENTE NO CÓDIGO
monthly_dates = ['2024-10-31', '2024-11-30', '2024-12-31', '2025-01-31', '2025-02-28']
cumulative_members_monthly = [16, 17, 26, 27, 35]

# Criar DataFrame diretamente com os dados
df_membros = pd.DataFrame({
    'Data': pd.to_datetime(monthly_dates),
    'Membros Acumulados': cumulative_members_monthly
})

plt.figure(figsize=(10, 6))
plt.plot(df_membros['Data'], df_membros['Membros Acumulados'], marker='o', linestyle='-', color='blue')

# Configurações do Gráfico (em Português)
plt.title('Crescimento do Número de Membros ao Longo do Tempo', fontsize=14)
plt.xlabel('Mês', fontsize=12)
plt.ylabel('Número de Membros Acumulados', fontsize=12)
plt.ylim(0, 40) # Ajustar limite do eixo Y se necessário
plt.grid(True)
plt.tight_layout()

# Salvar o Gráfico em Arquivo PNG
plt.savefig('member_growth_pt_standalone.png') # Salvar com novo nome para não sobrescrever outros gráficos
plt.show()

print("Gráfico de crescimento de membros gerado e salvo como 'member_growth_pt_standalone.png'")