import { useCallback, useEffect, useRef, useState } from 'react';
import { API_URL } from '../config.js';

// Vetorização de Imagem Base de Dados: painel TEMPORÁRIO, só de visualização, sem login (por enquanto).
// Existe apenas enquanto está aberto: ao fechar, a lista e as imagens saem da memória do navegador.
// Os dados vêm da API no Render (tabela ia_imagens do Aiven); só as rotas de leitura de imagens são abertas.

const formatSize = (bytes) =>
  bytes >= 1048576 ? `${(bytes / 1048576).toFixed(2)} MB` : `${(bytes / 1024).toFixed(1)} KB`;

async function callApi(path, { blob = false } = {}) {
  const response = await fetch(`${API_URL}${path}`);
  if (!response.ok) {
    let message = `Erro ${response.status}`;
    try {
      message = (await response.json()).detail || message;
    } catch {
      /* resposta sem JSON */
    }
    throw new Error(message);
  }
  return blob ? response.blob() : response.json();
}

function toRows(data) {
  const index = Object.fromEntries(data.colunas.map((name, i) => [name, i]));
  return data.linhas.map((row) => ({
    id: row[index.id],
    name: row[index.nome_arquivo],
    width: row[index.largura],
    height: row[index.altura],
    originalBytes: row[index.tamanho_original_bytes],
    finalBytes: row[index.tamanho_final_bytes],
    quality: row[index.qualidade],
    createdAt: row[index.criado_em],
  }));
}

export default function VetorizacaoImagens({ onClose }) {
  const [rows, setRows] = useState(null);
  const [summary, setSummary] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);
  const previewRef = useRef(null);
  const closeRef = useRef(null);

  // Esc fecha; trava a rolagem da página por baixo; foco no botão de fechar.
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

  // Ao fechar o painel, libera a imagem da memória.
  useEffect(() => {
    previewRef.current = previewUrl;
  }, [previewUrl]);
  useEffect(
    () => () => {
      if (previewRef.current) URL.revokeObjectURL(previewRef.current);
    },
    [],
  );

  const load = useCallback(async () => {
    setBusy(true);
    setMessage('Buscando no banco… (se a API estava dormindo, pode levar até 1 minuto)');
    try {
      const data = await callApi('/aiven/imagens');
      setRows(toRows(data));
      setSummary(data.resumo);
      setSelectedId(null);
      setPreviewUrl(null);
      setMessage('');
    } catch (error) {
      setMessage(`Erro: ${error.message}`);
    } finally {
      setBusy(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  async function select(row) {
    setSelectedId(row.id);
    setPreviewUrl(null);
    try {
      const blob = await callApi(`/aiven/imagens/${row.id}`, { blob: true });
      setPreviewUrl(URL.createObjectURL(blob));
    } catch (error) {
      setMessage(`Erro: ${error.message}`);
    }
  }

  function download() {
    const row = rows.find((item) => item.id === selectedId);
    const link = document.createElement('a');
    link.href = previewUrl;
    link.download = `${String(row.name).replace(/\.[^.]+$/, '')}.webp`;
    link.click();
  }

  const selected = rows?.find((row) => row.id === selectedId);

  return (
    <div className="dbv" role="dialog" aria-modal="true" aria-labelledby="dbv-title">
      <div className="dbv__backdrop" onClick={onClose} />
      <div className="dbv__panel">
        <header className="dbv__head">
          <div>
            <p className="dbv__eyebrow">Aiven · MySQL · tabela ia_imagens</p>
            <h2 id="dbv-title">Vetorização de Imagem Base de Dados</h2>
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
          <div className="dbv__toolbar">
            <button className="dbv__btn" type="button" onClick={load} disabled={busy}>
              Atualizar
            </button>
            <button className="dbv__btn" type="button" onClick={download} disabled={!previewUrl}>
              Baixar imagem
            </button>
            {summary && (
              <span className="dbv__muted">
                {summary.quantidade} imagem(ns): {formatSize(summary.original_bytes)} →{' '}
                {formatSize(summary.final_bytes)}
              </span>
            )}
          </div>

          <div className="dbv__content">
            <div className="dbv__table-wrap">
              {rows && rows.length === 0 && <p className="dbv__muted">Nenhuma imagem no banco.</p>}
              {rows && rows.length > 0 && (
                <table className="dbv__table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Arquivo</th>
                      <th>Tamanho</th>
                      <th>Original</th>
                      <th>Final</th>
                      <th>Qual.</th>
                      <th>Criado em</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rows.map((row) => (
                      <tr
                        key={row.id}
                        className={row.id === selectedId ? 'is-selected' : ''}
                        onClick={() => select(row)}
                      >
                        <td>{row.id}</td>
                        <td className="dbv__name" title={row.name}>
                          {row.name}
                        </td>
                        <td>
                          {row.width}×{row.height}
                        </td>
                        <td>{formatSize(row.originalBytes)}</td>
                        <td>{formatSize(row.finalBytes)}</td>
                        <td>{row.quality}</td>
                        <td>{row.createdAt}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>

            <aside className="dbv__preview">
              {previewUrl ? (
                <>
                  <img src={previewUrl} alt={selected?.name ?? 'Imagem selecionada'} />
                  <p className="dbv__muted">{selected?.name}</p>
                </>
              ) : (
                <p className="dbv__muted">
                  {selectedId ? 'Carregando imagem…' : 'Clique em uma linha para ver a imagem.'}
                </p>
              )}
            </aside>
          </div>

          {message && <p className="dbv__message">{message}</p>}
        </div>
      </div>
    </div>
  );
}
