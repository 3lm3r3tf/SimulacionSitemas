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

# Función principal de simulación
def simular():
    try:
        saldo_inicial = int(entry_saldo.get())
        monto_apuesta = int(entry_monto.get())
        n_jugadas = int(entry_intentos.get())
        apuesta = combo_apuesta.get()

        datos = []
        saldo = saldo_inicial

        for nro in range(1, n_jugadas + 1):
            dado1 = random.randint(1, 6)
            dado2 = random.randint(1, 6)
            suma = dado1 + dado2

            if suma == 7:
                resultado = "pierde"
                saldo -= monto_apuesta
            elif (apuesta == "Menor" and suma <= 6) or (apuesta == "Mayor" and suma >= 8):
                resultado = "gana"
                saldo += monto_apuesta
            else:
                resultado = "pierde"
                saldo -= monto_apuesta

            datos.append([nro, dado1, dado2, suma, resultado, apuesta, monto_apuesta, saldo])

        # Guardar Excel
        df = pd.DataFrame(datos, columns=["nro", "dado1", "dado2", "suma", "resultado", "apuesta", "monto", "saldo"])
        df.to_excel(f"{ruta}\\simulacion_mayor_menor.xlsx", index=False)

        # Generar PDF
        pdf_file = f"{ruta}\\simulacion_mayor_menor.pdf"
        doc = SimpleDocTemplate(pdf_file, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Simulación Juego Mayor y Menor", styles['Title']))
        elements.append(Spacer(1, 12))

        descripcion = (
            f"Saldo inicial: {saldo_inicial} <br/>"
            f"Monto por jugada: {monto_apuesta} <br/>"
            f"Número de jugadas: {n_jugadas} <br/>"
            f"Estrategia: apostar siempre '{apuesta}'"
        )
        elements.append(Paragraph(descripcion, styles['Normal']))
        elements.append(Spacer(1, 12))

        data = [["nro", "dado1", "dado2", "suma", "resultado", "apuesta", "monto", "saldo"]] + datos
        table = Table(data, colWidths=[40,40,40,40,60,60,40,50])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.gray),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
        ]))
        elements.append(table)
        doc.build(elements)

        messagebox.showinfo("Éxito", f"Simulación completa.\nPDF y Excel generados en:\n{ruta}")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

# ---------------- GUI con Tkinter ----------------
root = Tk()
root.title("Juego Mayor y Menor - Simulación")

Label(root, text="Saldo inicial:").grid(row=0, column=0, padx=5, pady=5, sticky=E)
Label(root, text="Monto por jugada:").grid(row=1, column=0, padx=5, pady=5, sticky=E)
Label(root, text="Cantidad de intentos:").grid(row=2, column=0, padx=5, pady=5, sticky=E)
Label(root, text="Apuesta:").grid(row=3, column=0, padx=5, pady=5, sticky=E)

entry_saldo = Entry(root)
entry_saldo.grid(row=0, column=1, padx=5, pady=5)
entry_monto = Entry(root)
entry_monto.grid(row=1, column=1, padx=5, pady=5)
entry_intentos = Entry(root)
entry_intentos.grid(row=2, column=1, padx=5, pady=5)

combo_apuesta = ttk.Combobox(root, values=["Mayor","Menor"])
combo_apuesta.grid(row=3, column=1, padx=5, pady=5)
combo_apuesta.current(0)

Button(root, text="Simular y Generar PDF/Excel", command=simular).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
