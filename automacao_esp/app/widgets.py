"""Componentes visuais reutilizáveis (sem efeitos animados)."""
import math

from PyQt6.QtCore import QEvent, QPointF, QRectF, Qt, QVariantAnimation
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPixmap
from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QPushButton

from .paths import resource_path
from .theme import theme

_BG_FILES = {True: "assets/background_iot.jpg", False: "assets/background_iot_l.jpg"}  # dark / light
_bg_source = {}  # tema escuro? -> imagem original, carregada uma vez
_bg_cache = {}   # (escuro?, largura, altura) em pixels físicos -> imagem já escalada


def _background(width, height):
    """Imagem de fundo do tema atual cobrindo (width x height), sem distorcer: escala até cobrir e corta o
    excesso, ancorada embaixo à direita (onde fica o texto 'Automação IOT')."""
    dark = theme.is_dark
    if dark not in _bg_source:
        _bg_source[dark] = QPixmap(str(resource_path(_BG_FILES[dark])))
    source = _bg_source[dark]
    if source.isNull() or width <= 0 or height <= 0:
        return None
    key = (dark, width, height)
    if key not in _bg_cache:
        if len(_bg_cache) > 8:
            _bg_cache.clear()
        scaled = source.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                               Qt.TransformationMode.SmoothTransformation)
        _bg_cache[key] = scaled.copy(scaled.width() - width, scaled.height() - height, width, height)
    return _bg_cache[key]


class BackgroundMixin:
    """Pinta o background do tema no fundo da janela (Dark: background_iot.jpg, Light: background_iot_l.jpg),
    responsivo ao tamanho. Usar antes do QWidget/QMainWindow/QDialog na herança."""

    def paintEvent(self, event):
        if getattr(self, "sem_fundo", False):  # dentro de um card da janela principal: o card já tem o fundo
            return
        painter = QPainter(self)
        dpr = self.devicePixelRatioF()
        pm = _background(round(self.width() * dpr), round(self.height() * dpr))
        if pm is None:
            painter.fillRect(self.rect(), QColor(theme.colors["bg"]))
        else:
            pm.setDevicePixelRatio(dpr)
            painter.drawPixmap(QPointF(0, 0), pm)
        painter.end()


def _brilho(widget, raio):
    """Brilho (glow) neon em volta do widget; a cor é ajustada depois por `_cor_do_brilho`."""
    efeito = QGraphicsDropShadowEffect(widget)
    efeito.setBlurRadius(raio)
    efeito.setOffset(0, 0)
    widget.setGraphicsEffect(efeito)
    return efeito


class Card(QFrame):
    """Card com borda e brilho neon azul."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self._brilho = _brilho(self, 26)
        self._atualizar_brilho()
        theme.changed.connect(self._atualizar_brilho)

    def _atualizar_brilho(self):
        cor = QColor(theme.neon("primary"))
        cor.setAlpha(150 if theme.is_dark else 90)
        self._brilho.setColor(cor)


class ActionButton(QPushButton):
    """Botão neon: contorno e texto na cor do tipo (primary azul, success verde, danger vermelho), com brilho."""

    def __init__(self, text, kind="primary", parent=None):
        super().__init__(text, parent)
        self._kind = kind
        self.setObjectName(kind)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._brilho = _brilho(self, 22)
        self._atualizar_brilho()
        theme.changed.connect(self._atualizar_brilho)

    def set_kind(self, kind):
        self._kind = kind
        self.setObjectName(kind)
        self.style().unpolish(self)
        self.style().polish(self)
        self._atualizar_brilho()

    def _atualizar_brilho(self):
        cor = QColor(theme.neon(self._kind))
        cor.setAlpha(230 if theme.is_dark else 150)
        self._brilho.setColor(cor)
        self._brilho.setEnabled(self.isEnabled())

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.Type.EnabledChange:
            self._brilho.setEnabled(self.isEnabled())  # desabilitado: sem brilho


class ThemeButton(QPushButton):
    """Chave deslizante escuro/claro, no mesmo estilo do seletor de tema do portal (rótulo + trilho + bolinha com lua/sol)."""

    _CORES = {  # mesmos tokens do portal: fundo, borda, texto, bolinha, fundo do trilho
        True: ("#242832", "#383d49", "#dce0e9", "#17191f", "#17191f"),
        False: ("#d0d4dc", "#b3b9c5", "#3b4251", "#eceef2", "#d5d8df"),
    }
    _ACCENT = "#2b3cf5"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("themeToggle")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(112, 34)
        self.setFlat(True)
        self.clicked.connect(theme.toggle)
        self._pos = 0.0 if theme.is_dark else 1.0  # 0 = bolinha à esquerda (escuro), 1 = à direita (claro)
        self._anim = QVariantAnimation(self, duration=180, startValue=0.0, endValue=1.0)
        self._anim.valueChanged.connect(self._mover)
        theme.changed.connect(self._refresh)
        self._refresh()

    def _mover(self, valor):
        self._pos = float(valor)
        self.update()

    def _refresh(self):
        alvo = 0.0 if theme.is_dark else 1.0
        self._anim.stop()
        self._anim.setStartValue(self._pos)
        self._anim.setEndValue(alvo)
        self._anim.start()
        self.setToolTip("Alternar para o modo claro" if theme.is_dark else "Alternar para o modo escuro")
        self.update()

    def paintEvent(self, event):
        fundo, borda, texto, bolinha, trilho = (QColor(c) for c in self._CORES[theme.is_dark])
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        painter.setPen(QPen(QColor(self._ACCENT) if self.underMouse() else borda, 1))
        painter.setBrush(fundo)
        painter.drawRoundedRect(r, r.height() / 2, r.height() / 2)
        # rótulo
        painter.setPen(texto)
        fonte = painter.font()
        fonte.setPixelSize(11)
        fonte.setWeight(QFont.Weight.Medium)
        painter.setFont(fonte)
        painter.drawText(QRectF(10, 0, 56, r.height()), Qt.AlignmentFlag.AlignVCenter, "Escuro" if theme.is_dark else "Claro")
        # trilho
        trilho_rect = QRectF(r.right() - 44, (r.height() - 24) / 2 + 0.5, 40, 24)
        painter.setPen(QPen(borda, 1))
        painter.setBrush(trilho)
        painter.drawRoundedRect(trilho_rect, 12, 12)
        # bolinha
        x = trilho_rect.left() + 3 + 16 * self._pos
        bola = QRectF(x, trilho_rect.top() + 3, 18, 18)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bolinha)
        painter.drawEllipse(bola)
        # ícone lua/sol na cor de destaque
        painter.setPen(QPen(QColor(self._ACCENT), 1.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        c = bola.center()
        if theme.is_dark:
            lua = QPainterPath()
            lua.addEllipse(c, 4.2, 4.2)
            corte = QPainterPath()
            corte.addEllipse(QPointF(c.x() + 2.2, c.y() - 1.6), 3.8, 3.8)
            painter.setBrush(QColor(self._ACCENT))
            painter.drawPath(lua.subtracted(corte))
        else:
            painter.drawEllipse(c, 2.6, 2.6)
            for i in range(8):
                ang = i * math.pi / 4
                painter.drawLine(QPointF(c.x() + 4.2 * math.cos(ang), c.y() + 4.2 * math.sin(ang)),
                                 QPointF(c.x() + 5.6 * math.cos(ang), c.y() + 5.6 * math.sin(ang)))
        painter.end()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.update()
