"""Modelo e leitura de .xlsx para a API do site (Automação de IT's).

Cópia, sem PyQt6, da parte pura de aiven_gerenciamento/planilha_view.py (leitura das abas, planos de padronização e
alinhamento do bloco de aprovação e gravação de edições no XML). O programa não foi alterado: se aquele arquivo
mudar nessa parte, copiar de novo para cá.
"""
import colorsys
import math
import re
import posixpath
import xml.etree.ElementTree as ET
from bisect import bisect_left, bisect_right
from collections import Counter
from datetime import datetime, timedelta
from xml.sax.saxutils import escape

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
}
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
EMBED = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
EMU = 9525.0
MAX_COLS = 300


# ---------------------------------------------------------------- utilidades de célula
def colname(i):
    s, i = "", i + 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def colidx(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def ref_rc(ref):
    m = re.match(r"([A-Z]+)(\d+)", ref)
    return int(m.group(2)) - 1, colidx(m.group(1))


def rc_ref(r, c):
    return f"{colname(c)}{r + 1}"


def _tag(el):
    return el.tag.rsplit("}", 1)[-1]


def rels_de(z, names, path):
    d, b = posixpath.split(path)
    rp = posixpath.join(d, "_rels", b + ".rels")
    res = {}
    if rp in names:
        for r in ET.fromstring(z.read(rp)).findall("rel:Relationship", NS):
            if r.get("TargetMode") == "External":
                continue
            t = r.get("Target")
            t = t.lstrip("/") if t.startswith("/") else posixpath.normpath(posixpath.join(d, t))
            res[r.get("Id")] = (r.get("Type").rsplit("/", 1)[-1], t)
    return res


def caminhos_abas(z):
    """{nome_da_aba: caminho_do_xml}"""
    names = set(z.namelist())
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    wrels = rels_de(z, names, "xl/workbook.xml")
    return {s.get("name"): wrels[s.get(RID)][1] for s in wb.find("m:sheets", NS)}


# ---------------------------------------------------------------- cores
_INDEXADAS = {8: "000000", 9: "FFFFFF", 10: "FF0000", 11: "00FF00", 12: "0000FF", 13: "FFFF00", 14: "FF00FF",
              15: "00FFFF", 16: "800000", 17: "008000", 18: "000080", 19: "808000", 20: "800080", 21: "008080",
              22: "C0C0C0", 23: "808080", 64: "000000"}
_TEMA_PADRAO = ["FFFFFF", "000000", "EEECE1", "1F497D", "4F81BD", "C0504D", "9BBB59", "8064A2", "4BACC6", "F79646",
                "0000FF", "800080"]
_NOMES_TEMA = {"bg1": 0, "lt1": 0, "tx1": 1, "dk1": 1, "bg2": 2, "lt2": 2, "tx2": 3, "dk2": 3, "accent1": 4,
               "accent2": 5, "accent3": 6, "accent4": 7, "accent5": 8, "accent6": 9, "hlink": 10, "folhlink": 11}
_PRESET = {"black": "000000", "white": "FFFFFF", "red": "FF0000", "green": "008000", "blue": "0000FF",
           "yellow": "FFFF00", "gray": "808080", "grey": "808080"}


def ajusta_cor(hexrgb, tint=None, lum_mod=None, lum_off=None):
    r, g, b = (int(hexrgb[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if tint:
        l = l * (1 + tint) if tint < 0 else l * (1 - tint) + tint
    if lum_mod is not None:
        l *= lum_mod
    if lum_off is not None:
        l += lum_off
    l = min(max(l, 0.0), 1.0)
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))


# ---------------------------------------------------------------- estilos
_FORMATOS = {0: "General", 1: "0", 2: "0.00", 3: "#,##0", 4: "#,##0.00", 9: "0%", 10: "0.00%", 14: "dd/mm/yyyy",
             15: "d-mmm-yy", 16: "d-mmm", 17: "mmm-yy", 18: "h:mm AM/PM", 19: "h:mm:ss AM/PM", 20: "h:mm",
             21: "h:mm:ss", 22: "dd/mm/yyyy hh:mm", 45: "mm:ss", 46: "[h]:mm:ss", 47: "mmss.0", 49: "@"}
_PADRAO = dict(fonte=dict(nome="Calibri", tam=11.0, b=False, i=False, u=False, cor="000000"), fill=None, borda={},
               numfmt="General", h=None, v=None, wrap=False, indent=0)


def _limpa_fmt(code):
    return re.sub(r'"[^"]*"|\[[^\]]*\]|\\.|_.|\*.', "", code)


def eh_data(code):
    s = _limpa_fmt(code)
    return bool(re.search(r"[dmyhs]", s, re.I)) and not re.search(r"[0#]", s)


def formata_data(v, code):
    dt = datetime(1899, 12, 30) + timedelta(days=v)
    s, out, prev = _limpa_fmt(code), "", ""
    for tok in re.finditer(r"yyyy|yy|mmmm|mmm|mm|m|dddd|ddd|dd|d|hh|h|ss|s|AM/PM|am/pm|.", s, re.I):
        t = tok.group(0)
        tl = t.lower()
        if tl in ("yyyy",):
            out += dt.strftime("%Y")
        elif tl == "yy":
            out += dt.strftime("%y")
        elif tl in ("mm", "m"):
            minuto = prev in ("h", "hh") or s[tok.end():tok.end() + 1] == ":"
            out += dt.strftime("%M") if minuto else (dt.strftime("%m") if tl == "mm" else str(dt.month))
        elif tl == "mmm":
            out += dt.strftime("%b")
        elif tl == "mmmm":
            out += dt.strftime("%B")
        elif tl in ("dd", "d"):
            out += dt.strftime("%d") if tl == "dd" else str(dt.day)
        elif tl in ("ddd", "dddd"):
            out += dt.strftime("%a" if tl == "ddd" else "%A")
        elif tl in ("hh", "h"):
            out += dt.strftime("%H") if "am/pm" not in s.lower() else dt.strftime("%I")
        elif tl in ("ss", "s"):
            out += dt.strftime("%S")
        elif tl == "am/pm":
            out += dt.strftime("%p")
        else:
            out += t
        prev = tl
    return out


def formata_numero(raw, code):
    try:
        v = float(raw)
    except (TypeError, ValueError):
        return raw
    code = code or "General"
    if code in ("@",):
        return raw
    if eh_data(code):
        try:
            return formata_data(v, code)
        except (OverflowError, ValueError):
            return raw
    parte = code.split(";")[0]
    pct = "%" in parte
    if pct:
        v *= 100
    if parte.lower() == "general" or not re.search(r"[0#]", parte):
        txt = repr(round(v, 10))
        return txt[:-2] if txt.endswith(".0") else txt
    dec = len(re.search(r"\.([0#]*)", parte).group(1)) if "." in parte else 0
    txt = f"{v:,.{dec}f}" if "," in parte else f"{v:.{dec}f}"
    if "," in parte:
        txt = txt.replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        txt = txt.replace(".", ",")
    return txt + ("%" if pct else "")


class Estilos:
    def __init__(self, z, names):
        self.tema = list(_TEMA_PADRAO)
        if "xl/theme/theme1.xml" in names:
            esq = ET.fromstring(z.read("xl/theme/theme1.xml")).find(".//a:clrScheme", NS)
            if esq is not None:
                ordem = ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6",
                         "hlink", "folHlink"]
                v = {}
                for el in esq:
                    ch = el[0] if len(el) else None
                    if ch is not None:
                        v[_tag(el)] = ch.get("lastClr") or ch.get("val")
                try:  # índice do Excel: 0=lt1 1=dk1 2=lt2 3=dk2 4..9=accent 10=hlink 11=folHlink
                    self.tema = [v["lt1"], v["dk1"], v["lt2"], v["dk2"]] + [v[k] for k in ordem[4:]]
                except KeyError:
                    pass
        self.xfs = [dict(_PADRAO)]
        if "xl/styles.xml" not in names:
            return
        root = ET.fromstring(z.read("xl/styles.xml"))
        numfmts = {int(n.get("numFmtId")): n.get("formatCode") for n in root.findall("m:numFmts/m:numFmt", NS)}
        fontes = []
        for f in root.findall("m:fonts/m:font", NS):
            def flag(tag):
                e = f.find(f"m:{tag}", NS)
                return e is not None and e.get("val", "1") not in ("0", "false")
            nome, tam = f.find("m:name", NS), f.find("m:sz", NS)
            fontes.append(dict(nome=nome.get("val") if nome is not None else "Calibri",
                               tam=float(tam.get("val")) if tam is not None else 11.0,
                               b=flag("b"), i=flag("i"), u=f.find("m:u", NS) is not None,
                               cor=self.cor_xl(f.find("m:color", NS)) or "000000"))
        fills = []
        for f in root.findall("m:fills/m:fill", NS):
            pf = f.find("m:patternFill", NS)
            fills.append(self.cor_xl(pf.find("m:fgColor", NS)) if pf is not None and pf.get("patternType") == "solid"
                         and pf.find("m:fgColor", NS) is not None else None)
        bordas = []
        for b in root.findall("m:borders/m:border", NS):
            d = {}
            for lado, nome in (("left", "esq"), ("right", "dir"), ("top", "sup"), ("bottom", "inf")):
                e = b.find(f"m:{lado}", NS)
                if e is not None and e.get("style"):
                    d[nome] = (e.get("style"), self.cor_xl(e.find("m:color", NS)) or "000000")
            bordas.append(d)
        self.xfs = []
        for xf in root.findall("m:cellXfs/m:xf", NS):
            al = xf.find("m:alignment", NS)
            fid = int(xf.get("numFmtId", 0))
            fo, fi, bo = int(xf.get("fontId", 0)), int(xf.get("fillId", 0)), int(xf.get("borderId", 0))
            self.xfs.append(dict(
                fonte=fontes[fo] if fo < len(fontes) else _PADRAO["fonte"],
                fill=fills[fi] if fi < len(fills) else None,
                borda=bordas[bo] if bo < len(bordas) else {},
                numfmt=numfmts.get(fid) or _FORMATOS.get(fid, "General"),
                h=al.get("horizontal") if al is not None else None,
                v=al.get("vertical") if al is not None else None,
                wrap=al is not None and al.get("wrapText") in ("1", "true"),
                indent=int(al.get("indent", 0)) if al is not None else 0))
        if not self.xfs:
            self.xfs = [dict(_PADRAO)]

    def cor_xl(self, e):
        if e is None:
            return None
        if e.get("rgb"):
            return e.get("rgb")[-6:].upper()
        tint = float(e.get("tint", 0)) or None
        if e.get("theme") is not None:
            i = int(e.get("theme"))
            return ajusta_cor(self.tema[i], tint=tint) if i < len(self.tema) else None
        if e.get("indexed") is not None:
            base = _INDEXADAS.get(int(e.get("indexed")), "000000")
            return ajusta_cor(base, tint=tint) if tint else base
        return None

    def cor_dml(self, e):
        """Cor de um elemento DrawingML (srgbClr, schemeClr, sysClr, prstClr)."""
        if e is None:
            return None
        t = _tag(e)
        if t == "srgbClr":
            base = e.get("val", "000000").upper()
        elif t == "sysClr":
            base = (e.get("lastClr") or "000000").upper()
        elif t == "prstClr":
            base = _PRESET.get(e.get("val", "black"), "000000")
        elif t == "schemeClr":
            i = _NOMES_TEMA.get(e.get("val", "tx1").lower(), 1)
            base = self.tema[i] if i < len(self.tema) else "000000"
        else:
            return None
        mod = off = tint = alpha = None
        for ch in e:
            ct = _tag(ch)
            if ct == "alpha":
                alpha = int(ch.get("val", 100000)) / 100000
                if alpha < 0.05:  # praticamente transparente
                    return None
            if ct == "lumMod":
                mod = int(ch.get("val")) / 100000
            elif ct == "lumOff":
                off = int(ch.get("val")) / 100000
            elif ct == "tint":
                tint = (int(ch.get("val")) / 100000) - 1
        cor = ajusta_cor(base, tint=None, lum_mod=mod, lum_off=off) if (mod is not None or off is not None) else base
        if alpha is not None and alpha < 1:  # transparência parcial: "AARRGGBB", formato que o QColor aceita depois do "#"
            return f"{round(alpha * 255):02X}{cor}"
        return cor


# ---------------------------------------------------------------- modelo
class Cell:
    __slots__ = ("texto", "tipo", "estilo", "formula", "orig", "editado")

    def __init__(self, texto="", tipo="texto", estilo=None, formula=False):
        self.texto, self.tipo, self.estilo, self.formula = texto, tipo, estilo or _PADRAO, formula
        self.orig, self.editado = texto, False


class Planilha:
    def __init__(self, nome, estado, ordem, path):
        self.nome, self.estado, self.ordem, self.path = nome, estado, ordem, path
        self.cells = {}
        self.merges = {}      # (r1,c1) -> (r2,c2)
        self.cobertas = {}    # (r,c) -> (r1,c1,r2,c2)
        self.col_w, self.row_h = {}, {}
        self.larg_padrao, self.alt_padrao = 64.0, 20.0
        self.grade = True
        self.elementos = []
        self.ncols = self.nrows = 0
        self.col_x, self.row_y = [0.0], [0.0]
        self.drawings = []

    def finalizar(self):
        self.ncols = min(self.ncols + 3, MAX_COLS)
        self.nrows = self.nrows + 25
        self.col_x, self.row_y = [0.0], [0.0]
        for c in range(self.ncols):
            self.col_x.append(self.col_x[-1] + self.col_w.get(c, self.larg_padrao))
        for r in range(self.nrows):
            self.row_y.append(self.row_y[-1] + self.row_h.get(r, self.alt_padrao))

    @property
    def largura(self):
        return self.col_x[-1]

    @property
    def altura(self):
        return self.row_y[-1]

    def rect(self, r, c):
        return (self.col_x[c], self.row_y[r], self.col_x[c + 1] - self.col_x[c], self.row_y[r + 1] - self.row_y[r])

    def rect_mescla(self, mg):
        r1, c1, r2, c2 = mg
        return (self.col_x[c1], self.row_y[r1], self.col_x[c2 + 1] - self.col_x[c1],
                self.row_y[r2 + 1] - self.row_y[r1])


def _px_col(w):
    return float(round(w * 7))


def _ler_celulas(root, est, ss, pl):
    sd = root.find("m:sheetData", NS)
    if sd is None:
        return
    for row in sd.findall("m:row", NS):
        r = int(row.get("r")) - 1
        if row.get("hidden") in ("1", "true"):
            pl.row_h[r] = 0.0
        elif row.get("ht"):
            pl.row_h[r] = float(row.get("ht")) * 96 / 72
        for c in row.findall("m:c", NS):
            rr, cc = ref_rc(c.get("r"))
            if cc >= MAX_COLS:
                continue
            xf = est.xfs[int(c.get("s", 0))] if int(c.get("s", 0)) < len(est.xfs) else est.xfs[0]
            t, v = c.get("t"), c.find("m:v", NS)
            formula = c.find("m:f", NS) is not None
            tipo, texto = "texto", ""
            if t == "inlineStr":
                texto = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
            elif t == "s" and v is not None and v.text is not None:
                texto = ss[int(v.text)]
            elif t == "str" and v is not None:
                texto = v.text or ""
            elif t == "b" and v is not None:
                tipo, texto = "bool", "VERDADEIRO" if v.text == "1" else "FALSO"
            elif t == "e" and v is not None:
                tipo, texto = "erro", v.text or ""
            elif v is not None and v.text is not None:
                tipo, texto = "num", formata_numero(v.text, xf["numfmt"])
            pl.cells[(rr, cc)] = Cell(texto, tipo, xf, formula)
            pl.ncols, pl.nrows = max(pl.ncols, cc + 1), max(pl.nrows, rr + 1)


def _extremos_desenho(root, pl):
    for anc in root:
        for tag in ("from", "to"):
            e = anc.find(f"xdr:{tag}", NS)
            if e is not None:
                pl.ncols = max(pl.ncols, min(int(e.find("xdr:col", NS).text) + 1, MAX_COLS))
                pl.nrows = max(pl.nrows, int(e.find("xdr:row", NS).text) + 1)


def _ponto(pl, e):
    c, r = int(e.find("xdr:col", NS).text), int(e.find("xdr:row", NS).text)
    co, ro = int(e.find("xdr:colOff", NS).text) / EMU, int(e.find("xdr:rowOff", NS).text) / EMU
    c, r = min(c, len(pl.col_x) - 2), min(r, len(pl.row_y) - 2)
    return pl.col_x[c] + co, pl.row_y[r] + ro


def _xfrm(parent):
    x = parent.find("a:xfrm", NS) if parent is not None else None
    if x is None:
        return None
    off, ext = x.find("a:off", NS), x.find("a:ext", NS)
    cho, che = x.find("a:chOff", NS), x.find("a:chExt", NS)
    g = lambda e, a: float(e.get(a, 0)) if e is not None else 0.0  # noqa: E731
    return dict(x=g(off, "x"), y=g(off, "y"), cx=g(ext, "cx"), cy=g(ext, "cy"),
                chx=g(cho, "x") if cho is not None else g(off, "x"), chy=g(cho, "y") if cho is not None else g(off, "y"),
                chcx=g(che, "cx") if che is not None else g(ext, "cx"), chcy=g(che, "cy") if che is not None else g(ext, "cy"),
                rot=float(x.get("rot", 0)) / 60000.0, fh=x.get("flipH") in ("1", "true"), fv=x.get("flipV") in ("1", "true"))


def _texto_forma(node, est):
    tb = node.find("xdr:txBody", NS)
    if tb is None:
        return [], "t"
    anc = (tb.find("a:bodyPr", NS).get("anchor") if tb.find("a:bodyPr", NS) is not None else None) or "t"
    paras = []
    for p in tb.findall("a:p", NS):
        ppr = p.find("a:pPr", NS)
        runs = []
        for el in p:
            t = _tag(el)
            if t == "r":
                rp, tx = el.find("a:rPr", NS), el.find("a:t", NS)
                sf = rp.find("a:solidFill", NS) if rp is not None else None
                cor = est.cor_dml(sf[0]) if sf is not None and len(sf) else None
                runs.append((tx.text or "" if tx is not None else "",
                             float(rp.get("sz", 1100)) / 100 if rp is not None and rp.get("sz") else 11.0,
                             rp is not None and rp.get("b") in ("1", "true"),
                             rp is not None and rp.get("i") in ("1", "true"), cor or "000000"))
            elif t == "br":
                runs.append(("\n", 11.0, False, False, "000000"))
        paras.append(dict(runs=runs, algn=(ppr.get("algn") if ppr is not None else None) or "l"))
    return paras, anc


def _ler_custgeom(node):
    """Forma livre (custGeom): devolve [{w, h, fill, stroke, cmds}] com os comandos do caminho, ou None."""
    cg = node.find("xdr:spPr/a:custGeom", NS)
    if cg is None:
        return None
    paths = []
    try:
        for pa in cg.findall("a:pathLst/a:path", NS):
            cmds = []
            for ch in pa:
                t = _tag(ch)
                pts = [(float(p.get("x")), float(p.get("y"))) for p in ch.findall("a:pt", NS)]
                if t == "moveTo":
                    cmds.append(("M",) + pts[0])
                elif t == "lnTo":
                    cmds.append(("L",) + pts[0])
                elif t == "cubicBezTo":
                    cmds.append(("C",) + pts[0] + pts[1] + pts[2])
                elif t == "quadBezTo":
                    cmds.append(("Q",) + pts[0] + pts[1])
                elif t == "arcTo":
                    cmds.append(("A", float(ch.get("wR")), float(ch.get("hR")), float(ch.get("stAng")), float(ch.get("swAng"))))
                elif t == "close":
                    cmds.append(("Z",))
            paths.append(dict(w=float(pa.get("w", 0)), h=float(pa.get("h", 0)), fill=pa.get("fill", "norm") != "none",
                              stroke=pa.get("stroke", "1") not in ("0", "false"), cmds=cmds))
    except (TypeError, ValueError):
        return None  # pontos que são fórmulas (não números): cai no desenho simplificado
    return paths or None


def _ler_desenho(z, names, tgt, pl, est):
    root = ET.fromstring(z.read(tgt))
    dr = rels_de(z, names, tgt)
    _extremos_desenho(root, pl)
    return root, dr, tgt


def _construir_elementos(root, dr, pl, est, tgt="", objetos=None, tamanhos=None, movimentos=None):
    """Percorre os anchors do desenho e gera elementos (pic/forma/linha) com coordenadas em px.
    objetos = {índice do anchor: imagem}: anchors de formas que o usuário trocou por uma imagem.
    tamanhos = {(célula, seq): (largura_px, altura_px)}: tamanho escolhido para uma imagem."""
    n = 0
    idx = -1
    for anc in root:
        tipo = _tag(anc)
        if tipo not in ("twoCellAnchor", "oneCellAnchor", "absoluteAnchor"):
            continue
        idx += 1
        fr = anc.find("xdr:from", NS)
        fx, fy = _ponto(pl, fr) if fr is not None else (0.0, 0.0)
        celula = rc_ref(int(fr.find("xdr:row", NS).text), int(fr.find("xdr:col", NS).text)) if fr is not None else "A1"
        if tipo == "twoCellAnchor":
            tx, ty = _ponto(pl, anc.find("xdr:to", NS))
            caixa = (fx, fy, max(tx - fx, 1.0), max(ty - fy, 1.0))
        elif tipo == "oneCellAnchor":
            ex = anc.find("xdr:ext", NS)
            caixa = (fx, fy, float(ex.get("cx")) / EMU, float(ex.get("cy")) / EMU)
        else:
            pos, ex = anc.find("xdr:pos", NS), anc.find("xdr:ext", NS)
            caixa = (float(pos.get("x")) / EMU, float(pos.get("y")) / EMU, float(ex.get("cx")) / EMU, float(ex.get("cy")) / EMU)
        seq_blip = {}
        for b in anc.iter("{%s}blip" % NS["a"]):
            emb = b.get(EMBED)
            if emb and emb in dr:
                n += 1
                seq_blip[id(b)] = (n, dr[emb][1])
        filhos = [c for c in anc if _tag(c) in ("pic", "sp", "grpSp", "cxnSp", "AlternateContent")]
        solo = len(filhos) == 1 and _tag(filhos[0]) == "pic"      # imagem solta: o tamanho pode ser editado
        orig = (caixa[2], caixa[3])
        tams = tamanhos or {}
        if objetos and idx in objetos:                            # forma trocada por imagem: ocupa o quadro do anchor
            seq = 1000 + idx
            novo = tams.get((celula, seq))
            if novo:
                caixa = (caixa[0], caixa[1], float(novo[0]), float(novo[1]))
            mov = (movimentos or {}).get((celula, seq), (0.0, 0.0))
            caixa = (caixa[0] + mov[0], caixa[1] + mov[1], caixa[2], caixa[3])
            x, y, w, h = caixa
            pl.elementos.append(dict(tipo="pic", w=w, h=h, m=_mul(_ID, _local(x, y, w, h, 0, False, False)),
                                     crop=(0, 0, 0, 0), midia=objetos[idx], seq=seq, celula=celula, nome="", anc=idx,
                                     desenho=tgt, tam_ok=True, orig=orig, obj=True, mov=mov))
            continue
        mov = (0.0, 0.0)
        if solo and len(seq_blip) == 1:
            (seq, _), = seq_blip.values()
            novo = tams.get((celula, seq))
            if novo:
                caixa = (caixa[0], caixa[1], float(novo[0]), float(novo[1]))
            mov = (movimentos or {}).get((celula, seq), (0.0, 0.0))
            caixa = (caixa[0] + mov[0], caixa[1] + mov[1], caixa[2], caixa[3])
        ctx = dict(celula=celula, seq=seq_blip, est=est, pl=pl, idx=idx, tgt=tgt, solo=solo, orig=orig, mov=mov)
        for ch in anc:
            _visita(ch, _ID, None, caixa, ctx, None)


_ID = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def _mul(A, B):
    """Composição de transformações afins (a,b,c,d,e,f): aplica B e depois A."""
    a1, b1, c1, d1, e1, f1 = A
    a2, b2, c2, d2, e2, f2 = B
    return (a1 * a2 + c1 * b2, b1 * a2 + d1 * b2, a1 * c2 + c1 * d2, b1 * c2 + d1 * d2,
            a1 * e2 + c1 * f2 + e1, b1 * e2 + d1 * f2 + f1)


def _local(x, y, w, h, rot, fh, fv):
    """Do desenho local (0..w, 0..h) para o espaço do pai: espelha, gira (horário) em torno do centro e posiciona em (x,y)."""
    cx, cy = w / 2, h / 2
    r = math.radians(rot)
    cs, sn = math.cos(r), math.sin(r)
    m = (1.0, 0.0, 0.0, 1.0, x + cx, y + cy)
    m = _mul(m, (cs, sn, -sn, cs, 0.0, 0.0))
    m = _mul(m, (-1.0 if fh else 1.0, 0.0, 0.0, -1.0 if fv else 1.0, 0.0, 0.0))
    return _mul(m, (1.0, 0.0, 0.0, 1.0, -cx, -cy))


def _visita(node, P, cm, caixa, ctx, gfill):
    """P: transformação do espaço local do pai para a planilha (px). cm: (chX, chY, escalaX, escalaY) que leva as
    coordenadas EMU dos filhos do grupo pai para o espaço local dele (None no nível do anchor). gfill: cor do grupo
    (as peças com <a:grpFill/> herdam essa cor)."""
    t = _tag(node)
    if t == "AlternateContent":
        ch = node.find("mc:Choice", NS)
        for x in (ch if ch is not None else []):
            _visita(x, P, cm, caixa, ctx, gfill)
        return
    if t not in ("grpSp", "sp", "pic", "cxnSp"):
        return
    pr = node.find("xdr:grpSpPr", NS) if t == "grpSp" else node.find("xdr:spPr", NS)
    xf = _xfrm(pr)
    if cm is None:
        x, y, w, h = caixa
        if xf and abs(xf["rot"]) > 0.01 and xf["cx"] and xf["cy"]:
            # forma girada: o anchor é a caixa visual; o quadro real (antes de girar) vem do xfrm, com o mesmo centro
            cxm, cym = x + w / 2, y + h / 2
            w, h = xf["cx"] / EMU, xf["cy"] / EMU
            x, y = cxm - w / 2, cym - h / 2
    elif xf is not None:
        chx, chy, sx, sy = cm
        x, y = (xf["x"] - chx) * sx, (xf["y"] - chy) * sy
        w, h = xf["cx"] * sx, xf["cy"] * sy
    else:
        return
    rot, fh, fv = (xf["rot"], xf["fh"], xf["fv"]) if xf else (0.0, False, False)
    M = _mul(P, _local(x, y, w, h, rot, fh, fv))   # do desenho local da forma até a planilha
    pl, est, out = ctx["pl"], ctx["est"], ctx["pl"].elementos
    if t == "grpSp":
        if xf is None:
            return
        sx = w / xf["chcx"] if xf["chcx"] else 1.0
        sy = h / xf["chcy"] if xf["chcy"] else 1.0
        sf = node.find("xdr:grpSpPr/a:solidFill", NS)
        g2 = est.cor_dml(sf[0]) if sf is not None and len(sf) else gfill
        for ch in node:
            _visita(ch, M, (xf["chx"], xf["chy"], sx, sy), caixa, ctx, g2)
        return
    blip = node.find(".//a:blip", NS)
    if t == "pic" or (t == "sp" and blip is not None and id(blip) in ctx["seq"]):
        if blip is not None and id(blip) in ctx["seq"]:
            seq, midia = ctx["seq"][id(blip)]
            sr = node.find(".//a:srcRect", NS)
            crop = tuple(int(sr.get(k, 0)) / 100000 for k in "ltrb") if sr is not None else (0, 0, 0, 0)
            nome = node.find(".//xdr:cNvPr", NS)
            out.append(dict(tipo="pic", w=w, h=h, m=M, crop=crop, midia=midia, seq=seq, celula=ctx["celula"],
                            nome=nome.get("name") if nome is not None else "", anc=ctx["idx"], desenho=ctx["tgt"],
                            tam_ok=bool(ctx["solo"]) and cm is None and abs(rot) < 0.01, orig=ctx["orig"], obj=False, mov=ctx["mov"]))
        return
    geom = node.find("xdr:spPr/a:prstGeom", NS)
    prst = geom.get("prst") if geom is not None else "rect"
    if t == "cxnSp" or prst in ("line", "straightConnector1") or prst.startswith("bentConnector") or prst.startswith("curvedConnector"):
        ln = node.find("xdr:spPr/a:ln", NS)
        cor, larg = "000000", 1.0
        if ln is not None:
            sf = ln.find("a:solidFill", NS)
            if sf is not None and len(sf):
                cor = est.cor_dml(sf[0]) or cor
            larg = max(float(ln.get("w", 9525)) / EMU, 1.0)
        elif node.find("xdr:style/a:lnRef", NS) is not None and len(node.find("xdr:style/a:lnRef", NS)):
            cor = est.cor_dml(node.find("xdr:style/a:lnRef", NS)[0]) or cor
        out.append(dict(tipo="linha", w=w, h=h, m=M, cor=cor, larg=larg, anc=ctx["idx"], desenho=ctx["tgt"],
                        celula=ctx["celula"], orig=ctx["orig"]))
        return
    sp = node.find("xdr:spPr", NS)
    fill, line = None, None
    if sp is not None:
        sf = sp.find("a:solidFill", NS)
        if sf is not None and len(sf):
            fill = est.cor_dml(sf[0])
        gs = sp.find("a:gradFill/a:gsLst/a:gs", NS)  # degradê: usa a cor da primeira parada
        if fill is None and gs is not None and len(gs):
            fill = est.cor_dml(gs[0])
        pf = sp.find("a:pattFill/a:fgClr", NS)
        if fill is None and pf is not None and len(pf):
            fill = est.cor_dml(pf[0])
        if sp.find("a:grpFill", NS) is not None:      # herda o preenchimento do grupo
            fill = gfill
        ln = sp.find("a:ln", NS)
        if ln is not None and ln.find("a:noFill", NS) is None:
            lf = ln.find("a:solidFill", NS)
            lc = est.cor_dml(lf[0]) if lf is not None and len(lf) else None
            if lc or ln.get("w"):
                line = (lc or "000000", max(float(ln.get("w", 9525)) / EMU, 1.0))
    st = node.find("xdr:style", NS)
    if st is not None and sp is not None:
        if (fill is None and sp.find("a:noFill", NS) is None and sp.find("a:solidFill", NS) is None
                and sp.find("a:gradFill", NS) is None and sp.find("a:pattFill", NS) is None
                and sp.find("a:grpFill", NS) is None):
            fr = st.find("a:fillRef", NS)
            if fr is not None and fr.get("idx") != "0" and len(fr):
                fill = est.cor_dml(fr[0])
        if line is None and (sp.find("a:ln", NS) is None) and st.find("a:lnRef", NS) is not None:
            lr = st.find("a:lnRef", NS)
            if lr.get("idx") != "0" and len(lr):
                line = (est.cor_dml(lr[0]) or "000000", 1.0)
    paras, anc_v = _texto_forma(node, est)
    adj = {}
    for gd in node.findall("xdr:spPr/a:prstGeom/a:avLst/a:gd", NS):
        mm = re.match(r"val\s+(-?\d+)", gd.get("fmla", ""))
        if mm:
            adj[gd.get("name")] = int(mm.group(1))
    out.append(dict(tipo="forma", geom=prst, w=w, h=h, m=M, fill=fill, line=line, paras=paras, anc_v=anc_v, adj=adj,
                    paths=_ler_custgeom(node), anc=ctx["idx"], desenho=ctx["tgt"], celula=ctx["celula"], orig=ctx["orig"]))


def ler_pasta(z, progress=None, larguras=None, mesclagens=None, objetos=None, tamanhos=None, movimentos=None):
    """Lê todas as abas do xlsx e devolve a lista de Planilha (modelos puros, sem Qt).
    larguras = {aba: {coluna (0..): largura em caracteres}} e mesclagens = {aba: {referência original: nova}}:
    ajustes que valem por cima do arquivo. objetos = {aba: {índice do anchor: imagem}} (formas trocadas por imagem) e
    tamanhos = {aba: {(célula, seq): (largura, altura)}} (tamanho de imagens, em px) e
    movimentos = {aba: {(célula, seq): (dx, dy)}} (deslocamento de imagens em relação ao arquivo, em px)."""
    names = set(z.namelist())
    est = Estilos(z, names)
    ss = []
    if "xl/sharedStrings.xml" in names:
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    wrels = rels_de(z, names, "xl/workbook.xml")
    abas = list(wb.find("m:sheets", NS))
    planilhas = []
    for idx, s in enumerate(abas, 1):
        path = wrels[s.get(RID)][1]
        pl = Planilha(s.get("name"), s.get("state", "visible"), idx, path)
        root = ET.fromstring(z.read(path))
        fmt = root.find("m:sheetFormatPr", NS)
        if fmt is not None:
            if fmt.get("defaultRowHeight"):
                pl.alt_padrao = float(fmt.get("defaultRowHeight")) * 96 / 72
            if fmt.get("defaultColWidth"):
                pl.larg_padrao = _px_col(float(fmt.get("defaultColWidth")))
        sv = root.find("m:sheetViews/m:sheetView", NS)
        pl.grade = sv is None or sv.get("showGridLines", "1") not in ("0", "false")
        for col in root.findall("m:cols/m:col", NS):
            mn, mx = int(col.get("min")) - 1, min(int(col.get("max")) - 1, MAX_COLS - 1)
            w = 0.0 if col.get("hidden") in ("1", "true") else _px_col(float(col.get("width", 8.43)))
            for i in range(mn, mx + 1):
                pl.col_w[i] = w
        for ci, chars in (larguras or {}).get(pl.nome, {}).items():
            pl.col_w[ci] = _px_col(float(chars))
            pl.ncols = max(pl.ncols, ci + 1)
        _ler_celulas(root, est, ss, pl)
        ajustes_m = (mesclagens or {}).get(pl.nome, {})
        refs_m = [ajustes_m.get(mc.get("ref"), mc.get("ref")) for mc in root.findall("m:mergeCells/m:mergeCell", NS)]
        for velha, nova in ajustes_m.items():
            for pos in celulas_liberadas(velha, nova):
                if pos in pl.cells:
                    pl.cells[pos].estilo = _PADRAO
        for ref_mc in refs_m:
            a, b = ref_mc.split(":") if ":" in ref_mc else (ref_mc, ref_mc)
            (r1, c1), (r2, c2) = ref_rc(a), ref_rc(b)
            if c2 >= MAX_COLS:
                continue
            pl.merges[(r1, c1)] = (r2, c2)
            for rr in range(r1, r2 + 1):
                for cc in range(c1, c2 + 1):
                    pl.cobertas[(rr, cc)] = (r1, c1, r2, c2)
            pl.ncols, pl.nrows = max(pl.ncols, c2 + 1), max(pl.nrows, r2 + 1)
        desenhos = []
        for typ, tgt in rels_de(z, names, path).values():
            if typ == "drawing" and tgt in names:
                desenhos.append(_ler_desenho(z, names, tgt, pl, est))
        pl.finalizar()
        for root_d, dr, tgt_d in desenhos:
            _construir_elementos(root_d, dr, pl, est, tgt_d, (objetos or {}).get(pl.nome), (tamanhos or {}).get(pl.nome),
                                (movimentos or {}).get(pl.nome))
        planilhas.append(pl)
        if progress:
            progress(idx, len(abas))
    return planilhas


# ---------------------------------------------------------------- padronizar o bloco de aprovação
_ROT_BLOCO = (("ELABORADO / REVISADO POR:", "ELABORADO POR:"), ("APROVADO POR:", "REVISADO POR:"), ("HOMOLOGADO POR (SGQ):",))


def blocos_aprovacao(pl):
    """Acha os três cabeçalhos do bloco de aprovação (ELABORADO / APROVADO / HOMOLOGADO) na mesma linha.
    Devolve [(linha, col_ini, col_fim)] x3 ou None."""
    achou = {}
    for (r, c), cell in pl.cells.items():
        t = cell.texto.strip()
        for k, rotulos in enumerate(_ROT_BLOCO):
            if t in rotulos:
                mg = pl.cobertas.get((r, c))
                achou[k] = (r, mg[1], mg[3]) if mg else (r, c, c)
    if len(achou) == 3 and len({v[0] for v in achou.values()}) == 1:
        return [achou[0], achou[1], achou[2]]
    return None


def plano_padronizacao(planilhas):
    """Define o padrão das colunas do bloco de aprovação: entre as abas que têm o mesmo formato (mesmo número de
    colunas em cada um dos três cabeçalhos), vale o padrão mais comum. Só mexe em grupos com 3+ abas.
    Devolve ({aba: {coluna: largura_em_caracteres}}, resumo)."""
    grupos = {}
    for pl in planilhas:
        b = blocos_aprovacao(pl)
        if b:
            cols = [c for _, c1, c2 in b for c in range(c1, c2 + 1)]
            larg = tuple(pl.col_w.get(c, pl.larg_padrao) for c in cols)
            grupos.setdefault(tuple(c2 - c1 + 1 for _, c1, c2 in b), []).append((pl, cols, larg))
    plano, resumo = {}, []
    for formato, itens in grupos.items():
        if len(itens) < 3:
            resumo.append(("ignorada", formato, [pl.nome for pl, _, _ in itens]))
            continue
        padrao = Counter(larg for _, _, larg in itens).most_common(1)[0][0]
        for pl, cols, larg in itens:
            dif = {c: padrao[i] / 7 for i, c in enumerate(cols) if abs(larg[i] - padrao[i]) > 0.5}
            if dif:
                plano[pl.nome] = dif
        resumo.append(("padronizada", formato, [pl.nome for pl, _, _ in itens if pl.nome in plano]))
    return plano, resumo


def plano_alinhamento(planilhas):
    """Nas abas em que as células do corpo do bloco de aprovação (ELABORADO / APROVADO / HOMOLOGADO) terminam em linhas
    diferentes, iguala o fim delas: vale a linha em que a maioria termina (empate: a mais curta, ou seja, a célula que
    "passa para baixo" encolhe). Só altera mesclagens que já existem.
    Devolve ({aba: {mesclagem original: nova}}, resumo [(aba, fim de cada célula antes, fim depois)])."""
    plano, resumo = {}, []
    for pl in planilhas:
        b = blocos_aprovacao(pl)
        if not b:
            continue
        existentes = [pl.merges.get((lin + 1, c1)) for lin, c1, _ in b]   # (linha_fim, col_fim) ou None
        fins = [mg[0] for mg in existentes if mg]
        if len(fins) < 2 or len(set(fins)) == 1:
            continue
        mais_comum, qtd = Counter(fins).most_common(1)[0]
        alvo = mais_comum if qtd >= 2 else min(fins)
        mud = {}
        for (lin, c1, _), mg in zip(b, existentes):
            if mg and mg[0] != alvo:
                r1 = lin + 2
                mud[f"{colname(c1)}{r1}:{colname(mg[1])}{mg[0] + 1}"] = f"{colname(c1)}{r1}:{colname(mg[1])}{alvo + 1}"
        plano[pl.nome] = mud
        resumo.append((pl.nome, [mg[0] + 1 if mg else None for mg in existentes], alvo + 1))
    return plano, resumo


def celulas_liberadas(velha, nova):
    """Células que deixam de fazer parte da mesclagem quando ela encolhe (de `velha` para `nova`)."""
    a1, b1 = velha.split(":")
    a2, b2 = nova.split(":")
    (_, c1), (r2_velha, c2) = ref_rc(a1), ref_rc(b1)
    r2_nova = ref_rc(b2)[0]
    return [(r, c) for r in range(r2_nova + 1, r2_velha + 1) for c in range(c1, c2 + 1)]


def aplicar_mesclagens_xml(xml_bytes, mesclagens):
    """Troca no XML da aba as referências de células mescladas ({referência original: nova}) e tira o estilo
    (bordas, preenchimento) das células que ficaram livres, para não sobrar resíduo da mesclagem antiga."""
    xml = xml_bytes.decode("utf-8")
    for velha, nova in mesclagens.items():
        padrao = f'<mergeCell ref="{velha}"/>'
        if padrao in xml:
            xml = xml.replace(padrao, f'<mergeCell ref="{nova}"/>', 1)
        for r, c in celulas_liberadas(velha, nova):
            ref = rc_ref(r, c)
            tag = re.search(rf'<c\b(?=[^>]*?\sr="{ref}")[^>]*?/?>', xml)
            if tag:
                xml = xml[:tag.start()] + re.sub(r'\ss="[^"]*"', "", tag.group(0)) + xml[tag.end():]
    return xml.encode("utf-8")


def aplicar_larguras_xml(xml_bytes, larguras):
    """Grava {coluna(0..): largura em caracteres} no <cols> do XML da aba, dividindo as faixas quando preciso."""
    xml = xml_bytes.decode("utf-8")
    segs = []   # [mn, mx, {atributos}]
    m = re.search(r"<cols>(.*?)</cols>", xml, re.S)
    if m:
        for c in re.findall(r"<col\b[^>]*/>", m.group(1)):
            a = dict(re.findall(r'([\w:]+)="([^"]*)"', c))
            segs.append([int(a.pop("min")), int(a.pop("max")), a])
    for ci, chars in sorted(larguras.items()):
        n = ci + 1                                   # o XML conta colunas a partir de 1
        novo = []
        achou = False
        for mn, mx, a in segs:
            if mn <= n <= mx:
                achou = True
                if mn < n:
                    novo.append([mn, n - 1, dict(a)])
                novo.append([n, n, dict(a, width=f"{chars:.10g}", customWidth="1")])
                if n < mx:
                    novo.append([n + 1, mx, dict(a)])
            else:
                novo.append([mn, mx, a])
        if not achou:
            novo.append([n, n, {"width": f"{chars:.10g}", "customWidth": "1"}])
        segs = sorted(novo, key=lambda s: s[0])

    def col_xml(mn, mx, a):
        resto = "".join(f' {k}="{v}"' for k, v in a.items())
        return f'<col min="{mn}" max="{mx}"{resto}/>'

    bloco = "<cols>" + "".join(col_xml(*s) for s in segs) + "</cols>"
    if m:
        xml = xml[:m.start()] + bloco + xml[m.end():]
    else:
        xml = xml.replace("<sheetData", bloco + "<sheetData", 1)
    return xml.encode("utf-8")


# ---------------------------------------------------------------- desenho: trocar forma por imagem / mudar tamanho
_ANCORA = re.compile(r"<xdr:(twoCellAnchor|oneCellAnchor|absoluteAnchor)\b.*?</xdr:\1>", re.S)
_NS_REL_IMG = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
_ALTERNATIVO = re.compile(r"<mc:AlternateContent\b.*?</mc:AlternateContent>", re.S)


def _ancoras_topo(xml):
    """Os anchors do desenho na mesma ordem e contagem do leitor (ElementTree): só os filhos diretos do desenho,
    sem os que estão dentro de mc:AlternateContent."""
    alt = [(a.start(), a.end()) for a in _ALTERNATIVO.finditer(xml)]
    return [m for m in _ANCORA.finditer(xml) if not any(i < m.start() < f for i, f in alt)]


def _desloca_ponto(trecho, pl, dx, dy):
    """Desloca (px) um <xdr:from>/<xdr:to>: recalcula célula + deslocamento a partir das larguras/alturas da aba."""
    col, col_off, row, row_off = (int(re.search(rf"<xdr:{k}>(-?\d+)</xdr:{k}>", trecho).group(1))
                                  for k in ("col", "colOff", "row", "rowOff"))
    x = max(pl.col_x[min(col, len(pl.col_x) - 2)] + col_off / EMU + dx, 0.0)
    y = max(pl.row_y[min(row, len(pl.row_y) - 2)] + row_off / EMU + dy, 0.0)
    c = min(max(bisect_right(pl.col_x, x) - 1, 0), len(pl.col_x) - 2)
    r = min(max(bisect_right(pl.row_y, y) - 1, 0), len(pl.row_y) - 2)
    novo = {"col": c, "colOff": int(round((x - pl.col_x[c]) * EMU)), "row": r, "rowOff": int(round((y - pl.row_y[r]) * EMU))}
    for k, v in novo.items():
        trecho = re.sub(rf"(<xdr:{k}>)-?\d+(</xdr:{k}>)", lambda mm: f"{mm.group(1)}{v}{mm.group(2)}", trecho, count=1)
    return trecho


def aplicar_movimentos_xml(desenho_bytes, pl, movimentos):
    """Desloca imagens no XML do desenho (o tamanho não muda). movimentos = {índice do anchor: (dx_px, dy_px)} em relação
    à posição do arquivo; pl = modelo da aba (larguras de coluna e alturas de linha)."""
    xml = desenho_bytes.decode("utf-8")
    ms = _ancoras_topo(xml)
    for idx, (dx, dy) in sorted(movimentos.items(), reverse=True):
        m = ms[idx]
        trecho = m.group(0)
        if m.group(1) == "absoluteAnchor":
            def _pos(mm):
                x = max(int(mm.group(2)) + round(dx * EMU), 0)
                y = max(int(mm.group(4)) + round(dy * EMU), 0)
                return f'{mm.group(1)}{x}{mm.group(3)}{y}{mm.group(5)}'
            trecho = re.sub(r'(<xdr:pos x=")(-?\d+)(" y=")(-?\d+)(")', _pos, trecho, count=1)
        else:
            for tag in ("from", "to"):
                trecho = re.sub(rf"<xdr:{tag}>(.*?)</xdr:{tag}>",
                                lambda mm, tag=tag: f"<xdr:{tag}>{_desloca_ponto(mm.group(1), pl, dx, dy)}</xdr:{tag}>",
                                trecho, count=1, flags=re.S)
        xml = xml[:m.start()] + trecho + xml[m.end():]
    return xml.encode("utf-8")


def aplicar_objetos_xml(desenho_bytes, rels_bytes, trocas):
    """Troca, no XML do desenho, o anchor de uma forma por um anchor de imagem no mesmo lugar e tamanho.
    trocas = {índice do anchor: (arquivo da imagem em xl/media, id do relacionamento, largura_px, altura_px)}.
    Devolve (desenho, rels) atualizados."""
    xml, rels = desenho_bytes.decode("utf-8"), rels_bytes.decode("utf-8")
    ms = _ancoras_topo(xml)
    for idx, (arquivo, rid, w, h) in sorted(trocas.items(), reverse=True):   # de trás para frente: os índices não mudam
        m = ms[idx]
        if m.group(1) != "twoCellAnchor":
            raise ValueError("Só dá para trocar formas ancoradas em duas células (twoCellAnchor).")
        de = re.search(r"<xdr:from>.*?</xdr:from>", m.group(0), re.S).group(0)
        ate = re.search(r"<xdr:to>.*?</xdr:to>", m.group(0), re.S).group(0)
        novo = (f'<xdr:twoCellAnchor>{de}{ate}<xdr:pic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
                f'<xdr:nvPicPr><xdr:cNvPr id="{900000 + idx}" name="Imagem IA {idx + 1}"/><xdr:cNvPicPr>'
                '<a:picLocks noChangeAspect="0"/></xdr:cNvPicPr></xdr:nvPicPr><xdr:blipFill>'
                f'<a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="{rid}"/>'
                '<a:stretch><a:fillRect/></a:stretch></xdr:blipFill><xdr:spPr><a:xfrm><a:off x="0" y="0"/>'
                f'<a:ext cx="{int(w * EMU)}" cy="{int(h * EMU)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
                '</xdr:spPr></xdr:pic><xdr:clientData/></xdr:twoCellAnchor>')
        xml = xml[:m.start()] + novo + xml[m.end():]
        rels = rels.replace("</Relationships>", f'<Relationship Id="{rid}" Type="{_NS_REL_IMG}" '
                                                 f'Target="../media/{arquivo}"/></Relationships>')
    return xml.encode("utf-8"), rels.encode("utf-8")


def aplicar_tamanhos_xml(desenho_bytes, pl, tamanhos):
    """Muda o tamanho de imagens soltas no XML do desenho: o canto de cima/esquerda fica onde está e o de baixo/direita
    é recalculado (célula + deslocamento) a partir das larguras de coluna e alturas de linha da aba (pl).
    tamanhos = {índice do anchor: (largura_px, altura_px)}."""
    xml = desenho_bytes.decode("utf-8")
    ms = _ancoras_topo(xml)
    for idx, (w, h) in sorted(tamanhos.items(), reverse=True):
        m = ms[idx]
        if m.group(1) != "twoCellAnchor":
            raise ValueError("Só dá para mudar o tamanho de imagens ancoradas em duas células (twoCellAnchor).")
        trecho = m.group(0)
        de = re.search(r"<xdr:from>(.*?)</xdr:from>", trecho, re.S).group(1)
        col, col_off, row, row_off = (int(re.search(rf"<xdr:{k}>(-?\d+)</xdr:{k}>", de).group(1))
                                      for k in ("col", "colOff", "row", "rowOff"))
        x0 = pl.col_x[min(col, len(pl.col_x) - 2)] + col_off / EMU
        y0 = pl.row_y[min(row, len(pl.row_y) - 2)] + row_off / EMU
        x1, y1 = x0 + w, y0 + h
        c1 = min(max(bisect_right(pl.col_x, x1) - 1, 0), len(pl.col_x) - 2)
        r1 = min(max(bisect_right(pl.row_y, y1) - 1, 0), len(pl.row_y) - 2)
        ate = (f"<xdr:to><xdr:col>{c1}</xdr:col><xdr:colOff>{int(round((x1 - pl.col_x[c1]) * EMU))}</xdr:colOff>"
               f"<xdr:row>{r1}</xdr:row><xdr:rowOff>{int(round((y1 - pl.row_y[r1]) * EMU))}</xdr:rowOff></xdr:to>")
        novo = re.sub(r"<xdr:to>.*?</xdr:to>", lambda _: ate, trecho, count=1, flags=re.S)
        novo = re.sub(r'(<a:ext cx=")\d+(" cy=")\d+(")', lambda mm: f"{mm.group(1)}{int(w * EMU)}{mm.group(2)}{int(h * EMU)}{mm.group(3)}",
                      novo, count=1)
        xml = xml[:m.start()] + novo + xml[m.end():]
    return xml.encode("utf-8")


# ---------------------------------------------------------------- gravar células editadas no XML da aba
_NUM = re.compile(r"^-?\d+([.,]\d+)?$")


def _celula_xml(ref, resto, texto, numerico):
    if texto == "":
        return f'<c r="{ref}"{resto}/>'
    if numerico and _NUM.match(texto.strip()):
        return f'<c r="{ref}"{resto}><v>{texto.strip().replace(",", ".")}</v></c>'
    return f'<c r="{ref}"{resto} t="inlineStr"><is><t xml:space="preserve">{escape(texto)}</t></is></c>'


def aplicar_edicoes_xml(xml_bytes, edicoes):
    """Grava {ref: texto} no XML da aba, no nível de texto (preserva o resto do arquivo byte a byte)."""
    xml = xml_bytes.decode("utf-8")
    for ref, texto in edicoes.items():
        cpat = re.compile(rf'<c\b(?=[^>]*?\sr="{ref}")([^>]*?)(/>|>.*?</c>)', re.S)
        m = cpat.search(xml)
        if m:
            resto = re.sub(r'\s(?:r|t)="[^"]*"', "", m.group(1))
            numerico = not re.search(r'\st="(?!n")', m.group(1))
            xml = xml[:m.start()] + _celula_xml(ref, resto, texto, numerico) + xml[m.end():]
            continue
        r, c = ref_rc(ref)
        nova = _celula_xml(ref, "", texto, True)
        rpat = re.compile(rf'<row\b(?=[^>]*?\sr="{r + 1}")([^>]*?)(/>|>(.*?)</row>)', re.S)
        mr = rpat.search(xml)
        if mr:
            attrs = re.sub(r'\sspans="[^"]*"', "", mr.group(1))
            if attrs.endswith("/"):
                attrs = attrs[:-1]
            inner = mr.group(3) or ""
            pos = len(inner)
            for mc in re.finditer(r'<c\b[^>]*?\sr="([A-Z]+)\d+"', inner):
                if colidx(mc.group(1)) > c:
                    pos = mc.start()
                    break
            xml = xml[:mr.start()] + f"<row{attrs}>{inner[:pos]}{nova}{inner[pos:]}</row>" + xml[mr.end():]
            continue
        linha = f'<row r="{r + 1}">{nova}</row>'
        pos = None
        for mm in re.finditer(r'<row\b[^>]*?\sr="(\d+)"', xml):
            if int(mm.group(1)) > r + 1:
                pos = mm.start()
                break
        if pos is not None:
            xml = xml[:pos] + linha + xml[pos:]
        elif "</sheetData>" in xml:
            xml = xml.replace("</sheetData>", linha + "</sheetData>", 1)
        else:
            xml = xml.replace("<sheetData/>", f"<sheetData>{linha}</sheetData>", 1)
    return xml.encode("utf-8")
