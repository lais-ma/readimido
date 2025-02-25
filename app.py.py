def censurar_palavroes(arquivo_entrada, arquivo_saida):
    """Substitui palavrões no PDF por retângulos brancos com palavras mais leves."""
    substituicoes = {
        "porra": "DROGA",
        "caralho": "CARAMBA",
        "foder": "CATAR",
        "fodido": "FERRADO",
        "puta": "SAFADA",
        "foda": "DROGA",
        "buceta": "FUÇA"
    }

    pdf = fitz.open(arquivo_entrada)

    for pagina in pdf:
        for palavrao, substituto in substituicoes.items():
            areas = pagina.search_for(rf"\b{palavrao}\b")  # 🔥 Detecta só palavras isoladas
            for area in areas:
                pagina.draw_rect(area, color=(1, 1, 1), fill=(1, 1, 1))
                x_inicial = area.x0  # Alinha ao início do retângulo
                y_central = area.y1 - ((area.y1 - area.y0) * 0.25)  # Ajuste vertical
                pagina.insert_text((x_inicial, y_central), substituto, fontsize=6, color=(0, 0, 0))

    pdf.save(arquivo_saida)
    pdf.close()
