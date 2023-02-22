#Automação web e busca de informações

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
import pandas as pd

navegador = webdriver.Chrome()

#1: Pegar a cotação do dólar (entrar no google)

navegador.get('https://www.google.com/')

navegador.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotação do dólar') #pesquisando o dólar

navegador.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER) #apertando enter na pesquisa

cotacao_dolar = navegador.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value') #pegando a info do dólar

print('-=' * 10)
print(f'Cotação dólar: \n{cotacao_dolar}')
print('-=' * 10)

#2: Pegar a cotação de euro

navegador.get('https://www.google.com/')

navegador.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotação do euro') #pesquisando o euro

navegador.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER) #apertando enter na pesquisa

cotacao_euro = navegador.find_element(By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value') #pegando a info do euro


print(f'Cotação Euro: \n{cotacao_euro}')
print('-=' * 10)

#3: Pegar a cotação do ouro

navegador.get('https://www.melhorcambio.com/ouro-hoje#:~:text=O%20valor%20do%20grama%20do,em%20R%24%20311%2C98.') #Acessando o site com a cotação do Ouro

cotacao_ouro = navegador.find_element(By.XPATH, '//*[@id="comercial"]').get_attribute('value') #Pegando a info do Ouro

cotacao_ouro = cotacao_ouro.replace(",",".")

print(f'Cotação Ouro: \n{cotacao_ouro}')


#4: Importar a base de dados e atualizar a base

tabela = pd.read_excel("Produtos.xlsx") #lendo a base de dados e armazenando ela em tabela
print('-=' * 47)

#5: Recalcular os preços
#atualizar a cotação
#1º cotação dolar
 
tabela.loc[tabela["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar) #comparando as moedas anteriores para a nova moeda
tabela.loc[tabela["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
tabela.loc[tabela["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)

#recalcular os preços
#preço de compra = cotação * preço original
tabela["Preço de Compra"] = tabela["Cotação"] * tabela["Preço Original"]

#preço de venda = preço de compra * margem

tabela["Preço de Venda"] = tabela["Preço de Compra"] * tabela["Margem"]

tabela["Preço de Venda"] = tabela["Preço de Compra"].map('R${:.2f}'.format)

#6: Exportar a base atualizada.

tabela.to_excel('Produtos Novo.xlsx', index=False)

print(tabela)
print('-=' * 47)

#input('Digite algo para fechar ')

