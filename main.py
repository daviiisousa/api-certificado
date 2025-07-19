from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fpdf import FPDF
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Configurações fixas do certificadopip install uvicorn
MODELO_CERTIFICADO = os.path.join(BASE_DIR, "modelo_certificado.png")  # Imagem sem nome
FONTE_PATH = os.path.join(BASE_DIR, "Montserrat-VariableFont_wght.ttf")  # substitua pela fonte TT Norms se possuir
FONTE_TAMANHO = 48
POSICAO_X = 642  # Posição exata aprovada por você (último ajuste)
POSICAO_Y = 720

@app.post("/gerar-certificado")
def gerar_certificado(dados: dict):
    nome = dados.get("nome")
    if not nome:
        raise HTTPException(status_code=400, detail="Nome não fornecido")

    # Carregar imagem base
    certificado = Image.open(MODELO_CERTIFICADO).convert("RGB")

    # Inserir nome
    draw = ImageDraw.Draw(certificado)
    fonte = ImageFont.truetype(FONTE_PATH, FONTE_TAMANHO)
    draw.text((POSICAO_X, POSICAO_Y), nome, font=fonte, fill="black")

    # Converter imagem para PDF
    pdf_bytes = BytesIO()
    pdf = FPDF(unit="pt", format=[certificado.size[0], certificado.size[1]])
    pdf.add_page()

    img_temp = BytesIO()
    certificado.save(img_temp, format="PNG")
    img_temp.seek(0)

    pdf.image(img_temp, x=0, y=0, w=certificado.size[0], h=certificado.size[1])
    pdf.output(pdf_bytes)

    pdf_bytes.seek(0)

    # Retornar PDF diretamente
    return Response(content=pdf_bytes.getvalue(), media_type="application/pdf")
