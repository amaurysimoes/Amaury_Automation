# Publicar o projeto no GitHub

Este guia explica como enviar atualizações do projeto para o GitHub e publicar o site no GitHub Pages sem ajuda.

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

## 2. Testar antes de publicar

Instale dependências caso seja a primeira vez neste computador ou se o `package-lock.json` mudou:

```powershell
npm ci
```

Gere o build de produção:

```powershell
npm run build
```

Se o build falhar, corrija os erros antes de continuar. A pasta `dist` é gerada automaticamente e não precisa ser adicionada ao Git.

## 3. Enviar uma atualização para o GitHub

Confira quais arquivos foram alterados:

```powershell
git status
```

Adicione as alterações, crie um commit descritivo e envie a branch `main`:

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

## 4. Publicação automática do site

O repositório está configurado para publicar o site pelo GitHub Actions. Cada `git push` para `main` inicia automaticamente um fluxo que:

1. instala as dependências;
2. executa `npm run build`;
3. publica o conteúdo da pasta `dist` no GitHub Pages.

O workflow está em `.github/workflows/deploy.yml`. O Vite já está configurado com a base `/Amaury_Automation/`, necessária para este endereço de projeto no Pages.

Na primeira publicação, confirme no GitHub:

1. Abra `https://github.com/amaurysimoes/Amaury_Automation`.
2. Acesse **Settings** → **Pages**.
3. Em **Build and deployment**, selecione **GitHub Actions** como origem.
4. Salve a configuração, se o GitHub solicitar.

Após o workflow concluir com sucesso, o site estará em:

```text
https://amaurysimoes.github.io/Amaury_Automation/
```

## 5. Conferir o andamento da publicação

No GitHub, abra a aba **Actions**, selecione a execução mais recente de **Deploy to GitHub Pages** e aguarde os trabalhos de build e deploy terminarem com sucesso. Também é possível consultar o estado pelo PowerShell, se o GitHub CLI (`gh`) estiver instalado e autenticado:

```powershell
gh run list --workflow deploy.yml --limit 5
```

Depois de uma execução bem-sucedida, abra o endereço do Pages acima. Pode levar alguns minutos para a nova versão aparecer; atualize o navegador se necessário.

## 6. Se a publicação falhar

- **Build falhou:** confira o log do trabalho em **Actions**, corrija o problema localmente, rode `npm run build` e faça novo commit e push.
- **Pages não está configurado:** em **Settings** → **Pages**, escolha **GitHub Actions** como origem.
- **Página em branco ou arquivos não carregam:** confirme que `vite.config.js` contém `base: '/Amaury_Automation/'` e que o deploy mais recente terminou com sucesso.
- **Push recusado:** use `git pull --rebase`, resolva conflitos com cuidado e tente enviar novamente; não use `git push --force`.
- **Autenticação solicitada:** autentique-se pelo Git Credential Manager ou pelo GitHub CLI. Nunca coloque senhas ou tokens em arquivos do projeto.

## 7. Resumo para cada atualização

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