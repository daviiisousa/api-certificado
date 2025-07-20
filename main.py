import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fpdf import FPDF
import os

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)
MODELO_CERTIFICADO = os.path.join(BASE_DIR, "modelo_certificado.png")
FONTE_PATH       = os.path.join(BASE_DIR, "Montserrat-Bold.ttf")
FONTE_TAMANHO    = 48
POSICAO_X        = 500
POSICAO_Y        = 720

@app.post("/gerar-certificado")
def gerar_certificado(dados: dict):
    nome = dados.get("nome")
    if not nome:
        raise HTTPException(status_code=400, detail="Nome não fornecido")

    # Abre template e desenha texto
    certificado = Image.open(MODELO_CERTIFICADO).convert("RGB")
    draw = ImageDraw.Draw(certificado)
    fonte = ImageFont.truetype(FONTE_PATH, FONTE_TAMANHO)
    draw.text((POSICAO_X, POSICAO_Y), nome, font=fonte, fill="black")

    # Cria PDF
    pdf = FPDF(unit="pt", format=[*certificado.size])
    pdf.add_page()

    # Usa um arquivo temporário em /tmp (sempre gravável)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        certificado.save(tmp.name, format="PNG")
        tmp_path = tmp.name

    pdf.image(tmp_path, x=0, y=0, w=certificado.size[0], h=certificado.size[1])

    # Gera bytes do PDF
    pdf_output = pdf.output(dest='S').encode('latin1')

    # Limpa o arquivo temporário
    os.remove(tmp_path)
    
    headers = {
        "Content-Disposition": f"attachment; filename=certificado-{nome.replace(' ', '_')}.pdf"
    }

    return Response(content=pdf_output, media_type="application/pdf", headers=headers)
