import subprocess
from pathlib import Path
from datetime import date, datetime
import locale
import tkinter as tk
from tkinter import messagebox
import shutil
import os
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

# Credenciais do login
email_username = ''
email_password = ''
email_client = '' #e-mail que receberá o arquivo

def get_username():
    return getpass.getuser()


def verify_psexec():

    name_user = get_username()

    specific_folder = 'C:/Windows/System32'  # Substitua pelo caminho da pasta específica que deseja verificar
    file_name = 'PsExec.exe'      # Substitua pelo nome do arquivo que deseja verificar
    file_path = os.path.join(specific_folder, file_name)
    path_destination = 'C:/Windows/System32/PsExec.exe'
    path_psexec = f'C:/Users/{name_user}/Downloads/PsExec.exe'


    if os.path.exists(file_path):
        subprocess.run(path_destination)
        print(f"O arquivo {file_name} existe na pasta {specific_folder}.")
        os.system("cls")

        return True
    else:
        if os.path.exists(path_psexec):
            print("Arquivo PsExec encontrado")
            # Caminho do arquivo .exe original
            original_path = f'C:/Users/{name_user}/Downloads/PsExec.exe'

            # Copiar o arquivo .exe para o destino desejado
            shutil.copy(original_path, path_destination)

            # Executar o arquivo .exe
            subprocess.run(path_destination)  

            return True         
        
        else:
            messagebox.showinfo("ERRO!", "Coloque o arquivo PsExec.exe na pasta Downloads para realizarmos a instalação")
            return False
        

def create_log_file(name):
    name_user = get_username()
    current_time = datetime.now()
    month_current = month()
    month_current_number = current_time.month
    month_day_current = current_time.day
    date_today = date.today()
    log_file = f"C:\\Users\\{name_user}\\Desktop\\LOG troca de senha\\{month_current_number:02d}.TrocaDeSenha.{month_current}\\{date_today}.SALA{name}.txt"
    path = Path(f"C:\\Users\\{name_user}\\Desktop\\LOG troca de senha\\{month_current_number:02d}.TrocaDeSenha.{month_current}")
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

    return f"-maquina 10.10.{room}.{machine} senha alterada com sucesso | USUARIO: {name_user} SENHA: {new_password}${room}{machine_password} " if txt.returncode == 0 else f"-maquina 10.10.{room}.{machine} Senha não alterada "

def month():
    locale.setlocale(locale.LC_ALL, '')
    today = datetime.today()
    return today.strftime("%b")

def start_password_change():
    rooms = [21, 22, 23, 31, 32, 33, 41, 42, 43, 51, 52, 53, 61, 62, 63] #Lista de salas da empresa

    if int(room_entry.get()) in rooms:
        number_room = room_entry.get()

        machine_start2 = int(start_entry.get())
        machineSTR = str(machine_start2)
       
        if machineSTR[0]=='0':
            machineSTR = machineSTR[1:]

        machine_start = int(machineSTR)
        
        machine_finish2 = int(finish_entry.get())
        machine_finishSTR = str(machine_finish2)

        if machine_finishSTR[0]=='0':
            machine_finishSTR = machine_finishSTR[1:]
        
        machine_finish = int(machine_finishSTR)

        user = user_var.get()
        password = password_entry.get()

        log_file = create_log_file(number_room)

        if machine_start >= machine_finish:

            while machine_start >= machine_finish:
                pings = [change_user_password(number_room, machine_start, user, password)]
                with open(log_file, "a", encoding='utf8') as arquivo:
                    for p in pings:
                        arquivo.write(f'{p}\n')
                machine_start -= 1

        else:
            while machine_start <= machine_finish:
                pings = [change_user_password(number_room, machine_start, user, password)]
                with open(log_file, "a", encoding='utf8') as arquivo:
                    for p in pings:
                        arquivo.write(f'{p}\n')
                machine_start += 1

        estado_botao = atualizar_estado_checkbox()
        if estado_botao == True:
            send_email()
        messagebox.showinfo("Concluído", "Troca de senha concluída com sucesso.")

    else:
        messagebox.showinfo("Erro", "Sala não encontrada")

def send_email():
    # Configurações do servidor SMTP do office
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    number_room = room_entry.get()
    log_file = create_log_file(number_room)

    msg = MIMEMultipart()
    msg['From'] = email_username
    msg['To'] = email_client 
    msg['Subject'] = f'SETUP SERVER - Arquivo LOG troca de senha | SALA: {number_room}'

    nome_arquivo = log_file

    # Inicializar a variável para armazenar o conteúdo do arquivo
    conteudo_arquivo = None

    # Tentar abrir e ler o arquivo
    try:
        with open(nome_arquivo, "r") as arquivo:
            conteudo_arquivo = arquivo.read()
            print("Conteúdo do arquivo lido com sucesso.")
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")

    # Verificar se o conteúdo foi lido com sucesso
    if conteudo_arquivo is not None:
        # Faça o que quiser com a variável 'conteudo_arquivo'
        print("Sucesso")
        print(conteudo_arquivo)

    minha_string_com_quebra = conteudo_arquivo.replace("-", "\n")

    body = f"Segue arquivo TXT de troca de senha. \n\nRELATORIO: \n{minha_string_com_quebra} \nPor favor testar."
    
    msg.attach(MIMEText(body, 'plain'))

    with open(log_file, "r") as f:
        attachment = MIMEText(f.read())
        attachment.add_header("Content-Disposition", "attachment", filename=log_file)
        msg.attach(attachment)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_username, email_password)
    server.sendmail(email_username, email_client, msg.as_string())
    server.quit()
    print('Email enviado!')

def validar_entrada(event):
    # Obter o caractere inserido
    char = event.char

    # Verificar se o caractere é um dígito
    if not char.isdigit() and char != '\x08':
        return 'break'  # Impede a inserção do caractere no campo de entrada


def avancar_para_proximo_widget(event):
    # Mova o foco para o próximo widget
    event.widget.tk_focusNext().focus()
    return 'break'

def atualizar_estado_checkbox():
    estado = checkbox_var.get()
    if estado == 1:
        return True
    else:
        return False
        
    
if verify_psexec() == True:

    # Criar a janela principal
    window = tk.Tk()
    window.title("Troca de Senha - Ka Solution")
    window.geometry("400x300")


    # Criar os rótulos e campos de entrada
    room_label = tk.Label(window, text="Número da Sala:")
    room_label.pack()
    room_entry = tk.Entry(window)
    room_entry.pack()

    # Adicionar a função de validação da entrada, para apenas deixar o usuario digitar apenas numeros
    room_entry.bind("<Key>", validar_entrada)
    room_entry.bind("<Tab>", avancar_para_proximo_widget)

    start_label = tk.Label(window, text="Máquina Inicial:")
    start_label.pack()
    start_entry = tk.Entry(window)
    start_entry.pack()

    # Adicionar a função de validação da entrada, para apenas deixar o usuario digitar apenas numeros
    start_entry.bind("<Key>", validar_entrada)
    start_entry.bind("<Tab>", avancar_para_proximo_widget)

    finish_label = tk.Label(window, text="Máquina Final:")
    finish_label.pack()
    finish_entry = tk.Entry(window)
    finish_entry.pack()

    # Adicionar a função de validação da entrada, para apenas deixar o usuario digitar apenas numeros
    finish_entry.bind("<Key>", validar_entrada)
    finish_entry.bind("<Tab>", avancar_para_proximo_widget)

    user_label = tk.Label(window, text="Tipo de Usuário:")
    user_label.pack()
    user_options = ["Loc", "Student", "Admin", "Ka.student"]
    user_var = tk.StringVar(window)
    user_var.set(user_options[0])
    user_dropdown = tk.OptionMenu(window, user_var, *user_options)
    user_dropdown.pack()

    password_label = tk.Label(window, text="Padrão de senha:")
    password_label.pack()
    password_entry = tk.Entry(window)
    password_entry.pack()

    # Criar a variável de controle para a caixa de seleção
    checkbox_var = tk.IntVar()

    # Criar a caixa de seleção
    checkbox = tk.Checkbutton(window, text="Enviar e-mail de LOG ", variable=checkbox_var, command=atualizar_estado_checkbox)
    checkbox.pack()

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
