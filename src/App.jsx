import { lazy, Suspense, useCallback, useEffect, useState } from 'react';

// Painel temporário carregado só quando é aberto (o Firebase não pesa no carregamento do portal).
const VetorizacaoImagens = lazy(() => import('./dbvision/VetorizacaoImagens.jsx'));
const PinosESP = lazy(() => import('./automacao/PinosESP.jsx'));

const THEME_STORAGE_KEY = 'amaury-automation-theme';
const PLACEHOLDER = './img/placeholder.svg';

const NAV_LINKS = [
  { label: 'Projetos Exemplo', href: '#recursos' },
  { label: 'Teste e Downloads', href: '#teste-downloads' },
];

// Miniaturas provisórias do menu lateral: depois serão trocadas por imagens operacionais e vídeos de uso.
// kind: 'image' | 'video'. thumb: miniatura (por enquanto reaproveita as imagens dos cards).
const MEDIA_ITEMS = [
  { id: 'm1', kind: 'image', title: 'Painel IoT residencial', note: 'Imagem operacional', thumb: './img/iot.jpg' },
  { id: 'm2', kind: 'image', title: 'Automação com IA', note: 'Imagem operacional', thumb: './img/automacao.jpg' },
  { id: 'm3', kind: 'image', title: 'Vetorização de imagens', note: 'Imagem operacional', thumb: './img/database.jpg' },
  { id: 'm4', kind: 'video', title: 'Uso do app web e mobile', note: 'Vídeo de uso', thumb: './img/webmob.jpg' },
  { id: 'm5', kind: 'video', title: 'Aplicação desktop passo a passo', note: 'Vídeo de uso', thumb: './img/desk.jpg' },
  { id: 'm6', kind: 'video', title: 'Novos projetos', note: 'Vídeo de uso', thumb: './img/pci.jpg' },
];

const FEATURES = [
  {
    id: 'iot',
    title: 'Aplicações IOT',
    image: './img/iot.jpg',
    description: 'Projetos de Integração com dispositivos Residenciais e Móveis.',
    tools: [{ id: 'pinos-esp', label: 'AUTOMAÇÃO ESP' }],
  },
  {
    id: 'automacao',
    title: 'IA e Automação',
    image: './img/automacao.jpg',
    description: 'Projetos de Automação e Integração de Hardwares com IA',
  },
  {
    id: 'web-mobile',
    title: 'Web e Mobile',
    image: './img/webmob.jpg',
    description: 'Desenvolvimento Back End, Front e App Mobile',
  },
  {
    id: 'desk',
    title: 'Programação Desk',
    image: './img/desk.jpg',
    description: 'Desenvolvimento e Integração de aplicações Desk',
  },
  {
    id: 'database',
    title: 'Desenvolvimento e Integração DB',
    image: './img/database.jpg',
    description: 'Aplicações Database PostgreSQL e MySQL (Neon e Aiven)',
    tools: [{ id: 'vetorizacao-imagens', label: 'Vetorização de Imagem Base de Dados' }],
  },
  {
    id: 'em-desenvolvimento-3',
    title: 'Em Desenvolvimento...',
    image: './img/pci.jpg',
    description: 'Sempre haverá um novo projeto!',
  },
];

function Icon({ name, size = 18 }) {
  const sharedProps = {
    'aria-hidden': true,
    fill: 'none',
    height: size,
    stroke: 'currentColor',
    strokeLinecap: 'round',
    strokeLinejoin: 'round',
    strokeWidth: 1.7,
    viewBox: '0 0 24 24',
    width: size,
  };

  if (name === 'menu') {
    return (
      <svg {...sharedProps}>
        <path d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    );
  }

  if (name === 'close') {
    return (
      <svg {...sharedProps}>
        <path d="m6 6 12 12M18 6 6 18" />
      </svg>
    );
  }

  if (name === 'database') {
    return (
      <svg {...sharedProps}>
        <ellipse cx="12" cy="5.5" rx="7.5" ry="2.8" />
        <path d="M4.5 5.5v13c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-13M4.5 12c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8" />
      </svg>
    );
  }

  if (name === 'moon') {
    return (
      <svg {...sharedProps}>
        <path d="M20.2 15.1A8.3 8.3 0 0 1 8.9 3.8 8.3 8.3 0 1 0 20.2 15.1Z" />
      </svg>
    );
  }

  if (name === 'sun') {
    return (
      <svg {...sharedProps}>
        <circle cx="12" cy="12" r="4" />
        <path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42" />
      </svg>
    );
  }

  return (
    <svg {...sharedProps}>
      <path d="m5 12.5 4.5 4.5L19 7.5" />
    </svg>
  );
}

function Placeholder({ className = '' }) {
  return <img className={`placeholder ${className}`.trim()} src={PLACEHOLDER} alt="" />;
}

function App() {
  const [theme, setTheme] = useState(() => {
    const savedTheme = window.localStorage.getItem(THEME_STORAGE_KEY);
    return savedTheme === 'light' ? 'light' : 'dark';
  });
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [openTool, setOpenTool] = useState(null);
  const closeTool = useCallback(() => setOpenTool(null), []);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    window.localStorage.setItem(THEME_STORAGE_KEY, theme);

    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (themeColor) {
      themeColor.setAttribute('content', theme === 'dark' ? '#17191f' : '#d5d8df');
    }

    function syncThemeAcrossTabs(event) {
      if (
        event.key === THEME_STORAGE_KEY &&
        (event.newValue === 'dark' || event.newValue === 'light')
      ) {
        setTheme(event.newValue);
      }
    }

    window.addEventListener('storage', syncThemeAcrossTabs);
    return () => window.removeEventListener('storage', syncThemeAcrossTabs);
  }, [theme]);

  useEffect(() => {
    function closeMenuOnEscape(event) {
      if (event.key === 'Escape') {
        setIsMenuOpen(false);
      }
    }

    window.addEventListener('keydown', closeMenuOnEscape);
    return () => window.removeEventListener('keydown', closeMenuOnEscape);
  }, []);

  function toggleTheme() {
    setTheme((currentTheme) => (currentTheme === 'dark' ? 'light' : 'dark'));
  }

  return (
    <div className="page">
      <a className="skip-link" href="#conteudo">Ir para o conteúdo</a>

      <header className="site-header">
        <div className="container site-header__inner">
          <a className="brand" href="#top">
            <img src="./img/circuito-azul.svg" alt="" />
            <span>Amaury<span className="brand__accent">Projects</span></span>
          </a>

          <nav className="site-nav" aria-label="Navegação principal">
            {NAV_LINKS.map((link) => (
              <a key={link.label} href={link.href}>
                {link.label}
              </a>
            ))}
          </nav>

          <div className="site-header__actions">
            <a className="button button--ghost header-login" href="#recursos">Login para Códigos</a>
            <a className="button button--primary header-join" href="#recursos">Instruções Site</a>
            <button
              className="icon-button site-header__menu"
              type="button"
              aria-label={isMenuOpen ? 'Fechar painel de mídia' : 'Abrir painel de mídia'}
              aria-expanded={isMenuOpen}
              aria-controls="painel-midia"
              onClick={() => setIsMenuOpen((open) => !open)}
            >
              <Icon name={isMenuOpen ? 'close' : 'menu'} />
            </button>
            <button
              className="theme-toggle"
              type="button"
              role="switch"
              aria-checked={theme === 'light'}
              aria-label={`Modo ${theme === 'dark' ? 'escuro' : 'claro'} ativado. Alternar para modo ${theme === 'dark' ? 'claro' : 'escuro'}`}
              onClick={toggleTheme}
            >
              <span className="theme-toggle__label" aria-hidden="true">
                {theme === 'dark' ? 'Escuro' : 'Claro'}
              </span>
              <span className="theme-toggle__track" aria-hidden="true">
                <span className="theme-toggle__thumb">
                  <Icon name={theme === 'dark' ? 'moon' : 'sun'} size={12} />
                </span>
              </span>
            </button>
          </div>
        </div>
      </header>

      {isMenuOpen && (
        <>
          <button
            className="media-backdrop"
            type="button"
            aria-label="Fechar painel de mídia"
            onClick={() => setIsMenuOpen(false)}
          />
          <aside className="media-panel" id="painel-midia" aria-label="Imagens operacionais e vídeos de uso">
            <nav className="media-panel__links" aria-label="Navegação principal">
              {NAV_LINKS.map((link) => (
                <a key={link.label} href={link.href} onClick={() => setIsMenuOpen(false)}>
                  {link.label}
                </a>
              ))}
            </nav>
            {['image', 'video'].map((kind) => (
              <section key={kind}>
                <h2 className="media-panel__title">
                  {kind === 'image' ? 'Imagens operacionais' : 'Vídeos de uso'}
                </h2>
                <ul className="media-list">
                  {MEDIA_ITEMS.filter((item) => item.kind === kind).map((item) => (
                    <li className="media-item" key={item.id}>
                      <span className="media-item__thumb">
                        <img src={item.thumb} alt="" loading="lazy" />
                        {kind === 'video' && (
                          <span className="media-item__play" aria-hidden="true">
                            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                              <path d="M8 5.5v13l11-6.5z" />
                            </svg>
                          </span>
                        )}
                      </span>
                      <span className="media-item__text">
                        <strong>{item.title}</strong>
                        <small>{item.note} · em breve</small>
                      </span>
                    </li>
                  ))}
                </ul>
              </section>
            ))}
          </aside>
        </>
      )}

      <main id="conteudo">
        <section className="hero" id="top">
          <div className="container hero__inner">
            <p className="hero__tag">Projetos e Automação</p>
          </div>
        </section>

        <section className="section section--alt" id="recursos">
          <div className="container">
            <div className="feature-grid">
              {FEATURES.map((feature, index) => (
                <article className="feature" key={index}>
                  {(() => {
                    const image = feature.image ? (
                      <img className="placeholder feature__image" src={feature.image} alt="" />
                    ) : (
                      <Placeholder className="feature__image" />
                    );

                    return (
                      <a
                        className="feature__link"
                        href={`#${feature.id}`}
                        aria-label={`Ir para ${feature.title}`}
                      >
                        {image}
                      </a>
                    );
                  })()}
                  <h3>{feature.title}</h3>
                  <p>
                    {feature.description ??
                      'Descrição curta do recurso. Substitua pelo texto definitivo.'}
                  </p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="topic" id="teste-downloads">
          <div className="container">
            <h2 className="topic__title">Testes e Download</h2>
          </div>
        </section>

        {FEATURES.map((feature) => (
          <section className="section detail" id={feature.id} key={feature.id}>
            <div className="container">
              <h2 className="section__title">{feature.title}</h2>
              <p className="section__lead">{feature.description}</p>
              <div className={`detail__image detail__soon${feature.tools ? ' detail__soon--content' : ''}`}>
                <img src="./img/circuito-cinza.svg" alt="" />
                {feature.tools?.map((tool) => (
                  <button
                    className="tool-link"
                    type="button"
                    key={tool.id}
                    onClick={() => setOpenTool(tool.id)}
                  >
                    <Icon name="database" size={16} />
                    <span>{tool.label}</span>
                    <span className="tool-link__arrow" aria-hidden="true">→</span>
                  </button>
                ))}
                {!feature.tools && <span>Em desenvolvimento</span>}
              </div>
              <a className="detail__back" href="#recursos">← Voltar aos projetos</a>
            </div>
          </section>
        ))}
      </main>

      <footer className="site-footer">
        <div className="container">
          <div className="site-footer__top">
            <a className="brand" href="#top">
              <img src="./img/circuito-azul.svg" alt="" />
              <span>Amaury<span className="brand__accent">Projects</span></span>
            </a>
          </div>
          <div className="site-footer__bottom">
            <span>Copyright © 2026 Amaury Huerb Simões</span>
          </div>
        </div>
      </footer>

      {openTool === 'pinos-esp' && (
        <Suspense fallback={null}>
          <PinosESP onClose={closeTool} />
        </Suspense>
      )}

      {openTool === 'vetorizacao-imagens' && (
        <Suspense fallback={null}>
          <VetorizacaoImagens onClose={closeTool} />
        </Suspense>
      )}
    </div>
  );
}

export default App;
