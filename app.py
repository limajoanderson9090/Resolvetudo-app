import streamlit as st
import random

# --- As classes e funções do nosso projeto (versão final) ---
class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.reputacao = 0
    def adicionar_reputacao(self, pontos):
        self.reputacao += pontos

class Problema:
    def __init__(self, titulo, autor: Usuario, categoria):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.solucoes = []

class Solucao:
    def __init__(self, texto, autor: Usuario):
        self.texto = texto
        self.autor = autor
        self.corretas = 0
        self.erradas = 0
    def marcar_como_correta(self):
        self.corretas += 1
    def marcar_como_errada(self):
        self.erradas += 1
    @property
    def nota_final(self):
        return self.corretas - self.erradas

def encontrar_melhor_solucao(lista_solucoes):
    if not lista_solucoes:
        return None
    solucoes_ordenadas = sorted(lista_solucoes, key=lambda solucao: solucao.nota_final, reverse=True)
    return solucoes_ordenadas[0]

def votar_em_solucoes(lista_solucoes):
    for solucao in lista_solucoes:
        if solucao.corretas + solucao.erradas == 0:
            votos_corretos = random.randint(1, 20)
            votos_errados = random.randint(0, 5)
            for _ in range(votos_corretos): solucao.marcar_como_correta()
            for _ in range(votos_errados): solucao.marcar_como_errada()

# --- Nossas bases de dados (com as novas categorias) ---
usuarios_existentes = {
    "Carlos": Usuario("Carlos"),
    "Ana": Usuario("Ana"),
    "Pedro": Usuario("Pedro")
}

base_de_dados_comunidade = {
    "Tecnologia": {
        "impressora não funciona": [
            Solucao(texto="Tente reverter o driver.", autor=usuarios_existentes["Carlos"]),
            Solucao(texto="Verifique o cabo USB.", autor=usuarios_existentes["Ana"])
        ],
        "computador lento": [
            Solucao(texto="Reinicie o computador.", autor=usuarios_existentes["Pedro"])
        ]
    }
}
# Simulação de votos iniciais
for categoria in base_de_dados_comunidade:
    for problema in base_de_dados_comunidade[categoria]:
        votar_em_solucoes(base_de_dados_comunidade[categoria][problema])

solucoes_do_google = {
    "celular superaquecendo": "Feche apps e remova a capa."
}

# --- O aplicativo final com Streamlit ---
st.title("ResolvaTudo")
st.write("Sua plataforma de soluções, movida pela comunidade.")

with st.form("buscar_solucao_form"):
    st.subheader("Digite seu problema:")
    autor_usuario = st.text_input("Seu nome:")
    categoria_selecionada = st.selectbox("Selecione a categoria:", ["Tecnologia", "Culinária", "Reparos"])
    pergunta_usuario = st.text_input("Qual é o seu problema?").lower()
    
    submitted = st.form_submit_button("Buscar Solução")
    
    if submitted:
        if pergunta_usuario in base_de_dados_comunidade.get(categoria_selecionada, {}):
            st.success("Problema encontrado na comunidade!")
            solucoes_do_problema = base_de_dados_comunidade[categoria_selecionada][pergunta_usuario]
            melhor_solucao = encontrar_melhor_solucao(solucoes_do_problema)
            
            st.subheader("A melhor solução é:")
            st.write(f"**Autor:** {melhor_solucao.autor.nome}")
            st.write(f"**Solução:** {melhor_solucao.texto}")
            st.write(f"**Pontuação:** {melhor_solucao.nota_final} ({melhor_solucao.corretas} corretas, {melhor_solucao.erradas} erradas)")
        
        elif pergunta_usuario in solucoes_do_google:
            st.warning("Problema novo! Buscando uma solução rápida...")
            solucao_encontrada = solucoes_do_google[pergunta_usuario]
            st.info(f"**Solução do Google:** {solucao_encontrada}")
        
        else:
            st.error("Desculpe, não encontramos uma solução ainda. Seja o primeiro a ajudar!")
