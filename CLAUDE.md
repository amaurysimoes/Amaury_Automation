# Histórico e continuidade do projeto

Este arquivo registra o contexto técnico, as decisões, as alterações e o estado atual do projeto para que o trabalho possa continuar em outra sessão.

## Projeto

- Nome: **Amaury Automation**.
- Pasta local: `C:\Dev-AHS\Amaury_Automation`.
- Repositório GitHub: `https://github.com/amaurysimoes/Amaury_Automation`.
- Branch de trabalho/publicação: `main`.
- Stack: JavaScript, React e Vite; não é um projeto Python.
- Objetivo atual: portal para organizar vários projetos, mantendo a área de conteúdo preparada para módulos que serão definidos posteriormente.
- Layout atual: página única em seções, seguindo apenas a estrutura de `https://master.dev/join/` (cabeçalho com navegação, hero, planos em três grupos, recursos incluídos, logos, depoimentos, FAQ e rodapé). Textos, marca, cores e código do template não são copiados; todo o conteúdo é provisório e as imagens são cinzas.
- O tema dark é predominante e o padrão. O seletor deslizante permite light, persiste a escolha em `localStorage` e sincroniza abas abertas do mesmo site.
- Referência de estilo: `C:\Dev-AHS\IA_automation_front`. Foi solicitada apenas a paleta escura, sem copiar componentes, imagens ou funcionalidades.
- Paleta atual (tokens em `src/styles.css`, tema dark): fundo `#17191f`, barra/seções alternadas `#13151a`, superfície `#1d2028`, texto `#edf0f7` e azul oficial `#2B3CF5` (extraído do ícone `img/circuito-azul.svg`). A paleta inicial `#212121`/`#ececec` foi substituída na evolução do layout.
- Imagens provisórias: `public/img/placeholder.svg` (cinza). Cada `<img class="placeholder">` em `src/App.jsx` deve ter seu `src` trocado pela imagem final.
- Preferência de apresentação do projeto: documentação e commits devem ser escritos como documentação normal do projeto, sem atribuições ou comentários sobre ferramentas de assistência.

## Estrutura atual

```text
Amaury_Automation/
├── .github/
│   └── workflows/
│       └── deploy.yml
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
│   └── img/
│       ├── circuito-azul.svg
│       ├── circuito-cinza.svg
│       └── placeholder.svg
├── img/
│   ├── circuito-azul.svg
│   └── circuito-cinza.svg
├── src/
│   ├── App.jsx
│   ├── main.jsx
│   └── styles.css
└── vite.config.js
```

### Arquivos importantes

- `src/App.jsx`: página em seções (cabeçalho com menu responsivo e seletor de tema, hero, planos, recursos, logos, depoimentos, FAQ e rodapé). Os dados das seções ficam em constantes no topo do arquivo.
- `src/main.jsx`: aplica o tema salvo antes da montagem do React, importa o CSS e monta a página em `#root`.
- `src/styles.css`: tokens de tema (dark por padrão e light), seletor, componentes das seções e responsividade (breakpoints 860px e 600px).
- `index.html`: HTML inicial, idioma `pt-BR`, metadados, favicon oficial e título da aba.
- `package.json`: dependências e comandos `dev`, `build` e `preview`.
- `package-lock.json`: lockfile npm; manter versionado e usar `npm ci` em instalação limpa.
- `vite.config.js`: configuração Vite e caminho relativo `base: './'`, para funcionar no GitHub Pages com domínio próprio.
- `public/CNAME`: contém exatamente `automationprojects.top`; durante o build, Vite copia para `dist/CNAME`.
- `img/circuito-azul.svg`: arquivo original do ícone oficial azul fornecido para o projeto. A cópia em `public/img` é disponibilizada no site e usada na página e como favicon.
- `img/circuito-cinza.svg`: variação cinza fornecida, mantida para uso futuro.
- `.github/workflows/deploy.yml`: build e deploy automáticos do GitHub Pages a cada push para `main`, além de execução manual (`workflow_dispatch`).
- `DocumentacaoTecnica/EstruturaProjeto.md`: guia detalhado para recriar manualmente o projeto do zero.
- `EstruturaProjeto.md`: guia introdutório semelhante na raiz. A cópia da pasta `DocumentacaoTecnica` é a documentação mais completa.
- `DocumentacaoTecnica/Atualizar_Git.md`: passos breves para enviar atualizações ao GitHub.
- `DocumentacaoTecnica/Git_Push.md`: instruções de configuração inicial do remoto e primeiro push.
- `DocumentacaoTecnica/PublicarGit.md`: publicação do site pelo GitHub Pages e configuração do domínio personalizado.
- `README.md`: apresentação e comandos básicos para rodar e gerar o build.

## Histórico de decisões e alterações

1. Foi solicitada uma página inicial Vite + React com aparência escura, aproveitando somente as cores do projeto de referência. O texto definido foi “Projetos em Desenvolvimento.” e “Amaury Huerb”.
2. A pasta de trabalho inicialmente continha apenas `DocumentacaoTecnica/Git_Push.txt`; não havia projeto Vite nem repositório Git local.
3. Foi criado o projeto web mínimo com React e Vite, sem dependências visuais desnecessárias. A página recebeu fundo `#212121`, texto claro e destaque azul, com grade sutil, brilho azul, centralização e ajustes para telas pequenas.
4. Foram adicionados `.gitignore`, `README.md`, arquivos Vite/React e documentação para execução e build.
5. A solicitação para documentar a recriação manual do projeto foi atendida em `DocumentacaoTecnica/EstruturaProjeto.md`; também há uma cópia resumida na raiz. O guia contém pré-requisitos, scaffolding Vite, conteúdo dos arquivos, execução, build, Git e publicação.
6. O projeto foi inicializado em Git, configurado com remoto `origin` para `https://github.com/amaurysimoes/Amaury_Automation.git`, e enviado para a branch `main`.
7. Foram criados guias separados para atualizar o Git e publicar o site como página web.
8. A publicação foi configurada via GitHub Pages e GitHub Actions. O workflow instala Node.js 22, executa `npm ci`, executa `npm run build`, faz upload de `dist` e implanta usando `actions/deploy-pages`.
9. O endereço planejado para o site passou do endereço padrão do Pages para o domínio próprio `automationprojects.top`.
10. Para suportar o domínio, `vite.config.js` foi alterado para `base: './'` e `public/CNAME` foi criado com o domínio.
11. `DocumentacaoTecnica/PublicarGit.md` documenta o DNS esperado, o cadastro em **Settings → Pages → Custom domain**, HTTPS, o fluxo de deploy, diagnóstico e publicação de futuras atualizações.
12. Foi solicitado que os arquivos e commits não tenham atribuições ou comentários de ferramentas de assistência. Não adicionar essas atribuições aos novos commits.
13. Foram fornecidos `img/circuito-azul.svg` e `img/circuito-cinza.svg`. O azul do ícone oficial é exatamente `#2B3CF5`; foi adotado como cor de destaque, no brilho e favicon. Os SVGs são copiados para `public/img` para que o Vite os inclua no build; o ícone azul também é exibido na página inicial.
14. A cor oficial azul foi aplicada ao token de destaque, aos efeitos de brilho, ao ícone exibido na página e ao favicon. Os SVGs originais e suas cópias em `public/img` permanecem no repositório.
15. Foi adicionado um botão deslizante para alternar entre tema escuro e claro. A escolha persiste em `localStorage`, atualiza a cor da barra do navegador e sincroniza outras abas abertas. O tema escuro continua sendo o padrão para primeiras visitas.
16. A página inicial evoluiu para uma workspace original, inspirada apenas na organização geral de uma interface de trabalho: sidebar responsiva, breadcrumb, seletor de tema e área vazia para projetos futuros. O conteúdo e a implementação são próprios; a logo já existente é mantida na navegação.
17. A identidade visual do ícone oficial foi aplicada (commit `3765831`).
18. O layout foi reorganizado conforme a estrutura do template `master.dev/join`, substituindo a sidebar/workspace por uma página única com seções. Imagens substituídas por placeholders cinza (`public/img/placeholder.svg`) a serem trocados depois. O texto “Projetos em Desenvolvimento” foi mantido como título do hero.

## Histórico de commits já enviados

Todos estes commits foram enviados para `origin/main`:

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

O commit `ba01788` também incluiu `DocumentacaoTecnica/Git_Push.md`, que já existia no workspace e tinha o URL e os comandos iniciais de GitHub fornecidos para o repositório. O histórico é aditivo; não reescrever/amendar commits existentes.

## Estado confirmado na última verificação

- Branch local: `main`.
- Remoto: `origin` → `https://github.com/amaurysimoes/Amaury_Automation.git`.
- A branch local estava sincronizada com `origin/main` antes de criar este histórico.
- O build `npm run build` passou após a configuração do domínio personalizado.
- O deploy do commit `6c04bdf` no workflow **Deploy to GitHub Pages** terminou com sucesso.
- A configuração Pages consultada pela API do GitHub indicava `build_type: workflow`, `https_enforced: true`, porém `cname: null`; portanto o domínio personalizado ainda não havia sido cadastrado nas configurações do repositório.
- A última consulta DNS encontrou `automationprojects.top A → 208.115.225.220`, que não é um IP do GitHub Pages. O domínio, portanto, ainda não estava direcionado a este site.
- O último status DNS confirmado foi em 4 de novembro de 2026. Consultar novamente antes de tirar conclusões sobre o estado atual.
- Não registrar, incluir ou expor credenciais, tokens ou segredos neste arquivo.

## O que falta para o domínio próprio funcionar

1. No painel do provedor que gerencia o DNS de `automationprojects.top`, substituir o registro `A` atual (`208.115.225.220`) pelos quatro registros abaixo. Remover registros conflitantes para o host `@`, incluindo registros AAAA antigos se houver:

   | Tipo | Host | Valor |
   | --- | --- | --- |
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |

2. Opcionalmente, para `www.automationprojects.top`, criar `CNAME`, host `www`, apontando para `amaurysimoes.github.io`.
3. No GitHub, abrir `https://github.com/amaurysimoes/Amaury_Automation/settings/pages`, informar `automationprojects.top` no campo **Custom domain** e salvar. A API ainda mostrava `cname: null` na última consulta; essa etapa precisa ser verificada.
4. Aguardar propagação do DNS e emissão/validação do certificado HTTPS. Ativar **Enforce HTTPS** quando o GitHub disponibilizar a opção.
5. Confirmar que `https://automationprojects.top/` abre o site. Propagação DNS pode demorar; consultar novamente DNS antes de diagnosticar.

Os registros A do provedor não foram alterados pelo projeto. A troca pode interromper qualquer serviço que ainda esteja usando o IP antigo `208.115.225.220`; verificar isso com o proprietário do domínio antes de alterá-los.

## Comandos usuais para continuar

### Rodar localmente

```powershell
Set-Location 'C:\Dev-AHS\Amaury_Automation'
npm ci
npm run dev
```

Abrir o endereço local mostrado pelo Vite, normalmente `http://localhost:5173`. Encerrar com `Ctrl+C`.

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

O push para `main` inicia o deploy do GitHub Pages. Conferir a execução na aba **Actions** ou, se o GitHub CLI estiver disponível e autenticado:

```powershell
gh run list --workflow deploy.yml --limit 5
```

Não versionar `node_modules` ou `dist` (ambos estão no `.gitignore`). Não usar `git push --force` para resolver divergências; primeiro sincronizar com `git pull --rebase` e tratar eventuais conflitos.

## Orientação para futuras alterações

- Manter React + Vite; não trocar a stack sem pedido.
- Preservar o texto inicial e a paleta acordada, a menos que haja solicitação para alterá-los.
- Tratar `#2B3CF5` do SVG `img/circuito-azul.svg` como azul oficial; sincronizar `public/img/circuito-azul.svg`, o favicon, o ícone da página, os tokens e os exemplos de CSS/documentação ao atualizar a identidade.
- Ao mexer em estilos ou dependências, conferir o comportamento local e executar `npm run build`.
- Ao alterar publicação, manter coerentes o `base` do Vite, `public/CNAME`, workflow e instruções.
- Atualizar a documentação técnica quando o processo de criação, execução ou publicação mudar.
- Fazer commits descritivos, sem atribuições de ferramentas, e nunca incluir segredos.