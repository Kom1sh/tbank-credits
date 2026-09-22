#!/usr/bin/env python3
"""Генерирует src/slides.html — содержание деки.

    python3 src/make_slides.py && python3 src/build.py && python3 src/qa.py

Правится ТОЛЬКО этот файл (содержание) и src/deck.tpl.html (оформление).
index.html — результат сборки, руками его не трогать.

Ниже: словари брендов, штриховые иконки, помощники компонентов, генераторы графиков
и, в самом низу, сами слайды. Демо-слайды показывают каждый компонент в деле —
заменяйте их своими и удаляйте лишнее.
"""
import json, pathlib, math, html

HERE = pathlib.Path(__file__).resolve().parent
BR = json.load(open(HERE / "brands.json")) if (HERE / "brands.json").exists() else {}
# D = json.load(open(HERE / "data.json", encoding="utf-8"))   # снимок живых данных, если он есть

INK = "#1C1C1E"
# Фирменные цвета из Simple Icons. Белый и чёрный заменяем чернилами: на белой плитке
# фирменный белый невидим, а чистый чёрный выглядит грязно.
for _k, _v in list(BR.items()):
    if _v.upper() in ("#000000", "#FFFFFF", "#181717", "#191919"):
        BR[_k] = INK

# Подписи под плитками логотипов: слуг → как называть по-русски.
NAME = {}

# Бренды, которых нет в Simple Icons, рисуются текстовой плиткой: слуг → (надпись, цвет).
WORD = {}

UI = {
 "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>',
 "robot": '<rect x="4.5" y="8.5" width="15" height="11" rx="2.5"/><path d="M12 8.5V4.5"/><circle cx="12" cy="3.5" r="1.2"/><circle cx="9" cy="14" r="1.3"/><circle cx="15" cy="14" r="1.3"/><path d="M2 13v3M22 13v3"/>',
 "book": '<path d="M3.5 5h6.5a2 2 0 0 1 2 2v13a2 2 0 0 0-2-2H3.5z"/><path d="M20.5 5H14a2 2 0 0 0-2 2v13a2 2 0 0 1 2-2h6.5z"/>',
 "podium": '<rect x="2.5" y="12.5" width="5.5" height="8.5" rx="1"/><rect x="9.25" y="5.5" width="5.5" height="15.5" rx="1"/><rect x="16" y="9.5" width="5.5" height="11.5" rx="1"/>',
 "link": '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l2.6-2.6a4.5 4.5 0 0 0-6.4-6.4L11.2 6.4"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0L5 12.6a4.5 4.5 0 0 0 6.4 6.4l1.4-1.4"/>',
 "sitemap": '<rect x="9" y="2.5" width="6" height="4.5" rx="1"/><rect x="2.5" y="17" width="6" height="4.5" rx="1"/><rect x="15.5" y="17" width="6" height="4.5" rx="1"/><path d="M12 7v4.5M5.5 17v-5.5h13V17"/>',
 "gauge": '<path d="M4 16a8 8 0 0 1 16 0"/><path d="M12 16l4.5-5.5"/><circle cx="12" cy="16" r="1.3"/><path d="M3 20h18"/>',
 "shield": '<path d="M12 2.5 4 6v6c0 5 3.4 8.4 8 9.5 4.6-1.1 8-4.5 8-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
 "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.6L16.5 9"/>',
 "no": '<circle cx="12" cy="12" r="9"/><path d="M6 6l12 12"/>',
 "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>',
 "list": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1.2"/><circle cx="4.5" cy="12" r="1.2"/><circle cx="4.5" cy="18" r="1.2"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "quote": '<path d="M4 15V9a3 3 0 0 1 3-3h2v5H6v4H4z"/><path d="M14 15V9a3 3 0 0 1 3-3h2v5h-3v4h-2z"/>',
 "chat": '<path d="M4 5.5h16v10H10l-5 4v-4H4z"/>',
 "doc": '<path d="M6 2.5h8l4 4v15H6z"/><path d="M14 2.5v4h4"/><path d="M9 12h6M9 16h6"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18z"/>',
 "megaphone": '<path d="M3 10v4l11 4V6z"/><path d="M14 6v12"/><path d="M17.5 9.5a3 3 0 0 1 0 5"/><path d="M6 14l1.5 5"/>',
 "pin": '<path d="M12 21.5s-7-6.2-7-11.3a7 7 0 0 1 14 0c0 5.1-7 11.3-7 11.3z"/><circle cx="12" cy="10" r="2.5"/>',
 "refresh": '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 3.5v4.5h-4.5"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "zap": '<path d="M13 2.5 5 13.5h6l-1 8 8-11h-6z"/>',
 "eye": '<path d="M1.5 12S5.5 5 12 5s10.5 7 10.5 7-4 7-10.5 7S1.5 12 1.5 12z"/><circle cx="12" cy="12" r="3"/>',
 "pen": '<path d="M4 20l3.2-.7L20 6.5a2.1 2.1 0 0 0-3-3L4.2 16.3z"/><path d="M15.5 5.5l3 3"/>',
 "arrow": '<path d="M4 12h16"/><path d="M13 5l7 7-7 7"/>',
 "coins": '<circle cx="9" cy="9" r="6"/><path d="M15.5 8.2A6 6 0 1 1 8.2 15.5"/>',
 "share": '<circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.6M8.2 13.2l7.6 4.6"/>',
 "star": '<path d="M12 3l2.8 5.8 6.2.9-4.5 4.4 1.1 6.3L12 17.4l-5.6 3 1.1-6.3L3 9.7l6.2-.9z"/>',
 "flag": '<path d="M5 21V4"/><path d="M5 4h12l-2 4 2 4H5"/>',
 "home": '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v10h13V10"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.3"/>',
 "layers": '<path d="M12 3 2.5 8 12 13l9.5-5z"/><path d="M2.5 12.5 12 17.5l9.5-5"/><path d="M2.5 17 12 22l9.5-5"/>',
}

def ui(name, cls=""): return f'<svg class="ui {cls}" viewBox="0 0 24 24" aria-hidden="true">{UI[name]}</svg>'

def ico(slug):
    return f'<svg class="ic" style="color:{BR.get(slug, INK)}"><use href="#i-{slug}"/></svg>'

def tile(slug, label=None, size="", extra=""):
    if slug in WORD:
        t, c = WORD[slug]; inner = f'<div class="tile word {size}" style="color:{c};{extra}">{t}</div>'
    else:
        inner = f'<div class="tile {size}" style="{extra}">{ico(slug)}</div>'
    if label is None or (slug in WORD and label == WORD[slug][0]): return inner
    return f'<div class="tl{" w" if slug in WORD else ""}">{inner}<span>{label}</span></div>'

def top(pill): return f'<div class="top"><span class="pill">{pill}</span><span class="cnt"></span></div>'

def slide(inner, title, cls=""): return f'<section class="s {cls}" data-t="{html.escape(title)}">{inner}</section>'

def sticky(kind, h, p, extra=""): return f'<div class="sticky {kind}">{extra}<h4>{h}</h4><p>{p}</p></div>'

def stat(n, l, cls=""): return f'<div class="stat {cls}"><div class="n">{n}</div><div class="l">{l}</div></div>'

def browser(url, img, w=None):
    """Окно браузера. Высота выводится из пропорций снимка, поэтому страница видна целиком."""
    st = f' style="max-width:{w}px"' if w else ""
    return f'<div class="browser"{st}><div class="bar"><i></i><i></i><i></i><span class="url">{url}</span></div><div class="shot"><img src="assets/{img}" alt=""></div></div>'

def arrow(): return '<div class="arr"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>'

def step(n, h, p, kind="", icon=None, i=0):
    ic = ui(icon, "sm") if icon else ""
    return f'<div class="step {kind} r" style="--i:{i}"><div class="hd"><span class="num">{n}</span>{ic}</div><h4>{h}</h4><p>{p}</p></div>'

def fmt(n): return f"{int(round(n)):,}".replace(",", " ")

def nice(v):
    """Округляет потолок оси до «красивого» числа: 1621 → 2000, 537 → 600, 38 → 40."""
    if v <= 0: return 1
    import math as _m
    mag = 10 ** _m.floor(_m.log10(v)); f = v / mag
    for step in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if f <= step: return step * mag
    return 10 * mag

def line_chart(points, w=760, h=330, color="#0FBCB0", fill="#C3FAF5", every=1, vline=None, ymax=None, mark_last=True, mark_peak=False, xfmt=None, dot_r=5):
    L, R, T, B = 74, 24, 28, 44
    vals = [v for _, v in points]; ymax = ymax or nice(max(vals) * 1.12) or 1
    n = len(points); xs = [L + (w - L - R) * i / max(1, n - 1) for i in range(n)]
    ys = [T + (h - T - B) * (1 - v / ymax) for v in vals]
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    ticks = 4
    for k in range(ticks + 1):
        yy = T + (h - T - B) * k / ticks; vv = ymax * (1 - k / ticks)
        out.append(f'<line x1="{L}" x2="{w-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#E0E2E8" stroke-width="1"/>')
        out.append(f'<text class="ax" x="{L-10}" y="{yy+5:.1f}" text-anchor="end">{fmt(vv)}</text>')
    area = f"M{xs[0]:.1f},{h-B} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in zip(xs, ys)) + f" L{xs[-1]:.1f},{h-B} Z"
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    out.append(f'<path d="{area}" fill="{fill}"/>'); out.append(f'<path d="{line}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, (lab, v) in enumerate(points):
        if i == n - 1 or (i % every == 0 and n - 1 - i >= max(2, every // 2)):
            out.append(f'<text class="ax" x="{xs[i]:.1f}" y="{h-14}" text-anchor="middle">{xfmt(lab) if xfmt else lab}</text>')
    if vline is not None:
        i, txt = vline; out.append(f'<line x1="{xs[i]:.1f}" x2="{xs[i]:.1f}" y1="{T-8}" y2="{h-B}" stroke="{INK}" stroke-width="2" stroke-dasharray="6 6"/>')
        out.append(f'<text class="val" x="{xs[i]+10:.1f}" y="{T+8}" text-anchor="start">{txt}</text>')
    if mark_last:
        out.append(f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="{dot_r+2}" fill="#fff" stroke="{color}" stroke-width="4"/>')
        out.append(f'<text class="val" x="{xs[-1]-14:.1f}" y="{ys[-1]-16:.1f}" text-anchor="end" style="font-size:22px">{fmt(vals[-1])}</text>')
    if mark_peak and n > 1:
        out.append(f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="{dot_r}" fill="#fff" stroke="{color}" stroke-width="3"/>')
        out.append(f'<text class="val" x="{xs[0]+12:.1f}" y="{ys[0]-14:.1f}" text-anchor="start">{fmt(vals[0])}</text>')
    out.append("</svg>"); return "".join(out)

def bars(cats, series, w=760, h=330, suffix="", ymax=None):
    L, R, T, B = 60, 16, 30, 44
    allv = [v for _, _, vals in series for v in vals]; ymax = ymax or nice(max(allv) * 1.15) or 1
    n, m = len(cats), len(series); gw = (w - L - R) / n; bw = min(78, gw * 0.7 / m); gap = 8
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    for k in range(5):
        yy = T + (h - T - B) * k / 4; out.append(f'<line x1="{L}" x2="{w-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#E0E2E8"/>')
        out.append(f'<text class="ax" x="{L-10}" y="{yy+5:.1f}" text-anchor="end">{ymax*(1-k/4):.0f}{suffix}</text>')
    for ci, c in enumerate(cats):
        cx = L + gw * ci + gw / 2; total = m * bw + (m - 1) * gap; x0 = cx - total / 2
        for si, (name, color, vals) in enumerate(series):
            v = vals[ci]; x = x0 + si * (bw + gap); hh = (h - T - B) * v / ymax; y = h - B - hh
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(hh,2):.1f}" rx="8" fill="{color}"/>')
            lab = ("—" if v is None else f"{v:g}{suffix}")
            out.append(f'<text class="val" x="{x+bw/2:.1f}" y="{y-10:.1f}" text-anchor="middle">{lab}</text>')
        out.append(f'<text class="ax" x="{cx:.1f}" y="{h-14}" text-anchor="middle" style="font-size:17px;fill:{INK};font-weight:500">{c}</text>')
    out.append("</svg>"); return "".join(out)

def hbars(items, w=700, rowh=52, maxv=None, labw=300, color="#0FBCB0", fmtv=fmt, mono=False):
    maxv = maxv or max(v for _, v, *_ in items)
    h = rowh * len(items); out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    for i, it in enumerate(items):
        lab, v = it[0], it[1]; col = it[2] if len(it) > 2 else color
        y = i * rowh; bw = (w - labw - 110) * v / maxv
        fam = "font-family:var(--fm);font-weight:500;font-size:16px" if mono else "font-size:18px;font-weight:500"
        out.append(f'<text x="{labw-14}" y="{y+rowh/2+6}" text-anchor="end" style="{fam};fill:{INK}">{html.escape(lab)}</text>')
        out.append(f'<rect x="{labw}" y="{y+rowh/2-14}" width="{max(bw,3):.1f}" height="28" rx="8" fill="{col}"/>')
        out.append(f'<text class="val" x="{labw+bw+12:.1f}" y="{y+rowh/2+6}">{fmtv(v)}</text>')
    out.append("</svg>"); return "".join(out)

def donut(parts, size=300, thick=46, center=""):
    r = (size - thick) / 2; c = math.pi * 2 * r; tot = sum(v for _, v, _ in parts); off = 0
    out = [f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" aria-hidden="true"><g transform="rotate(-90 {size/2} {size/2})">']
    for lab, v, col in parts:
        seg = c * v / tot
        out.append(f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{col}" stroke-width="{thick}" stroke-dasharray="{seg:.2f} {c-seg:.2f}" stroke-dashoffset="{-off:.2f}"/>')
        off += seg
    out.append("</g>")
    if center: out.append(f'<text x="{size/2}" y="{size/2+12}" text-anchor="middle" class="val" style="font-size:34px">{center}</text>')
    out.append("</svg>"); return "".join(out)

def plist(items, icon):
    return '<ul class="plist">' + "".join(
        f'<li>{ui(icon, "xs")}<div><b>{h}</b><i>{p}</i></div></li>' for h, p in items) + '</ul>'

def divider(n, title, sub, items):
    return slide(top("Раздел " + n) + f'<div class="body"><div class="row fill" style="gap:60px;align-items:flex-end"><div style="flex:1.2;display:flex;flex-direction:column;height:100%">'
      f'<div class="divn">{n}</div><div style="margin-top:auto"><div class="divt">{title}</div><div class="divs">{sub}</div></div></div>'
      f'<div class="divlist" style="flex:1;padding-bottom:12px">{"".join(f"<span>{x}</span>" for x in items)}</div></div></div>', f"Раздел {n}: {title}", "dark")

def qcard(kind, label, q, meta, page, win=None):
    tail = f'<span class="pill" style="margin-top:auto;align-self:flex-start">{win}</span>' if win else ""
    return f'<div class="sticky {kind}"><span class="lab">{label}</span><div class="qcard"><div class="q">{q}</div><div class="meta">{meta}</div></div><p>{page}</p>{tail}</div>'


# ═══════════════════════════════════════════════════════════════════════════
#  ДОКЛАД: КРЕДИТЫ Т-БАНКА, 3 МИНУТЫ, 5 СЛАЙДОВ
# ═══════════════════════════════════════════════════════════════════════════
import math as _m

SRC_DATE = "21 сентября 2026"

def scale(rows, thresholds, lo=1.0, hi=320.0):
    """Логарифмическая шкала ставок: имя, диапазон, значение. Порог — вертикальная линия."""
    def pos(v):
        v = max(v, lo)
        return 100.0 * _m.log10(v / lo) / _m.log10(hi / lo)
    out = ['<div class="scale">']
    for nm, sub, a, b, kind, lab, verdict in rows:
        if a == 0 and b == 0:
            bar = '<span class="fillbar" style="left:0;width:5px"></span>'
        else:
            left = pos(a) if b is not None else 0
            width = max(pos(b if b is not None else a) - left, 1.2)
            bar = f'<span class="fillbar" style="left:{left:.2f}%;width:{width:.2f}%"></span>'
        thr = "".join(f'<span class="thr" style="left:{pos(t):.2f}%;{"border-left:2px dashed var(--rule);background:none;width:0" if d else ""}"></span>'
                      for t, _, d in thresholds)
        vcol = "--good" if kind == "g" else "--bad" if kind == "b" else "--slate"
        out.append(f'<div class="srow {kind}"><span class="nm">{nm}<small>{sub}</small></span>'
                   f'<span class="track">{bar}{thr}</span><span class="val">{lab}</span>'
                   f'<span class="vd" style="color:var({vcol})">{verdict}</span></div>')
    marks = "".join(f'<span style="left:{pos(v):.2f}%">{v}%</span>' for v in (1, 3, 10, 30, 100, 300))
    out.append(f'<div class="axis"><span></span><span class="marks">{marks}</span><span></span><span></span></div></div>')
    return "".join(out)

def quote(kind, text, who, sumline=None):
    s = f'<span class="sum">{sumline}</span>' if sumline else ""
    return f'<div class="quote {kind}">{s}<p>{text}</p><span class="who">{who}</span></div>'

S = []

# ── 1. обложка и правило ────────────────────────────────────────────────────
S.append(slide(top("Банковские инструменты · доклад 3 минуты") +
  '<div class="body cover"><div class="row fill" style="gap:48px;align-items:center">'
  '<div style="flex:1.05;display:flex;flex-direction:column;min-width:0">'
  '<h1 style="font-size:82px">Кредиты<br>Т‑Банка</h1>'
  '<p class="sub">Какие из них выгодны и почему. Разбираю линейку по одному правилу.</p>'
  '<div class="who" style="margin-top:36px"><div><b>Протасов Егор</b><br><span>Т‑Банк · кредиты</span></div>'
  '<div><b>22 сентября 2026</b><br><span>ставки и условия на эту дату</span></div></div></div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:18px">'
  '<div class="rule"><span class="n">Правило, по которому я оцениваю любой кредит</span>'
  '<span class="f">Ставка <b>&lt;</b> инфляция <b>+</b> рост<br>того, что покупаю</span>'
  '<span class="n">Ниже порога долг дешевеет быстрее, чем дорожает покупка. Выше — вы платите за нетерпение.</span></div>'
  '<div class="g2" style="gap:14px">'
  + '<div class="card"><div class="stat sm"><div class="n">14%</div><div class="l">ключевая ставка ЦБ с 11 сентября 2026</div></div></div>'
  + '<div class="card"><div class="stat sm"><div class="n">6,3%</div><div class="l">годовая инфляция на 7 сентября 2026</div></div></div>'
  + '</div></div></div></div>', "Обложка и правило", "cover"))

# ── 2. линейка Т-Банка на шкале ─────────────────────────────────────────────
ROWS = [("Рассрочка у партнёров", "продавец платит проценты · до 24 мес", 0, 0, "g", "0%", "беру"),
        ("Семейная ипотека", "льготная · до 50 млн ₽ · до 30 лет", 6, None, "g", "6%", "беру"),
        ("Ипотека базовая", "без господдержки · до 50 млн ₽", 16.9, None, "b", "16,9%", "смотря на что"),
        ("Автокредит", "до 8 млн ₽ · ПСК 9,9—33,5%", 10, 32.9, "b", "10—32,9%", "смотря на что"),
        ("Кредит наличными", "до 30 млн ₽ · до 15 лет", 0, None, "u", "в тарифе", "только по нужде"),
        ("Микрозаём", "не продукт банка · 0,8% в день", 292, None, "b", "292%", "нет")]
S.append(slide(top("Линейка и правило") + '<h1>Порог сегодня — 6–8% годовых. Из линейки его проходят два продукта</h1>'
  '<div class="body"><div style="margin:auto 0">'
  + scale(ROWS, [(6.3, "инфляция", False), (8.2, "рост жилья", True)])
  + '<div class="leg" style="margin-top:20px"><span><i style="background:#4B3BEB"></i>инфляция 6,3%</span>'
    '<span><i style="background:#fff;border:2px dashed #4B3BEB"></i>рост цен на вторичное жильё 8,2% за 2025 год</span>'
    '<span><i style="background:#12805C"></i>ниже порога</span><span><i style="background:#C02434"></i>выше порога</span>'
    '<span>шкала логарифмическая</span></div>'
  '<p class="note-dark" style="margin-top:18px">Ставки и лимиты — tbank.ru, 22 сентября 2026. В линейке есть ещё образовательный кредит, рефинансирование и кредит под залог.</p></div></div>', "Линейка и правило"))

# ── 3. досрочное погашение ──────────────────────────────────────────────────
def mcase(kind, title, pay_, rows, verdict, vkind):
    lines = "".join(f'<div class="mline"><span>{a}</span><b>{b}</b></div>' for a, b in rows)
    return (f'<div class="sticky {kind}" style="gap:12px"><h4>{title}</h4>'
            f'<div class="mline big"><span>ежемесячный платёж</span><b>{pay_}</b></div>{lines}'
            f'<div class="verdict {vkind}">{verdict}</div></div>')
S.append(slide(top("Досрочка: базовая ипотека") + '<h1>Базовая ипотека под 16,9%: доплата экономит 6,9 млн ₽</h1>'
  '<div class="body">'
  '<div class="cond" style="grid-template-columns:repeat(4,minmax(0,1fr));margin-bottom:16px">'
  '<div><b>4 000 000 ₽</b><span>сумма кредита</span></div>'
  '<div><b>20 лет</b><span>срок по договору</span></div>'
  '<div><b>+20 000 ₽</b><span>доплата каждый месяц</span></div>'
  '<div><b>16,9%</b><span>ставка</span></div>'
  '</div>'
  '<div class="row" style="gap:22px;margin-bottom:16px;align-items:stretch">'
  '<div class="sticky grey" style="flex:1.05;gap:10px"><div class="mline"><span>платёж по графику</span><b>58 400 ₽</b></div><div class="mline"><span>всего отдадите банку за 20 лет</span><b>14,0 млн ₽</b></div><div class="mline"><span>из них проценты</span><b>10,0 млн ₽</b></div><div class="mline"><span>с доплатой кредит закрыт за</span><b>7 лет 7 мес</b></div><div class="mline"><span>всего отдадите банку с доплатой</span><b>7,1 млн ₽</b></div><div class="mline"><span>доплат внесено за это время</span><b>1,8 млн ₽</b></div>'
  '<div class="verdict good">Каждый рубль доплаты экономит 3,79 ₽ процентов</div></div>'
  '<div class="sticky lav" style="flex:1"><h4>Почему экономия такая большая</h4><p>Проценты — это плата за время. На ставке 16,9% каждые 100 000 ₽ долга обходятся в 16 900 ₽ в год: только за первый год набегает 674 000 ₽ процентов. Доплата сокращает срок, а вместе с ним и все проценты, которые начислились бы за оставшиеся годы. Поэтому 1,8 млн ₽ доплат убирают 6,9 млн ₽ процентов.</p></div>'
  '</div>'
  '<div class="rule" style="padding:14px 26px;margin-bottom:auto"><span class="f" style="font-size:25px">Дорогой кредит гасят досрочно: переплата по графику больше самого кредита в 2,5 раза</span></div></div>', "Досрочка: базовая ипотека"))

S.append(slide(top("Досрочка: льготная ипотека") + '<h1>Льготная под 6%: та же доплата экономит только 1,7 млн ₽</h1>'
  '<div class="body">'
  '<div class="cond" style="grid-template-columns:repeat(4,minmax(0,1fr));margin-bottom:16px">'
  '<div><b>4 000 000 ₽</b><span>сумма кредита</span></div>'
  '<div><b>20 лет</b><span>срок по договору</span></div>'
  '<div><b>+20 000 ₽</b><span>доплата каждый месяц</span></div>'
  '<div><b>6%</b><span>ставка</span></div>'
  '</div>'
  '<div class="row" style="gap:22px;margin-bottom:16px;align-items:stretch">'
  '<div class="sticky grey" style="flex:1.05;gap:10px"><div class="mline"><span>платёж по графику</span><b>28 700 ₽</b></div><div class="mline"><span>всего отдадите банку за 20 лет</span><b>6,9 млн ₽</b></div><div class="mline"><span>из них проценты</span><b>2,9 млн ₽</b></div><div class="mline"><span>с доплатой кредит закрыт за</span><b>8 лет 11 мес</b></div><div class="mline"><span>всего отдадите банку с доплатой</span><b>5,2 млн ₽</b></div><div class="mline"><span>доплат внесено за это время</span><b>2,1 млн ₽</b></div>'
  '<div class="verdict bad">Каждый рубль доплаты экономит 80 копеек</div></div>'
  '<div class="sticky lav" style="flex:1"><h4>Почему разница с базовой в четыре раза</h4><p>Здесь каждые 100 000 ₽ долга стоят 6 000 ₽ в год вместо 16 900 ₽, почти втрое дешевле. За первый год набегает 237 000 ₽ процентов против 674 000 ₽ на базовой — выкупать почти нечего. Доплат внесли даже больше, чем в первом случае — 2,1 млн ₽ против 1,8 млн ₽, — а сэкономили вчетверо меньше.</p></div>'
  '</div>'
  '<div class="rule" style="padding:14px 26px;margin-bottom:auto"><span class="f" style="font-size:25px">Ставка 6% ниже инфляции 6,3%: такой долг дешевеет сам, гасить его досрочно незачем</span></div></div>', "Досрочка: льготная ипотека"))

# ── 4. зачем занимают осознанно ─────────────────────────────────────────────
S.append(slide(top("Зачем занимают, когда деньги есть") + '<h1>Долг увеличивает и прибыль, и убыток. Работает, только если отдача выше ставки</h1>'
  '<div class="body"><div class="row fill" style="gap:24px;align-items:stretch">'
  '<div style="flex:1.3;display:flex;flex-direction:column;gap:14px">'
  + '<div class="g2" style="gap:14px">'
  + '<div class="sticky teal" style="gap:8px"><span class="lab">Дело идёт хорошо</span>'
    '<div class="mline"><span>свой миллион под 35% годовых</span><b>350 000 ₽</b></div>'
    '<div class="mline"><span>добавили миллион в кредит под 20%</span><b>700 000 ₽</b></div>'
    '<div class="mline"><span>минус проценты банку</span><b>−200 000 ₽</b></div>'
    '<div class="verdict good">Осталось 500 000 ₽ на свой миллион — 50% вместо 35%</div></div>'
  + '<div class="sticky coral" style="gap:8px"><span class="lab">Дело пошло хуже</span>'
    '<div class="mline"><span>те же два миллиона, но отдача 15%</span><b>300 000 ₽</b></div>'
    '<div class="mline"><span>минус проценты банку</span><b>−200 000 ₽</b></div>'
    '<div class="mline"><span>осталось на свой миллион</span><b>100 000 ₽</b></div>'
    '<div class="verdict bad">10% вместо 15% — с кредитом вышло хуже, чем без него</div></div>'
  + '</div>'
  + '<div class="rule" style="padding:18px 26px"><span class="f" style="font-size:27px">Занимать имеет смысл, пока отдача <b>заметно выше</b> ставки: разница и есть заработок на чужих деньгах</span>'
    '<span class="n">Проценты в примере условные: это арифметика рычага, а не обещание доходности.</span></div>'
  + '</div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:14px">'
  + sticky("lav", "Почему богатые не продают, а занимают", "Продать актив — значит заплатить налог и отдать будущий рост. Взять кредит под его залог — актив остаётся у вас и продолжает дорожать, а на руках появляются деньги. Так поступают, пока ставка по кредиту ниже, чем растёт актив.")
  + '<div class="card" style="gap:6px"><span class="note-dark" style="font-weight:500">Сколько занимают под залог акций</span>'
    '<div class="stat sm"><div class="n">25,7 <small>→</small> 76 <small>млрд $</small></div>'
    '<div class="l">столько денег клиенты Morgan Stanley взяли в долг, заложив свои акции вместо продажи: 25,7 млрд в 2016 году и около 76 млрд в 2021‑м</div></div></div>'
  + '</div></div></div>', "Рычаг и залог"))

# ── 5. МФО и отзывы ─────────────────────────────────────────────────────────
S.append(slide(top("Задание про МФО") + '<h1>Там, где правило нарушено сильнее всего: три отзыва о микрозаймах</h1>'
  '<div class="body" style="justify-content:center"><div class="g3" style="margin-bottom:22px">'
  + quote("bad", "«Взяла 56 тысяч, а погасила 113 тысяч». Заём закрыт вдвое дороже, чем взят.", "МигКредит, отзыв на topbanki.ru, 21 октября 2017", "56 000 → 113 000 ₽")
  + quote("bad", "Взяла 18 000 ₽, сразу списали 7 200 ₽ за навязанные услуги, долг вырос до 26 000 ₽. Звонки с угрозами начались до просрочки.", "EcoZaym, отзыв на 1mbank.ru, 11 мая 2026", "18 000 → 26 000 ₽")
  + quote("good", "Заём 15 000 ₽ на две недели, переплата около 250 ₽, всё дистанционно. Так МФО и задумана: очень коротко и по делу.", "Быстроденьги, отзыв на 1mbank.ru, 9 апреля 2026", "≈ 250 ₽ за 14 дней")
  + '</div><div class="g2">'
  + sticky("coral", "Цена спешки", "Предел ставки — 0,8% в день, это около 292% годовых. За две недели терпимо, за год — катастрофа. Опасны не проценты, а срок, на который заём затягивается.")
  + sticky("teal", "С 1 апреля 2026 стало строже", "Банк России снизил предельную переплату по коротким займам со 130% до 100% от суммы долга: взял 10 000 ₽ — вернёшь не больше 20 000 ₽ вместе со штрафами и комиссиями.")
  + '</div></div>', "МФО и отзывы"))

out = "\n".join(S)
(HERE / "slides.html").write_text(out, encoding="utf-8")
print(f"slides.html: {len(S)} слайдов, {len(out.encode()) // 1024} КБ")
