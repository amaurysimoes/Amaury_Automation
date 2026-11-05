"""API do site (fire_page) para os bancos Aiven (MySQL) e Neon (PostgreSQL). Roda no Render.

As senhas ficam nas variáveis de ambiente do Render (mesmos nomes do .env: AIVEN_..., NEON_...), nunca no site.
Toda rota (menos /saude) exige o login Google do site (token do Firebase) com o e-mail de EMAIL_PERMITIDO.

Rodar no PC:  uvicorn main:app --reload   (dentro de api_reder, com as variáveis do .env da raiz)
"""
import base64
import datetime
import decimal
import os
from pathlib import Path

import psycopg2
import pymysql
from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from psycopg2 import sql
from pydantic import BaseModel

from its_xlsx import (
    alinhar_aprovacao, desfazer_larguras, desfazer_mesclagens, envio_finalizar, envio_imagem, envio_iniciar, envio_parte,
    exportar_zip, modelo_json, montar_xlsx, padronizar_aprovacao,
)

AQUI = Path(__file__).resolve().parent
try:  # no PC: lê o .env da raiz do projeto (no Render as variáveis já vêm do painel)
    from dotenv import load_dotenv
    load_dotenv(AQUI.parent / ".env")
except ImportError:
    pass

PROJETO_FIREBASE = os.environ.get("FIREBASE_PROJECT", "amauryesp-active")
EMAIL_PERMITIDO = os.environ.get("EMAIL_PERMITIDO", "").lower()
NEON_SCHEMA = os.environ.get("NEON_DB_SCHEMA") or "public"
LIMITE = 200  # linhas por página, como no gerenciamentoDB.py
TABELA_IMAGENS = "ia_imagens"

app = FastAPI(title="API Automacao Amaury")
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://amauryesp-active.web.app", "https://amauryesp-active.firebaseapp.com",
                   "https://automationprojects.top", "https://www.automationprojects.top",
                   "https://amaurysimoes.github.io", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- login ----------

def usuario(authorization: str = Header(default="")):
    """Confere o token do login Google do site. Só passa o e-mail de EMAIL_PERMITIDO."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Faça login no site.")
    try:
        dados = id_token.verify_firebase_token(authorization[7:], google_requests.Request(), audience=PROJETO_FIREBASE)
    except Exception:
        raise HTTPException(401, "Login inválido ou expirado: entre de novo.")
    email = (dados.get("email") or "").lower()
    if not EMAIL_PERMITIDO or email != EMAIL_PERMITIDO or not dados.get("email_verified"):
        raise HTTPException(403, "Este e-mail não tem permissão.")
    return email


# ---------- conexões ----------

def conectar_aiven():
    return pymysql.connect(
        host=os.environ["AIVEN_HOST"], port=int(os.environ["AIVEN_PORT"]),
        user=os.environ["AIVEN_USER"], password=os.environ["AIVEN_PASSWORD"],
        database=os.environ.get("AIVEN_DB_NAME") or None,
        ssl={"ca": str(AQUI / "ca.pem")}, connect_timeout=15, autocommit=True)


def conectar_neon():
    conn = psycopg2.connect(
        host=os.environ["NEON_HOST"], port=int(os.environ.get("NEON_PORT") or 5432),
        user=os.environ["NEON_USER"], password=os.environ["NEON_PASSWORD"],
        dbname=os.environ["NEON_DB_NAME"], sslmode=os.environ.get("NEON_SSLMODE") or "require", connect_timeout=15)
    conn.autocommit = True
    return conn


def _valor(v):
    """Valor do banco -> JSON (datas e decimais viram texto; binário vira só o tamanho)."""
    if isinstance(v, (bytes, bytearray, memoryview)):
        return f"<{len(bytes(v))} bytes>"
    if isinstance(v, (datetime.date, datetime.time, datetime.timedelta, decimal.Decimal)):
        return str(v)
    return v


def _rodar(conn, comando, params=None):
    """{colunas, linhas, mensagem} de um comando qualquer."""
    with conn.cursor() as cur:
        cur.execute(comando, params)
        if cur.description:
            colunas = [d[0] for d in cur.description]
            linhas = [[_valor(v) for v in linha] for linha in cur.fetchmany(LIMITE)]
            return {"colunas": colunas, "linhas": linhas, "mensagem": f"{len(linhas)} linha(s)"}
        return {"colunas": [], "linhas": [],
                "mensagem": "OK" if cur.rowcount < 0 else f"OK ({cur.rowcount} linha(s) afetada(s))"}


def _erro_banco(e):
    return HTTPException(400, f"{type(e).__name__}: {e}")


class Sql(BaseModel):
    comando: str


@app.get("/saude")
def saude():
    """Sem login: o site chama para acordar a API (no plano grátis ela dorme depois de 15 min)."""
    return {"ok": True}


# ---------- Aiven (MySQL): Gerenciamento Database ----------

def _crase(nome):
    return "`" + nome.replace("`", "``") + "`"


@app.get("/aiven/tabelas")
def aiven_tabelas(_=Depends(usuario)):
    conn = conectar_aiven()
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW TABLES")
            return [r[0] for r in cur.fetchall()]
    finally:
        conn.close()


@app.get("/aiven/tabelas/{tabela}/dados")
def aiven_dados(tabela: str, offset: int = 0, _=Depends(usuario)):
    conn = conectar_aiven()
    try:
        r = _rodar(conn, f"SELECT * FROM {_crase(tabela)} LIMIT %s OFFSET %s", (LIMITE, max(0, offset)))
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {_crase(tabela)}")
            r["total"] = cur.fetchone()[0]
        r["offset"], r["limite"] = max(0, offset), LIMITE
        return r
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.get("/aiven/tabelas/{tabela}/estrutura")
def aiven_estrutura(tabela: str, _=Depends(usuario)):
    conn = conectar_aiven()
    try:
        return _rodar(conn, f"DESCRIBE {_crase(tabela)}")
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.post("/aiven/sql")
def aiven_sql(corpo: Sql, _=Depends(usuario)):
    conn = conectar_aiven()
    try:
        return _rodar(conn, corpo.comando)
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


# ---------- Aiven (MySQL): Vetorizar Imagem Database (tabela ia_imagens) ----------

class Imagem(BaseModel):
    nome_arquivo: str
    largura: int
    altura: int
    qualidade: int
    tamanho_original_bytes: int
    sha256: str          # do arquivo ORIGINAL (a mesma imagem não entra duas vezes)
    dados_base64: str    # a imagem já comprimida em WebP pelo navegador


# TEMPORÁRIO: as duas rotas de LEITURA de imagens abaixo estão abertas (sem login) para o painel público do portal.
# Para voltar a exigir login, acrescente `_=Depends(usuario)` nos parâmetros delas. As demais rotas continuam protegidas.
@app.get("/aiven/imagens")
def aiven_imagens():
    conn = conectar_aiven()
    try:
        lista = _rodar(conn, "SELECT id, nome_arquivo, largura, altura, tamanho_original_bytes, tamanho_final_bytes,"
                             f" qualidade, criado_em FROM {_crase(TABELA_IMAGENS)} ORDER BY id DESC LIMIT %s", (LIMITE,))
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*), COALESCE(SUM(tamanho_original_bytes),0), COALESCE(SUM(tamanho_final_bytes),0)"
                        f" FROM {_crase(TABELA_IMAGENS)}")
            qtd, orig, final = cur.fetchone()
        lista["resumo"] = {"quantidade": qtd, "original_bytes": int(orig), "final_bytes": int(final)}
        return lista
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.get("/aiven/imagens/{id_}")
def aiven_imagem(id_: int):
    conn = conectar_aiven()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT nome_arquivo, mime_type, dados FROM {_crase(TABELA_IMAGENS)} WHERE id = %s", (id_,))
            linha = cur.fetchone()
    finally:
        conn.close()
    if not linha:
        raise HTTPException(404, "Imagem não encontrada.")
    nome, mime, dados = linha
    return Response(bytes(dados), media_type=mime or "image/webp",
                    headers={"Content-Disposition": f'inline; filename="{Path(nome).stem}.webp"'})


@app.post("/aiven/imagens")
def aiven_enviar_imagem(img: Imagem, _=Depends(usuario)):
    dados = base64.b64decode(img.dados_base64)
    conn = conectar_aiven()
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {_crase(TABELA_IMAGENS)} (nome_arquivo, mime_type, largura, altura, tamanho_original_bytes,"
                " tamanho_final_bytes, qualidade, sha256, dados) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (img.nome_arquivo[:255], "image/webp", img.largura, img.altura, img.tamanho_original_bytes,
                 len(dados), img.qualidade, img.sha256, dados))
        return {"mensagem": f"{img.nome_arquivo} enviada ({len(dados)} bytes)."}
    except pymysql.err.IntegrityError as e:
        if e.args and e.args[0] == 1062:
            raise HTTPException(409, "Esta imagem já foi enviada (mesmo SHA-256).")
        raise _erro_banco(e)
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.delete("/aiven/imagens/{id_}")
def aiven_excluir_imagem(id_: int, _=Depends(usuario)):
    conn = conectar_aiven()
    try:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM {_crase(TABELA_IMAGENS)} WHERE id = %s", (id_,))
        return {"mensagem": f"Imagem {id_} excluída."}
    finally:
        conn.close()


# ---------- Aiven (MySQL): Automação de IT's (tabela ia_documentacao_tecnica, do it_automation-factory.py) ----------
# Linhas 'doc' = planilhas guardadas; 'img' = imagens (dados = WebP atual, dados_orig = original se trocada, flag=1);
# 'pos' = onde cada imagem aparece (ref = id da 'img'). Trocar uma 'img' troca em todas as posições.
# Enviar e baixar o .xlsx (montar o arquivo de volta) continuam só no programa.
TABELA_ITS = "ia_documentacao_tecnica"


class NovaImagem(BaseModel):
    dados_base64: str  # WebP já comprimido pelo navegador


@app.get("/aiven/its/documentos")
def its_documentos(_=Depends(usuario)):
    conn = conectar_aiven()
    try:
        return _rodar(conn, "SELECT d.id, d.chave AS documento, d.qtd AS tamanho_bytes, d.flag AS completo, d.atualizado_em, "
                            f"(SELECT COUNT(*) FROM {_crase(TABELA_ITS)} i WHERE i.doc_id = d.id AND i.tipo = 'img') AS imagens "
                            f"FROM {_crase(TABELA_ITS)} d WHERE d.tipo = 'doc' ORDER BY d.chave")
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.get("/aiven/its/documentos/{doc_id}/imagens")
def its_imagens(doc_id: int, _=Depends(usuario)):
    conn = conectar_aiven()
    try:
        return _rodar(conn, "SELECT i.id, i.chave AS parte, i.flag AS trocada, LENGTH(i.dados) AS tamanho_bytes, "
                            f"(SELECT COUNT(*) FROM {_crase(TABELA_ITS)} p WHERE p.doc_id = i.doc_id AND p.tipo = 'pos' "
                            "AND p.ref = i.id) AS posicoes, "
                            f"(SELECT GROUP_CONCAT(p.chave SEPARATOR ', ') FROM {_crase(TABELA_ITS)} p WHERE p.doc_id = i.doc_id "
                            "AND p.tipo = 'pos' AND p.ref = i.id) AS onde "
                            f"FROM {_crase(TABELA_ITS)} i WHERE i.doc_id = %s AND i.tipo = 'img' ORDER BY i.id", (doc_id,))
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.get("/aiven/its/documentos/{doc_id}/xlsx")
def its_xlsx(doc_id: int, _=Depends(usuario)):
    """O .xlsx remontado (esqueleto + imagens + textos, larguras e mesclagens editados), para a página abrir como Excel."""
    conn = conectar_aiven()
    try:
        dados = montar_xlsx(conn, TABELA_ITS, doc_id)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()
    return Response(dados, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.get("/aiven/its/documentos/{doc_id}/planilhas")
def its_planilhas(doc_id: int, aba: int | None = None, _=Depends(usuario)):
    """Sem `aba`: nomes das abas, imagens e textos editados. Com `aba` (posição, de 0): a aba já lida (células,
    estilos, mesclagens, imagens e formas) para a página desenhar."""
    conn = conectar_aiven()
    try:
        return modelo_json(conn, TABELA_ITS, doc_id, aba)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


class EdicaoCelula(BaseModel):
    aba: str
    ref: str            # ex.: B7
    texto: str | None   # None = volta ao texto do arquivo


class EdicoesCelulas(BaseModel):
    edicoes: list[EdicaoCelula]


@app.put("/aiven/its/documentos/{doc_id}/celulas")
def its_celulas(doc_id: int, corpo: EdicoesCelulas, _=Depends(usuario)):
    """Grava os textos editados (tipo 'cel', chave aba|célula), iguais aos do programa."""
    conn = conectar_aiven()
    try:
        with conn.cursor() as cur:
            for e in corpo.edicoes:
                chave = f"{e.aba}|{e.ref}"
                if e.texto is None:
                    cur.execute(f"DELETE FROM {_crase(TABELA_ITS)} WHERE doc_id = %s AND tipo = 'cel' AND chave = %s", (doc_id, chave))
                else:
                    cur.execute(f"INSERT INTO {_crase(TABELA_ITS)} (tipo, doc_id, chave, texto) VALUES ('cel', %s, %s, %s) "
                                "ON DUPLICATE KEY UPDATE texto = VALUES(texto)", (doc_id, chave, e.texto))
        return {"mensagem": f"{len(corpo.edicoes)} alteração(ões) salva(s) no banco."}
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


AJUSTES_ITS = {
    "padronizar": (padronizar_aprovacao, lambda r: "O bloco de aprovação já está padronizado em todas as abas." if r["colunas"] == 0
                   else f"Padronizado: {r['colunas']} coluna(s) ajustada(s) em {r['abas']} aba(s)."),
    "desfazer-larguras": (desfazer_larguras, lambda r: f"Ajustes de largura desfeitos ({r['colunas']} coluna(s))."),
    "alinhar": (alinhar_aprovacao, lambda r: "As células do bloco de aprovação já terminam na mesma linha em todas as abas."
                if r["mesclagens"] == 0 else f"Alinhado: {r['mesclagens']} célula(s) ajustada(s) em: {r['abas']}."),
    "desfazer-alinhamento": (desfazer_mesclagens, lambda r: f"Alinhamento desfeito ({r['mesclagens']} célula(s))."),
}


@app.post("/aiven/its/documentos/{doc_id}/ajustes/{acao}")
def its_ajustes(doc_id: int, acao: str, _=Depends(usuario)):
    """Ajustes do bloco de aprovação (Ajustes do programa). Gravam só linhas col/mrg; o arquivo guardado não muda."""
    if acao not in AJUSTES_ITS:
        raise HTTPException(404, "Ajuste desconhecido.")
    funcao, mensagem = AJUSTES_ITS[acao]
    conn = conectar_aiven()
    try:
        return {"mensagem": mensagem(funcao(conn, TABELA_ITS, doc_id))}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.get("/aiven/its/documentos/{doc_id}/exportar")
def its_exportar(doc_id: int, _=Depends(usuario)):
    """ZIP com as imagens (nomes escolhidos, formato original) e o mapeamento.json, como o Exportar do programa."""
    conn = conectar_aiven()
    try:
        dados, n = exportar_zip(conn, TABELA_ITS, doc_id)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()
    return Response(dados, media_type="application/zip", headers={"X-Imagens": str(n), "Access-Control-Expose-Headers": "X-Imagens"})


class EnvioInicio(BaseModel):
    documento: str
    tamanho: int        # bytes do esqueleto
    sha256: str         # hex do esqueleto


class EnvioFim(BaseModel):
    partes: int
    midias: list[str]   # caminhos (xl/media/...) das imagens compactadas enviadas


def _envio(funcao, *args):
    conn = conectar_aiven()
    try:
        return funcao(conn, TABELA_ITS, *args)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.post("/aiven/its/envio")
def its_envio_iniciar(corpo: EnvioInicio, _=Depends(usuario)):
    """Passo 1 do envio de um .xlsx pelo site: cria/reinicia o documento (flag=0) e devolve o id."""
    return {"doc_id": _envio(envio_iniciar, corpo.documento, corpo.tamanho, corpo.sha256)}


@app.put("/aiven/its/envio/{doc_id}/parte/{n}")
async def its_envio_parte(doc_id: int, n: int, request: Request, _=Depends(usuario)):
    """Passo 2: uma parte do esqueleto (corpo binário)."""
    _envio(envio_parte, doc_id, n, await request.body())
    return {"ok": True}


@app.put("/aiven/its/envio/{doc_id}/imagem")
async def its_envio_imagem(doc_id: int, midia: str, request: Request, _=Depends(usuario)):
    """Passo 3: uma imagem única já compactada em WebP (corpo binário); `midia` é o caminho dela no .xlsx."""
    _envio(envio_imagem, doc_id, midia, await request.body())
    return {"ok": True}


@app.post("/aiven/its/envio/{doc_id}/finalizar")
def its_envio_finalizar(doc_id: int, corpo: EnvioFim, _=Depends(usuario)):
    """Passo 4: confere o esqueleto, sincroniza as posições das imagens e libera o documento."""
    r = _envio(envio_finalizar, doc_id, corpo.partes, corpo.midias)
    return {"mensagem": f"Documento enviado: {r['imagens']} posição(ões) de imagem, {r['unicas']} imagem(ns) única(s).", **r}


class Movimento(BaseModel):
    aba: str
    celula: str
    seq: int
    dx: float
    dy: float


class Movimentos(BaseModel):
    movimentos: list[Movimento]


@app.put("/aiven/its/documentos/{doc_id}/movimentos")
def its_movimentos(doc_id: int, corpo: Movimentos, _=Depends(usuario)):
    """Grava o deslocamento (px) de imagens em relação ao arquivo (tipo 'mov', chave aba|célula|seq), como o programa."""
    conn = conectar_aiven()
    try:
        with conn.cursor() as cur:
            for mv in corpo.movimentos:
                chave = f"{mv.aba}|{mv.celula}|{mv.seq}"
                if abs(mv.dx) < 0.5 and abs(mv.dy) < 0.5:   # voltou ao lugar do arquivo
                    cur.execute(f"DELETE FROM {_crase(TABELA_ITS)} WHERE doc_id = %s AND tipo = 'mov' AND chave = %s", (doc_id, chave))
                else:
                    cur.execute(f"INSERT INTO {_crase(TABELA_ITS)} (tipo, doc_id, chave, texto) VALUES ('mov', %s, %s, %s) "
                                "ON DUPLICATE KEY UPDATE texto = VALUES(texto)", (doc_id, chave, f"{mv.dx:.2f},{mv.dy:.2f}"))
        return {"mensagem": f"{len(corpo.movimentos)} posição(ões) de imagem salva(s)."}
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


class NomePosicao(BaseModel):
    nome: str | None   # None = volta ao nome padrão


@app.put("/aiven/its/posicoes/{pos_id}/nome")
def its_nome_posicao(pos_id: int, corpo: NomePosicao, _=Depends(usuario)):
    """Nome do arquivo escolhido para a imagem naquela posição (None = nome padrão), como o programa."""
    conn = conectar_aiven()
    try:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE {_crase(TABELA_ITS)} SET texto = %s WHERE id = %s AND tipo = 'pos'", (corpo.nome, pos_id))
        return {"mensagem": "Nome salvo."}
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.get("/aiven/its/imagens/{img_id}")
def its_imagem(img_id: int, original: bool = False, _=Depends(usuario)):
    conn = conectar_aiven()
    try:
        with conn.cursor() as cur:
            coluna = "COALESCE(dados_orig, dados)" if original else "dados"
            cur.execute(f"SELECT {coluna} FROM {_crase(TABELA_ITS)} WHERE id = %s AND tipo = 'img'", (img_id,))
            linha = cur.fetchone()
    finally:
        conn.close()
    if not linha or linha[0] is None:
        raise HTTPException(404, "Imagem não encontrada.")
    return Response(bytes(linha[0]), media_type="image/webp")


@app.put("/aiven/its/imagens/{img_id}")
def its_trocar(img_id: int, img: NovaImagem, _=Depends(usuario)):
    """Troca a imagem em todas as posições; a primeira troca guarda a original em dados_orig."""
    conn = conectar_aiven()
    try:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE {_crase(TABELA_ITS)} SET dados_orig = COALESCE(dados_orig, dados), dados = %s, flag = 1 "
                        "WHERE id = %s AND tipo = 'img'", (base64.b64decode(img.dados_base64), img_id))
            if cur.rowcount == 0:
                raise HTTPException(404, "Imagem não encontrada.")
        return {"mensagem": "Imagem trocada em todas as posições."}
    finally:
        conn.close()


@app.post("/aiven/its/imagens/{img_id}/restaurar")
def its_restaurar(img_id: int, _=Depends(usuario)):
    conn = conectar_aiven()
    try:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE {_crase(TABELA_ITS)} SET dados = dados_orig, dados_orig = NULL, flag = 0 "
                        "WHERE id = %s AND tipo = 'img' AND dados_orig IS NOT NULL", (img_id,))
            return {"mensagem": "Imagem original restaurada." if cur.rowcount else "Esta imagem não foi trocada."}
    finally:
        conn.close()


@app.delete("/aiven/its/documentos/{doc_id}")
def its_excluir(doc_id: int, _=Depends(usuario)):
    conn = conectar_aiven()
    try:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM {_crase(TABELA_ITS)} WHERE doc_id = %s OR (id = %s AND tipo = 'doc')", (doc_id, doc_id))
            return {"mensagem": f"Documento excluído ({cur.rowcount} linha(s))."}
    finally:
        conn.close()


# ---------- Neon (PostgreSQL): Neon Console e Dinamic Database ----------

def _alvo(tabela):
    return sql.Identifier(NEON_SCHEMA, tabela)


@app.get("/neon/tabelas")
def neon_tabelas(_=Depends(usuario)):
    conn = conectar_neon()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s "
                        "AND table_type = 'BASE TABLE' ORDER BY table_name", (NEON_SCHEMA,))
            return [r[0] for r in cur.fetchall()]
    finally:
        conn.close()


@app.get("/neon/tabelas/{tabela}/dados")
def neon_dados(tabela: str, _=Depends(usuario)):
    conn = conectar_neon()
    try:
        return _rodar(conn, sql.SQL("SELECT * FROM {} ORDER BY 1 LIMIT %s").format(_alvo(tabela)), (LIMITE,))
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.get("/neon/tabelas/{tabela}/colunas")
def neon_colunas(tabela: str, _=Depends(usuario)):
    """Para o formulário do Neon Console: nome, tipo, obrigatório, tem padrão, automático (como no neon_console.py)."""
    conn = conectar_neon()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT a.attname, format_type(a.atttypid, a.atttypmod), a.attnotnull, "
                "d.adbin IS NOT NULL OR a.attidentity <> '', "
                "a.attidentity <> '' OR a.attgenerated <> '' "
                "  OR coalesce(pg_get_expr(d.adbin, d.adrelid), '') LIKE 'nextval(%%' "
                "FROM pg_attribute a LEFT JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum "
                "WHERE a.attrelid = to_regclass(%s) AND a.attnum > 0 AND NOT a.attisdropped ORDER BY a.attnum",
                (_alvo(tabela).as_string(conn),))
            return [{"nome": n, "tipo": t, "obrigatorio": nn and not padrao, "tem_padrao": padrao, "automatico": auto}
                    for n, t, nn, padrao, auto in cur.fetchall()]
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.get("/neon/tabelas/{tabela}/estrutura")
def neon_estrutura(tabela: str, _=Depends(usuario)):
    conn = conectar_neon()
    try:
        return _rodar(
            conn,
            "SELECT a.attname AS coluna, format_type(a.atttypid, a.atttypmod) AS tipo, "
            "CASE WHEN a.attnotnull THEN 'não' ELSE 'sim' END AS nulo, "
            "pg_get_expr(d.adbin, d.adrelid) AS padrao, col_description(a.attrelid, a.attnum) AS comentario "
            "FROM pg_attribute a LEFT JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum "
            "WHERE a.attrelid = to_regclass(%s) AND a.attnum > 0 AND NOT a.attisdropped ORDER BY a.attnum",
            (_alvo(tabela).as_string(conn),))
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


class Linha(BaseModel):
    valores: dict  # {coluna: texto}; colunas fora do dict usam o padrão (ou NULL)


@app.post("/neon/tabelas/{tabela}/linhas")
def neon_inserir(tabela: str, corpo: Linha, _=Depends(usuario)):
    conn = conectar_neon()
    try:
        v = corpo.valores
        if v:
            comando = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                _alvo(tabela), sql.SQL(", ").join(map(sql.Identifier, v)), sql.SQL(", ").join(sql.Placeholder() * len(v)))
        else:
            comando = sql.SQL("INSERT INTO {} DEFAULT VALUES").format(_alvo(tabela))
        _rodar(conn, comando, list(v.values()))
        return {"mensagem": "Registro inserido."}
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.delete("/neon/tabelas/{tabela}/linhas/{id_}")
def neon_excluir(tabela: str, id_: int, renumerar: bool = True, _=Depends(usuario)):
    """Igual ao Excluir linha do dinamic_database.py: com renumerar, os ids acima descem 1 e o contador volta
    para MAX(id) + 1. Tudo numa transação: se algo falhar (ex.: outra tabela usa esse id), nada muda."""
    conn = conectar_neon()
    alvo = _alvo(tabela)
    try:
        nome = alvo.as_string(conn)
        with conn.cursor() as cur:
            cur.execute("BEGIN")
            try:
                cur.execute(sql.SQL("DELETE FROM {} WHERE id = %s").format(alvo), (id_,))
                if cur.rowcount == 0:
                    raise ValueError(f"Nenhuma linha com id = {id_}.")
                if renumerar:
                    cur.execute("SELECT attidentity FROM pg_attribute WHERE attrelid = to_regclass(%s) "
                                "AND attname = 'id'", (nome,))
                    sempre = cur.fetchone()[0] == "a"
                    if sempre:
                        cur.execute(sql.SQL("ALTER TABLE {} ALTER COLUMN id SET GENERATED BY DEFAULT").format(alvo))
                    cur.execute(sql.SQL("UPDATE {} SET id = -id WHERE id > %s").format(alvo), (id_,))
                    cur.execute(sql.SQL("UPDATE {} SET id = -id - 1 WHERE id < 0").format(alvo))
                    if sempre:
                        cur.execute(sql.SQL("ALTER TABLE {} ALTER COLUMN id SET GENERATED ALWAYS").format(alvo))
                    cur.execute("SELECT pg_get_serial_sequence(%s, 'id')", (nome,))
                    sequencia = cur.fetchone()[0]
                    if sequencia:
                        cur.execute(sql.SQL("SELECT setval(%s, (SELECT COALESCE(MAX(id), 0) + 1 FROM {}), false)")
                                    .format(alvo), (sequencia,))
                cur.execute("COMMIT")
            except Exception:
                cur.execute("ROLLBACK")
                raise
        return {"mensagem": f"Linha id {id_} apagada" + (" e ids renumerados." if renumerar else ".")}
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()


@app.post("/neon/sql")
def neon_sql(corpo: Sql, _=Depends(usuario)):
    """Aba SQL do Dinamic Database (e o Criar/Alterar tabela, que montam o SQL na página)."""
    conn = conectar_neon()
    try:
        return _rodar(conn, corpo.comando)
    except Exception as e:
        raise _erro_banco(e)
    finally:
        conn.close()
