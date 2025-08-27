import random
import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# Carpeta donde se guardarán los archivos
ruta = r"C:\Users\elmer\Desktop\Simulacion De Sistema\P02"

# Función principal de simulación Martingala simple
def simular():
    try:
        saldo = int(entry_saldo.get())
        apuesta_inicial = int(entry_monto.get())
        eleccion = combo_apuesta.get()

        datos = []
        apuesta_actual = apuesta_inicial
        nro = 0
        ganador = False

        while saldo >= apuesta_actual and not ganador:
            nro += 1
            dado1 = random.randint(1, 6)
            dado2 = random.randint(1, 6)
            suma = dado1 + dado2

            if suma == 7:
                resultado = "pierde"
                saldo -= apuesta_actual
                apuesta_actual = min(apuesta_actual*2, saldo)  # duplicar apuesta, máximo lo que queda
            elif (eleccion=="Menor" and suma <=6) or (eleccion=="Mayor" and suma >=8):
                resultado = "gana"
                saldo += apuesta_actual
                ganador = True
            else:
                resultado = "pierde"
                saldo -= apuesta_actual
                apuesta_actual = min(apuesta_actual*2, saldo)  # duplicar apuesta, máximo lo que queda

            datos.append([nro,dado1,dado2,suma,resultado,apuesta_actual,saldo])

        # Guardar Excel
        df = pd.DataFrame(datos, columns=["nro","dado1","dado2","suma","resultado","apuesta","saldo"])
        df.to_excel(f"{ruta}\\simulacion_martingala.xlsx", index=False)

        # Generar PDF
        pdf_file = f"{ruta}\\simulacion_martingala.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Simulación Juego Mayor y Menor - Estrategia Martingala", styles['Title']))
        elements.append(Spacer(1,12))
        descripcion = (
            f"Saldo inicial: {entry_saldo.get()} <br/>"
            f"Apuesta inicial: {apuesta_inicial} <br/>"
            f"Estrategia: apostar '{eleccion}' y duplicar la apuesta si se pierde, retirarse si se gana."
        )
        elements.append(Paragraph(descripcion, styles['Normal']))
        elements.append(Spacer(1,12))

        # Tabla de resultados
        data = [["nro","dado1","dado2","suma","resultado","apuesta","saldo"]] + datos
        table = Table(data, colWidths=[40,40,40,40,60,60,50])
        table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.gray),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold')
        ]))
        elements.append(table)
        elements.append(Spacer(1,12))

        # Propuesta / análisis
        analisis = (
            "Propuesta de estrategia:\n"
            "- La estrategia Martingala permite recuperar pérdidas apostando el doble tras cada pérdida.\n"
            "- Riesgo: si se encadenan varias pérdidas, se puede agotar rápidamente el saldo.\n"
            "- Recomendación: apostar montos pequeños y retirarse inmediatamente al ganar.\n"
            "- Esta simulación muestra cómo funciona la estrategia y los riesgos asociados."
        )
        elements.append(Paragraph("Análisis y Propuesta", styles['Heading2']))
        elements.append(Paragraph(analisis.replace("\n","<br/>"), styles['Normal']))

        doc.build(elements)
        messagebox.showinfo("Éxito", f"Simulación completa.\nPDF y Excel generados en:\n{ruta}")

    except ValueError:
        messagebox.showerror("Error","Por favor, ingrese valores válidos.")

# ---------------- GUI ----------------
root = Tk()
root.title("Juego Mayor y Menor - Martingala Simple")

Label(root, text="Saldo inicial:").grid(row=0,column=0,padx=5,pady=5,sticky=E)
Label(root, text="Apuesta inicial:").grid(row=1,column=0,padx=5,pady=5,sticky=E)
Label(root, text="Apuesta:").grid(row=2,column=0,padx=5,pady=5,sticky=E)

entry_saldo = Entry(root); entry_saldo.grid(row=0,column=1,padx=5,pady=5)
entry_monto = Entry(root); entry_monto.grid(row=1,column=1,padx=5,pady=5)

combo_apuesta = ttk.Combobox(root, values=["Mayor","Menor"])
combo_apuesta.grid(row=2,column=1,padx=5,pady=5)
combo_apuesta.current(0)

Button(root,text="Simular y Generar PDF/Excel",command=simular).grid(row=3,column=0,columnspan=2,pady=10)

root.mainloop()
