"""Lê o arquivo .env (opcional) com os dados que não devem ir para o GitHub: Wi-Fi e chave do Firebase.

O .env fica ao lado do programa: na pasta do projeto (python main.py) ou ao lado do .exe.
Veja .env.example e o manual do portal."""
import sys
from pathlib import Path


def env_path():
    base = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent.parent
    return base / ".env"


def carregar_env():
    """Devolve {CHAVE: valor} do .env (vazio se não existir). Aceita comentários (#) e aspas."""
    valores = {}
    try:
        linhas = env_path().read_text(encoding="utf-8-sig").splitlines()
    except OSError:
        return valores
    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, _, valor = linha.partition("=")
        valor = valor.strip()
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
            valor = valor[1:-1]
        valores[chave.strip()] = valor
    return valores


# chave do .env -> campo da configuração do app
CAMPOS = {"ESP_NOME": "nome", "ESP_MODELO": "modelo", "WIFI_SSID": "ssid", "WIFI_SENHA": "senha",
          "FIREBASE_HOST": "host", "FIREBASE_AUTH": "auth"}


def aplicar_env(cfg):
    """Copia da configuração com os valores preenchidos do .env por cima (os vazios são ignorados)."""
    env = carregar_env()
    novo = dict(cfg)
    for chave, campo in CAMPOS.items():
        if env.get(chave):
            novo[campo] = env[chave]
    return novo
