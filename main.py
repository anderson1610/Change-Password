import subprocess
from pathlib import Path
from datetime import date, datetime
import locale
import tkinter as tk
from tkinter import messagebox
import shutil
import os

def verify_psexec():

    specific_folder = 'C:/Windows/System32'  # Substitua pelo caminho da pasta específica que deseja verificar
    file_name = 'PsExec.exe'      # Substitua pelo nome do arquivo que deseja verificar
    file_path = os.path.join(specific_folder, file_name)
    path_destination = 'C:/Windows/System32/PsExec.exe'
    path_psexec = 'C:/Users/Administrator/Downloads/PsExec.exe'


    if os.path.exists(file_path):
        subprocess.run(path_destination)
        print(f"O arquivo {file_name} existe na pasta {specific_folder}.")
        os.system("cls")

        return True
    else:
        if os.path.exists(path_psexec):
            print("Arquivo PsExec encontrado")
            # Caminho do arquivo .exe original
            original_path = 'C:/Users/Administrator/Downloads/PsExec.exe'

            # Copiar o arquivo .exe para o destino desejado
            shutil.copy(original_path, path_destination)

            # Executar o arquivo .exe
            subprocess.run(path_destination)  

            return True         
        
        else:
            messagebox.showinfo("ERRO!", "Coloque o arquivo PsExec.exe na pasta Downloads para realizarmos a instalação")
            return False
        

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
    print("----------------------------------------------------------------")
    print(f"--Conectando na maquina {machine} Sala: {room}--")
    # user_password para alterar a senha de um usuário no Windows
    if machine <= 9:
        machine_password = f"0{machine}"
    else:
        machine_password = machine

    user_password = f"psexec \\\\10.10.{room}.{machine}  net user {name_user} {new_password}${room}{machine_password}"
    group_rdp = f'psexec \\\\10.10.{room}.{machine}  net localgroup "Remote Desktop Users" {name_user} /add '

    # Executa o user_password no prompt de user_password
    txt = subprocess.run(user_password, stdout=subprocess.PIPE)
    print(f"Adicionando {name_user} ao grupo RDP... ")
    txt2 = subprocess.run(group_rdp, stdout=subprocess.PIPE)

    if txt2 == 0:
        print("Usuario Adicionado")
    else:
        print("\n")
        print("Usuario ja pertence ao grupo")

    stdout = txt.stdout

    return f"maquina 10.10.{room}.{machine} senha alterada com sucesso | USUARIO: {name_user} SENHA: {new_password}${room}{machine_password} " if txt.returncode == 0 else f"maquina 10.10.{room}.{machine} Senha não alterada "

def month():
    locale.setlocale(locale.LC_ALL, '')
    today = datetime.today()
    return today.strftime("%b")

def start_password_change():
    rooms = [21, 22, 23, 31, 32, 33, 41, 42, 43, 51, 52, 53, 61, 62, 63] #Lista de salas da empresa

    if int(room_entry.get()) in rooms:
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

    else:
        messagebox.showinfo("Erro", "Sala não encontrada")


if verify_psexec() == True:


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

    assinatura_label = tk.Label(window, text="Desenvolvido por: Anderson Camargo", fg="gray")
    assinatura_label.pack(side=tk.BOTTOM, padx=5, pady=5)
    # Iniciar o loop principal da interface gráfica
    window.mainloop()

else:
    print("Verifique se possui o instalador do PsExec esta na pasta Downloads")

#desenvolvido por Anderson Camargo
