import streamlit as st
import mysql.connector
from mysql.connector import Error

# Função para criar conexão com o banco de dados
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Substitua pelo seu usuário do MySQL
            password="valena12",  # Substitua pela sua senha do MySQL
            database="programacoes_de_filmes"  # Nome do banco de dados
        )
        if connection.is_connected():
            st.success("Conexão bem-sucedida ao banco de dados!")
    except Error as e:
        st.error(f"Erro ao conectar ao MySQL: {e}")
    return connection

# Função para adicionar filme
def add_filme(connection):
    st.subheader("Adicionar Filme")
    titulo_original = st.text_input("Título Original:")
    titulo_brasil = st.text_input("Título no Brasil:")
    ano_lancamento = st.number_input("Ano de Lançamento:", min_value=1900, max_value=2024)
    pais_origem = st.text_input("País de Origem:")
    categoria = st.text_input("Categoria:")
    duracao = st.number_input("Duração (min):", min_value=1)

    if st.button("Adicionar Filme"):
        cursor = connection.cursor()
        sql = """
            INSERT INTO Filme (titulo_original, titulo_brasil, ano_lancamento, país_origem, categoria, duracao)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao))
        connection.commit()
        cursor.close()
        st.success("Filme adicionado com sucesso!")

# Função para visualizar filmes
def view_filmes(connection):
    st.subheader("Filmes Cadastrados")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Filme")
    filmes = cursor.fetchall()
    cursor.close()

    for filme in filmes:
        st.write(f"Título Original: {filme[1]}, Título no Brasil: {filme[2]}, Ano: {filme[3]}, País: {filme[4]}, Categoria: {filme[5]}, Duração: {filme[6]} min")

# Função para atualizar filme
def update_filme(connection):
    st.subheader("Atualizar Filme")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Filme")
    filmes = cursor.fetchall()
    cursor.close()

    titulo_original = st.selectbox("Escolha um filme para atualizar:", [filme[1] for filme in filmes])

    novo_titulo_original = st.text_input("Novo Título Original:")
    novo_titulo_brasil = st.text_input("Novo Título no Brasil:")
    novo_ano_lancamento = st.number_input("Novo Ano de Lançamento:", min_value=1900, max_value=2024)
    novo_pais_origem = st.text_input("Novo País de Origem:")
    nova_categoria = st.text_input("Nova Categoria:")
    nova_duracao = st.number_input("Nova Duração (min):", min_value=1)

    if st.button("Atualizar Filme"):
        cursor = connection.cursor()
        sql = """
            UPDATE Filme SET titulo_original = %s, titulo_brasil = %s, ano_lancamento = %s, país_origem = %s, categoria = %s, duracao = %s
            WHERE titulo_original = %s
        """
        cursor.execute(sql, (novo_titulo_original, novo_titulo_brasil, novo_ano_lancamento, novo_pais_origem, nova_categoria, nova_duracao, titulo_original))
        connection.commit()
        cursor.close()
        st.success("Filme atualizado com sucesso!")

# Função para remover filme
def delete_filme(connection):
    st.subheader("Remover Filme")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Filme")
    filmes = cursor.fetchall()
    cursor.close()

    titulo_original = st.selectbox("Escolha um filme para remover:", [filme[1] for filme in filmes])

    if st.button("Remover Filme"):
        cursor = connection.cursor()
        sql = "DELETE FROM Filme WHERE titulo_original = %s"
        cursor.execute(sql, (titulo_original,))
        connection.commit()
        cursor.close()
        st.success("Filme removido com sucesso!")

# Função principal para controle do menu
def main():
    connection = create_connection()
    st.title("Sistema de Programação de Filmes")

    menu = ["Adicionar Filme", "Ver Filmes", "Atualizar Filme", "Remover Filme"]
    choice = st.sidebar.selectbox("Selecione uma opção:", menu)

    if choice == "Adicionar Filme":
        add_filme(connection)
    elif choice == "Ver Filmes":
        view_filmes(connection)
    elif choice == "Atualizar Filme":
        update_filme(connection)
    elif choice == "Remover Filme":
        delete_filme(connection)

if __name__ == "__main__":
    main()
