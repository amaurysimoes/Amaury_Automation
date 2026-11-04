# Recriar o projeto do zero — Vite + React

Este guia permite recriar manualmente a página inicial deste repositório usando **JavaScript, React e Vite**.

A página apresenta “Projetos em Desenvolvimento.” e “Amaury Huerb”. Do projeto `C:\Dev-AHS\IA_automation_front` é usada somente a paleta escura: fundo `#212121`, texto `#ececec`, azul `#3b82f6`, superfície `#1f2937`, fundo secundário `#171717` e borda `#2d2d2d`.

## 1. Pré-requisitos

- Windows, PowerShell e um editor de código (por exemplo, VS Code).
- Node.js 20.19+ ou 22.12+ e npm.

Confira as instalações:

```powershell
node --version
npm --version
```

## 2. Criar o projeto React com Vite

No PowerShell:

```powershell
Set-Location 'C:\Dev-AHS\Amaury_Automation'
npm create vite@latest . -- --template react
```

Esse comando cria um projeto Vite usando o modelo React com JavaScript. Se a pasta não estiver vazia, escolha **Ignore files and continue** para preservar arquivos existentes; não escolha apagar arquivos. Em uma pasta nova, crie-a primeiro e execute o mesmo comando dentro dela.

Instale as dependências:

```powershell
npm install
```

## 3. Estrutura final

```text
Amaury_Automation/
├── .gitignore
├── index.html
├── package.json
├── package-lock.json       # Gerado por npm install
├── vite.config.js
├── README.md
├── DocumentacaoTecnica/
│   └── EstruturaProjeto.md
└── src/
    ├── App.jsx
    ├── main.jsx
    └── styles.css
```

Se necessário, crie `src`:

```powershell
New-Item -ItemType Directory -Force -Path '.\src'
```

Nos passos a seguir, crie/substitua cada arquivo usando o editor. O `package-lock.json` é gerado pelo npm e não deve ser escrito à mão.

## 4. `package.json`

Ele define dependências e comandos. Após salvar, execute `npm install` para gerar/atualizar o lockfile.

```json
{
  "name": "amaury-automation",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.2.7",
    "react-dom": "^19.2.7"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^6.0.2",
    "vite": "^8.1.0"
  }
}
```

## 5. `vite.config.js`

O plugin habilita o processamento de componentes JSX pelo Vite:

```js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
```

## 6. `index.html`

Este HTML define idioma, metadados, título da aba e ponto de montagem do React:

```html
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="theme-color" content="#212121" />
    <meta
      name="description"
      content="Projetos em desenvolvimento de Amaury Huerb."
    />
    <title>Projetos em Desenvolvimento | Amaury Huerb</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

## 7. `src/App.jsx`

O componente principal mostra o título e a assinatura. `aria-hidden` marca os elementos decorativos:

```jsx
function App() {
  return (
    <main className="landing">
      <div className="landing__glow" aria-hidden="true" />
      <section className="intro" aria-labelledby="page-title">
        <span className="intro__accent" aria-hidden="true" />
        <h1 id="page-title">Projetos em Desenvolvimento.</h1>
        <p className="intro__name">Amaury Huerb</p>
      </section>
    </main>
  );
}

export default App;
```

## 8. `src/main.jsx`

Este é o ponto de entrada: importa React, a página e o CSS, e monta o componente no `root`:

```jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
```

## 9. `src/styles.css`

O CSS completo controla a paleta, a grade de fundo, o brilho azul e a adaptação a telas menores:

```css
:root {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
  color: #ececec;
  background: #212121;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  --background: #212121;
  --surface: #1f2937;
  --surface-muted: #171717;
  --text: #ececec;
  --text-muted: #a1a1aa;
  --border: #2d2d2d;
  --accent: #3b82f6;
}

* {
  box-sizing: border-box;
}

body {
  min-width: 320px;
  min-height: 100vh;
  margin: 0;
  background: var(--background);
}

body::before {
  position: fixed;
  z-index: 0;
  inset: 0;
  background-image:
    linear-gradient(to right, rgb(255 255 255 / 2.2%) 1px, transparent 1px),
    linear-gradient(to bottom, rgb(255 255 255 / 2.2%) 1px, transparent 1px);
  background-size: 64px 64px;
  content: "";
  mask-image: linear-gradient(to bottom, black, transparent 85%);
  pointer-events: none;
}

#root {
  min-height: 100vh;
}

.landing {
  position: relative;
  display: grid;
  min-height: 100vh;
  overflow: hidden;
  place-items: center;
  padding: 48px 24px;
  isolation: isolate;
}

.landing__glow {
  position: absolute;
  z-index: -1;
  top: 50%;
  left: 50%;
  width: min(76vw, 820px);
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgb(59 130 246 / 12%) 0,
    rgb(59 130 246 / 4%) 38%,
    transparent 70%
  );
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.intro {
  width: min(100%, 900px);
  text-align: center;
}

.intro__accent {
  display: block;
  width: 52px;
  height: 3px;
  margin: 0 auto 30px;
  border-radius: 999px;
  background: var(--accent);
  box-shadow: 0 0 24px rgb(59 130 246 / 65%);
}

.intro h1 {
  margin: 0;
  color: var(--text);
  font-size: clamp(2.5rem, 7vw, 5.5rem);
  font-weight: 650;
  letter-spacing: -0.065em;
  line-height: 1.08;
  text-wrap: balance;
}

.intro__name {
  margin: 26px 0 0;
  color: var(--text-muted);
  font-size: clamp(1rem, 2vw, 1.2rem);
  font-weight: 400;
  letter-spacing: 0.12em;
}

@media (max-width: 520px) {
  .landing {
    padding-inline: 22px;
  }

  .intro__accent {
    margin-bottom: 24px;
  }

  .intro__name {
    margin-top: 20px;
  }
}
```

## 10. `.gitignore` e `README.md`

Use este `.gitignore` para não versionar dependências ou arquivos de build:

```gitignore
node_modules/
dist/
*.local
.DS_Store
Thumbs.db
```

Um `README.md` inicial:

````markdown
# Amaury Automation

Página inicial para reunir projetos em desenvolvimento, criada com React e Vite.

## Executar localmente

```powershell
npm install
npm run dev
```

## Gerar build de produção

```powershell
npm run build
npm run preview
```
````

## 11. Executar e validar

Na pasta do projeto, instale os pacotes e inicie o servidor local:

```powershell
npm install
npm run dev
```

Abra o endereço mostrado pelo Vite no terminal (normalmente `http://localhost:5173`). Confira a página em uma janela normal e em uma janela estreita. Pare o servidor com `Ctrl+C`.

Valide também o build de produção:

```powershell
npm run build
npm run preview
```

Os arquivos de produção ficam em `dist`. Essa pasta e `node_modules` são geradas localmente e estão excluídas do Git pelo `.gitignore`.

## 12. Publicar no GitHub pela primeira vez

O remoto deste projeto é `https://github.com/amaurysimoes/Amaury_Automation.git`. Antes de publicar, faça um build e confira o que será versionado:

```powershell
Set-Location 'C:\Dev-AHS\Amaury_Automation'
npm run build
git status
```

Se ainda não existe Git nesta pasta e o repositório GitHub está vazio:

```powershell
git init
git add -A
git commit -m "Criar página inicial em React"
git branch -M main
git remote add origin https://github.com/amaurysimoes/Amaury_Automation.git
git push -u origin main
```

Se Git já estiver inicializado, não repita `git init`. Confira os remotos:

```powershell
git remote -v
```

Se não houver `origin`, adicione-o com `git remote add origin https://github.com/amaurysimoes/Amaury_Automation.git`; depois use `git add -A`, `git commit -m "Descreva a atualização"` e `git push`. Não inclua senhas ou tokens em arquivos. Se o remoto já tiver commits que não existem localmente, sincronize os históricos antes de enviar; nunca use `git push --force` para contornar a divergência.

## 13. Fazer alterações futuras

- Conteúdo da página: `src/App.jsx`.
- Cores, layout e responsividade: `src/styles.css`.
- Título e metadados: `index.html`.
- Dependências e comandos: `package.json`.
- Depois de alterar: execute `npm run dev`, confira no navegador e rode `npm run build`.
- Para publicar: consulte `DocumentacaoTecnica/Atualizar_Git.md`.