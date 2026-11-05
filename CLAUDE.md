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
   | Em Desenvolvimento (`em-desenvolvimento-3`) | `pci.jpg` | Aplicação em Desenvolvimento |

4. **Tópico "Testes e Download"** (`#teste-downloads`): título pequeno, discreto, alinhado à esquerda (`.topic`). Sem conteúdo ainda.
5. **Seções de detalhe**: uma por card, geradas da mesma lista `FEATURES` (título, descrição, bloco cinza em degradê com o símbolo `circuito-cinza.svg` e o texto "Em desenvolvimento", e o link "← Voltar aos projetos" para `#recursos`).
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
│   └── img/ (circuito-azul.svg, circuito-cinza.svg, placeholder.svg, background_projeto.jpg,
│            iot.jpg, automacao.jpg, webmob.jpg, desk.jpg, database.jpg, pci.jpg)
├── img/ (originais das imagens acima)
├── src/
│   ├── App.jsx
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

O histórico é aditivo; não reescrever/amendar commits existentes.

## Estado confirmado na última verificação

- Branch local `main`, sincronizada com `origin/main` após o commit `3350b04` (itens 28 e 29 já enviados, junto com `img/iotfire.jpg`, que continua sem uso). Um commit seguinte registra apenas este histórico.
- O build `npm run build` passou antes do envio.
- O deploy do commit `3350b04` ainda não foi conferido (verificar em **Actions**).
- Deploy do commit `4e5cc47` falhou por timeout na etapa de publicação; o deploy do commit seguinte (`b3e3d95`) terminou com sucesso. Nada foi conferido depois disso.
- A API do Pages indicava `cname: automationprojects.top` (domínio cadastrado) e `https_enforced: true`. Em 4 de novembro de 2026 o DNS já apontava para os IPs do GitHub Pages (185.199.x.x), mas `https://automationprojects.top/` ainda não respondia (certificado pendente) e o `http` devolvia 403. Como o `github.io` redireciona os arquivos do site para o domínio, o site pode aparecer quebrado até o certificado sair. **Consultar novamente antes de concluir qualquer coisa.**
- Não registrar, incluir ou expor credenciais, tokens ou segredos neste arquivo.

## Pendências conhecidas

- Confirmar que `https://automationprojects.top/` abre o site novo e ativar **Enforce HTTPS** quando disponível; opcionalmente criar `CNAME` `www` → `amaurysimoes.github.io`.
- Definir imagem e texto do último card "Em Desenvolvimento" e o conteúdo real das seções de detalhe (hoje com bloco cinza "Em desenvolvimento").
- Definir o conteúdo da seção "Testes e Download" e o destino dos botões "Entrar" e "Participar".
- Decidir o uso de `img/iotfire.jpg`.
- Limpar CSS sem uso (estilos de planos, depoimentos, FAQ, logos, avatares e aviso do hero) e atualizar `EstruturaProjeto.md`/`README.md` para a página atual.
- O ano do copyright está fixo no código.

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
