# Histórico e continuidade do projeto

Este arquivo registra o contexto técnico, as decisões, as alterações e o estado atual do projeto para que o trabalho possa continuar em outra sessão.

**Regra permanente (pedido do proprietário):** toda alteração feita no projeto deve ser registrada neste arquivo no mesmo momento, sem exceção. Se o console for fechado, este arquivo deve bastar para retomar o trabalho de onde parou. Atualizar: estrutura, estado atual, histórico de alterações e pendências.

## Projeto

- Nome: **Amaury Automation**.
- Pasta local: `C:\Dev-AHS\Amaury_Automation`.
- Repositório GitHub: `https://github.com/amaurysimoes/Amaury_Automation`.
- Branch de trabalho/publicação: `main`.
- Stack: JavaScript, React e Vite; não é um projeto Python.
- Objetivo atual: portal para organizar vários projetos (automação, IoT, web/mobile, desktop, bancos de dados), com seções e cards que levam a cada aplicação.
- O tema dark é predominante e o padrão. O seletor deslizante permite light, persiste a escolha em `localStorage` e sincroniza abas abertas do mesmo site.
- Referência de estilo: `C:\Dev-AHS\IA_automation_front` (somente a paleta escura; sem copiar componentes, imagens ou funcionalidades).
- Referência estrutural: `https://master.dev/join/`. Usada apenas para a organização geral da página; textos, marca, cores e código do template não são copiados.
- Preferência de apresentação do projeto: documentação e commits devem ser escritos como documentação normal do projeto, sem atribuições ou comentários sobre ferramentas de assistência.
- O proprietário escreve rápido e às vezes com erros de digitação nos textos pedidos. Corrigir erros óbvios de ortografia e avisar a correção; em dúvida, perguntar.
- Commit e push somente quando o proprietário pedir.

## Estado atual da página (`src/App.jsx`)

Página única, na ordem:

1. **Cabeçalho fixo**: marca "AmauryProjects" (ícone azul + texto, fonte 0.94rem + 2px), menu com **Projetos Exemplo** (→ `#recursos`) e **Teste e Downloads** (→ `#teste-downloads`), seletor de tema, botões "Entrar" e "Participar" (ainda sem destino) e menu para celular (até 860px).
2. **Hero**: imagem de fundo `background_projeto.jpg` (opacidade `--hero-image-opacity`: 0.32 no dark, 0.16 no light, com esmaecimento na base) e apenas o texto **"Projetos e Automação"** (`.hero__tag`): verde neon com brilho no tema escuro, azul neon no claro, fonte 0.78rem + 4px.
3. **Grade de cards** (`#recursos`, 3 colunas, 2 fileiras): lista `FEATURES` no topo do arquivo (`id`, `title`, `image`, `description`). A imagem de cada card é um link para a seção de detalhe com o mesmo `id`.

   | Card | Imagem | Descrição |
   | --- | --- | --- |
   | Aplicações IOT (`iot`) | `iot.jpg` | Projetos de Integração com dispositivos Residenciais e Móveis. |
   | IA e Automação (`automacao`) | `automacao.jpg` | Projetos de Automação e Integração de Hardwares com IA |
   | Web e Mobile (`web-mobile`) | `webmob.jpg` | Desenvolvimento Back End, Front e App Mobile |
   | Programação Desk (`desk`) | `desk.jpg` | Desenvolvimento e Integração de aplicações Desk |
   | Desenvolvimento e Integração DB (`database`) | `database.jpg` | Aplicações Database PostgreSQL e MySQL (Neon e Aiven) |
   | Em Desenvolvimento... (`em-desenvolvimento-3`) | `pci.jpg` | Sempre haverá um novo projeto! |

4. **Tópico "Testes e Download"** (`#teste-downloads`): título pequeno, discreto, alinhado à esquerda (`.topic`). Sem conteúdo ainda.
5. **Seções de detalhe**: uma por card, geradas da mesma lista `FEATURES` (título, descrição, painel com fundo `background_card.jpg`, o símbolo `circuito-cinza.svg` e o texto "Em desenvolvimento", e o link "← Voltar aos projetos" para `#recursos`).
6. **Rodapé**: marca "AmauryProjects" e, centralizado, "Copyright © 2026 Amaury Huerb Simões" (ano escrito direto no código).

### Efeitos visuais (`src/styles.css`)

- Token `--neon`: `#39ff14` (dark) e `#1f51ff` (light). Todos os efeitos neon usam esse token.
- Cada card tem caixa com borda neon, brilho ao redor (mais forte no hover) e um brilho que percorre a borda (`@property --glow-angle` + `conic-gradient`, 4s).
- O bloco "Em desenvolvimento" das seções de detalhe tem borda neon pulsante e sombra larga (`@keyframes neon-pulse`, 2.8s).
- `prefers-reduced-motion` desliga animações.
- Rolagem suave (`scroll-behavior: smooth`) e `scroll-margin-top: 84px` por causa do cabeçalho fixo.
- Espaçamentos ajustados a pedido: hero com 32px embaixo; `#recursos` com 40px em cima; seções `.detail` com padding `12px 0 40px`.
- **Tema light** em cinza suave (pedido: o branco estava forte): fundo `#d5d8df`, barra/faixas `#e0e3e9`, superfície `#e6e8ee`, texto `#1c202b`. `theme-color` do navegador no light: `#d5d8df`.
- Paleta dark: fundo `#17191f`, barra `#13151a`, superfície `#1d2028`, texto `#edf0f7`, azul oficial `#2B3CF5`.

### Imagens

- Os arquivos originais ficam em `img/` e **devem ser copiados para `public/img/`** (somente o que está em `public/` vai para o site). Se uma imagem for substituída mantendo o nome, copiar de novo para `public/img/` e conferir com `cmp`.
- Imagens dos cards: **1280 × 800 px (16:10)**; as atuais têm 1312 × 816 e encaixam sem cortes.
- `public/img/placeholder.svg`: cinza, usado em cards sem imagem.
- `img/iotfire.jpg`: arquivo adicionado pelo proprietário, ainda sem uso no código (não versionado na última verificação).

## Estrutura atual

```text
Amaury_Automation/
├── .github/workflows/deploy.yml
├── .gitignore
├── CLAUDE.md
├── DocumentacaoTecnica/
│   ├── Atualizar_Git.md
│   ├── EstruturaProjeto.md
│   ├── Git_Push.md
│   └── PublicarGit.md
├── EstruturaProjeto.md
├── README.md
├── index.html
├── package-lock.json
├── package.json
├── public/
│   ├── CNAME
│   └── img/ (circuito-azul.svg, circuito-cinza.svg, placeholder.svg, background_projeto.jpg, background_card.jpg,
│            iot.jpg, automacao.jpg, webmob.jpg, desk.jpg, database.jpg, pci.jpg)
├── img/ (originais das imagens acima)
├── src/
│   ├── App.jsx
│   ├── config.js
│   ├── dbvision/ (firebase.js, VetorizacaoImagens.jsx)
│   ├── main.jsx
│   └── styles.css
└── vite.config.js
```

### Arquivos importantes

- `src/App.jsx`: página em seções; dados dos cards na constante `FEATURES`, menu em `NAV_LINKS`.
- `src/main.jsx`: aplica o tema salvo antes da montagem do React, importa o CSS e monta a página em `#root`.
- `src/styles.css`: tokens de tema (dark e light), componentes, efeitos neon e responsividade (breakpoints 860px e 600px).
- `index.html`: HTML inicial, idioma `pt-BR`, metadados, favicon oficial e título da aba.
- `vite.config.js`: Vite com `base: './'`, para funcionar no GitHub Pages com domínio próprio.
- `public/CNAME`: exatamente `automationprojects.top`; o Vite copia para `dist/CNAME`.
- `.github/workflows/deploy.yml`: build e deploy automáticos do GitHub Pages a cada push para `main`, além de execução manual (`workflow_dispatch`).
- `DocumentacaoTecnica/` e `EstruturaProjeto.md` (raiz): guias de recriação, Git e publicação. **O guia de estrutura ainda descreve a versão antiga da página (sidebar); atualizar quando o proprietário pedir.**
- `img/circuito-azul.svg`: ícone oficial azul (`#2B3CF5`), usado na marca e no favicon. `circuito-cinza.svg`: usado nos blocos "Em desenvolvimento".

## Histórico de decisões e alterações

1. Página inicial Vite + React com aparência escura, usando só as cores do projeto de referência. Texto inicial: “Projetos em Desenvolvimento.” e “Amaury Huerb”.
2. A pasta continha apenas `DocumentacaoTecnica/Git_Push.txt`; não havia projeto Vite nem repositório Git.
3. Criado o projeto mínimo com React e Vite, sem dependências visuais desnecessárias.
4. Adicionados `.gitignore`, `README.md`, arquivos Vite/React e documentação.
5. Guia de recriação manual em `DocumentacaoTecnica/EstruturaProjeto.md` (cópia resumida na raiz).
6. Git inicializado, remoto `origin` configurado e enviado para `main`.
7. Guias separados para atualizar o Git e publicar o site.
8. Publicação via GitHub Pages e GitHub Actions (Node.js 22, `npm ci`, `npm run build`, `actions/deploy-pages`).
9. Endereço planejado: domínio próprio `automationprojects.top`.
10. `vite.config.js` com `base: './'` e `public/CNAME` criado.
11. `DocumentacaoTecnica/PublicarGit.md` documenta DNS, domínio, HTTPS, deploy e diagnóstico.
12. Arquivos e commits sem atribuições de ferramentas de assistência.
13. Fornecidos `img/circuito-azul.svg` e `img/circuito-cinza.svg`; azul oficial `#2B3CF5` adotado como destaque e favicon.
14. Cor oficial aplicada ao token de destaque, brilhos, ícone da página e favicon.
15. Botão deslizante de tema escuro/claro com persistência em `localStorage`, `theme-color` e sincronização entre abas.
16. Página evoluiu para uma workspace com sidebar, breadcrumb e área vazia (depois substituída, ver 18).
17. Identidade visual do ícone oficial aplicada (commit `3765831`).
18. Layout reorganizado conforme a estrutura do template `master.dev/join`: página única com seções; imagens substituídas por placeholders cinza.
19. Seções do template removidas a pedido, uma a uma: planos (Indivíduos/Equipes/Empresas), "O que está incluído?", depoimentos, FAQ, subtítulo/prova social/aviso do hero, links do rodapé, selos de lojas e textos do rodapé ("AMAURY AUTOMATION", "Um espaço para novas ideias"). Links "Blog" e "Recursos" saíram do menu.
20. Fundo do hero: `background.jpg` foi usado como marca d'água, depois movido para o hero no lugar do quadriculado; trocado por `background_projeto.jpg` (o antigo foi apagado).
21. Cards definidos com imagens reais e textos (tabela acima). Chave de lista passou a ser o `id`.
22. Clique na imagem do card leva (rolagem suave) à seção de detalhe correspondente; as seções são geradas da lista `FEATURES`. Título "Projetos" acima dos cards removido por redundância.
23. Hero: texto "Projetos e Automação" em neon (verde no dark, azul no light). Antes passou por "Painel de Projetos" (removido) e "Projetos em Desenvolvimento".
24. Menu: "Projetos Exemplo" e "Teste e Downloads" (→ seção `#teste-downloads`, título "Testes e Download", discreto no canto esquerdo).
25. Cards com borda neon, brilho e brilho percorrendo a borda; blocos "Em desenvolvimento" com borda neon pulsante.
26. Tema light escurecido para cinza suave.
27. Copyright centralizado no rodapé: "Copyright © 2026 Amaury Huerb Simões".
28. `webmob.jpg` substituído por nova versão (mesmo nome); cópia em `public/img` atualizada.
29. Cards 4 e 5 definidos: **Programação Desk** (`desk.jpg`) e **Desenvolvimento e Integração DB** (`database.jpg`; texto "MySQL" com a grafia correta). Apenas o último card segue como "Em Desenvolvimento" (`pci.jpg`).

30. Último card alterado para o título **"Em Desenvolvimento..."** e a descrição **"Sempre haverá um novo projeto!"** (imagem `pci.jpg`). Medida informada para imagens do bloco das seções de detalhe: 1600 × 700 px (16:7).

31. Painéis "Em desenvolvimento" das seções de detalhe (`.detail__soon`): o degradê cinza foi trocado pela imagem `background_card.jpg` (1568 × 672, estilo código verde; proporção quase igual à do painel 16:7). O símbolo `circuito-cinza.svg` e o texto "Em desenvolvimento" continuam centralizados no mesmo lugar; borda neon pulsante mantida. Cópia em `public/img/background_card.jpg`.

32. Primeira etapa da integração do projeto externo `C:\Automaca_Amaury` (programa Python + site Firebase): a API FastAPI (`api_reder` do original) foi copiada para **`api_render/`** (`main.py`, `its_xlsx.py`, `planilha_modelo.py`, `requirements.txt`, `ca.pem`). Sem `.env` e sem `__pycache__`; conferido que o código não tem senhas escritas (as chaves vêm de variáveis de ambiente). A pasta vazia `backend_iot` foi removida. Enviado ao GitHub pelo proprietário no commit `7b4881a` ("Update API Render"), em repositório público (decisão do proprietário de manter o código neste repositório). Contexto: o site `https://amauryesp-active.web.app/` falha com "Failed to fetch" porque o serviço `automacao-api` do Render (`automacao-api-1awz.onrender.com`) não existe mais; o repositório `amaurysimoes/Automacao_Amaury` (privado) continua intacto.

33. **Render (5 de novembro de 2026, em andamento):** o painel do proprietário está em **inglês** e estava totalmente vazio. Serviço sendo criado como Web Service a partir do repositório público `amaurysimoes/Amaury_Automation`, branch `main`, região Oregon, projeto "My project"/Production. Configuração definida: Name `automacao-api`; Language **Python 3** (a tela vem em Node); Root Directory `api_render`; Build `pip install -r requirements.txt`; Start `uvicorn main:app --host 0.0.0.0 --port $PORT`; Compute **Free** (a tela vem pré-selecionada no plano pago de US$ 7/mês; conferir que o botão final mostra $0); variável `PYTHON_VERSION=3.12.3`; Advanced → Health Check Path `/saude`, Auto-Deploy `On Commit`, demais campos vazios. O serviço **já foi criado** (a página Environment do serviço só tinha `PYTHON_VERSION=3.12.3`). As variáveis são cadastradas na página do serviço → **Environment** → botão **Edit** → adicionar linhas → **Save**. **Faltam**: cadastrar as chaves (`AIVEN_PORT=16132` e as demais variáveis abaixo, valores só do `.env` do proprietário, nunca copiados para cá) uma por vez; depois testar `<endereço>/saude` (deve responder `{"ok":true}`) e conferir se o endereço gerado é igual a `automacao-api-1awz.onrender.com`. Se for diferente, trocar `API_URL` no site (`fire_page/src/api.js` do projeto original) e republicar no Firebase.

    **Atualização (5 de novembro de 2026):** o proprietário decidiu cadastrar as variáveis por **Environment Group** (Render → Environment Groups → + New Environment Group, nome sugerido `automacao-env`), colando o conteúdo do `.env` de uma vez (valores só no painel do Render, nunca neste repositório). Passo obrigatório depois: vincular o grupo ao serviço `automacao-api` (Environment → Linked Environment Groups). `PYTHON_VERSION` continua nas variáveis do próprio serviço. Estado: parado na tela "+ New Environment Group".

    **Atualização 2 (5 de novembro de 2026):** o proprietário informou que `/saude` **já respondeu `{"ok":true}`** (o serviço está no ar). Atenção: `/saude` não usa banco nem variáveis, então isso **não prova** que o grupo de variáveis foi criado e vinculado. O `.env` original (`C:\Automaca_Amaury\.env`) tem as chaves `AIVEN_HOST/PORT/USER/PASSWORD/DB_NAME`, `AIVEN_SSL_CA` e `NEON_HOST/PORT/USER/PASSWORD/DB_NAME/SSLMODE`; **não tem `EMAIL_PERMITIDO`**, que a API exige (sem ela toda rota recusa o login). `AIVEN_SSL_CA` **não deve ir para o Render**: o código usa `api_render/ca.pem` direto. Lista correta do grupo `automacao-env`: as 11 chaves AIVEN (sem SSL_CA) e NEON acima + `EMAIL_PERMITIDO` (e-mail Google usado no login do site). Falta confirmar: grupo criado e vinculado ao serviço, endereço do serviço igual a `automacao-api-1awz.onrender.com`, e teste real no site `https://amauryesp-active.web.app/` (sem "Failed to fetch").

    **Atualização 3 (5 de novembro de 2026):** o proprietário está em `https://dashboard.render.com/new/env-group`, colando as variáveis do `.env` (via "Add from .env"). Decisão dele: criar o grupo **primeiro só com as variáveis do `.env`** (sem `AIVEN_SSL_CA`) e adicionar `EMAIL_PERMITIDO` **depois**. Ordem combinada: (1) criar o grupo `automacao-env`; (2) vincular ao serviço `automacao-api` (Environment → Linked Environment Groups); (3) adicionar `EMAIL_PERMITIDO` ao grupo; (4) aguardar o deploy e testar o site.

    **Atualização 4 (5 de novembro de 2026):** o proprietário **criou o Environment Group `automacao-env`** no Render. Próximo passo: vincular ao serviço `automacao-api`; depois adicionar `EMAIL_PERMITIDO` ao grupo e testar o site.

    **Atualização 6 (5 de novembro de 2026):** o log do Render mostrou o serviço **no ar** ("Your service is live") e o endereço real é **`https://automacao-api-0f6w.onrender.com`** (diferente do antigo `automacao-api-1awz`). **Pendente:** trocar `API_URL` em `fire_page/src/api.js` (projeto original `C:\Automaca_Amaury`) para esse endereço e republicar no Firebase. Plano Free hiberna (~50 s de atraso); por isso `src/main.jsx` agora faz um "wake" (`fetch` `no-cors` em `/saude`) ao abrir o portal, com o comentário "wake do Render para acesso - Amaury". Se o endereço do Render mudar, atualizar essa URL também. Ainda não enviado ao GitHub (aguarda pedido de commit/push).

    **Atualização 5 (5 de novembro de 2026):** o proprietário declarou que **já cadastrou no Render tudo o que a API precisa** (grupo de variáveis e demais), sem depender do `.env`. Falta apenas o **teste real**: abrir `https://amauryesp-active.web.app/`, entrar com o Google e conferir se carrega sem "Failed to fetch"; conferir também se o endereço do serviço é `automacao-api-1awz.onrender.com` (senão trocar `API_URL` em `fire_page/src/api.js` do projeto original e republicar no Firebase).

34. **Recurso "Vetorização de Imagem Base de Dados" (5 de novembro de 2026, implementado e com build passando; ainda NÃO enviado ao GitHub):**
    - Origem: página `#/aiven_imagens` do site original (`C:\Automaca_Amaury\fire_page`, arquivo `src/inserirImagensDB.jsx`). Versão do portal é **somente visualização** (lista, prévia, baixar); upload e exclusão ficaram de fora de propósito (site público).
    - Onde aparece: no card e na seção de detalhe **Desenvolvimento e Integração DB** (`id: database`), como botão neon "Vetorização de Imagem Base de Dados" (campo `tools` em `FEATURES`, `src/App.jsx`). Ao clicar abre um **painel temporário** (modal) com fundo IoT (`background_iot.jpg` no dark e `background_iot_l.jpg` no light, copiados do original para `img/` e `public/img/`). Ao fechar (✕, Esc ou clique fora) a lista e a imagem saem da memória.
    - Arquivos novos: `src/config.js` (`API_URL = https://automacao-api-0f6w.onrender.com`, usado também pelo "wake" de `src/main.jsx`), `src/dbvision/firebase.js` (config web pública do Firebase `amauryesp-active` + login Google), `src/dbvision/VetorizacaoImagens.jsx` (painel; carregado com `React.lazy`, então o Firebase só baixa ao clicar). Estilos `.tool-link` e `.dbv*` no fim de `src/styles.css`. Dependência nova: `firebase` (o `npm audit` acusa 4 avisos em `@grpc/grpc-js`/firestore, que o portal não usa; não rodar `npm audit fix --force`).
    - API: dados de `GET /aiven/imagens` e `GET /aiven/imagens/{id}` (exigem login Google + `EMAIL_PERMITIDO`). Em `api_render/main.py` o CORS ganhou `https://automationprojects.top`, `https://www.automationprojects.top` e `https://amaurysimoes.github.io`.
    - **Segurança:** havia um `.env` (senhas Aiven/Neon) na raiz deste repositório público, fora do `.gitignore`. Corrigido: `.gitignore` agora ignora `.env`, `.env.*` e `__pycache__`. Conferido que o `.env` nunca entrou no histórico do Git.
    - **Para funcionar em produção falta (nesta ordem):** (a) commit e push (só quando o proprietário pedir) para publicar o portal e fazer o Render atualizar o CORS; (b) no Firebase Console → Authentication → Settings → **Authorized domains**, adicionar `automationprojects.top` (e `amaurysimoes.github.io`); sem isso o popup do Google falha; (c) cadastrar `EMAIL_PERMITIDO` no grupo `automacao-env` do Render (sem ele a API recusa todo login); (d) testar no portal: clicar no botão, entrar com Google, ver a lista. Testar também localmente com `npm run dev` (`http://localhost:5173` já está no CORS).
    - Pendente do site original: trocar `API_URL` em `fire_page/src/api.js` para o endereço `automacao-api-0f6w` e republicar no Firebase.

35. **Cabeçalho reformulado (5 de novembro de 2026, build passando; não enviado ao GitHub):** "Entrar" virou **"Login para Códigos"** (corrigido o acento do pedido "Codigos") e "Participar" virou **"Instruções Site"**; ambos ainda apontam para `#recursos` (sem destino definido). O seletor de tema foi para o **canto direito** (último item do cabeçalho). O botão de 3 linhas agora aparece **em todas as telas** e abre um **painel lateral** (`.media-panel`, `src/App.jsx`) com miniaturas em duas listas: "Imagens operacionais" e "Vídeos de uso" (vídeos com ícone de play). Os itens vêm da constante `MEDIA_ITEMS`, hoje **provisória**: reaproveita as imagens dos cards como miniaturas e marca "em breve"; quando o proprietário fornecer imagens e vídeos reais, trocar `thumb` e transformar o item em link/reprodutor. No celular (≤860px) o menu "Projetos Exemplo / Teste e Downloads" fica dentro desse painel. Fecha com Esc, clique fora ou ✕. O botão "Login para Códigos" some em ≤860px e "Instruções Site" em ≤600px (comportamento herdado).

36. **Painel sem login (5 de novembro de 2026, build passando; não enviado ao GitHub):** a pedido do proprietário ("por enquanto não exige login"; o erro vinha de "Este e-mail não tem permissão", pois `EMAIL_PERMITIDO` não está cadastrado), o painel "Vetorização de Imagem Base de Dados" **não usa mais login**. Em `api_render/main.py` **somente** `GET /aiven/imagens` e `GET /aiven/imagens/{id}` ficaram abertas (comentário "TEMPORÁRIO" no código; para voltar a exigir login, acrescentar `_=Depends(usuario)` nas duas). **Todas as outras rotas (SQL, exclusão, envio, Neon, ITs) continuam exigindo login** — não abrir a API inteira. Consequências: `src/dbvision/firebase.js` foi apagado e a dependência `firebase` removida (o `npm audit` agora dá 0 vulnerabilidades); o item (b) do passo 34 (domínios autorizados no Firebase) e o (c) (`EMAIL_PERMITIDO`) **deixam de ser necessários para o portal** (continuam necessários para o site original). Para valer no ar: commit e push (o Render redeploya a API sozinho) e esperar o deploy. Qualquer pessoa que abra o portal passa a poder ver/baixar as imagens da tabela `ia_imagens`.

37. **Botão só na seção de detalhe (5 de novembro de 2026):** o botão "Vetorização de Imagem Base de Dados" foi **removido do card da grade** (`#recursos`) e permanece **somente na seção de detalhe** de "Desenvolvimento e Integração DB" (acima do bloco "Em desenvolvimento"). Isso corrige o item 34, que dizia "no card e na seção de detalhe". O `tools` em `FEATURES` continua sendo a fonte do botão.

## Histórico de commits enviados

| Commit | Mensagem |
| --- | --- |
| `ba01788` | Criar página inicial em React |
| `9aa446f` | Documentar recriação manual do projeto |
| `b869e81` | Ajustar documentação do projeto |
| `f6710c5` | Configurar publicação no GitHub Pages |
| `586a4e7` | Documentar publicação do projeto |
| `d7b888d` | Esclarecer publicação do site como página web |
| `6c04bdf` | Preparar domínio personalizado para o site |
| `eec3456` | Registrar histórico e continuidade do projeto |
| `3765831` | Aplicar identidade visual do ícone oficial |
| `4e5cc47` | Reorganizar página em seções com imagem de fundo e cards de projetos |
| `b3e3d95` | update |
| `04d18eb` | Update |
| `3350b04` | Adicionar cards Programação Desk e Integração DB e atualizar histórico do projeto |
| `cfa7faf` | Registrar envio dos cards no histórico do projeto |
| `8c89b75` | Aplicar imagem de fundo nos painéis e ajustar texto do último card |

O histórico é aditivo; não reescrever/amendar commits existentes.

## Estado confirmado na última verificação

- Branch local `main`, sincronizada com `origin/main` após o envio dos itens 28 a 31 (`img/iotfire.jpg` continua sem uso). O commit mais recente é `8c89b75` (mais um commit só de registro no histórico).
- O build `npm run build` passou antes do envio.
- Deploys conferidos: o do commit `cfa7faf` terminou com sucesso. O deploy dos itens 30 e 31 ainda não foi conferido (verificar em **Actions**).
- Deploy do commit `4e5cc47` falhou por timeout na etapa de publicação; o deploy do commit seguinte (`b3e3d95`) terminou com sucesso. Nada foi conferido depois disso.
- A API do Pages indicava `cname: automationprojects.top` (domínio cadastrado) e `https_enforced: true`. Em 4 de novembro de 2026 o DNS já apontava para os IPs do GitHub Pages (185.199.x.x), mas `https://automationprojects.top/` ainda não respondia (certificado pendente) e o `http` devolvia 403. Como o `github.io` redireciona os arquivos do site para o domínio, o site pode aparecer quebrado até o certificado sair. **Consultar novamente antes de concluir qualquer coisa.**
- Não registrar, incluir ou expor credenciais, tokens ou segredos neste arquivo.

## Pendências conhecidas

- Confirmar que `https://automationprojects.top/` abre o site novo e ativar **Enforce HTTPS** quando disponível; opcionalmente criar `CNAME` `www` → `amaurysimoes.github.io`.
- Definir a imagem do último card ("Em Desenvolvimento...", hoje `pci.jpg`) e o conteúdo real das seções de detalhe (hoje com bloco cinza "Em desenvolvimento").
- Definir o conteúdo da seção "Testes e Download" e o destino dos botões "Entrar" e "Participar".
- Decidir o uso de `img/iotfire.jpg`.
- Limpar CSS sem uso (estilos de planos, depoimentos, FAQ, logos, avatares e aviso do hero) e atualizar `EstruturaProjeto.md`/`README.md` para a página atual.
- O ano do copyright está fixo no código.
- **Integração do backend (em andamento):** `api_render/` já está neste repositório público (código visível, senhas não). Resta terminar o serviço no Render (ver item 33; Root Directory `api_render`, Build `pip install -r requirements.txt`, Start `uvicorn main:app --host 0.0.0.0 --port $PORT`, Health Check `/saude`, `PYTHON_VERSION=3.12.3`) e cadastrar no painel do Render as variáveis `AIVEN_HOST`, `AIVEN_PORT`, `AIVEN_USER`, `AIVEN_PASSWORD`, `AIVEN_DB_NAME`, `NEON_HOST`, `NEON_PORT`, `NEON_USER`, `NEON_PASSWORD`, `NEON_DB_NAME`, `NEON_SSLMODE`, `EMAIL_PERMITIDO` (opcionais: `NEON_DB_SCHEMA`, `FIREBASE_PROJECT`). Se o endereço do Render mudar, trocar `API_URL` em `fire_page/src/api.js` (projeto original) e republicar o site no Firebase.
- **Plano de downloads (decisão em 5 de novembro de 2026, ainda não executado):** vai entrar no projeto um sistema com parte Python e parte Firebase web, a ser desmembrado por partes e ligado à seção "Testes e Download". Hospedagem do executável: **GitHub Releases** no próprio repositório `Amaury_Automation` (grátis, link direto, até 2 GB por arquivo); não usar Google Drive (aviso de vírus em arquivos grandes, sem link direto). Não é preciso criar outro repositório agora; só vale criar um repositório separado se o código do projeto Python precisar de histórico próprio ou ficar privado (este repositório é público). Publicar o executável em `.zip`, com o hash SHA-256 e um aviso na página sobre o alerta do Windows (executável sem assinatura). Antes de colocar qualquer código do projeto no repositório, **ler o conteúdo e remover chaves, credenciais e arquivos de conta de serviço**; nada dentro de `public/` deve conter segredos, pois tudo ali é publicado no site. Os projetos podem ficar em pastas dentro deste repositório (por exemplo `projetos/<nome>/`), fora de `public/` e `src/`.

## Comandos usuais para continuar

### Rodar localmente

```powershell
Set-Location 'C:\Dev-AHS\Amaury_Automation'
npm ci
npm run dev
```

Abrir `http://localhost:5173`. Encerrar com `Ctrl+C` (no Windows responder `s` à pergunta sobre finalizar o arquivo em lotes).

### Validar produção

```powershell
npm run build
npm run preview
```

### Enviar novas alterações

```powershell
git status
npm run build
git add -A
git commit -m "Descrever a alteração"
git push
```

O push para `main` inicia o deploy do GitHub Pages. Conferir na aba **Actions** ou:

```powershell
gh run list --workflow deploy.yml --limit 5
```

Se o `git add .` for seguido de `git commit` e o Git disser que há arquivos não preparados, algum arquivo foi gravado pelo editor depois do `add`; salvar tudo e repetir com `git add -A`.

Não versionar `node_modules` ou `dist` (estão no `.gitignore`). Não usar `git push --force`; primeiro `git pull --rebase`.

## Orientação para futuras alterações

- Manter React + Vite; não trocar a stack sem pedido.
- **Atualizar este arquivo a cada alteração** (regra permanente acima).
- Preservar a paleta acordada, a menos que haja pedido para alterá-la; usar o token `--neon` para efeitos neon.
- Tratar `#2B3CF5` de `img/circuito-azul.svg` como azul oficial; sincronizar `public/img/circuito-azul.svg`, o favicon, o ícone da página e os tokens ao atualizar a identidade.
- Ao mexer em estilos, imagens ou dependências, conferir o comportamento local e executar `npm run build`.
- Imagem nova ou substituída: copiar de `img/` para `public/img/`.
- Ao alterar publicação, manter coerentes o `base` do Vite, `public/CNAME`, workflow e instruções.
- Atualizar a documentação técnica quando o processo de criação, execução ou publicação mudar.
- Commits descritivos, sem atribuições de ferramentas, e nunca incluir segredos.
