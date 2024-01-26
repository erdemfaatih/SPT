import json

import pdfplumber
import pandas as pd

def extract_and_clean_tables(pdf_path):
    all_cleaned_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()

            for table in tables:
                sondaj_no_values = [None]  # Sondaj No değerlerini tutacak liste, başlangıçta None ekledik
                cleaned_table = []  # Düzgünleştirilmiş tabloyu oluşturacak liste
                is_header = True

                for row in table:
                    # Başlık satırlarını atla
                    if is_header:
                        is_header = False
                        continue

                    sondaj_no_value = row[0] if row and row[0] is not None else sondaj_no_values[-1]
                    sondaj_no_values.append(sondaj_no_value)

                    # Her bir satır için düzgünleştirilmiş tabloya ekle
                    cleaned_row = [sondaj_no_value, row[2] if row and len(row) > 2 else None,
                                   row[-2] if row and len(row) > 0 else None]

                    cleaned_table.append(cleaned_row)

                cleaned_table.pop(0)
                # Düzgünleştirilmiş tabloyu pandas DataFrame'e çevir
                df = pd.DataFrame(cleaned_table, columns=["Sondaj No", "Derinlik (m)", "Formasyon/Litoloji"])
                # DataFrame'i görüntüle veya başka bir işlem yap
                print(f"Table on Page {page_number}:\n{df}\n")

                # Düzgünleştirilmiş tabloyu listeye ekle
                all_cleaned_tables.append(df)

    return all_cleaned_tables

# Örnek olarak PDF dosyasının yolu
pdf_path = "C:\\Users\\Fatih\\Desktop\\SPT\\input.pdf"

extracted_tables = extract_and_clean_tables(pdf_path)

json_output_path = "C:\\Users\\Fatih\\Desktop\\SPT\\output.json"
json_data = []

for idx, table_df in enumerate(extracted_tables, start=1):
    json_data.append({
        f"Page_{idx}": table_df.to_dict(orient='records')
    })

with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, indent=2, ensure_ascii=False)
