"""Build a printable PDF pack from selected course modules."""

from __future__ import annotations

import html
import io
import re
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.config import APP_NAME, BASE_DIR

_FONT_REG = False
_FONT = "Helvetica"
_FONT_BOLD = "Helvetica-Bold"
_FONT_MONO = "Courier"


def _register_fonts() -> None:
    global _FONT_REG, _FONT, _FONT_BOLD, _FONT_MONO
    if _FONT_REG:
        return
    _FONT_REG = True
    pairs = [
        (
            Path(r"C:\Windows\Fonts\arial.ttf"),
            Path(r"C:\Windows\Fonts\arialbd.ttf"),
            Path(r"C:\Windows\Fonts\cour.ttf"),
        ),
        (
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
        ),
    ]
    for regular, bold, mono in pairs:
        if regular.is_file() and bold.is_file():
            pdfmetrics.registerFont(TTFont("CissSans", str(regular)))
            pdfmetrics.registerFont(TTFont("CissSans-Bold", str(bold)))
            _FONT = "CissSans"
            _FONT_BOLD = "CissSans-Bold"
            if mono.is_file():
                pdfmetrics.registerFont(TTFont("CissMono", str(mono)))
                _FONT_MONO = "CissMono"
            return


def _styles() -> dict:
    _register_fonts()
    base = getSampleStyleSheet()
    ink = colors.HexColor("#0f172a")
    mute = colors.HexColor("#334155")
    accent = colors.HexColor("#3730a3")
    styles = {
        "cover": ParagraphStyle(
            "cover",
            parent=base["Title"],
            fontName=_FONT_BOLD,
            fontSize=22,
            leading=26,
            textColor=ink,
            alignment=TA_CENTER,
            spaceAfter=12,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            parent=base["Normal"],
            fontName=_FONT,
            fontSize=11,
            leading=15,
            textColor=mute,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "h1": ParagraphStyle(
            "mh1",
            parent=base["Heading1"],
            fontName=_FONT_BOLD,
            fontSize=16,
            leading=20,
            textColor=ink,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "mh2",
            parent=base["Heading2"],
            fontName=_FONT_BOLD,
            fontSize=13,
            leading=17,
            textColor=accent,
            spaceBefore=12,
            spaceAfter=6,
            borderPadding=2,
        ),
        "h3": ParagraphStyle(
            "mh3",
            parent=base["Heading3"],
            fontName=_FONT_BOLD,
            fontSize=11,
            leading=14,
            textColor=ink,
            spaceBefore=10,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "mbody",
            parent=base["Normal"],
            fontName=_FONT,
            fontSize=9.5,
            leading=13,
            textColor=ink,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
        ),
        "meta": ParagraphStyle(
            "mmeta",
            parent=base["Normal"],
            fontName=_FONT,
            fontSize=9,
            leading=12,
            textColor=mute,
            spaceAfter=8,
        ),
        "cell": ParagraphStyle(
            "mcell",
            parent=base["Normal"],
            fontName=_FONT,
            fontSize=8,
            leading=10.5,
            textColor=ink,
        ),
        "cell_h": ParagraphStyle(
            "mcellh",
            parent=base["Normal"],
            fontName=_FONT_BOLD,
            fontSize=8,
            leading=10.5,
            textColor=ink,
        ),
        "quote": ParagraphStyle(
            "mquote",
            parent=base["Normal"],
            fontName=_FONT,
            fontSize=9,
            leading=12,
            textColor=mute,
            leftIndent=12,
            borderPadding=4,
            spaceAfter=8,
        ),
        "code": ParagraphStyle(
            "mcode",
            parent=base["Code"],
            fontName=_FONT_MONO,
            fontSize=7.5,
            leading=10,
            textColor=ink,
        ),
        "li": ParagraphStyle(
            "mli",
            parent=base["Normal"],
            fontName=_FONT,
            fontSize=9.5,
            leading=13,
            textColor=ink,
            leftIndent=4,
        ),
        "caption": ParagraphStyle(
            "mcaption",
            parent=base["Normal"],
            fontName=_FONT,
            fontSize=8,
            leading=11,
            textColor=mute,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "toc": ParagraphStyle(
            "mtoc",
            parent=base["Normal"],
            fontName=_FONT,
            fontSize=10,
            leading=14,
            textColor=ink,
            leftIndent=8,
            spaceAfter=2,
        ),
        "footer": ParagraphStyle(
            "mfooter",
            parent=base["Normal"],
            fontName=_FONT,
            fontSize=8,
            textColor=mute,
            alignment=TA_LEFT,
        ),
    }
    return styles


def _clean_inline(raw: str) -> str:
    text = raw or ""
    text = re.sub(r"<br\s*/?>", "<br/>", text, flags=re.I)
    text = re.sub(r"</?(span|div|section|article|figure)[^>]*>", "", text, flags=re.I)
    text = re.sub(r"<img[^>]*>", "", text, flags=re.I)
    # ReportLab Paragraph understands a small HTML subset
    allowed = ("b", "strong", "i", "em", "u", "code", "sup", "sub", "br", "a")
    text = re.sub(
        r"</?(?!(?:%s)\b)[a-zA-Z][^>]*>" % "|".join(allowed),
        "",
        text,
    )
    text = text.replace("<strong>", "<b>").replace("</strong>", "</b>")
    text = text.replace("<em>", "<i>").replace("</em>", "</i>")
    return text.strip()


def _plain(raw: str) -> str:
    text = re.sub(r"<[^>]+>", "", raw or "")
    return html.unescape(text).strip()


def _local_image(src: str) -> Path | None:
    if not src:
        return None
    if src.startswith("/static/"):
        path = BASE_DIR / "app" / src.lstrip("/")
        return path if path.is_file() else None
    if src.startswith("app/static/") or src.startswith("static/"):
        path = BASE_DIR / src
        return path if path.is_file() else None
    return None


def _fetch_plantuml_png(src: str) -> bytes | None:
    if "plantuml.com" not in src and "/plantuml/" not in src:
        return None
    png = src.replace("/plantuml/svg/", "/plantuml/png/")
    try:
        req = Request(png, headers={"User-Agent": "CISS-Capstone-PDF/1.0"})
        with urlopen(req, timeout=8) as resp:
            data = resp.read()
        if data[:8].startswith(b"\x89PNG") or data[:2] == b"\xff\xd8":
            return data
    except Exception:
        return None
    return None


class _BlockParser(HTMLParser):
    """Collect top-level block tags from markdown HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.blocks: list[tuple[str, str, dict]] = []
        self._stack: list[str] = []
        self._buf: list[str] = []
        self._attrs: dict = {}

    def handle_starttag(self, tag: str, attrs):
        ad = dict(attrs)
        if not self._stack and tag in {
            "h1", "h2", "h3", "h4", "p", "ul", "ol", "pre",
            "table", "blockquote", "div", "hr", "img",
        }:
            self._stack.append(tag)
            self._attrs = ad
            self._buf = []
            if tag == "hr":
                self.blocks.append(("hr", "", {}))
                self._stack.pop()
            elif tag == "img":
                self.blocks.append(("img", "", ad))
                self._stack.pop()
            return
        if self._stack:
            attr = "".join(f' {k}="{html.escape(v, quote=True)}"' for k, v in attrs if v)
            self._buf.append(f"<{tag}{attr}>")

    def handle_endtag(self, tag: str):
        if self._stack and tag == self._stack[-1] and len(self._stack) == 1:
            self.blocks.append((tag, "".join(self._buf), self._attrs))
            self._stack.pop()
            self._buf = []
            return
        if self._stack:
            self._buf.append(f"</{tag}>")

    def handle_startendtag(self, tag: str, attrs):
        if not self._stack and tag in {"hr", "img", "br"}:
            if tag == "img":
                self.blocks.append(("img", "", dict(attrs)))
            elif tag == "hr":
                self.blocks.append(("hr", "", {}))
            return
        if self._stack:
            attr = "".join(f' {k}="{html.escape(v, quote=True)}"' for k, v in attrs if v)
            self._buf.append(f"<{tag}{attr} />")

    def handle_data(self, data):
        if self._stack:
            self._buf.append(html.escape(data))

    def handle_entityref(self, name):
        if self._stack:
            self._buf.append(f"&{name};")

    def handle_charref(self, name):
        if self._stack:
            self._buf.append(f"&#{name};")


def _list_items(inner: str) -> list[str]:
    return [html.unescape(_plain(m)) for m in re.findall(
        r"<li[^>]*>(.*?)</li>", inner, flags=re.I | re.S
    ) if _plain(m)]


def _table_rows(inner: str) -> list[list[str]]:
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", inner, flags=re.I | re.S):
        cells = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, flags=re.I | re.S)
        rows.append([_clean_inline(c) or " " for c in cells])
    return rows


def html_to_flowables(body_html: str, styles: dict, *, content_width: float) -> list:
    parser = _BlockParser()
    try:
        # Markdown HTML is a sequence of sibling blocks — do not wrap in <div>
        # or the parser treats the entire module as one blob.
        parser.feed(body_html or "")
        parser.close()
    except Exception:
        return [Paragraph(_clean_inline(body_html or ""), styles["body"])]

    story: list = []
    for tag, inner, attrs in parser.blocks:
        if tag == "hr":
            story.append(Spacer(1, 8))
            continue
        if tag in {"h1", "h2", "h3", "h4"}:
            key = tag if tag in styles else "h3"
            text = _clean_inline(inner) or _plain(inner)
            if text:
                story.append(Paragraph(text, styles[key]))
            continue
        if tag == "p":
            text = _clean_inline(inner)
            if text:
                story.append(Paragraph(text, styles["body"]))
            continue
        if tag == "blockquote":
            text = _clean_inline(inner) or _plain(inner)
            if text:
                story.append(Paragraph(text, styles["quote"]))
            continue
        if tag in {"ul", "ol"}:
            items = _list_items(inner)
            if not items:
                continue
            numbered = tag == "ol"
            flow_items = [
                ListItem(Paragraph(html.escape(item), styles["li"]), leftIndent=12)
                for item in items
            ]
            story.append(
                ListFlowable(
                    flow_items,
                    bulletType="1" if numbered else "bullet",
                    start="1",
                    leftIndent=18,
                    spaceAfter=6,
                )
            )
            continue
        if tag == "pre":
            cls = (attrs.get("class") or "") + " " + inner[:80]
            code = _plain(inner)
            if "mermaid" in cls or code.strip().startswith("flowchart") or "mermaid" in inner[:200]:
                story.append(Paragraph(
                    "<i>[Mermaid diagram — use Print / Save as PDF in the browser to include the rendered figure.]</i>",
                    styles["caption"],
                ))
                if code.strip():
                    story.append(_code_block(code, styles, content_width))
                continue
            if code.strip():
                story.append(_code_block(code, styles, content_width))
            continue
        if tag == "table":
            rows = _table_rows(inner)
            if rows:
                story.append(_pdf_table(rows, styles, content_width))
            continue
        if tag == "img":
            flow = _image_flowable(attrs.get("src") or "", attrs.get("alt") or "", styles, content_width)
            if flow:
                story.append(flow)
            continue
        if tag == "div":
            cls = attrs.get("class") or ""
            img_m = re.search(r'<img[^>]+src="([^"]+)"', inner, flags=re.I)
            if img_m:
                flow = _image_flowable(html.unescape(img_m.group(1)), "Diagram", styles, content_width)
                if flow:
                    story.append(flow)
                    continue
            if "mermaid" in cls:
                story.append(Paragraph(
                    "<i>[Mermaid diagram — use Print / Save as PDF in the browser for the rendered figure.]</i>",
                    styles["caption"],
                ))
                continue
            text = _clean_inline(inner)
            if text:
                story.append(Paragraph(text, styles["body"]))
            continue
    return story


def _code_block(code: str, styles: dict, width: float):
    # Keep lines from overflowing the page
    wrapped = []
    for line in code.replace("\t", "    ").splitlines() or [""]:
        while len(line) > 98:
            wrapped.append(line[:98])
            line = "    " + line[98:]
        wrapped.append(line)
    body = "\n".join(wrapped)
    pre = Preformatted(body, styles["code"])
    box = Table([[pre]], colWidths=[width])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([box, Spacer(1, 8)])


def _pdf_table(rows: list[list[str]], styles: dict, width: float):
    cols = max(len(r) for r in rows)
    padded = [r + [" "] * (cols - len(r)) for r in rows]
    header = padded[0]
    rest = padded[1:]
    data = [[Paragraph(c, styles["cell_h"]) for c in header]]
    for row in rest:
        data.append([Paragraph(c, styles["cell"]) for c in row])
    # Wider last columns for prose
    if cols == 1:
        widths = [width]
    elif cols == 2:
        widths = [width * 0.32, width * 0.68]
    elif cols == 3:
        widths = [width * 0.22, width * 0.32, width * 0.46]
    else:
        first = width * 0.18
        rest = (width - first) / (cols - 1)
        widths = [first] + [rest] * (cols - 1)
    tbl = Table(data, colWidths=widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#94a3b8")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return KeepTogether([tbl, Spacer(1, 8)])


def _image_flowable(src: str, alt: str, styles: dict, width: float):
    local = _local_image(src)
    img_data = None
    if local and local.suffix.lower() != ".svg":
        try:
            img = Image(str(local))
            img.hAlign = "CENTER"
            iw, ih = img.imageWidth, img.imageHeight
            if iw > width:
                img.drawWidth = width
                img.drawHeight = ih * (width / iw)
            else:
                img.drawWidth = iw * 0.5 if iw > width * 0.9 else min(iw, width)
                img.drawHeight = ih * (img.drawWidth / iw)
            cap = Paragraph(html.escape(alt or "Figure"), styles["caption"]) if alt else Spacer(1, 4)
            return KeepTogether([img, cap])
        except Exception:
            pass
    png = _fetch_plantuml_png(src)
    if png:
        try:
            img = Image(io.BytesIO(png))
            img.hAlign = "CENTER"
            iw, ih = img.imageWidth, img.imageHeight
            if iw > width:
                img.drawWidth = width
                img.drawHeight = max(20, ih * (width / iw))
            cap = Paragraph(html.escape(alt or "Diagram"), styles["caption"])
            return KeepTogether([img, cap])
        except Exception:
            pass
    if alt:
        return Paragraph(f"<i>[{html.escape(alt)}]</i>", styles["caption"])
    return None


def _header_footer(canvas, doc, subtitle: str):
    canvas.saveState()
    w, h = letter
    canvas.setStrokeColor(colors.HexColor("#c7d2fe"))
    canvas.setLineWidth(0.6)
    canvas.line(0.7 * inch, h - 0.5 * inch, w - 0.7 * inch, h - 0.5 * inch)
    canvas.setFont(_FONT, 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(0.7 * inch, h - 0.42 * inch, APP_NAME)
    canvas.drawRightString(w - 0.7 * inch, h - 0.42 * inch, "Unclassified training")
    canvas.line(0.7 * inch, 0.5 * inch, w - 0.7 * inch, 0.5 * inch)
    canvas.drawString(0.7 * inch, 0.35 * inch, (subtitle or "")[:80])
    canvas.drawRightString(w - 0.7 * inch, 0.35 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_modules_pdf(modules: list[dict], outfile) -> None:
    """Write a multi-module PDF to a path or binary file object."""
    styles = _styles()
    page_w, _ = letter
    content_w = page_w - 1.4 * inch
    titles = [m.get("title") or m.get("id") for m in modules]
    subtitle = f"{len(modules)} module{'s' if len(modules) != 1 else ''}"
    if len(modules) == 1:
        subtitle = modules[0].get("title") or subtitle

    doc = SimpleDocTemplate(
        outfile,
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title=f"{APP_NAME} — {subtitle}",
        author=APP_NAME,
        subject="Course module export",
    )

    story: list = []
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph(html.escape(APP_NAME), styles["cover"]))
    story.append(Paragraph("Module pack", styles["cover_sub"]))
    story.append(Paragraph(html.escape(date.today().isoformat()), styles["cover_sub"]))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "Unclassified intern training. Do not add classified or production data.",
        styles["cover_sub"],
    ))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Contents", styles["h2"]))
    for i, title in enumerate(titles, start=1):
        track = modules[i - 1].get("track_short") or ""
        label = f"{i}. {html.escape(title)}"
        if track:
            label = f"{i}. [{html.escape(track)}] {html.escape(title)}"
        story.append(Paragraph(label, styles["toc"]))
    story.append(PageBreak())

    for i, mod in enumerate(modules):
        if i:
            story.append(PageBreak())
        track = html.escape(mod.get("track_short") or "")
        dur = mod.get("duration_min")
        meta = " · ".join(
            p for p in [
                track,
                f"~{dur} min" if dur else "",
                html.escape(mod.get("id") or ""),
            ] if p
        )
        story.append(Paragraph(html.escape(mod.get("title") or "Module"), styles["h1"]))
        if meta:
            story.append(Paragraph(meta, styles["meta"]))
        if mod.get("summary"):
            story.append(Paragraph(html.escape(mod["summary"]), styles["meta"]))
        story.extend(html_to_flowables(mod.get("body_html") or "", styles, content_width=content_w))

    def on_page(canvas, doc_):
        _header_footer(canvas, doc_, subtitle)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


def suggested_filename(modules: list[dict]) -> str:
    day = date.today().isoformat()
    if len(modules) == 1:
        slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", modules[0].get("id") or "module")
        return f"CISS-{slug}.pdf"
    tracks = sorted({m.get("track") for m in modules if m.get("track")})
    if len(tracks) == 1:
        return f"CISS-{tracks[0]}-modules-{len(modules)}-{day}.pdf"
    return f"CISS-modules-{len(modules)}-{day}.pdf"
