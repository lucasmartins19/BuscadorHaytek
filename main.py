import login
import requests
import PySimpleGUI as sg
from concurrent.futures import ThreadPoolExecutor

def main():
    empresas = usuario.verificar_empresas()
    empresas = [f"{empresa}: {empresas[empresa]['Nome']}" for empresa in empresas]
    usuario.codigo_empresa = empresas[0].split(":")[0]

    layout_principal = [
        [sg.Text("Empresa:"), sg.Combo(values=empresas, default_value=empresas[0], key="empresa", enable_events=True, readonly=True, size=(30))],
        [sg.Input(size=(20), key="campo_pesquisa"), sg.Button("Pesquisar", key="pesquisar")],
        [sg.Table(usuario.extrair_dados_pedidos(), key="tabela", headings = ["Lente", "Nome", "OD ESF.", "OD CIL", "OE ESF", "OE CIL", "AD OD", "AD OE", "PEDIDO", "VALOR"])]
    ]
    window_principal = sg.Window("BuscadorHayTek", layout=layout_principal)
    while True:
        event, values = window_principal.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "empresa":
            usuario.codigo_empresa = values['empresa'].split(":")[0]
        elif event == "pesquisar":
            if values['campo_pesquisa'] == "":
                window_principal['tabela'].update(values=usuario.pedidos_l_org)
            else:
                window_principal['tabela'].update(values=usuario.filtrar_resultados(values['campo_pesquisa']))

    window_principal.close()

class Usuario:
    def __init__(self, dados_login):
        self.id = dados_login['ID']
        self.token = dados_login['TOKEN']
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Token": self.token,
        "Iduser": str(self.id)}

    def requisicoes_get(self, url):
        try:
            return requests.get(url, headers=self.headers)
        except:
            return None

    def filtrar_resultados(self, termo):
        return [lista for lista in self.pedidos_l_org for item in lista if termo.lower() in item.lower()]
        
    def verificar_empresas(self):
        requisicao = self.requisicoes_get("https://api.haytek.com.br/api/v1/user/legacy/users/24342/config")
        if requisicao is not None:
            empresas = requisicao.json()['RESULT']['COMPANIES']
            empresas_dict = dict()
            for empresa in empresas:
                empresas_dict[empresa['A1_COD']] = {}
                empresas_dict[empresa['A1_COD']]['Nome'] = empresa['A1_NOME']
            return empresas_dict
        return None
    
    def funcao_auxiliar_requisicao(self, pedido):
        try:
            requisicao = self.requisicoes_get(f"https://api.haytek.com.br/v1.1/orders/{pedido}/details/PARAPAR").json()['RESULT']['PARAPAR']
            if len(requisicao) > 1:
                for req in requisicao:
                    self.pedidos_l.append(req)
            else:
                self.pedidos_l.append(requisicao[0])
        except:
            return None

    def extrair_dados_pedidos(self):
        pedidos = self.lista_pedidos()
        if pedidos is not None:
            self.pedidos_l = list()
            with ThreadPoolExecutor(max_workers=10) as pool:
                pool.map(self.funcao_auxiliar_requisicao, pedidos)
            self.pedidos_l_org = sorted([[pedido['DESCRICAO'].strip("Lente Haytek Visão Simples Acabada"), pedido['NOME'], pedido['DIR_ESFER'], pedido['DIR_CIL'], pedido['ESQ_ESFER'], pedido['ESQ_CIL'], pedido['DIR_ADD'], pedido['ESQ_ADD'], pedido['PEDIDO'], str(pedido['VALOR'])] for pedido in self.pedidos_l], reverse=True, key=lambda l: l[8])
            return self.pedidos_l_org
   
    def lista_pedidos(self):
        try:
            json = {
                "id_ini": 0,
                "id_qtd": 10,
                "status": "T",
                "data_ini": "19000101",
                "data_fim": "21000101",
                "companies": [self.codigo_empresa]
            }
            pedidos = requests.post(f"https://api.haytek.com.br/v1.1/orders/history/v2/{self.codigo_empresa}", headers=self.headers, json=json).json()['RESULT']
            return [pedido['Pedhtk'] for pedido in pedidos]
        except:
            return None

if __name__ == "__main__":
    dados_login = login.iniciar_login()
    if dados_login is not None:
        usuario = Usuario(dados_login)
        main()