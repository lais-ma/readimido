import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os

# 📌 Caminho da imagem enviada
image_path = "image.png"

# 📌 Estilo CSS para sobrepor a área de upload na imagem
st.markdown(
    f"""
    <style>
    .container {{
        position: relative;
        width: 100%;
        text-align: center;
    }}
    .background-img {{
        width: 100%;
        height: auto;
    }}
    .upload-box {{
        position: absolute;
        bottom: 10%;
        right: 10%;
        background: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 📌 Criar container com imagem + upload sobreposto
st.markdown('<div class="container">', unsafe_allow_html=True)
st.image(image_path, use_container_width=True)
st.markdown('<div class="upload-box">', unsafe_allow_html=True)
arquivo = st.file_uploader("Arraste e solte o PDF aqui", type="pdf")
st.markdown('</div></div>', unsafe_allow_html=True)

# 📌 Processamento do PDF
if arquivo:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
        temp_input.write(arquivo.read())
        temp_input_path = temp_input.name  

    def censurar_palavroes(arquivo_entrada, arquivo_saida):
        """Substitui palavrões no PDF por retângulos brancos com palavras mais leves."""
        substituicoes = {
            "porra": "DROGA",
            "caralho": "CARAMBA",
            "foder": "DANE-SE",
            "fodido": "FERRADO",
            "puta": "QUENGA",
            "foda": "DROGA"
        }
        pdf = fitz.open(arquivo_entrada)

        for pagina in pdf:
            for palavrao, substituto in substituicoes.items():
                areas = pagina.search_for(palavrao)
                for area in areas:
                    pagina.draw_rect(area, color=(1, 1, 1), fill=(1, 1, 1))
                    pagina.insert_text((area.x0, area.y0), substituto, fontsize=10, color=(0, 0, 0))

        pdf.save(arquivo_saida)
        pdf.close()

    # Criar arquivo temporário de saída
    temp_output_path = temp_input_path.replace(".pdf", "_censurado.pdf")
    censurar_palavroes(temp_input_path, temp_output_path)

    # Permitir que o usuário escolha o nome do arquivo
    nome_arquivo = st.text_input("Escolha o nome do arquivo para salvar:", "livro_censurado.pdf")

    # Criar botão para download do PDF processado
    with open(temp_output_path, "rb") as file:
        st.download_button(
            label="📥 Baixar PDF Censurado",
            data=file,
            file_name=nome_arquivo,
            mime="application/pdf",
        )

    # Remover arquivos temporários
    os.remove(temp_input_path)
    os.remove(temp_output_path)
