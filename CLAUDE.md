# Histórico e continuidade do projeto

Resumo do contexto técnico e do estado atual, para retomar o trabalho em outra sessão.

**Regra permanente (pedido do proprietário):** toda alteração feita no projeto deve ser registrada neste arquivo no mesmo momento, sem exceção. Se o console fechar, este arquivo deve bastar para continuar de onde parou. Manter o arquivo **curto**: atualizar "Próximo passo" e "Estado atual", e resumir o que já foi concluído em vez de acumular histórico detalhado.

## Projeto

- **Amaury Automation**: portal para organizar projetos (automação, IoT, web/mobile, desktop, bancos de dados), com cards que levam a cada aplicação.
- Pasta: `C:\Dev-AHS\Amaury_Automation`. Repositório: `https://github.com/amaurysimoes/Amaury_Automation` (público). Branch: `main`.
- Stack: JavaScript, React e Vite (não é Python; só a API em `api_render/` é Python/FastAPI).
- Site: `https://automationprojects.top` (GitHub Pages, domínio próprio via `public/CNAME`, deploy automático a cada push em `main` por `.github/workflows/deploy.yml`).
- API: Render, serviço `automacao-api` em `https://automacao-api-0f6w.onrender.com` (plano Free hiberna; `src/main.jsx` faz um "wake" em `/saude`). URL em `src/config.js`.
- Tema dark padrão (`#17191f`, azul oficial `#2B3CF5`); light em cinza suave (`#d5d8df`); escolha salva em `localStorage`. Token `--neon`: `#39ff14` (dark) / `#1f51ff` (light).

## Preferências do proprietário

- **Commit e push somente quando ele pedir.** Commits sem atribuições de ferramentas de assistência; nunca amendar, nunca `push --force`.
- Escreve rápido e com erros de digitação: corrigir erros óbvios avisando; em dúvida, perguntar.
- Nunca registrar nem copiar credenciais, tokens ou conteúdo do `.env` (nem neste arquivo). O `.env` está no `.gitignore`.
- Documentação escrita como documentação normal do projeto.
- Referência de estilo: só a paleta escura de `C:\Dev-AHS\IA_automation_front`; estrutura geral inspirada em `master.dev/join` (sem copiar textos, marca ou código).

## O que já existe (concluído)

**Página única (`src/App.jsx`, estilos em `src/styles.css`)**
- Cabeçalho fixo: marca "AmauryProjects", menu (Projetos Exemplo, Teste e Downloads), botões "Login para Códigos" e "Instruções Site" (ainda sem destino, apontam para `#recursos`), seletor de tema à direita e botão de 3 linhas que abre painel lateral de mídia (`MEDIA_ITEMS`, provisório).
- Hero com `background_projeto.jpg` e o texto neon "Projetos e Automação".
- Grade de 6 cards (`FEATURES`): IoT, IA e Automação, Web e Mobile, Programação Desk, Desenvolvimento e Integração DB, "Em Desenvolvimento...". Imagens 1280×800 em `img/` e `public/img/` (copiar sempre para `public/`).
- Cada card leva à seção de detalhe (quadro neon 16:7 com `background_card.jpg`). Itens com `tools` mostram o botão da ferramenta e a logomarca no canto; os demais mostram o símbolo e "Em desenvolvimento".
- Tópico "Testes e Download" (`#teste-downloads`), ainda vazio. Rodapé com copyright 2026.
- Efeitos neon nos cards e quadros; `prefers-reduced-motion` desliga animações.

**Vetorização de Imagem Base de Dados** (`src/dbvision/`, botão na seção de detalhe de Desenvolvimento e Integração DB)
- Painel modal com abas **Visualizar** (pública: lista, prévia, download, código SHA-256 com botão Copiar) e **Upload** (exige login Google via Firebase; comprime em WebP, calcula SHA-256, `POST /aiven/imagens`; duplicata responde 409).
- Arquivos: `VetorizacaoImagens.jsx`, `UploadImagem.jsx` (carregado com `React.lazy`), `firebase.js`. Dependência `firebase` (o `npm audit` acusa 4 avisos em `@grpc/grpc-js`, não usados; não rodar `audit fix --force`).

**API (`api_render/`)**
- FastAPI com Aiven/Neon. Só `GET /aiven/imagens` e `GET /aiven/imagens/{id}` são abertas (marcadas "TEMPORÁRIO" no código); todas as outras rotas exigem login Google + `EMAIL_PERMITIDO`. CORS inclui `automationprojects.top`, `www`, `amaurysimoes.github.io` e `localhost:5173`.
- Render: Root `api_render`, Build `pip install -r requirements.txt`, Start `uvicorn main:app --host 0.0.0.0 --port $PORT`, Health `/saude`, `PYTHON_VERSION=3.12.3`. Variáveis no Environment Group `automacao-env` (só no painel do Render).
- Origem: projeto externo `C:\Automaca_Amaury` (Python + site Firebase `https://amauryesp-active.web.app/`; repositório privado `amaurysimoes/Automacao_Amaury`).

**Confirmado pelo proprietário (5 de novembro de 2026):** lista, SHA-256, upload, variáveis do Render, domínios autorizados no Firebase e `EMAIL_PERMITIDO` já funcionam. Etapa de vetorização/upload **encerrada**.

## Estrutura

```text
Amaury_Automation/
├── .github/workflows/deploy.yml
├── api_render/ (main.py, its_xlsx.py, planilha_modelo.py, requirements.txt, ca.pem)
├── DocumentacaoTecnica/ (Atualizar_Git.md, EstruturaProjeto.md, Git_Push.md, PublicarGit.md)
├── img/ (originais)   public/ (CNAME, img/ publicado)
├── src/ (App.jsx, config.js, main.jsx, styles.css, dbvision/)
├── CLAUDE.md, README.md, EstruturaProjeto.md, index.html, package.json, vite.config.js
```

Nada dentro de `public/` pode conter segredos (tudo ali é publicado). `img/iotfire.jpg` existe sem uso no código.

## Commits enviados (principais)

`ba01788` página inicial · `f6710c5` publicação no Pages · `4e5cc47` seções e cards · `3350b04` cards Desk e DB · `8c89b75` imagem nos painéis · `7b4881a` API Render · `f33671e` painel de vetorização, novo cabeçalho e mídia · `223012b` upload, SHA-256 e ajustes do painel · `a10d059` painel AUTOMAÇÃO ESP e app `automacao_esp` (enviado em 5 de novembro de 2026). O histórico é aditivo.

## Estado atual

- Branch `main`, enviada até `a10d059`. Build passando. O registro deste envio no CLAUDE.md fica para o próximo commit.
- Etapa anterior (vetorização + API + upload) concluída.

## PRÓXIMO PASSO

**Etapa atual: Automação Firebase (ESP) no portal.** Origem: `C:\Automaca_Amaury` (site em `fire_page/src/Automacao.jsx`, firmware em `automacao_iot/`, app Python em `automacao_iot/app/screens/flash_dialog.py`). **App Python do ESP copiado para este repositório (5 de novembro de 2026, sem commit): `automacao_esp/`** (cópia do formulário "Automação FireBase" de `C:\Automaca_Amaury\automacao_iot`: `AutomacaoFirebase.py`, `app/` com `paths/theme/widgets/serial_link` e `screens/firebase|flash_dialog|repetidor`, `assets/`, `firmware/Automacao/`, `requirements.txt` enxuto com `platformio`, `README.md`; guia do `.env` em `DocumentacaoTecnica/Criar.env_automacao_esp.md`). Os arquivos Python compilam, mas o app **não foi executado** nem testado com ESP. `firmware/Automacao/include/automacao_config.h` foi **higienizado** (Wi-Fi e `FIREBASE_AUTH` em branco; o original tinha valores reais). `.gitignore` ganhou `.venv/` e `.pio/`. A pasta `C:\Automaca_Amaury\automacao_esp` segue vazia e sem uso. Não copiados: firmware Repetidor, brokers/MQTT, agentes (o `FlashDialog` do repetidor aponta para um firmware ausente; a tela de Automação não usa isso).

**Visual do app `automacao_esp` (5 de novembro de 2026, sem commit):** ícone trocado pelo oficial do portal (`assets/circuito-azul.svg`, azul `#2B3CF5`; `icone_ia.png/.ico` gerados dele, mesmos nomes de antes) e o botão de tema virou a **chave deslizante do portal** (`ThemeButton` em `app/widgets.py`: rótulo Escuro/Claro, trilho, bolinha com lua/sol, animação de 180 ms, mesmas cores dos tokens do portal). Conferido só por captura offscreen; ainda não visto no app real. As cores neon dos botões do app seguem as antigas.

**Download e manual (5 de novembro de 2026, sem commit; build passando):** o painel AUTOMAÇÃO ESP ganhou, abaixo da lista, os botões **Baixar projeto Python (.zip)** e **Manual passo a passo**. O `.zip` é gerado a cada `npm run dev/build` por `scripts/zip-automacao-esp.mjs` (devDependency `fflate`; exclui `.venv`, `.pio`, `__pycache__`, `.env`) em `public/downloads/` (ignorado pelo Git; o deploy do Pages gera de novo). Manual: `public/manual-automacao-esp.html` (Python, VS Code, abrir o projeto, venv, `.env`, `python main.py`, executável PyInstaller, gravar o ESP, controlar pelo portal). O app agora **lê `.env`** (`automacao_esp/app/env_config.py`; chaves `ESP_NOME`, `ESP_MODELO`, `WIFI_SSID`, `WIFI_SENHA`, `FIREBASE_HOST`, `FIREBASE_AUTH`; modelo em `.env.example`), tem `main.py` e não grava `FIREBASE_AUTH` em disco. Antes o app não tinha campo de chave (o `auth` ia sempre vazio); isso corrige o guia anterior. Comando do `.exe` testado: gera e abre; gravação real no ESP e fluxo completo pelo manual **não testados**.

Decisão: o **site só gerencia** (Firebase); **gravar o ESP (PlatformIO/USB) fica no app Python desktop**, que entrará depois em "Testes e Download" via GitHub Releases. Console Python no navegador não grava ESP; gravação web só seria possível com Web Serial + `.bin` pronto (etapa futura, opcional).

Feito (5 de novembro de 2026, sem commit): painel **Automação Firebase** (`src/automacao/PinosESP.jsx`, lazy) aberto pelo botão **"AUTOMAÇÃO ESP"** na seção de detalhe de **Aplicações IOT** (`id: iot`). Lê `esps/<nome>` no Realtime Database (`db` exportado em `src/dbvision/firebase.js`, com `databaseURL`), lista os ESPs (online = `visto_em` < 30 s), abre os pinos (`pinos/<gpio>`: `nome`, `tipo`, `estado`) e aciona: Ligar/Desligar (`estado`) e Pulso (`pulso: true`). Entradas só mostram ON/OFF. Cópia fiel do comportamento da página original, sem login.

**Pendências desta etapa:**
1. Testar com `npm run dev` e um ESP real ligado (ver se a lista e os pinos aparecem).
2. **Segurança:** o controle dos pinos é público se as regras do Realtime Database estiverem abertas (como no site original). Conferir as regras no Firebase Console; avaliar exigir login Google para Ligar/Desligar/Pulso.
3. Rodar o app (`automacao_esp/README.md`) e gravar um ESP de teste; depois empacotar em `.zip` (GitHub Releases) para a seção Testes e Download.
4. Commit/push só quando o proprietário pedir.

Candidatos já conhecidos (não iniciados):
1. Plano de downloads: levar o sistema Python + Firebase web para o portal em partes, ligado à seção "Testes e Download"; executável em `.zip` via **GitHub Releases** neste repositório, com SHA-256 e aviso sobre o alerta do Windows. Antes de copiar qualquer código, ler e remover chaves e credenciais; projetos em `projetos/<nome>/`, fora de `public/` e `src/`.
2. Destino dos botões "Login para Códigos" e "Instruções Site"; imagens e vídeos reais do painel de mídia.
3. Conteúdo real das demais seções de detalhe e da imagem do último card.
4. Conferir `https://automationprojects.top/` com HTTPS forçado e, se desejado, `CNAME` `www`.
5. Limpar CSS sem uso e atualizar `README.md` e `EstruturaProjeto.md` (ainda descrevem a versão antiga com sidebar).
6. Se o endereço do Render mudar: atualizar `src/config.js` e `API_URL` do site original (`fire_page/src/api.js`).

## Comandos usuais

```powershell
Set-Location 'C:\Dev-AHS\Amaury_Automation'
npm ci
npm run dev        # http://localhost:5173
npm run build      # validar produção
```

Enviar (só quando o proprietário pedir): `git status`, `npm run build`, `git add -A`, `git commit -m "..."`, `git push`. Conferir o deploy com `gh run list --workflow deploy.yml --limit 5`. Não versionar `node_modules` nem `dist`.

## Orientação para futuras alterações

- Manter React + Vite; preservar a paleta; usar `--neon` nos efeitos neon.
- Imagem nova ou substituída: copiar de `img/` para `public/img/`.
- Ao mexer em estilos, imagens ou dependências, rodar `npm run build`.
- Manter coerentes `base` do Vite, `public/CNAME`, workflow e a documentação.
- **Atualizar este arquivo a cada alteração, mantendo-o curto.**
