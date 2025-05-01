import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pyodbc  # Alterado de pymysql para pyodbc
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

BlobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
BlobContainerName = os.getenv("BLOB_CONTAINER_NAME")
BlobAccountName = os.getenv("BLOB_ACCOUNT_NAME")

SqlServer = os.getenv("SQL_SERVER")
SqlDatabase = os.getenv("SQL_DATABASE")
SqlUsername = os.getenv("SQL_USERNAME")
SqlPassword = os.getenv("SQL_PASSWORD")

# Form de cadastro de produtos
st.title("Cadastro de produtos")

product_name = st.text_input("Nome do produto")
product_price = st.number_input("Preço do produto", min_value=0.0, format="%.2f")
product_description = st.text_area("Descrição do produto")
product_image = st.file_uploader("Imagem do produto", type=["jpg", "jpeg", "png"])

# Função para fazer o upload da imagem para o Azure Blob Storage
def upload_image_to_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
    containerClient = blob_service_client.get_container_client(BlobContainerName)
    blob_name = str(uuid.uuid4()) + file.name
    blob_client = containerClient.get_blob_client(blob_name)
    blob_client.upload_blob(file, overwrite=True)
    image_url = f"https://{BlobAccountName}.blob.core.windows.net/{BlobContainerName}/{blob_name}"
    return image_url

# Função para cadastrar o produto no banco de dados
def insert_product_to_db(nome, descricao, preco, product_image):
    try:
        imagem_url = upload_image_to_blob(product_image)
        
        # Conexão com o banco de dados usando pyodbc
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SqlServer};DATABASE={SqlDatabase};UID={SqlUsername};PWD={SqlPassword}')
        print("Conexão com o banco de dados estabelecida com sucesso!")
        
        cursor = conn.cursor()
        print("Cursor criado com sucesso!")
        
        sql = "INSERT INTO dbo.Produtos (nome, descricao, preco, imagem_url) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (nome, descricao, preco, imagem_url))
        
        print("Produto cadastrado com sucesso!")
        conn.commit()
        print("Transação confirmada com sucesso!")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao cadastrar produto: {e}")
        return False

def list_products_from_db():
    try:
        # Conexão com o banco de dados usando pyodbc
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SqlServer};DATABASE={SqlDatabase};UID={SqlUsername};PWD={SqlPassword}')
        print("Conexão com o banco de dados estabelecida com sucesso!")
        
        cursor = conn.cursor()
        print("Cursor criado com sucesso!")
        
        sql = "SELECT * FROM dbo.Produtos"
        cursor.execute(sql)
        produtos = cursor.fetchall()
        
        print("Produtos listados com sucesso!")
        cursor.close()
        conn.close()
        return produtos
    except Exception as e:
        print(f"Erro ao listar produtos: {e}")
        return []

def display_products():
    products_list = list_products_from_db()
    if products_list:
        cards_por_linha = 3
        cols = st.columns(cards_por_linha)
        for i, product in enumerate(products_list):
            with cols[i % cards_por_linha]:
                st.markdown(f"### {product.nome}")
                st.write(f"Descrição: {product.descricao}")
                st.write(f"Preço: {product.preco:.2f}")
                if product.imagem_url:
                    html_img = f'<img src="{product.imagem_url}" alt="Imagem do produto" style="width: 200; height: 200;">'
                    st.markdown(html_img, unsafe_allow_html=True)
            if (i + 1) % cards_por_linha == 0 and i + 1 < len(products_list):
                cols = st.columns(cards_por_linha)
    else:
        st.write("Nenhum produto cadastrado.")

if st.button("Cadastrar produto"):
    insert_product_to_db(product_name, product_description, product_price, product_image)
    return_message = "Produto cadastrado com sucesso!"

st.header("Produtos Cadastrados")

if st.button("Listar produtos"):
    display_products()
    return_message = "Produtos listados com sucesso!"
