from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem
from PySide6.QtGui import QFontMetrics, QPainter, QColor, QPen
from PySide6.QtCore import QRect, QSize, Qt
from .message_model import ROLE_USER, ROLE_AGENT

PAD_X = 12
PAD_Y = 10
LINE_SPACING = 6
TIME_H = 16
CARD_MAX_W = 720   # wider, IDE-like

class MsgDelegate(QStyledItemDelegate):
    def sizeHint(self, option: QStyleOptionViewItem, index) -> QSize:
        item = index.data(Qt.DisplayRole) or {}
        text = item.get("text","")
        fm = option.fontMetrics
        text_rect = fm.boundingRect(0, 0, CARD_MAX_W - PAD_X*2, 100000,
                                    Qt.TextWordWrap, text)
        h = text_rect.height() + PAD_Y*2 + TIME_H + LINE_SPACING
        w = min(text_rect.width() + PAD_X*2, CARD_MAX_W)
        return QSize(max(w + 120, option.rect.width()), h + 8)

    def paint(self, p: QPainter, opt: QStyleOptionViewItem, index):
        p.save()
        item = index.data(Qt.DisplayRole) or {}
        text = item.get("text","")
        role = item.get("role", ROLE_AGENT)
        is_user = role == ROLE_USER

        fm = opt.fontMetrics
        text_rect = fm.boundingRect(0, 0, CARD_MAX_W - PAD_X*2, 100000,
                                    Qt.TextWordWrap, text)
        card_w = text_rect.width() + PAD_X*2
        card_h = text_rect.height() + PAD_Y*2 + TIME_H + LINE_SPACING

        view_w = opt.rect.width()
        x = opt.rect.left() + (view_w - card_w - 30 if is_user else 30)
        y = opt.rect.top() + 6
        card_rect = QRect(x, y, card_w, card_h - TIME_H - LINE_SPACING)

        # Colors (dark, professional)
        bg = QColor("#0f1a2b") if is_user else QColor("#161616")
        border = QColor("#2f6fed") if is_user else QColor("#2a2a2a")
        fg = QColor("#e6e6e6")

        # Card
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(QPen(border))
        p.setBrush(bg)
        p.drawRoundedRect(card_rect, 12, 12)

        # Text
        p.setPen(fg)
        txt_area = QRect(card_rect.left()+PAD_X, card_rect.top()+PAD_Y,
                         text_rect.width(), text_rect.height())
        p.drawText(txt_area, Qt.TextWordWrap | Qt.AlignLeft | Qt.AlignVCenter, text)

        # Time
        p.setPen(QColor("#9aa0a6"))
        time_area = QRect(card_rect.left(), card_rect.bottom()+2, card_rect.width(), TIME_H)
        p.drawText(time_area, Qt.AlignRight if is_user else Qt.AlignLeft,
                   item.get("meta", {}).get("time", ""))

        p.restore()
