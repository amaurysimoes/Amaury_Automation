# Configuração secreta do automacao_esp (resumo)

O `automacao_esp` **não lê arquivo `.env`**. Wi-Fi e chave do Firebase são digitados no formulário do app e ficam só no seu computador. Nada disso sobe para o GitHub.

## Passos

1. `cd automacao_esp`, depois `python -m venv .venv`, `.venv\Scripts\activate` e `pip install -r requirements.txt`.
2. `python AutomacaoFirebase.py`.
3. Preencha o formulário:

| Campo | Valor |
| --- | --- |
| Nome | nome do ESP (letras, números, `-` e `_`); aparece no Firebase como `esps/<nome>` |
| Modelo | `ESP32` |
| SSID / Senha | sua rede Wi-Fi |
| Host | `amauryesp-active-default-rtdb.firebaseio.com` (já vem preenchido) |
| Auth | chave de acesso do Realtime Database (Firebase Console → Configurações do projeto → Contas de serviço → Secrets do banco de dados) |

4. Escolha a porta serial e grave.

O app guarda a última configuração em `%LOCALAPPDATA%` (fora do repositório). Nunca coloque Wi-Fi ou chave em `firmware/Automacao/include/automacao_config.h`: ele fica em branco no repositório.
