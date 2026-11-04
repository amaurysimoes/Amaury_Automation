# Estrutura do projeto — Vite + React

Este guia explica como criar manualmente esta página web do zero usando **JavaScript, React e Vite**.

A referência visual é somente a paleta escura do projeto `C:\Dev-AHS\IA_automation_front`: fundo `#212121`, texto `#ececec`, superfície `#1f2937`, fundo secundário `#171717` e borda `#2d2d2d`. O azul oficial é `#2B3CF5`, extraído de `img/circuito-azul.svg`. A página mostra “Projetos em Desenvolvimento.” e “Amaury Huerb”.

## 1. Pré-requisitos

- Windows e PowerShell.
- Node.js instalado (Node 20 ou compatível com a versão de Vite instalada).
- npm, que acompanha o Node.js.
- Editor de código, como VS Code.

Confirme as instalações:

```powershell
node --version
npm --version
```

## 2. Criar o projeto React com Vite

Para criar o projeto nesta pasta:

```powershell
Set-Location 'C:\Dev-AHS\Amaury_Automation'
npm create vite@latest . -- --template react
npm install
```

O comando `npm create vite@latest` inicia o scaffolding do Vite; `--template react` seleciona React com JavaScript. Se preferir criar primeiro uma subpasta, use:

```powershell
Set-Location 'C:\Dev-AHS'
npm create vite@latest Amaury_Automation -- --template react
Set-Location '.\Amaury_Automation'
npm install
```

Se o Vite avisar que a pasta já contém arquivos, confirme que está no local correto antes de continuar e não sobrescreva arquivos importantes.

## 3. Estrutura de arquivos

Organize os arquivos principais assim:

```text
Amaury_Automation/
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
├── .gitignore
├── README.md
├── EstruturaProjeto.md
├── img/
│   ├── circuito-azul.svg
│   └── circuito-cinza.svg
├── public/
│   ├── CNAME
│   └── img/
│       ├── circuito-azul.svg
│       └── circuito-cinza.svg
└── src/
    ├── App.jsx
    ├── main.jsx
    └── styles.css
```

- `index.html`: documento HTML e elemento raiz onde o React será montado.
- `src/main.jsx`: entrada JavaScript, imports e montagem do React.
- `src/App.jsx`: componente da página inicial.
- `src/styles.css`: paleta, layout, tipografia e responsividade.
- `package.json`: dependências e comandos npm.
- `vite.config.js`: configuração do Vite e plugin React.
- `package-lock.json`: versões resolvidas pelo npm; mantenha-o no Git.
- `.gitignore`: arquivos gerados/localmente que não devem ser enviados ao Git.
- `img/circuito-azul.svg`: ícone oficial; seu azul `#2B3CF5` é usado nos destaques.
- `public/img/`: cópias dos ícones servidas pelo Vite, incluindo favicon e imagem da página.

## 4. Configurar `package.json`

O Vite gerado pelo modelo React já cria este arquivo. Confira que os scripts e dependências estão presentes. Uma configuração equivalente é:

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

As versões que o Vite gerar podem ser diferentes. O `package-lock.json` deve corresponder ao `package.json`; depois de editar dependências, execute `npm install`.

## 5. Configurar `vite.config.js`

O plugin habilita o suporte do Vite a React e JSX:

```js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
```

## 6. Configurar `index.html`

Defina português do Brasil, metadados, título da aba e o ponto de montagem:

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
    <link rel="icon" type="image/svg+xml" href="./img/circuito-azul.svg" />
    <title>Projetos em Desenvolvimento | Amaury Huerb</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

## 7. Criar a entrada React em `src/main.jsx`

Importe o componente e o CSS, e monte a aplicação no elemento `root`:

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

## 8. Criar a página em `src/App.jsx`

O componente inicial tem um título principal e a assinatura. `aria-hidden` marca os elementos meramente decorativos para que leitores de tela os ignorem:

```jsx
function App() {
  return (
    <main className="landing">
      <div className="landing__glow" aria-hidden="true" />
      <section className="intro" aria-labelledby="page-title">
        <img
          className="intro__logo"
          src="./img/circuito-azul.svg"
          alt=""
          aria-hidden="true"
        />
        <span className="intro__accent" aria-hidden="true" />
        <h1 id="page-title">Projetos em Desenvolvimento.</h1>
        <p className="intro__name">Amaury Huerb</p>
      </section>
    </main>
  );
}

export default App;
```

## 9. Estilizar em `src/styles.css`

Declare as cores no `:root` para manter o tema consistente e fácil de alterar:

```css
:root {
  color: #ececec;
  background: #212121;

  --background: #212121;
  --surface: #1f2937;
  --surface-muted: #171717;
  --text: #ececec;
  --text-muted: #a1a1aa;
  --border: #2d2d2d;
  --accent: #2B3CF5;
}
```

Complete o CSS seguindo estas etapas:

1. Aplique `box-sizing: border-box` globalmente e remova a margem padrão do `body`.
2. Dê ao `body` e ao `#root` altura mínima de `100vh`, usando `var(--background)` como fundo.
3. Torne `.landing` uma grade CSS com `place-items: center`, `min-height: 100vh` e espaçamento interno para telas pequenas.
4. Desenhe a grade decorativa usando gradientes lineares no pseudo-elemento `body::before`.
5. Desenhe o brilho azul decorativo em `.landing__glow` com um gradiente radial.
6. Centralize o conteúdo de `.intro`; use `clamp()` no título para adaptar o tamanho da fonte à largura da tela.
7. Use `var(--accent)` no detalhe azul e `var(--text-muted)` na assinatura.
8. Use uma media query (por exemplo, `max-width: 520px`) para ajustar espaçamentos em telas estreitas.

O CSS completo da página está no arquivo `src/styles.css`. Os tokens de superfície e borda ficam declarados para reutilização ao adicionar futuras seções.

## 10. Executar no navegador

Instale as dependências (se ainda não instalou) e inicie o servidor local:

```powershell
npm install
npm run dev
```

Abra no navegador o endereço informado pelo Vite, normalmente `http://localhost:5173`. Para encerrar, use `Ctrl+C` no terminal.

## 11. Validar o build

Crie o build de produção e, se quiser, visualize-o localmente:

```powershell
npm run build
npm run preview
```

O Vite gera os arquivos finais em `dist/`. Essa pasta é criada pelo build e não deve ser adicionada ao Git.

## 12. Preparar e enviar ao GitHub

O remoto informado para este projeto é `https://github.com/amaurysimoes/Amaury_Automation.git`. Antes de enviar:

```powershell
Set-Location 'C:\Dev-AHS\Amaury_Automation'
npm run build
git status
```

Se ainda não houver Git inicializado nesta pasta:

```powershell
git init
git add .
git commit -m "Criar página inicial em React"
git branch -M main
git remote add origin https://github.com/amaurysimoes/Amaury_Automation.git
git push -u origin main
```

Se o repositório já estiver inicializado, confira o remoto antes de adicioná-lo:

```powershell
git remote -v
```

Se não existir um remoto chamado `origin`, adicione-o e envie:

```powershell
git remote add origin https://github.com/amaurysimoes/Amaury_Automation.git
git add .
git commit -m "Criar página inicial em React"
git branch -M main
git push -u origin main
```

Autentique-se pelo Git/GitHub quando solicitado. Não salve tokens ou senhas nos arquivos do projeto. Se o GitHub já tiver commits que não existem localmente, sincronize os históricos antes de enviar; não use `git push --force`.

## 13. Onde fazer alterações futuras

- Conteúdo da página: `src/App.jsx`.
- Cores, tipografia, layout e responsividade: `src/styles.css`.
- Título da aba, idioma e descrição: `index.html`.
- Dependências e comandos: `package.json`.
- Após alterar: confira com `npm run dev`, valide com `npm run build`, revise com `git status`, faça commit e então envie com `git push`.
