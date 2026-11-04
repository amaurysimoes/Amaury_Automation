# Publicar o site como página web

Este guia explica como deixar o projeto acessível como um site na internet usando o GitHub Pages. O endereço publicado é:

**https://amaurysimoes.github.io/Amaury_Automation/**

O GitHub Actions cria e publica o site automaticamente sempre que a branch `main` recebe um `push`. Não é necessário enviar a pasta `dist` manualmente.

## 1. Abrir o projeto

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

## 2. Conferir o site antes de publicar

Instale dependências caso seja a primeira vez neste computador ou se o `package-lock.json` mudou:

```powershell
npm ci
```

Gere o build de produção:

```powershell
npm run build
```

Se o build falhar, corrija os erros antes de continuar. A pasta `dist` é gerada automaticamente e não precisa ser adicionada ao Git.

## 3. Publicar ou atualizar o site

Para a primeira publicação, confirme uma vez que o GitHub Pages está configurado:

1. Abra as configurações Pages do repositório: `https://github.com/amaurysimoes/Amaury_Automation/settings/pages`.
2. Em **Build and deployment**, selecione **GitHub Actions** como origem.
3. Salve a configuração, se solicitado.

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

Esse envio inicia o workflow em `.github/workflows/deploy.yml`. Ele instala as dependências, executa `npm run build` e publica o conteúdo de `dist` no GitHub Pages. O endereço do site não muda:

```text
https://amaurysimoes.github.io/Amaury_Automation/
```

## 4. Acompanhar a publicação

No repositório, abra a aba **Actions**, selecione a execução mais recente de **Deploy to GitHub Pages** e aguarde build e deploy terminarem com sucesso. Também é possível consultar pelo PowerShell, se o GitHub CLI (`gh`) estiver instalado e autenticado:

```powershell
gh run list --workflow deploy.yml --limit 5
```

Após o sucesso, abra o endereço do site. A atualização pode levar alguns minutos para aparecer; atualize o navegador se necessário.

## 5. Se a publicação falhar

- **Build falhou:** confira o log do trabalho em **Actions**, corrija o problema localmente, rode `npm run build` e faça novo commit e push.
- **Pages não está configurado:** em **Settings** → **Pages**, escolha **GitHub Actions** como origem.
- **Página em branco ou arquivos não carregam:** confirme que `vite.config.js` contém `base: '/Amaury_Automation/'` e que o deploy mais recente terminou com sucesso.
- **Push recusado:** use `git pull --rebase`, resolva conflitos com cuidado e tente enviar novamente; não use `git push --force`.
- **Autenticação solicitada:** autentique-se pelo Git Credential Manager ou pelo GitHub CLI. Nunca coloque senhas ou tokens em arquivos do projeto.

## 6. Resumo para publicar cada atualização

Depois de editar o projeto, execute sempre:

```powershell
Set-Location 'C:\Dev-AHS\Amaury_Automation'
npm run build
git status
git add -A
git commit -m "Descreva a alteração"
git push
```

O push inicia a publicação do site automaticamente. Acompanhe a execução na aba **Actions** e confira o resultado em `https://amaurysimoes.github.io/Amaury_Automation/`.