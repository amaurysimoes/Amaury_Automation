# Automação ESP (aplicação desktop)

Aplicação Python (PyQt6) que configura, compila (PlatformIO) e grava o firmware **Automação Firebase** no ESP32 pela USB.
O ESP, ao ligar, se registra em `esps/<nome>` no Firebase; o portal (botão **AUTOMAÇÃO ESP**) lista os ESPs e aciona os pinos.

## Uso

```powershell
Set-Location automacao_esp
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python AutomacaoFirebase.py
```

No formulário informe nome, modelo, Wi-Fi (SSID e senha), host e chave do Firebase e escolha a porta serial. O app gera `automacao_config.h`
numa cópia de trabalho (`%LOCALAPPDATA%`), compila e grava. **Nenhuma senha ou chave fica neste repositório**:
`firmware/Automacao/include/automacao_config.h` contém apenas valores em branco.

## Estrutura

- `AutomacaoFirebase.py`: ponto de entrada.
- `app/`: tema, widgets, caminhos e ligação serial; `app/screens/firebase.py` (formulário), `flash_dialog.py` (PlatformIO) e `repetidor.py` (lista de portas).
- `firmware/Automacao/`: firmware C++ (`src/automacao_iot.cpp`) e `platformio.ini`.
- `assets/`: ícones e fundos.
