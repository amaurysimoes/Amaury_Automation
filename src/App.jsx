import { useEffect, useState } from 'react';

const THEME_STORAGE_KEY = 'amaury-automation-theme';
const PLACEHOLDER = './img/placeholder.svg';

const NAV_LINKS = ['Trilhas', 'Projetos'];

const FEATURES = [
  {
    title: 'Aplicações IOT',
    image: './img/iot.jpg',
    description: 'Projetos de Integração com dispositivos Residenciais e Móveis.',
  },
  {
    title: 'IA e Automação',
    image: './img/automacao.jpg',
    description: 'Projetos de Automação e Integração de Hardwares com IA',
  },
  {
    title: 'Web e Mobile',
    image: './img/webmob.jpg',
    description: 'Desenvolvimento Back End, Front e App Mobile',
  },
  {
    title: 'Em Desenvolvimento',
    image: './img/pci.jpg',
    description: 'Aplicação em Desenvolvimento',
  },
  {
    title: 'Em Desenvolvimento',
    image: './img/pci.jpg',
    description: 'Aplicação em Desenvolvimento',
  },
  {
    title: 'Em Desenvolvimento',
    image: './img/pci.jpg',
    description: 'Aplicação em Desenvolvimento',
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

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    window.localStorage.setItem(THEME_STORAGE_KEY, theme);

    const themeColor = document.querySelector('meta[name="theme-color"]');
    if (themeColor) {
      themeColor.setAttribute('content', theme === 'dark' ? '#17191f' : '#f4f6fa');
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

          <nav
            className={`site-nav${isMenuOpen ? ' site-nav--open' : ''}`}
            aria-label="Navegação principal"
          >
            {NAV_LINKS.map((link) => (
              <a key={link} href="#recursos" onClick={() => setIsMenuOpen(false)}>{link}</a>
            ))}
          </nav>

          <div className="site-header__actions">
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
            <a className="button button--ghost header-login" href="#recursos">Entrar</a>
            <a className="button button--primary header-join" href="#recursos">Participar</a>
            <button
              className="icon-button site-header__menu"
              type="button"
              aria-label={isMenuOpen ? 'Fechar menu' : 'Abrir menu'}
              aria-expanded={isMenuOpen}
              onClick={() => setIsMenuOpen((open) => !open)}
            >
              <Icon name={isMenuOpen ? 'close' : 'menu'} />
            </button>
          </div>
        </div>
      </header>

      <main id="conteudo">
        <section className="hero" id="top">
          <div className="container hero__inner">
            <h1>Projetos em Desenvolvimento</h1>
          </div>
        </section>

        <section className="section section--alt" id="recursos">
          <div className="container">
            <h2 className="section__title">Projetos</h2>
            <div className="feature-grid">
              {FEATURES.map((feature, index) => (
                <article className="feature" key={index}>
                  {feature.image ? (
                    <img className="placeholder feature__image" src={feature.image} alt="" />
                  ) : (
                    <Placeholder className="feature__image" />
                  )}
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
    </div>
  );
}

export default App;
