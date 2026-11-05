# Criar o .env do automacao_esp (resumo)

O `.env` guarda Wi-Fi e chave do Firebase só no computador de quem usa. Ele nunca sobe para o GitHub (`.gitignore`).

1. Na pasta `automacao_esp`: `Copy-Item .env.example .env`
2. Abra o `.env` e preencha:

| Chave | Valor |
| --- | --- |
| `ESP_NOME` | nome do ESP (letras, números, `-` e `_`); vira `esps/<nome>` no Firebase |
| `ESP_MODELO` | `ESP32` |
| `WIFI_SSID` / `WIFI_SENHA` | sua rede Wi-Fi (2,4 GHz) |
| `FIREBASE_HOST` | `amauryesp-active-default-rtdb.firebaseio.com` (sem `https://`) |
| `FIREBASE_AUTH` | opcional: chave do banco; em branco se as regras permitem o ESP gravar |

3. `python main.py`: o formulário abre já preenchido. Valores em branco continuam editáveis no formulário.

Executável (`.exe`): o `.env` fica na mesma pasta do `.exe`. Manual completo: `public/manual-automacao-esp.html` (link no painel AUTOMAÇÃO ESP do portal).
