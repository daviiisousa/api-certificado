import os
import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fpdf import FPDF

app = FastAPI()
BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
MODELO_FRENTE  = os.path.join(BASE_DIR, "modelo_certificado_IA_frente.jpg")
MODELO_VERSO   = os.path.join(BASE_DIR, "modelo_certificado_verso.png")
FONTE_PATH     = os.path.join(BASE_DIR, "Montserrat-Bold.ttf")
FONTE_TAMANHO  = 48
FONTE_TAMANHO_SERIE  = 25
POS_FRENTE     = (980, 580)
POS_VERSO_NSER = (840, 1175)

# arquivo onde guardamos o último serial
COUNTER_FILE = os.path.join(BASE_DIR, "counter.txt")

def get_next_serial() -> str:
    # inicializa em 0 se ainda não existir
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
    # lê, incrementa e grava de volta
    with open(COUNTER_FILE, "r+") as f:
        last = int(f.read().strip() or "0")
        nxt  = last + 1
        f.seek(0)
        f.write(str(nxt))
        f.truncate()
    # formata com 11 dígitos, preenchendo com zeros
    return f"{nxt:011d}"

@app.post("/gerar-certificado")
def gerar_certificado(dados: dict):
    nome = dados.get("nome")
    if not nome:
        raise HTTPException(400, "Nome não fornecido")

    # obtém o serial incremental
    serial = get_next_serial()

    # === Monta a frente ===
    img_f = Image.open(MODELO_FRENTE).convert("RGB")
    draw = ImageDraw.Draw(img_f)
    fonte = ImageFont.truetype(FONTE_PATH, FONTE_TAMANHO)

    bbox = draw.textbbox((0, 0), nome, font=fonte)
    text_width = bbox[2] - bbox[0]

    x_base, y_base = POS_FRENTE
    x_adjusted = x_base - text_width // 2
    draw.text((x_adjusted, y_base), nome, font=fonte, fill="black")

    # cria PDF e coloca a frente
    pdf = FPDF(unit="pt", format=[*img_f.size])
    pdf.add_page()
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpf:
        img_f.save(tmpf.name, "PNG")
        pdf.image(tmpf.name, 0, 0, *img_f.size)
    os.remove(tmpf.name)

    # === Monta o verso com o nº de série ===
    # img_v = Image.open(MODELO_VERSO).convert("RGB")
    # draw = ImageDraw.Draw(img_v)
    # fonte_v = ImageFont.truetype(FONTE_PATH, int(FONTE_TAMANHO_SERIE * 0.8))
    # draw.text(POS_VERSO_NSER,
    #           f"{serial}",
    #           font=fonte_v,
    #           fill="black")

    # pdf.add_page()
    # with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpv:
    #     img_v.save(tmpv.name, "PNG")
    #     pdf.image(tmpv.name, 0, 0, *img_v.size)
    # os.remove(tmpv.name)

    # gera bytes e retorna com nome usando o serial
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    headers = {
        "Content-Disposition":
           f"attachment; filename=certificado-{nome}.pdf"
    }
    return Response(content=pdf_bytes,
                    media_type="application/pdf",
                    headers=headers)
