from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fpdf import FPDF
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Configurações fixas do certificado
MODELO_CERTIFICADO = os.path.join(BASE_DIR, "modelo_certificado.png")
FONTE_PATH = os.path.join(BASE_DIR, "Montserrat-VariableFont_wght.ttf")
FONTE_TAMANHO = 48
POSICAO_X = 642
POSICAO_Y = 720

@app.post("/gerar-certificado")
def gerar_certificado(dados: dict):
    nome = dados.get("nome")
    if not nome:
        raise HTTPException(status_code=400, detail="Nome não fornecido")

    certificado = Image.open(MODELO_CERTIFICADO).convert("RGB")
    draw = ImageDraw.Draw(certificado)
    fonte = ImageFont.truetype(FONTE_PATH, FONTE_TAMANHO)
    draw.text((POSICAO_X, POSICAO_Y), nome, font=fonte, fill="black")

    pdf_bytes = BytesIO()
    pdf = FPDF(unit="pt", format=[certificado.size[0], certificado.size[1]])
    pdf.add_page()

    temp_img_path = os.path.join(BASE_DIR, "temp_certificado.png")
    certificado.save(temp_img_path, format="PNG")
    
    pdf.image(temp_img_path, x=0, y=0, w=certificado.size[0], h=certificado.size[1])
    pdf_output = pdf.output(dest='S').encode('latin1')  # <-- Corrige o erro

    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)

    return Response(content=pdf_output, media_type="application/pdf")

