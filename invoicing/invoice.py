import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path
import os

def generate(excel_path, pdf_path, image_path, id_column, name_column, qty_column, unit_price_column, total_price_column):
    """
    This program converts an excel invoice into a pdf invoice
    :param excel_path:
    :param pdf_path:
    :param image_path:
    :param id_column:
    :param name_column:
    :param qty_column:
    :param unit_price_column:
    :param total_price_column:
    :return:
    """
    filepaths = glob.glob(f"{excel_path}/*.xlsx")

    for filepath in filepaths:

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        filename = Path(filepath).stem
        invoice_nr, date = filename.split("-")

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        # Add a header
        columns = df.columns
        columns = [item.replace("_", " ").title() for item in columns]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns[0], border=1)
        pdf.cell(w=70, h=8, txt=columns[1], border=1)
        pdf.cell(w=30, h=8, txt=columns[2], border=1)
        pdf.cell(w=30, h=8, txt=columns[3], border=1)
        pdf.cell(w=30, h=8, txt=columns[4], border=1, ln=1)

        # Add rows to the table
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[id_column]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[name_column]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[qty_column]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[unit_price_column]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price_column]), border=1, ln=1)

        total_sum = df[total_price_column].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=70, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

        # Add total sum sentence
        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)

        # Add company name and logo
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=25, h=8, txt=f"PythonHow")
        pdf.image(image_path, w=10)

        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)

        pdf.output(f"{pdf_path}.pdf")
