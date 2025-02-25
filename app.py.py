import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os
import re

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
            "foder": "CATAR",
            "fodido": "QUEBRADO",
            "puta merda": "DROGA",
            "puta que pariu": "CARAMBA",
            r"\bputa\b": "DOIDA",
            "filho da puta": "IDIOTA",
            "filha da puta": "IDIOTA",
            "foda": "DROGA",
            "buceta": "FUÇA",
            r"\bputo\b": "IRADO"
        }
        pdf = fitz.open(arquivo_entrada)

        for pagina in pdf:
            texto = pagina.get_text("text")
            for padrao, substituto in substituicoes.items():
                ocorrencias = [m for m in re.finditer(padrao, texto, re.IGNORECASE)]
                for ocorrencia in ocorrencias:
                    bbox = pagina.search_for(ocorrencia.group())[0]  # Pega a primeira ocorrência encontrada
                    pagina.draw_rect(bbox, color=(1, 1, 1), fill=(1, 1, 1))
                    x_inicial = bbox.x0  # Alinha ao início do retângulo
                    y_central = bbox.y1 - ((bbox.y1 - bbox.y0) * 0.25)  # Ajuste vertical
                    pagina.insert_text((x_inicial, y_central), substituto, fontsize=7, color=(0, 0, 0))

        pdf.save(arquivo_saida)
        pdf.close()

    # Criar arquivo temporário de saída
    temp_output_path = temp_input_path.replace(".pdf", "_censurado.pdf")
    temp_reviewed_path = temp_input_path.replace(".pdf", "_revisado.pdf")
    
    # Rodar o código duas vezes para garantir a censura completa
    censurar_palavroes(temp_input_path, temp_output_path)
    censurar_palavroes(temp_output_path, temp_reviewed_path)

    # Opções de formato de salvamento
    formato = st.selectbox("Escolha o formato para salvar o arquivo:", ["PDF", "TXT"])

    if formato == "PDF":
        with open(temp_reviewed_path, "rb") as file:
            st.download_button(
                label="💾 Baixar PDF Censurado",
                data=file,
                file_name="livro_censurado.pdf",
                mime="application/pdf",
            )
    else:
        with open(temp_reviewed_path, "rb") as file:
            text_content = fitz.open(file).get_text("text")
            st.download_button(
                label="💾 Baixar TXT Censurado",
                data=text_content,
                file_name="livro_censurado.txt",
                mime="text/plain",
            )
    
    # Remover arquivos temporários
    os.remove(temp_input_path)
    os.remove(temp_output_path)
    os.remove(temp_reviewed_path)

