---
name: tbank-credits
description: "Доклад на 3 минуты про кредиты Т-Банка. Донор токенов — Stripe из awesome-design-md: глубокие сине-чернильные тексты, почти белый холст, табличные цифры. Отстройка: акцент не единый индиго-CTA, а смысловая тройка «правило / выгодно / дорого»."
colors:
  canvas: "#FFFFFF"
  surface: "#F5F8FC"
  surface-2: "#EEF2F8"
  ink: "#0D253D"
  body: "#3A4A5E"
  muted: "#64748D"
  hairline: "#E3E8EE"
  hairline-strong: "#CBD5E3"
  rule: "#4B3BEB"
  rule-soft: "#E9E7FE"
  good: "#12805C"
  good-soft: "#DFF3EB"
  bad: "#C02434"
  bad-soft: "#FBE4E7"
  warn: "#B26A00"
  warn-soft: "#FCEFD9"
  dark-canvas: "#0B1B2B"
  on-dark: "#FFFFFF"
typography:
  display-xl: {fontFamily: Geologica, fontSize: 68px, fontWeight: 600, lineHeight: 1.04, letterSpacing: -0.02em}
  heading:    {fontFamily: Geologica, fontSize: 46px, fontWeight: 600, lineHeight: 1.1, letterSpacing: -0.015em}
  card-title: {fontFamily: Geologica, fontSize: 24px, fontWeight: 500, lineHeight: 1.2}
  body:       {fontFamily: Golos Text, fontSize: 22px, fontWeight: 400, lineHeight: 1.42}
  stat:       {fontFamily: Geologica, fontSize: 80px, fontWeight: 600, lineHeight: 1, fontVariantNumeric: tabular-nums}
  mono:       {fontFamily: JetBrains Mono, fontSize: 19px, fontWeight: 500}
rounded: {sm: 8px, md: 12px, lg: 16px, xl: 24px, full: 9999px}
spacing: {xs: 8px, sm: 12px, md: 16px, lg: 24px, xl: 32px, xxl: 48px, frame-x: 84px, frame-y: 58px}
components:
  rule-card: {background: "{colors.rule-soft}", rounded: "{rounded.xl}"}
  scale-bar: {good: "{colors.good}", bad: "{colors.bad}", threshold: "{colors.rule}"}
  quote: {background: "{colors.surface}", rounded: "{rounded.lg}", border-left: "3px solid {colors.hairline-strong}"}
---

## Overview
Три минуты, пять слайдов, аудитория — однокурсники и преподаватель по банковским продуктам.
Характер: спокойный финансовый документ, где решает цифра, а не украшение. Всё держится на
одном правиле и на том, проходит ли конкретный продукт это правило.

## Colors
Индиго — только правило и порог на шкале. Зелёный — ставка ниже порога, то есть выгодно.
Красный — ставка выше порога. Больше цвет нигде не появляется: карточки серые, текст чернильный.

## Typography
Geologica на заголовках и цифрах: у неё узкие плотные знаки, длинный заголовок помещается в две строки.
Golos Text на тексте. JetBrains Mono на ставках, суммах и адресах, везде табличные цифры,
чтобы разряды выстраивались по вертикали.

## Layout
Кадр 1600×900, поля 84×58. На слайде одна мысль и один визуальный блок: таблица, шкала или цитаты.
Источник и дата — всегда внизу кадра.

## Do's and Don'ts
- Делать: ставку писать как ПСК, где банк её раскрывает; рядом с любой цифрой — дата снятия.
- Делать: считать выгоду относительно порога, а не «дорого или дёшево» на глаз.
- Не делать: фирменные цвета Т-Банка и его логотип — это доклад о банке, а не его реклама.
- Не делать: обещаний доходности, советов брать конкретный кредит, скрытых допущений в расчёте.
