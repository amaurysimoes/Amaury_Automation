import { useEffect, useRef, useState } from 'react';
import { onValue, ref, update } from 'firebase/database';
import { db } from '../dbvision/firebase.js';

// Automação Firebase: lista os ESPs registrados em esps/<nome> e aciona os pinos.
// O ESP se registra sozinho quando liga (firmware gravado pelo app Python em automacao_esp);
// este painel só lista e aciona. Online = renovou "visto_em" há menos de 30 s.
const ONLINE_MS = 30000;
const isOnline = (esp, now) =>
  !!esp && esp.ativo !== false && typeof esp.visto_em === 'number' && now - esp.visto_em < ONLINE_MS;

export default function PinosESP({ onClose }) {
  const [esps, setEsps] = useState({});
  const [selected, setSelected] = useState(null);
  const [now, setNow] = useState(Date.now());
  const [error, setError] = useState('');
  const closeRef = useRef(null);

  useEffect(() => {
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    closeRef.current?.focus();
    const onKey = (event) => event.key === 'Escape' && onClose();
    window.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener('keydown', onKey);
    };
  }, [onClose]);

  // Assina o banco só enquanto o painel está aberto.
  useEffect(() => {
    const off = onValue(
      ref(db, 'esps'),
      (snap) => setEsps(snap.val() || {}),
      (err) => setError(err.message || String(err)),
    );
    const timer = setInterval(() => setNow(Date.now()), 5000);
    return () => {
      off();
      clearInterval(timer);
    };
  }, []);

  const names = Object.keys(esps).sort();
  const current = selected && esps[selected] ? selected : null;
  const esp = current ? esps[current] : null;
  const pins = esp?.pinos || {};

  // O ESP aberto caiu: volta para a lista (onde ele aparece desabilitado).
  useEffect(() => {
    if (current && !isOnline(esps[current], now)) setSelected(null);
  }, [now, esps, current]);

  const fail = (err) => setError(err.message || String(err));
  const toggle = (gpio, state) =>
    update(ref(db, `esps/${current}/pinos/${gpio}`), { estado: !state }).catch(fail);
  const pulse = (gpio) => update(ref(db, `esps/${current}/pinos/${gpio}`), { pulso: true }).catch(fail);

  return (
    <div className="dbv" role="dialog" aria-modal="true" aria-labelledby="esp-title">
      <div className="dbv__backdrop" onClick={onClose} />
      <div className="dbv__panel esp">
        <header className="dbv__head">
          <div>
            <p className="dbv__eyebrow">Firebase · Realtime Database · esps</p>
            <h2 id="esp-title">Automação Firebase</h2>
          </div>
          <div className="dbv__head-actions">
            <button
              ref={closeRef}
              className="dbv__btn dbv__btn--close"
              type="button"
              aria-label="Fechar painel"
              onClick={onClose}
            >
              ✕
            </button>
          </div>
        </header>

        <div className="dbv__body">
          {!current ? (
            <>
              <p className="dbv__muted">
                Clique num ESP online para abrir os pinos. O ESP aparece sozinho quando liga.
              </p>
              <ul className="esp__list">
                {names.length === 0 && (
                  <li className="esp__empty">Nenhum ESP ainda. Grave um pelo app Python (Automação FireBase).</li>
                )}
                {names.map((name) => {
                  const on = isOnline(esps[name], now);
                  return (
                    <li key={name}>
                      <button
                        type="button"
                        className="esp__item"
                        disabled={!on}
                        onClick={() => setSelected(name)}
                      >
                        <span>
                          <span className={`esp__dot${on ? ' is-on' : ''}`} /> <b>{name}</b>
                        </span>
                        <span className="dbv__muted">
                          {on ? `${esps[name].ip || '—'} · ${esps[name].modelo || '—'}` : 'offline'}
                        </span>
                      </button>
                    </li>
                  );
                })}
              </ul>
              <div className="esp__download">
                <p className="dbv__muted">
                  Quer gravar o seu próprio ESP? Baixe o programa Python e siga o manual (Python, VS Code,
                  .env, executável, gravação e acesso pelo Firebase).
                </p>
                <div className="esp__download-actions">
                  <a className="dbv__btn dbv__btn--primary" href="./downloads/automacao_esp.zip" download>
                    Baixar projeto Python (.zip)
                  </a>
                  <a className="dbv__btn" href="./manual-automacao-esp.html" target="_blank" rel="noopener">
                    Manual passo a passo ↗
                  </a>
                </div>
              </div>
            </>
          ) : (
            <>
              <div className="dbv__toolbar">
                <button className="dbv__btn" type="button" onClick={() => setSelected(null)}>
                  ← Lista de ESPs
                </button>
                <span className="dbv__muted">
                  <span className="esp__dot is-on" /> <b>{current}</b>
                  {esp.ip ? ` — ${esp.ip}` : ''}
                  {typeof esp.vcc === 'number' ? ` · ${esp.vcc.toFixed(2)} V` : ''}
                </span>
              </div>
              <ul className="esp__list">
                {Object.keys(pins).length === 0 && (
                  <li className="esp__empty">Este ESP ainda não informou pinos.</li>
                )}
                {Object.entries(pins).map(([gpio, pin]) => (
                  <li key={gpio} className="esp__pin">
                    <span>
                      <b>{pin.nome || `Pino ${gpio}`}</b> <span className="dbv__muted">GPIO {gpio}</span>
                    </span>
                    {pin.tipo === 'entrada' ? (
                      <span className="esp__actions">
                        <span className="dbv__muted">Entrada</span>
                        <span className={`esp__badge${pin.estado ? ' is-on' : ''}`}>
                          {pin.estado ? 'ON' : 'OFF'}
                        </span>
                      </span>
                    ) : (
                      <span className="esp__actions">
                        <button
                          type="button"
                          className={`dbv__btn${pin.estado ? '' : ' dbv__btn--primary'}`}
                          onClick={() => toggle(gpio, pin.estado)}
                        >
                          {pin.estado ? 'Desligar' : 'Ligar'}
                        </button>
                        <button type="button" className="dbv__btn" onClick={() => pulse(gpio)}>
                          Pulso
                        </button>
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            </>
          )}
          {error && <p className="dbv__message">{error}</p>}
        </div>
      </div>
    </div>
  );
}
