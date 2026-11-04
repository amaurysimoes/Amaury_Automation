# Atualizar o projeto no GitHub

Depois de alterar o projeto, abra o PowerShell na pasta:

```powershell
Set-Location 'C:\Dev-AHS\Amaury_Automation'
```

Confira as alterações e valide o build:

```powershell
git status
npm run build
```

Adicione as alterações, crie um commit com uma mensagem curta e envie para o GitHub:

```powershell
git add -A
git commit -m "Descreva a atualização"
git push
```

Repita esse procedimento a cada atualização. Se `git status` não mostrar alterações, não há nada novo para enviar. Não use `git push --force`.