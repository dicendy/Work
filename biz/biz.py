import re
import tkinter as tk
from tkinter import messagebox


def parse_gta5rp_events(text):
    blocks = re.split(r'Дата ', text)[1:]
    parsed_data = []
    
    date_header = None
    table_rows = []
    
    for block in blocks:
        date_match = re.search(r'и время:\s*\n(\d{2}\.\d{2}\.\d{4}), (\d{2}:\d{2}:\d{2})', block)
        number_match = re.search(r'Номер забива:\s*\n(\d{4}-\d+-\d+-\d+)', block)
        business_match = re.search(r'Бизнес:\s*\n(.+)', block)
        players_match = re.search(r'Участники:\s*\n(\d+x\d+)', block)
        attack_match = re.search(r'⚔️Атака:\s*\n(.+)', block)
        defense_match = re.search(r'🛡️Защита:\s*\n(.+)', block)
        result_match = re.search(r'Результат:\s*\n(.+)', block)
        
        date = date_match.group(1) if date_match else '—'
        time = date_match.group(2) if date_match else '—'
        number = number_match.group(1) if number_match else '—'
        business = business_match.group(1) if business_match else '—'
        players = players_match.group(1) if players_match else '—'
        attack = attack_match.group(1) if attack_match else '—'
        defense = defense_match.group(1) if defense_match else '—'
        result = result_match.group(1).replace("Победа ", "") if result_match else 'Отменен'
        
        if not date_header:
            date_header = date
        
        table_rows.append(f"{time},{number},{business},{players},{attack},{defense},{result}")
    
    parsed_data.append(date_header)
    parsed_data.extend(table_rows)
    
    return '\n'.join(parsed_data)


def insert_text():
    input_text.delete("1.0", tk.END)
    input_text.insert(tk.END, root.clipboard_get())


def format_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Ошибка", "Введите текст для форматирования")
        return
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, parse_gta5rp_events(text))


def copy_text():
    root.clipboard_clear()
    root.clipboard_append(output_text.get("1.0", tk.END))
    root.update()
    messagebox.showinfo("Готово", "Текст скопирован в буфер обмена")


root = tk.Tk()
root.title("GTA5RP Events")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

input_text = tk.Text(frame, height=10, width=60)
input_text.pack()

btn_insert = tk.Button(frame, text="Вставить", command=insert_text)
btn_insert.pack(side=tk.LEFT, padx=5, pady=5)

btn_format = tk.Button(frame, text="Форматировать", command=format_text)
btn_format.pack(side=tk.LEFT, padx=5, pady=5)

btn_copy = tk.Button(frame, text="Копировать", command=copy_text)
btn_copy.pack(side=tk.LEFT, padx=5, pady=5)

output_text = tk.Text(frame, height=10, width=60, state=tk.NORMAL)
output_text.pack()

root.mainloop()
