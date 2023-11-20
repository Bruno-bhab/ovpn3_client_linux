import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Tk
import subprocess
import pexpect

class MinhaAplicacao:
    def __init__(self, root):

        self.shell_comand = "openvpn3 sessions-list"
        self.connections = self.execComand()
        self.info_message = ""

        self.root = root
        self.root.title("Open Vpn 3 client tool. By bhab")
        # Defina a geometria da janela para um tamanho maior
        self.root.geometry("600x300")

        self.components()

    def components(self):
        # Adicionar um Label no início do aplicativo
        self.label_conections = tk.Label(self.root, text="Connections:")
        self.label_conections.pack(pady=10)

        self.label_conections_list = tk.Label(self.root, text=self.connections)
        self.label_conections_list.pack(pady=10)

        #todo - criar botão para adicionar novo arquivo de vpn
        # self.btn_selecionar_arquivo = tk.Button(self.root, text="Selecionar Arquivo", command=self.select_file)
        # self.btn_selecionar_arquivo.pack(pady=10)

        self.btn_executar_comando = tk.Button(self.root, text="Turn on vpn", command=self.connect_to_vpn)
        self.btn_executar_comando.pack(pady=10)

        self.btn_executar_comando = tk.Button(self.root, text="Turn off vpn", command=self.disconnecVpn)
        self.btn_executar_comando.pack(pady=10)

    def updateSessionsList(self):
        self.shell_comand = "openvpn3 sessions-list"
        self.connections = self.execComand()
        self.label_conections_list.config(text=self.connections)

    def disconnecVpn(self):
        self.shell_comand = 'openvpn3 session-manage --config beedoo --disconnect'
        self.execComand()
        self.updateSessionsList()

    def select_file(self):
        # Abrir uma janela de seleção de arquivo
        filename = filedialog.askopenfilename(title="Selecionar Arquivo", filetypes=[("Arquivos de Texto", "*.ovpn")])
        print("Arquivo selecionado:", filename)

    def execComand(self):
        result = subprocess.run(self.shell_comand, shell=True, capture_output=True, text=True)
        return result.stdout

    def get_user_code(self):
        return simpledialog.askstring("Authenticator Code", "Enter Authenticator Code:", parent=self.root)
    
    def infoDialog(self):
        messagebox.showinfo("Alert", self.info_message)

    def connect_to_vpn(self):
        # Substitua estas variáveis pelos valores que você deseja fornecer
        login = ""
        password = ""
        vpnConfigName = ""
        connectVpnComand = "openvpn3 session-start --config " + vpnConfigName

        try:
            processo = pexpect.spawn(connectVpnComand, timeout=20)

            # Aguarde a solicitação do login e envie a resposta
            processo.expect("Auth User name:")
            processo.sendline(login)

            # Aguarde a solicitação da senha e envie a resposta
            processo.expect("Auth Password:")
            processo.sendline(password)

            # Aguarde a solicitação do código secreto e envie a resposta
            processo.expect("Enter Authenticator Code:")
            codigo_secreto = self.get_user_code()
            if codigo_secreto is not None:
                processo.sendline(codigo_secreto)
            else:
                processo.sendline("111111")

            processo.expect("Connected")
            self.updateSessionsList()
            self.info_message = 'Connected!'
            self.infoDialog()

            # Aguarde o término do processo
            processo.wait()

        except pexpect.ExceptionPexpect as e:
            self.disconnecVpn()
            self.info_message = 'Error when connecting. Try again.'
            self.infoDialog()
  
if __name__ == "__main__":
    root = tk.Tk()
    app = MinhaAplicacao(root)
    root.mainloop()
