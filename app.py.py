import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os
import re

# 🖼️ Verificar se a imagem de fundo existe
image_path = "image.png"
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)

# 📂 Upload do PDF
arquivo = st.file_uploader("📚 Arraste e solte o PDF aqui", type="pdf")

if arquivo:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
        temp_input.write(arquivo.read())
        temp_input_path = temp_input.name
    
    def censurar_palavroes(arquivo_entrada, arquivo_saida):
        """Substitui palavrões no PDF por palavras mais leves e um fundo branco."""
        substituicoes = {
            "porra": "DROGA",
            "caralho": "CARAMBA",
            "foder": "CATAR",
            "fodido": "QUEBRADO",
            "fodida": "QUEBRADA",
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
                    bbox_list = pagina.search_for(ocorrencia.group())
                    for bbox in bbox_list:  # Percorre todas as ocorrências
                        pagina.draw_rect(bbox, color=(1, 1, 1), fill=(1, 1, 1))
                        x_inicial = bbox.x0
                        y_central = bbox.y1 - ((bbox.y1 - bbox.y0) * 0.25)
                        pagina.insert_text((x_inicial, y_central), substituto, fontsize=7, color=(0, 0, 0))
        
        pdf.save(arquivo_saida)
        pdf.close()
    
    # Criar arquivo temporário de saída
    temp_output_path = temp_input_path.replace(".pdf", "_censurado.pdf")
    censurar_palavroes(temp_input_path, temp_output_path)
    
    # Opções de formato de salvamento
    formato = st.selectbox("Escolha o formato para salvar o arquivo:", ["PDF", "TXT"])
    
    if formato == "PDF":
        with open(temp_output_path, "rb") as file:
            st.download_button(
                label="💾 Baixar PDF Censurado",
                data=file,
                file_name="livro_censurado.pdf",
                mime="application/pdf",
            )
    else:
        with open(temp_output_path, "rb") as file:
            doc = fitz.open(file)
            text_content = "\n".join([page.get_text("text") for page in doc])
            doc.close()
        
        st.download_button(
            label="💾 Baixar TXT Censurado",
            data=text_content,
            file_name="livro_censurado.txt",
            mime="text/plain",
        )
    
    # Remover arquivos temporários após o download
    os.remove(temp_input_path)
    os.remove(temp_output_path)

