import streamlit as st
import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="valena12",
            database="programacoes_de_filmes"
        )
        if connection.is_connected():
            st.success("Conexão bem-sucedida ao banco de dados!")
    except Error as e:
        st.error(f"Erro ao conectar ao MySQL: {e}")
    return connection

def filme_crud(connection):
    st.subheader("Gerenciar Filmes")

    with st.expander("Adicionar Filme"):
        titulo_original = st.text_input("Título Original:")
        titulo_brasil = st.text_input("Título no Brasil:")
        ano_lancamento = st.number_input("Ano de Lançamento:", min_value=1900, max_value=2024)
        pais_origem = st.text_input("País de Origem:")
        categoria = st.text_input("Categoria:")
        duracao = st.number_input("Duração (min):", min_value=1)

        if st.button("Adicionar Filme"):
            cursor = connection.cursor()
            sql = """
                INSERT INTO Filme (titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao))
            connection.commit()
            cursor.close()
            st.success("Filme adicionado com sucesso!")

    with st.expander("Ver Filmes"):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Filme")
        filmes = cursor.fetchall()
        cursor.close()
        for filme in filmes:
            st.write(
                f"Título Original: {filme[1]}, Título no Brasil: {filme[2]}, Ano: {filme[3]}, País: {filme[4]}, Categoria: {filme[5]}, Duração: {filme[6]} min")

    with st.expander("Remover Filme"):
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

    with st.expander("Atualizar Filme"):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Filme")
        filmes = cursor.fetchall()
        cursor.close()

        filme_selecionado = st.selectbox("Escolha um filme para atualizar:", [filme[1] for filme in filmes])
        filme = [f for f in filmes if f[1] == filme_selecionado][0]

        titulo_original = st.text_input("Título Original:", value=filme[1])
        titulo_brasil = st.text_input("Título no Brasil:", value=filme[2])
        ano_lancamento = st.number_input("Ano de Lançamento:", min_value=1900, max_value=2024, value=filme[3])
        pais_origem = st.text_input("País de Origem:", value=filme[4])
        categoria = st.text_input("Categoria:", value=filme[5])
        duracao = st.number_input("Duração (min):", min_value=1, value=filme[6])

        if st.button("Atualizar Filme"):
            cursor = connection.cursor()
            sql = """
                UPDATE Filme
                SET titulo_original = %s, titulo_brasil = %s, ano_lancamento = %s, pais_origem = %s, categoria = %s, duracao = %s
                WHERE num_filme = %s
            """
            cursor.execute(sql,
                           (titulo_original, titulo_brasil, ano_lancamento, pais_origem, categoria, duracao, filme[0]))
            connection.commit()
            cursor.close()
            st.success("Filme atualizado com sucesso!")

def canal_crud(connection):
    st.subheader("Gerenciar Canais")

    with st.expander("Adicionar Canal"):
        nome = st.text_input("Nome do Canal:")
        sigla = st.text_input("Sigla:")
        if st.button("Adicionar Canal"):
            cursor = connection.cursor()
            sql = """
                INSERT INTO Canal (nome, sigla)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (nome, sigla))
            connection.commit()
            cursor.close()
            st.success("Canal adicionado com sucesso!")

    with st.expander("Ver Canais"):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Canal")
        canais = cursor.fetchall()
        cursor.close()
        for canal in canais:
            st.write(f"Nome: {canal[1]}, Sigla: {canal[2]}")

    with st.expander("Remover Canal"):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Canal")
        canais = cursor.fetchall()
        cursor.close()
        nome_canal = st.selectbox("Escolha um canal para remover:", [canal[1] for canal in canais])
        if st.button("Remover Canal"):
            cursor = connection.cursor()
            sql = "DELETE FROM Canal WHERE nome = %s"
            cursor.execute(sql, (nome_canal,))
            connection.commit()
            cursor.close()
            st.success("Canal removido com sucesso!")

    with st.expander("Atualizar Canal"):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Canal")
        canais = cursor.fetchall()
        cursor.close()

        canal_selecionado = st.selectbox("Escolha um canal para atualizar:", [canal[1] for canal in canais])
        canal = [c for c in canais if c[1] == canal_selecionado][0]

        nome = st.text_input("Nome do Canal:", value=canal[1])
        sigla = st.text_input("Sigla:", value=canal[2])

        if st.button("Atualizar Canal"):
            cursor = connection.cursor()
            sql = """
                UPDATE Canal
                SET nome = %s, sigla = %s
                WHERE num_canal = %s
            """
            cursor.execute(sql, (nome, sigla, canal[0]))
            connection.commit()
            cursor.close()
            st.success("Canal atualizado com sucesso!")

def exibicao_crud(connection):
    st.subheader("Gerenciar Exibições")

    with st.expander("Adicionar Exibição"):
        cursor = connection.cursor()
        cursor.execute("SELECT num_filme, titulo_original FROM Filme")
        filmes = cursor.fetchall()
        cursor.execute("SELECT num_canal, nome FROM Canal")
        canais = cursor.fetchall()
        cursor.close()

        filme_escolhido = st.selectbox("Escolha o Filme:", [f"{filme[1]}" for filme in filmes], key="filme_add")
        canal_escolhido = st.selectbox("Escolha o Canal:", [f"{canal[1]}" for canal in canais], key="canal_add")
        data_exibicao = st.date_input("Data de Exibição:")

        num_filme = [filme[0] for filme in filmes if filme[1] == filme_escolhido][0]
        num_canal = [canal[0] for canal in canais if canal[1] == canal_escolhido][0]

        if st.button("Adicionar Exibição"):
            cursor = connection.cursor()
            sql = """
                INSERT INTO Exibicao (num_filme, num_canal, data)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (num_filme, num_canal, data_exibicao))
            connection.commit()
            cursor.close()
            st.success("Exibição adicionada com sucesso!")

    with st.expander("Ver Exibições"):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT e.num_filme, f.titulo_original, c.nome, e.data
            FROM Exibicao e
            JOIN Filme f ON e.num_filme = f.num_filme
            JOIN Canal c ON e.num_canal = c.num_canal
        """)
        exibicoes = cursor.fetchall()
        cursor.close()
        for exibicao in exibicoes:
            st.write(f"Filme: {exibicao[1]}, Canal: {exibicao[2]}, Data: {exibicao[3]}")

    with st.expander("Remover Exibição"):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT e.num_filme, f.titulo_original, c.nome, e.data
            FROM Exibicao e
            JOIN Filme f ON e.num_filme = f.num_filme
            JOIN Canal c ON e.num_canal = c.num_canal
        """)
        exibicoes = cursor.fetchall()
        cursor.close()

        exibicao_escolhida = st.selectbox("Escolha a exibição para remover:",
                                            [f"{exibicao[1]} - {exibicao[2]} - {exibicao[3]}" for exibicao in exibicoes],
                                            key="exibicao_remover")

        if st.button("Remover Exibição"):
            num_filme = [exibicao[0] for exibicao in exibicoes if f"{exibicao[1]} - {exibicao[2]} - {exibicao[3]}" == exibicao_escolhida][0]
            num_canal = [exibicao[0] for exibicao in exibicoes if f"{exibicao[1]} - {exibicao[2]} - {exibicao[3]}" == exibicao_escolhida][0]
            data_exibicao = exibicao_escolhida.split(" - ")[2]

            cursor = connection.cursor()
            sql = "DELETE FROM Exibicao WHERE num_filme = %s AND num_canal = %s AND data = %s"
            cursor.execute(sql, (num_filme, num_canal, data_exibicao))
            connection.commit()
            cursor.close()
            st.success("Exibição removida com sucesso!")

    with st.expander("Atualizar Exibição"):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT e.num_filme, f.titulo_original, c.nome, e.data
            FROM Exibicao e
            JOIN Filme f ON e.num_filme = f.num_filme
            JOIN Canal c ON e.num_canal = c.num_canal
        """)
        exibicoes = cursor.fetchall()
        cursor.close()

        exibicao_selecionada = st.selectbox("Escolha a exibição para atualizar:",
                                              [f"{exibicao[1]} - {exibicao[2]} - {exibicao[3]}" for exibicao in exibicoes],
                                              key="exibicao_atualizar")

        exibicao = [e for e in exibicoes if f"{e[1]} - {e[2]} - {e[3]}" == exibicao_selecionada][0]

        filme_escolhido = st.selectbox("Escolha o Filme:",
                                        [f"{filme[1]}" for filme in filmes],
                                        index=[filme[1] for filme in filmes].index(exibicao[1]),
                                        key="filme_atualizar")
        canal_escolhido = st.selectbox("Escolha o Canal:",
                                        [f"{canal[1]}" for canal in canais],
                                        index=[canal[1] for canal in canais].index(exibicao[2]),
                                        key="canal_atualizar")
        data_exibicao = st.date_input("Data de Exibição:", value=exibicao[3])

        num_filme = [filme[0] for filme in filmes if filme[1] == filme_escolhido][0]
        num_canal = [canal[0] for canal in canais if canal[1] == canal_escolhido][0]

        if st.button("Atualizar Exibição"):
            cursor = connection.cursor()
            print(
                f"Updating Exibicao with: num_filme={num_filme}, num_canal={num_canal}, data={data_exibicao}, original_num_filme={exibicao[0]}, original_num_canal={exibicao[1]}, original_data={exibicao[3]}")

            sql = """
                UPDATE Exibicao
                SET num_filme = %s, num_canal = %s, data = %s
                WHERE num_filme = %s AND num_canal = %s AND data = %s
            """
            cursor.execute(sql, (num_filme, num_canal, data_exibicao, exibicao[0], exibicao[1], exibicao[3]))
            connection.commit()
            cursor.close()
            st.success("Exibição atualizada com sucesso!")

def main():
    connection = create_connection()
    st.title("Sistema de Programação de Filmes")

    menu = ["Gerenciar Filmes", "Gerenciar Canais", "Gerenciar Exibições"]
    choice = st.sidebar.selectbox("Selecione uma opção:", menu)

    if choice == "Gerenciar Filmes":
        filme_crud(connection)
    elif choice == "Gerenciar Canais":
        canal_crud(connection)
    elif choice == "Gerenciar Exibições":
        exibicao_crud(connection)

if __name__ == "__main__":
    main()
