# Automação ESP (aplicação desktop)

Aplicação Python (PyQt6) que configura, compila (PlatformIO) e grava o firmware **Automação Firebase** no ESP32 pela USB.
O ESP, ao ligar, se registra em `esps/<nome>` no Firebase; o portal (botão **AUTOMAÇÃO ESP**) lista os ESPs e aciona os pinos.

## Uso rápido

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env   # preencha Wi-Fi e Firebase
python main.py
```

O `.env` fica fora do GitHub. Manual completo (Python, VS Code, .env, executável, gravação): `public/manual-automacao-esp.html` do portal.

## Estrutura

- `main.py` / `AutomacaoFirebase.py`: ponto de entrada.
- `app/`: tema, widgets, `env_config.py` (lê o `.env`), ligação serial; `app/screens/firebase.py` (formulário), `flash_dialog.py` (PlatformIO) e `repetidor.py` (lista de portas).
- `firmware/Automacao/`: firmware C++ e `platformio.ini` (`automacao_config.h` fica em branco no repositório).
- `assets/`: ícones e fundos.
