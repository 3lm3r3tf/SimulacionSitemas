import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Parámetros del generador congruencial lineal (Unix-like)
a = 1103515245
c = 12345
m = 2**31

# Semilla inicial
x0 = 111

# Generar números aleatorios y calcular período
n = 1000
numeros = []
x = x0
periodo = 0
seen = set()
for i in range(n):
    x = (a * x + c) % m
    numeros.append(x)
    if x in seen and periodo == 0:
        periodo = i  # El primer momento en que se repite un número
    seen.add(x)

# Si no se encontró repetición en n pasos, aproximamos el período
if periodo == 0:
    periodo = "Mayor a " + str(n)

# Guardar en DataFrame (opcional)
df = pd.DataFrame(numeros, columns=["Numeros Aleatorios"])
print(df)

# Crear PDF
ruta = r"C:\Users\elmer\Desktop\Simulacion De Sistema\P01"
pdf_file = f"{ruta}\\numeros_aleatorios.pdf"

doc = SimpleDocTemplate(pdf_file, pagesize=A4)
styles = getSampleStyleSheet()
elements = []

# Título
elements.append(Paragraph("Generador de Números Aleatorios (Unix)", styles['Title']))
elements.append(Spacer(1, 12))

# Descripción
descripcion = f"Semilla inicial (x0): {x0} <br/>Total números generados: {n} <br/>Periodo estimado: {periodo}"
elements.append(Paragraph(descripcion, styles['Normal']))
elements.append(Spacer(1, 12))

# Código fuente
codigo = """
import pandas as pd
# Parámetros del generador
a = 1103515245
c = 12345
m = 2**31
x0 = 111
n = 1000
numeros = []
x = x0
for _ in range(n):
    x = (a * x + c) % m
    numeros.append(x)
"""
monospace_style = ParagraphStyle(
    name="Monospace",
    fontName="Courier",
    fontSize=8,
    leading=10
)
elements.append(Paragraph("Código fuente utilizado:", styles['Heading2']))
elements.append(Spacer(1, 6))
elements.append(Paragraph(codigo.replace(" ", "&nbsp;").replace("\n", "<br/>"), monospace_style))
elements.append(Spacer(1, 12))

# Preparar tabla
data = [["Índice", "Número Aleatorio"]]
for i, num in enumerate(numeros, start=1):
    data.append([i, num])

table = Table(data, colWidths=[80, 300])
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.gray),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
]))
elements.append(table)

# Construir PDF
doc.build(elements)

print(f"PDF generado: {pdf_file}")
