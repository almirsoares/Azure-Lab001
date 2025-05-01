# 🛍️ Cadastro de Produtos com Streamlit, Azure Blob e SQL Server

Este projeto é uma aplicação web simples desenvolvida com **Streamlit** para realizar o **cadastro e listagem de produtos**, incluindo upload de imagem para o **Azure Blob Storage** e armazenamento de dados em um banco de dados **SQL Server**.

---

## 📌 Funcionalidades

- Cadastro de produtos com nome, descrição, preço e imagem.
- Upload automático da imagem para o Azure Blob Storage.
- Armazenamento das informações no banco de dados SQL Server.
- Exibição dos produtos cadastrados com imagem.
  
---

### 🔄 Migração de `pymysql` para `pyodbc`

🔄 Migração de pymysql para pyodbc
O projeto originalmente utilizava o pacote pymysql para conectar-se ao banco de dados SQL Server. Apesar de alguns exemplos (incluindo o de um professor) funcionarem com pymysql, no contexto deste projeto, a integração apresentou dificuldades práticas que impactaram o funcionamento da aplicação.

⚠️ Dificuldades enfrentadas com pymysql:
A conexão com o banco de dados falhava constantemente, mesmo com os dados corretos.

Erros como Nome da fonte de dados não encontrado ou falhas silenciosas dificultavam o diagnóstico.

A compatibilidade parecia depender do ambiente ou configurações específicas do servidor.

Diante dessas limitações, optou-se pela substituição por pyodbc.

✅ Vantagens com pyodbc:
Conexão estável com bancos SQL Server utilizando drivers ODBC.

Suporte nativo a recursos do SQL Server, como criptografia e autenticação integrada.

Maior previsibilidade e facilidade de configuração, especialmente em ambiente Windows ou Azure.

Essa mudança permitiu que a aplicação funcionasse de forma mais confiável e estável no ambiente de produção.


Essa mudança permite:
- Conexão adequada com o Microsoft SQL Server.
- Compatibilidade com drivers ODBC disponíveis no Windows e Azure.
- Maior estabilidade e suporte corporativo.

---

## 🧱 Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)** – Para a criação da interface web.
- **[Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/)** – Para armazenamento de imagens.
- **[pyodbc](https://pypi.org/project/pyodbc/)** – Para conexão com SQL Server.
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** – Para carregar variáveis de ambiente.
- **Python 3.9+**

---
