# Histórico e continuidade do projeto

Este arquivo registra o contexto técnico, as decisões, as alterações e o estado atual do projeto para que o trabalho possa continuar em outra sessão.

## Projeto

- Nome: **Amaury Automation**.
- Pasta local: `C:\Dev-AHS\Amaury_Automation`.
- Repositório GitHub: `https://github.com/amaurysimoes/Amaury_Automation`.
- Branch de trabalho/publicação: `main`.
- Stack: JavaScript, React e Vite; não é um projeto Python.
- Objetivo inicial: página web de apresentação simples com fundo escuro e os textos “Projetos em Desenvolvimento.” e “Amaury Huerb”, para acrescentar outros projetos posteriormente.
- Referência de estilo: `C:\Dev-AHS\IA_automation_front`. Foi solicitada apenas a paleta escura, sem copiar componentes, imagens ou funcionalidades.
- Paleta adotada: fundo `#212121`, texto `#ececec`, azul `#3b82f6`, superfície `#1f2937`, fundo secundário `#171717` e borda `#2d2d2d`.
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
│   └── CNAME
├── src/
│   ├── App.jsx
│   ├── main.jsx
│   └── styles.css
└── vite.config.js
```

### Arquivos importantes

- `src/App.jsx`: componente da página inicial, título, assinatura e elementos decorativos.
- `src/main.jsx`: importa o componente e CSS e monta o React em `#root`.
- `src/styles.css`: paleta, grade de fundo, brilho azul, tipografia, layout e media query para telas estreitas.
- `index.html`: HTML inicial, idioma `pt-BR`, metadados e título da aba.
- `package.json`: dependências e comandos `dev`, `build` e `preview`.
- `package-lock.json`: lockfile npm; manter versionado e usar `npm ci` em instalação limpa.
- `vite.config.js`: configuração Vite e caminho relativo `base: './'`, para funcionar no GitHub Pages com domínio próprio.
- `public/CNAME`: contém exatamente `automationprojects.top`; durante o build, Vite copia para `dist/CNAME`.
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
- Ao mexer em estilos ou dependências, conferir o comportamento local e executar `npm run build`.
- Ao alterar publicação, manter coerentes o `base` do Vite, `public/CNAME`, workflow e instruções.
- Atualizar a documentação técnica quando o processo de criação, execução ou publicação mudar.
- Fazer commits descritivos, sem atribuições de ferramentas, e nunca incluir segredos.