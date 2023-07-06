import subprocess
from pathlib import Path
from datetime import date, datetime
import locale
import tkinter as tk
from tkinter import messagebox

def create_log_file(name):
    current_time = datetime.now()
    month_current = month()
    month_current_number = current_time.month
    month_day_current = current_time.day
    date_today = date.today()
    log_file = f"C:\\Users\\Administrator\\Desktop\\Log_troca de senha\\{month_current_number:02d}_TrocaDeSenha_{month_current}\\{month_day_current:02d}_Sala{name}_{date_today}.txt"
    path = Path(f"C:\\Users\\Administrator\\Desktop\\Log_troca de senha\\{month_current_number:02d}_TrocaDeSenha_{month_current}")
    path.mkdir(parents=True, exist_ok=True)
    return log_file

def change_user_password(room, machine, name_user, new_password):
    # Comando para alterar a senha de um usuário no Windows
    if machine <= 9:
        machine_password = f"0{machine}"
    else:
        machine_password = machine

    comando = f"psexec \\\\10.10.{room}.{machine}  net user {name_user} {new_password}${room}{machine_password}"

    # Executa o comando no prompt de comando
    txt = subprocess.run(comando, stdout=subprocess.PIPE)

    return f"maquina 10.10.{room}.{machine} senha alterada com sucesso : {new_password}${room}{machine_password} " if txt.returncode == 0 else f"maquina 10.10.{room}.{machine} Senha não alterada "

def month():
    locale.setlocale(locale.LC_ALL, '')
    today = datetime.today()
    return today.strftime("%b")

def start_password_change():
    number_room = room_entry.get()
    machine_start = int(start_entry.get())
    machine_finish = int(finish_entry.get())
    user = user_var.get()
    password = password_entry.get()

    log_file = create_log_file(number_room)

    while machine_start <= machine_finish:
        pings = [change_user_password(number_room, machine_start, user, password)]
        with open(log_file, "a", encoding='utf8') as arquivo:
            for p in pings:
                arquivo.write(f'{p}\n')
        machine_start += 1

    messagebox.showinfo("Concluído", "Troca de senha concluída com sucesso.")

# Criar a janela principal
window = tk.Tk()
window.title("Troca de Senha")
window.geometry("400x300")

# Criar os rótulos e campos de entrada
room_label = tk.Label(window, text="Número da Sala:")
room_label.pack()
room_entry = tk.Entry(window)
room_entry.pack()

start_label = tk.Label(window, text="Máquina Inicial:")
start_label.pack()
start_entry = tk.Entry(window)
start_entry.pack()

finish_label = tk.Label(window, text="Máquina Final:")
finish_label.pack()
finish_entry = tk.Entry(window)
finish_entry.pack()

user_label = tk.Label(window, text="Tipo de Usuário:")
user_label.pack()
user_options = ["Loc", "Student", "Admin"]
user_var = tk.StringVar(window)
user_var.set(user_options[0])
user_dropdown = tk.OptionMenu(window, user_var, *user_options)
user_dropdown.pack()

password_label = tk.Label(window, text="Padrão de senha:")
password_label.pack()
password_entry = tk.Entry(window)
password_entry.pack()

# Criar o botão de iniciar
start_button = tk.Button(window, text="Iniciar", command=start_password_change)
start_button.pack()

# Iniciar o loop principal da interface gráfica
window.mainloop()
