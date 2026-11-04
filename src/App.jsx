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
