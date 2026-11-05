"""Remonta o .xlsx guardado no banco (Automação de IT's) para a página do site.

Cópia, sem PyQt6, da remontagem de aiven_gerenciamento/it_automation-factory.py (o programa não foi alterado).
Aplica as edições de texto (cel), larguras (col), mesclagens (mrg) e deslocamentos de imagem (mov).
"""
import hashlib
import io
import posixpath
import zipfile

from PIL import Image

import json
import re
import xml.etree.ElementTree as ET

from planilha_modelo import (
    NS, RID, aplicar_edicoes_xml, aplicar_larguras_xml, aplicar_mesclagens_xml, aplicar_movimentos_xml, caminhos_abas,
    colidx, colname, ler_pasta, plano_alinhamento, plano_padronizacao, rels_de,
)

FORMATOS = {"png": "PNG", "jpeg": "JPEG", "jpg": "JPEG", "gif": "GIF", "bmp": "BMP"}


# ---------- imagens ----------

def webp_para_ext(dados, ext):
    """Imagem guardada (WebP) -> formato da parte no xlsx (png/jpeg/gif/bmp)."""
    ext = ext.lower().lstrip(".")
    if ext not in FORMATOS:
        raise ValueError(f"Formato .{ext} não suportado para remontar o xlsx.")
    img = Image.open(io.BytesIO(dados))
    if FORMATOS[ext] == "JPEG":
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            fundo = Image.new("RGB", img.size, "white")
            fundo.paste(img, mask=img.getchannel("A"))
            img = fundo
        else:
            img = img.convert("RGB")
    elif FORMATOS[ext] == "BMP" and img.mode not in ("RGB", "RGBA", "L", "P"):
        img = img.convert("RGB")
    saida = io.BytesIO()
    img.save(saida, FORMATOS[ext], **({"quality": 92} if FORMATOS[ext] == "JPEG" else {}))
    return saida.getvalue()


# ---------- remontagem ----------

def _por_aba(linhas):
    r = {}
    for chave, texto in linhas:
        aba, ref = chave.rsplit("|", 1)
        r.setdefault(aba, {})[ref] = texto
    return r


def _esqueleto(cur, tabela, doc_id, exigir_completo=True):
    """Bytes do .xlsx guardado no banco (em partes, sem as imagens), conferido pelo hash. Com exigir_completo=False
    aceita um envio que ainda não terminou (usado ao finalizar o envio)."""
    cur.execute(f"SELECT qtd, sha256, ref, flag FROM `{tabela}` WHERE id=%s AND tipo='doc'", (doc_id,))
    r = cur.fetchone()
    if not r:
        raise ValueError("Documento não encontrado no banco.")
    tam, sha_bin, n_partes, flag = r
    if exigir_completo and flag != 1:
        raise ValueError("O envio deste documento não terminou. Envie o arquivo de novo.")
    esqueleto = bytearray()
    for p in range(n_partes):
        cur.execute(f"SELECT dados FROM `{tabela}` WHERE doc_id=%s AND tipo='parte' AND chave=%s", (doc_id, str(p)))
        esqueleto += bytes(cur.fetchone()[0])
    if hashlib.sha256(esqueleto).digest() != bytes(sha_bin):
        raise ValueError("O arquivo guardado no banco não confere com o hash gravado.")
    return bytes(esqueleto)


def montar_xlsx(conn, tabela, doc_id):
    """.xlsx pronto (bytes): esqueleto guardado em partes + imagens + textos, larguras e mesclagens editados."""
    cur = conn.cursor()
    esqueleto = _esqueleto(cur, tabela, doc_id)
    cur.execute(f"SELECT chave, id FROM `{tabela}` WHERE doc_id=%s AND tipo='img'", (doc_id,))
    midias = dict(cur.fetchall())
    cur.execute(f"SELECT chave, texto FROM `{tabela}` WHERE doc_id=%s AND tipo='cel'", (doc_id,))
    celulas = {a: {k: (v or "") for k, v in d.items()} for a, d in _por_aba(cur.fetchall()).items()}
    cur.execute(f"SELECT chave, texto FROM `{tabela}` WHERE doc_id=%s AND tipo='col'", (doc_id,))
    larguras = {a: {colidx(k): float(v) for k, v in d.items()} for a, d in _por_aba(cur.fetchall()).items()}
    cur.execute(f"SELECT chave, texto FROM `{tabela}` WHERE doc_id=%s AND tipo='mrg'", (doc_id,))
    mesclagens = _por_aba(cur.fetchall())

    cur.execute(f"SELECT chave, texto FROM `{tabela}` WHERE doc_id=%s AND tipo='mov'", (doc_id,))
    movimentos = {}
    for chave, texto in cur.fetchall():
        aba, celula, seq = chave.rsplit("|", 2)
        dx, dy = (float(v) for v in texto.split(","))
        movimentos.setdefault(aba, {})[(celula, int(seq))] = (dx, dy)

    saida = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(esqueleto)) as zin:
        caminhos = caminhos_abas(zin)
        troca = {}
        for aba in set(celulas) | set(larguras) | set(mesclagens):
            if aba not in caminhos:
                continue
            xml = zin.read(caminhos[aba])
            if aba in larguras:
                xml = aplicar_larguras_xml(xml, larguras[aba])
            if aba in mesclagens:
                xml = aplicar_mesclagens_xml(xml, mesclagens[aba])
            if aba in celulas:
                xml = aplicar_edicoes_xml(xml, celulas[aba])
            troca[caminhos[aba]] = xml
        if movimentos:  # o anchor de cada imagem é achado pelo mesmo leitor do programa e reescrito no XML do desenho
            modelo = ler_pasta(zin, None, larguras, mesclagens)
            for pl in modelo:
                por_desenho = {}
                for el in pl.elementos:
                    d = movimentos.get(pl.nome, {}).get((el.get("celula"), el.get("seq")))
                    if el["tipo"] == "pic" and d and el.get("tam_ok"):
                        por_desenho.setdefault(el["desenho"], {})[el["anc"]] = d
                for desenho, movs in por_desenho.items():
                    troca[desenho] = aplicar_movimentos_xml(troca.get(desenho) or zin.read(desenho), pl, movs)
        with zipfile.ZipFile(saida, "w") as zout:
            for info in zin.infolist():
                zi = zipfile.ZipInfo(info.filename, info.date_time)
                zi.compress_type = info.compress_type
                zi.external_attr = info.external_attr
                if info.filename in midias:
                    cur.execute(f"SELECT dados FROM `{tabela}` WHERE id=%s", (midias[info.filename],))
                    dados = webp_para_ext(bytes(cur.fetchone()[0]), posixpath.splitext(info.filename)[1])
                else:
                    dados = troca.get(info.filename)
                    if dados is None:
                        dados = zin.read(info.filename)
                zout.writestr(zi, dados)
    return saida.getvalue()


# ---------- modelo para a tela (JSON) ----------

def _ajustes(cur, tabela, doc_id):
    """(larguras, mesclagens, movimentos, celulas editadas) guardados no banco, no formato do leitor."""
    def linhas(tipo):
        cur.execute(f"SELECT chave, texto FROM `{tabela}` WHERE doc_id=%s AND tipo=%s", (doc_id, tipo))
        return cur.fetchall()
    larguras = {a: {colidx(k): float(v) for k, v in d.items()} for a, d in _por_aba(linhas("col")).items()}
    mesclagens = _por_aba(linhas("mrg"))
    movimentos = {}
    for chave, texto in linhas("mov"):
        aba, celula, seq = chave.rsplit("|", 2)
        dx, dy = (float(v) for v in texto.split(","))
        movimentos.setdefault(aba, {})[(celula, int(seq))] = (dx, dy)
    celulas = {a: {k: (v or "") for k, v in d.items()} for a, d in _por_aba(linhas("cel")).items()}
    return larguras, mesclagens, movimentos, celulas


def _planilha_json(pl):
    estilos, idx = [], {}
    def est(e):
        k = id(e)
        if k not in idx:
            idx[k] = len(estilos)
            estilos.append({**e, "borda": {lado: list(v) for lado, v in e["borda"].items()}})
        return idx[k]
    cells = [[r, c, x.texto, x.tipo, est(x.estilo), x.formula] for (r, c), x in pl.cells.items()]
    return {
        "nome": pl.nome, "estado": pl.estado, "grade": pl.grade, "ncols": pl.ncols, "nrows": pl.nrows,
        "col_x": pl.col_x, "row_y": pl.row_y, "cells": cells, "estilos": estilos,
        "merges": [[r1, c1, r2, c2] for (r1, c1), (r2, c2) in pl.merges.items()],
        "elementos": pl.elementos,
    }


def modelo_json(conn, tabela, doc_id, aba=None):
    """Abas lidas do .xlsx do banco (células, estilos, mesclagens, imagens e formas, com os ajustes) para o navegador
    desenhar. Sem `aba`: só os nomes das abas, `imagens` (liga o caminho da mídia no xlsx ao id da imagem no banco) e
    `edicoes` (textos editados). Com `aba` (posição, de 0): essa aba inteira."""
    cur = conn.cursor()
    esqueleto = _esqueleto(cur, tabela, doc_id)
    larguras, mesclagens, movimentos, celulas = _ajustes(cur, tabela, doc_id)
    cur.execute(f"SELECT chave, id, flag FROM `{tabela}` WHERE doc_id=%s AND tipo='img'", (doc_id,))
    imagens = {c: {"id": i, "trocada": bool(f)} for c, i, f in cur.fetchall()}
    cur.execute(f"SELECT chave, id, texto, ref FROM `{tabela}` WHERE doc_id=%s AND tipo='pos'", (doc_id,))
    posicoes = {c: {"id": i, "nome": t, "img": r} for c, i, t, r in cur.fetchall()}
    with zipfile.ZipFile(io.BytesIO(esqueleto)) as z:
        planilhas = ler_pasta(z, None, larguras, mesclagens, movimentos=movimentos)
    if aba is not None:
        if not 0 <= aba < len(planilhas):
            raise ValueError("Aba não encontrada.")
        return _planilha_json(planilhas[aba])
    return {"abas": [{"nome": p.nome, "estado": p.estado} for p in planilhas], "imagens": imagens, "posicoes": posicoes,
            "edicoes": celulas}


# ---------- ajustes do bloco de aprovação (iguais aos do programa) ----------

def _doc_planilhas(cur, tabela, doc_id):
    with zipfile.ZipFile(io.BytesIO(_esqueleto(cur, tabela, doc_id))) as z:
        return ler_pasta(z)   # sem ajustes: os planos partem sempre do que está no arquivo


def padronizar_aprovacao(conn, tabela, doc_id):
    """Iguala as colunas do bloco ELABORADO / APROVADO / HOMOLOGADO nas abas de mesmo formato. Grava só os ajustes (col)."""
    cur = conn.cursor()
    plano, _ = plano_padronizacao(_doc_planilhas(cur, tabela, doc_id))
    cur.execute(f"DELETE FROM `{tabela}` WHERE doc_id=%s AND tipo='col'", (doc_id,))
    linhas = [(doc_id, f"{aba}|{colname(c)}", f"{chars:.10g}") for aba, cols in plano.items() for c, chars in cols.items()]
    if linhas:
        cur.executemany(f"INSERT INTO `{tabela}` (tipo, doc_id, chave, texto) VALUES ('col',%s,%s,%s)", linhas)
    return {"abas": len(plano), "colunas": len(linhas)}


def desfazer_larguras(conn, tabela, doc_id):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM `{tabela}` WHERE doc_id=%s AND tipo='col'", (doc_id,))
    return {"colunas": cur.rowcount}


def alinhar_aprovacao(conn, tabela, doc_id):
    """Faz as células ELABORADO / APROVADO / HOMOLOGADO terminarem na mesma linha. Grava só os ajustes (mrg)."""
    cur = conn.cursor()
    plano, resumo = plano_alinhamento(_doc_planilhas(cur, tabela, doc_id))
    cur.execute(f"DELETE FROM `{tabela}` WHERE doc_id=%s AND tipo='mrg'", (doc_id,))
    linhas = [(doc_id, f"{aba}|{velha}", nova) for aba, m in plano.items() for velha, nova in m.items()]
    if linhas:
        cur.executemany(f"INSERT INTO `{tabela}` (tipo, doc_id, chave, texto) VALUES ('mrg',%s,%s,%s)", linhas)
    return {"abas": ", ".join(r[0].strip() for r in resumo), "mesclagens": len(linhas)}


def desfazer_mesclagens(conn, tabela, doc_id):
    cur = conn.cursor()
    cur.execute(f"DELETE FROM `{tabela}` WHERE doc_id=%s AND tipo='mrg'", (doc_id,))
    return {"mesclagens": cur.rowcount}


# ---------- exportar mapeamento + imagens ----------

_NSX = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
_EMBED = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"


def _nome_seguro(s):
    return re.sub(r'[\\/:*?"<>|\s]+', "_", s).strip("_")[:60] or "x"


def extrair_xlsx(z):
    """Cada imagem posicionada do xlsx: aba, células, textos de contexto e mídia (cópia de extrair_xlsx do programa)."""
    names = set(z.namelist())
    ss = []
    if "xl/sharedStrings.xml" in names:
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", _NSX):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % _NSX["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    wrels = rels_de(z, names, "xl/workbook.xml")
    rows = []
    for idx, s in enumerate(wb.find("m:sheets", NS), 1):
        sname, state, spath = s.get("name"), s.get("state", "visible"), wrels[s.get(RID)][1]
        root = ET.fromstring(z.read(spath))
        cells = {}
        for c in root.iter("{%s}c" % _NSX["m"]):
            v, t = c.find("m:v", NS), c.get("t")
            txt = None
            if t == "inlineStr":
                txt = "".join(x.text or "" for x in c.iter("{%s}t" % _NSX["m"]))
            elif v is not None and v.text is not None:
                txt = ss[int(v.text)] if t == "s" else v.text
            if txt and txt.strip():
                m = re.match(r"([A-Z]+)(\d+)", c.get("r"))
                cells[(int(m.group(2)) - 1, colidx(m.group(1)))] = txt.strip()
        n = 0
        for typ, tgt in rels_de(z, names, spath).values():
            if typ != "drawing":
                continue
            dr = rels_de(z, names, tgt)
            for anc in ET.fromstring(z.read(tgt)):
                fr, to = anc.find("xdr:from", _NSX), anc.find("xdr:to", _NSX)
                r0, c0 = (int(fr.find("xdr:row", _NSX).text), int(fr.find("xdr:col", _NSX).text)) if fr is not None else (0, 0)
                r1, c1 = (int(to.find("xdr:row", _NSX).text), int(to.find("xdr:col", _NSX).text)) if to is not None else (r0, c0)
                shape_txt = " | ".join(t.text for t in anc.iter("{%s}t" % _NSX["a"]) if t.text and t.text.strip())
                descr = ""
                for e in anc.iter("{%s}cNvPr" % _NSX["xdr"]):
                    descr = e.get("descr") or e.get("name") or ""
                    break
                for b in [b.get(_EMBED) for b in anc.iter("{%s}blip" % _NSX["a"]) if b.get(_EMBED)]:
                    if b not in dr:
                        continue
                    media = dr[b][1]
                    n += 1
                    cell = f"{colname(c0)}{r0 + 1}"
                    row_txt = " | ".join(cells[k] for k in sorted(cells) if r0 <= k[0] <= r1 and k[1] != c0)
                    above = ""
                    for rr in range(r0 - 1, max(r0 - 6, -1), -1):
                        cand = [cells[k] for k in sorted(cells) if k[0] == rr]
                        if cand:
                            above = f"L{rr + 1}: " + " | ".join(cand)
                            break
                    rows.append(dict(
                        aba_ordem=idx, aba_nome=sname,
                        aba_visibilidade=state if state in ("visible", "hidden", "veryHidden") else "visible",
                        celula_inicio=cell, celula_fim=f"{colname(c1)}{r1 + 1}", seq_na_aba=n, midia_original=media,
                        nome_arquivo=f"{idx:02d}_{_nome_seguro(sname)}__{cell}__{n:02d}__{posixpath.basename(media)}",
                        texto_celula_ancora=cells.get((r0, c0), ""), texto_mesma_linha=row_txt[:500],
                        texto_linha_acima=above[:300], texto_no_desenho=shape_txt[:300], nome_descricao=descr))
    return rows


def exportar_zip(conn, tabela, doc_id):
    """ZIP (bytes) com as imagens no formato original, com os nomes escolhidos, e o mapeamento.json."""
    cur = conn.cursor()
    with zipfile.ZipFile(io.BytesIO(_esqueleto(cur, tabela, doc_id))) as z:
        linhas = extrair_xlsx(z)
    cur.execute(f"SELECT chave, texto, ref FROM `{tabela}` WHERE doc_id=%s AND tipo='pos'", (doc_id,))
    db = {c: (t, r) for c, t, r in cur.fetchall()}
    saida, usados, conv = [], set(), {}
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as zo:
        for i, e in enumerate(linhas, 1):
            texto, ref = db.get(f"{e['aba_nome']}|{e['celula_inicio']}|{e['seq_na_aba']}", (None, None))
            base = re.sub(r'[\\/:*?"<>|]+', "_", texto or e["nome_arquivo"]).strip() or f"imagem_{i}"
            final, k = base, 2
            while final.lower() in usados:
                stem, ext = posixpath.splitext(base)
                final, k = f"{stem}_{k}{ext}", k + 1
            usados.add(final.lower())
            if ref not in conv:
                blob = None
                if ref:
                    cur.execute(f"SELECT dados FROM `{tabela}` WHERE id=%s", (ref,))
                    r = cur.fetchone()
                    blob = r[0] if r else None
                conv[ref] = webp_para_ext(bytes(blob), posixpath.splitext(e["midia_original"])[1]) if blob else None
            if conv[ref] is not None:
                zo.writestr(final, conv[ref])
            saida.append(dict(ordem_aba=e["aba_ordem"], aba=e["aba_nome"], visibilidade=e["aba_visibilidade"],
                              arquivo=final if conv[ref] is not None else None, midia_original=e["midia_original"],
                              celula_inicio=e["celula_inicio"], celula_fim=e["celula_fim"],
                              texto_celula_ancora=e["texto_celula_ancora"], texto_mesma_linha=e["texto_mesma_linha"],
                              texto_linha_acima=e["texto_linha_acima"], texto_no_desenho=e["texto_no_desenho"],
                              nome_descricao=e["nome_descricao"]))
        zo.writestr("mapeamento.json", json.dumps(saida, ensure_ascii=False, indent=1))
    return buf.getvalue(), len(linhas)


# ---------- enviar .xlsx pelo site ----------
# O navegador abre o .xlsx, compacta as imagens em WebP e monta o esqueleto (o .xlsx sem as imagens compactadas); a API
# só recebe o esqueleto em partes e cada imagem, e no fim sincroniza as posições. Mesmo formato do programa
# (enviar_xlsx de it_automation-factory.py): linhas doc, parte, img e pos.

def envio_iniciar(conn, tabela, documento, tamanho, sha256_hex):
    """Cria (ou reinicia) a linha do documento, com flag=0 (enviando), e apaga as partes antigas. Devolve o id."""
    if not documento or len(documento) > 190:
        raise ValueError("O nome do arquivo passa de 190 caracteres.")
    sha = bytes.fromhex(sha256_hex)
    if len(sha) != 32:
        raise ValueError("Hash inválido.")
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM `{tabela}` WHERE tipo='doc' AND doc_id=0 AND chave=%s", (documento,))
    r = cur.fetchone()
    if r:
        doc_id = r[0]
        cur.execute(f"UPDATE `{tabela}` SET flag=0, qtd=%s, sha256=%s, ref=0 WHERE id=%s", (tamanho, sha, doc_id))
        cur.execute(f"DELETE FROM `{tabela}` WHERE doc_id=%s AND tipo='parte'", (doc_id,))
    else:
        cur.execute(f"INSERT INTO `{tabela}` (tipo, doc_id, chave, qtd, sha256, ref, flag) VALUES ('doc',0,%s,%s,%s,0,0)",
                    (documento, tamanho, sha))
        doc_id = cur.lastrowid
    return doc_id


def envio_parte(conn, tabela, doc_id, n, dados):
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM `{tabela}` WHERE id=%s AND tipo='doc' AND flag=0", (doc_id,))
    if not cur.fetchone():
        raise ValueError("Não há envio em andamento para este documento.")
    cur.execute(f"DELETE FROM `{tabela}` WHERE doc_id=%s AND tipo='parte' AND chave=%s", (doc_id, str(n)))
    cur.execute(f"INSERT INTO `{tabela}` (tipo, doc_id, chave, dados) VALUES ('parte',%s,%s,%s)", (doc_id, str(n), dados))


def envio_imagem(conn, tabela, doc_id, midia, webp):
    """Imagem única do documento. Se o usuário já trocou esta imagem, a trocada fica e a nova vira o ponto de restauração."""
    cur = conn.cursor()
    cur.execute(f"SELECT id, flag FROM `{tabela}` WHERE doc_id=%s AND tipo='img' AND chave=%s", (doc_id, midia))
    r = cur.fetchone()
    if r is None:
        cur.execute(f"INSERT INTO `{tabela}` (tipo, doc_id, chave, dados) VALUES ('img',%s,%s,%s)", (doc_id, midia, webp))
    elif r[1]:
        cur.execute(f"UPDATE `{tabela}` SET dados_orig=%s WHERE id=%s", (webp, r[0]))
    else:
        cur.execute(f"UPDATE `{tabela}` SET dados=%s, dados_orig=NULL WHERE id=%s", (webp, r[0]))


def envio_finalizar(conn, tabela, doc_id, n_partes, midias):
    """Confere o esqueleto (hash), remove imagens que sumiram, sincroniza as posições (pos) e marca o documento como completo."""
    cur = conn.cursor()
    cur.execute(f"UPDATE `{tabela}` SET ref=%s WHERE id=%s AND tipo='doc'", (n_partes, doc_id))
    esqueleto = _esqueleto(cur, tabela, doc_id, exigir_completo=False)
    with zipfile.ZipFile(io.BytesIO(esqueleto)) as z:
        rows = extrair_xlsx(z)

    cur.execute(f"SELECT id, chave FROM `{tabela}` WHERE doc_id=%s AND tipo='img'", (doc_id,))
    existentes = cur.fetchall()
    manter = set(midias)
    for i, c in existentes:
        if c not in manter:
            cur.execute(f"DELETE FROM `{tabela}` WHERE id=%s", (i,))
    img_id = {c: i for i, c in existentes if c in manter}

    cur.execute(f"SELECT id, chave, ref FROM `{tabela}` WHERE doc_id=%s AND tipo='pos'", (doc_id,))
    pos = {c: (i, r) for i, c, r in cur.fetchall()}
    vistos, novas = set(), []
    for row in rows:
        chave = f"{row['aba_nome']}|{row['celula_inicio']}|{row['seq_na_aba']}"
        vistos.add(chave)
        ref = img_id.get(row["midia_original"])
        if chave in pos:
            if pos[chave][1] != ref:
                cur.execute(f"UPDATE `{tabela}` SET ref=%s WHERE id=%s", (ref, pos[chave][0]))
        else:
            novas.append((doc_id, chave, ref))
    if novas:
        cur.executemany(f"INSERT INTO `{tabela}` (tipo, doc_id, chave, ref) VALUES ('pos',%s,%s,%s)", novas)
    removidas = [i for c, (i, _) in pos.items() if c not in vistos]
    for rid in removidas:
        cur.execute(f"DELETE FROM `{tabela}` WHERE id=%s", (rid,))
    cur.execute(f"UPDATE `{tabela}` SET flag=1, ref=%s WHERE id=%s", (n_partes, doc_id))
    return {"imagens": len(rows), "unicas": len(manter), "removidas": len(removidas)}
