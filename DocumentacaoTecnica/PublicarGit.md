# Publicar o site como página web

Este guia explica como deixar o projeto acessível como um site na internet usando o GitHub Pages e o domínio personalizado `automationprojects.top`.

**https://automationprojects.top/**

O GitHub Actions cria e publica o site automaticamente sempre que a branch `main` recebe um `push`. Não é necessário enviar a pasta `dist` manualmente.

## 1. Configurar o domínio no provedor DNS

No painel onde o domínio `automationprojects.top` foi registrado, abra o gerenciamento de DNS e configure os registros para o GitHub Pages. Para o domínio raiz, crie estes quatro registros `A`:

| Tipo | Nome/Host | Valor/Aponta para |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |

Opcionalmente, para que `www.automationprojects.top` também funcione, crie:

| Tipo | Nome/Host | Valor/Aponta para |
| --- | --- | --- |
| CNAME | `www` | `amaurysimoes.github.io` |

Remova ou edite registros `A`, `AAAA` ou CNAME conflitantes para o mesmo host. A consulta feita antes da configuração mostrou que o registro `A` atual do domínio raiz aponta para `208.115.225.220`; ele precisa ser substituído pelos endereços do GitHub Pages para que o domínio abra este site. Alterar DNS pode interromper qualquer site que ainda esteja usando o endereço antigo. A propagação pode levar até 24 horas.

## 2. Cadastrar o domínio no GitHub Pages

1. Abra `https://github.com/amaurysimoes/Amaury_Automation/settings/pages`.
2. Em **Custom domain**, informe `automationprojects.top` e salve.
3. Aguarde a verificação de DNS. Quando a opção **Enforce HTTPS** estiver disponível, habilite-a.

O arquivo `public/CNAME` contém `automationprojects.top`. O workflow copia esse arquivo para a raiz publicada, preservando a configuração do domínio em cada deploy.

## 3. Abrir o projeto

Abra o PowerShell e entre na pasta do projeto:

```powershell
Set-Location 'C:\Dev-AHS\Amaury_Automation'
```

Confirme que a branch e o remoto estão corretos:

```powershell
git status
git branch --show-current
git remote -v
```

O remoto esperado é:

```text
https://github.com/amaurysimoes/Amaury_Automation.git
```

Se `origin` não estiver configurado, adicione-o uma única vez:

```powershell
git remote add origin https://github.com/amaurysimoes/Amaury_Automation.git
```

## 4. Conferir o site antes de publicar

Instale dependências caso seja a primeira vez neste computador ou se o `package-lock.json` mudou:

```powershell
npm ci
```

Gere o build de produção:

```powershell
npm run build
```

Se o build falhar, corrija os erros antes de continuar. A pasta `dist` é gerada automaticamente e não precisa ser adicionada ao Git.

## 5. Publicar ou atualizar o site

Em **Settings** → **Pages**, mantenha **GitHub Actions** como origem de build e deploy. Essa configuração é necessária para o workflow automático.

Depois, sempre que quiser publicar uma versão nova do site, envie as alterações para a branch `main`:

Confira quais arquivos foram alterados:

```powershell
git status
```

Adicione as alterações, crie um commit descritivo e envie:

```powershell
git add -A
git commit -m "Descreva a alteração"
git push
```

Exemplo de mensagem:

```powershell
git commit -m "Atualizar página inicial"
```

Se o Git informar que não há alterações para commit, nada novo precisa ser enviado. Se `git push` for recusado por haver alterações no remoto, não use `--force`; primeiro atualize sua cópia:

```powershell
git pull --rebase
```

Resolva eventuais conflitos nos arquivos indicados, continue o rebase se solicitado e depois tente `git push` novamente.

Esse envio inicia o workflow em `.github/workflows/deploy.yml`. Ele instala as dependências, executa `npm run build` e publica o conteúdo de `dist` no GitHub Pages. O endereço personalizado é:

```text
https://automationprojects.top/
```

## 6. Acompanhar a publicação

No repositório, abra a aba **Actions**, selecione a execução mais recente de **Deploy to GitHub Pages** e aguarde build e deploy terminarem com sucesso. Também é possível consultar pelo PowerShell, se o GitHub CLI (`gh`) estiver instalado e autenticado:

```powershell
gh run list --workflow deploy.yml --limit 5
```

Após o sucesso e a propagação do DNS, abra `https://automationprojects.top/`. A primeira configuração do DNS pode levar até 24 horas; atualizações posteriores do site normalmente aparecem em alguns minutos.

## 7. Se a publicação falhar

- **Build falhou:** confira o log do trabalho em **Actions**, corrija o problema localmente, rode `npm run build` e faça novo commit e push.
- **Pages não está configurado:** em **Settings** → **Pages**, escolha **GitHub Actions** como origem e confira o domínio personalizado.
- **Domínio não abre:** confira se os quatro registros `A` do domínio raiz apontam para os IPs do GitHub Pages e se não há registros conflitantes.
- **Página em branco ou arquivos não carregam:** confirme que `vite.config.js` contém `base: './'` e que o deploy mais recente terminou com sucesso.
- **Push recusado:** use `git pull --rebase`, resolva conflitos com cuidado e tente enviar novamente; não use `git push --force`.
- **Autenticação solicitada:** autentique-se pelo Git Credential Manager ou pelo GitHub CLI. Nunca coloque senhas ou tokens em arquivos do projeto.

## 8. Resumo para publicar cada atualização

Depois de editar o projeto, execute sempre:

```powershell
Set-Location 'C:\Dev-AHS\Amaury_Automation'
npm run build
git status
git add -A
git commit -m "Descreva a alteração"
git push
```

O push inicia a publicação do site automaticamente. Acompanhe a execução na aba **Actions** e confira o resultado em `https://automationprojects.top/`.