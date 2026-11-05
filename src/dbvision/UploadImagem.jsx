import { useEffect, useState } from 'react';
import { API_URL } from '../config.js';
import { auth, aoMudarLogin, entrar, sair } from './firebase.js';

// Upload de imagem para a tabela ia_imagens (Aiven). Exige login Google: a API só aceita o e-mail do dono.
// Igual ao projeto original (inserirImagensDB.jsx): o navegador reduz o lado máximo, comprime em WebP e envia.

const kb = (n) => (n >= 1048576 ? `${(n / 1048576).toFixed(2)} MB` : `${(n / 1024).toFixed(1)} KB`);

async function sha256(file) {
  const hash = await crypto.subtle.digest('SHA-256', await file.arrayBuffer());
  return [...new Uint8Array(hash)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

// Reduz até maxSide (mantém a proporção, só diminui) e comprime em WebP.
async function compress(file, quality, maxSide) {
  const bitmap = await createImageBitmap(file);
  const factor = Math.min(1, maxSide / Math.max(bitmap.width, bitmap.height));
  const width = Math.round(bitmap.width * factor);
  const height = Math.round(bitmap.height * factor);
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  canvas.getContext('2d').drawImage(bitmap, 0, 0, width, height);
  const blob = await new Promise((done) => canvas.toBlob(done, 'image/webp', quality / 100));
  return { blob, width, height };
}

const toBase64 = (blob) =>
  new Promise((done) => {
    const reader = new FileReader();
    reader.onload = () => done(reader.result.split(',')[1]);
    reader.readAsDataURL(blob);
  });

export default function UploadImagem({ onSent }) {
  const [user, setUser] = useState(undefined); // undefined = verificando; null = sem login
  const [file, setFile] = useState(null);
  const [quality, setQuality] = useState(80);
  const [maxSide, setMaxSide] = useState(1600);
  const [result, setResult] = useState(null); // {blob, width, height, url}
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => aoMudarLogin(setUser), []);

  // Recomprime ao mudar arquivo, qualidade ou lado máximo.
  useEffect(() => {
    if (!file) return undefined;
    let alive = true;
    let url = null;
    compress(file, quality, maxSide).then((r) => {
      if (!alive) return;
      url = URL.createObjectURL(r.blob);
      setResult({ ...r, url });
    });
    return () => {
      alive = false;
      if (url) URL.revokeObjectURL(url);
    };
  }, [file, quality, maxSide]);

  async function send() {
    setBusy(true);
    setMessage('Enviando… (se a API estava dormindo, pode levar até 1 minuto)');
    try {
      const body = {
        nome_arquivo: file.name,
        largura: result.width,
        altura: result.height,
        qualidade: quality,
        tamanho_original_bytes: file.size,
        sha256: await sha256(file),
        dados_base64: await toBase64(result.blob),
      };
      const response = await fetch(`${API_URL}/aiven/imagens`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${await auth.currentUser.getIdToken()}`,
        },
        body: JSON.stringify(body),
      });
      if (!response.ok) {
        let detail = `Erro ${response.status}`;
        try {
          detail = (await response.json()).detail || detail;
        } catch {
          /* sem JSON */
        }
        throw new Error(detail);
      }
      setMessage(`${file.name}: ${kb(file.size)} → ${kb(result.blob.size)}. Enviada.`);
      setFile(null);
      setResult(null);
      onSent();
    } catch (error) {
      setMessage(`Erro: ${error.message}`);
    } finally {
      setBusy(false);
    }
  }

  if (user === undefined) return <p className="dbv__muted">Verificando o login…</p>;

  if (user === null) {
    return (
      <div className="dbv__login">
        <p>O envio de imagens grava no banco: entre com a conta Google do dono do projeto.</p>
        <button
          className="dbv__btn dbv__btn--primary"
          type="button"
          onClick={() => entrar().catch((error) => setMessage(`Erro no login: ${error.message}`))}
        >
          Entrar com Google
        </button>
        {message && <p className="dbv__message">{message}</p>}
      </div>
    );
  }

  return (
    <div className="dbv__upload">
      <div className="dbv__form">
        <span>Imagem</span>
        <input
          type="file"
          accept="image/*"
          onChange={(event) => {
            setFile(event.target.files[0] || null);
            setResult(null);
          }}
        />
        <span>Qualidade: {quality}</span>
        <input
          type="range"
          min="40"
          max="99"
          value={quality}
          onChange={(event) => setQuality(+event.target.value)}
        />
        <span>Lado máximo (px)</span>
        <input
          type="number"
          min="64"
          max="8000"
          value={maxSide}
          onChange={(event) => setMaxSide(+event.target.value || 1600)}
        />
      </div>

      {result && (
        <>
          <p className="dbv__muted">
            {file.name}: {kb(file.size)} → <b>{kb(result.blob.size)}</b> ({result.width}×{result.height}, WebP)
          </p>
          <img className="dbv__upload-preview" src={result.url} alt="Prévia da imagem comprimida" />
        </>
      )}

      <div className="dbv__toolbar">
        <button className="dbv__btn dbv__btn--primary" type="button" disabled={!result || busy} onClick={send}>
          Enviar para o banco
        </button>
        <button className="dbv__btn" type="button" onClick={sair}>
          Sair
        </button>
      </div>
      {message && <p className="dbv__message">{message}</p>}
    </div>
  );
}
