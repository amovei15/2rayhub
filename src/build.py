#!/usr/bin/env python3
"""2rayhub.com — static site generator.

Builds 11 pages targeting the v2RayTun keyword core.
Output: ./dist/
"""
import os, json, html, shutil
from pathlib import Path
from related import RELATED

ROOT = Path(__file__).parent
DIST = ROOT.parent / "dist"
DOMAIN = "2rayhub.com"
SITE_NAME = "v2RayTun"
TODAY = "2026-06-19"
METRIKA_ID = ""

NAV = [
    ("/", "Главная"),
    ("/skachat-v2raytun/", "Скачать"),
    ("/podpiska/", "Подписка"),
    ("/konfigi/", "Конфиги"),
    ("/podklyuchenie/", "Подключение"),
    ("/pk/", "ПК"),
    ("/android/", "Android"),
    ("/ios/", "iPhone"),
    ("/tv/", "TV"),
    ("/problemy/", "Проблемы"),
    ("/faq/", "FAQ"),
]

# CTA wording
CTA_TG_ICON = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="margin-right:6px;vertical-align:-2px"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.24 3.64 11.94c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg>'
CTA_MAIL_ICON = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:6px;vertical-align:-2px"><circle cx="12" cy="12" r="4"/><path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-3.92 7.94"/></svg>'
CTA_PRIMARY = f'{CTA_MAIL_ICON}Получить на email'
CTA_PRIMARY_URL = "https://lk.chekdns.click/"
CTA_SECONDARY = f'{CTA_TG_ICON}Получить в Телеграм'
CTA_SECONDARY_URL = "https://t.me/tgbpn_bot?start=utm_2rayhub"
LK_URL = "https://lk.chekdns.click/"
BOT_URL = "https://t.me/tgbpn_bot?start=utm_2rayhub"


def head(title, desc, url, extra_jsonld=None):
    canonical = f"https://{DOMAIN}{url}"
    metrika_tag = ""
    if METRIKA_ID:
        metrika_tag = (
            f'<!-- Yandex.Metrika --><script>(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};'
            f'm[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return;}}}}'
            f'k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})'
            f'(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");'
            f'ym({METRIKA_ID},"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true}});</script>'
            f'<noscript><div><img src="https://mc.yandex.ru/watch/{METRIKA_ID}" style="position:absolute;left:-9999px;" alt=""/></div></noscript><!-- /Yandex.Metrika -->'
        )
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type":"Organization","@id":f"https://{DOMAIN}/#org","name":SITE_NAME,"url":f"https://{DOMAIN}/","logo":f"https://{DOMAIN}/favicon.svg"},
            {"@type":"WebSite","@id":f"https://{DOMAIN}/#site","url":f"https://{DOMAIN}/","name":SITE_NAME,"inLanguage":"ru-RU","publisher":{"@id":f"https://{DOMAIN}/#org"}},
        ],
    }
    if extra_jsonld:
        jsonld["@graph"].extend(extra_jsonld)
    jsonld_str = json.dumps(jsonld, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0a0b14">
<meta name="yandex-verification" content="39e4734c9e29e096">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:locale" content="ru_RU">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700&family=JetBrains+Mono:wght@500&display=swap">
<link rel="stylesheet" href="/assets/styles.css?v=5">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<script type="application/ld+json">{jsonld_str}</script>
{metrika_tag}
</head>
<body>"""


def nav(current_url):
    links_html = ""
    for u, label in NAV:
        cur = ' aria-current="page"' if u == current_url else ""
        links_html += f'<a href="{u}"{cur}>{label}</a>'
    drawer_html = ""
    for u, label in NAV:
        cur = ' aria-current="page"' if u == current_url else ""
        drawer_html += f'<a href="{u}"{cur}>{label}</a>'
    return f"""<header class="nav">
  <div class="nav-inner">
    <a href="/" class="brand"><span class="brand-mark">V</span>v2RayTun</a>
    <nav class="nav-links" aria-label="Главное меню">{links_html}</nav>
    <a href="{CTA_PRIMARY_URL}" class="nav-cta">{CTA_PRIMARY}</a>
    <button class="nav-burger" type="button" aria-label="Меню" onclick="document.querySelector('.drawer').classList.toggle('open')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
</header>
<nav class="drawer" aria-label="Мобильное меню">{drawer_html}<a href="{CTA_PRIMARY_URL}" class="btn btn-primary" style="margin-top:14px;justify-content:center">{CTA_PRIMARY}</a></nav>"""


OFFICES = {
    "moscow-city": ("Москва-Сити", "123100, Пресненская наб., д. 12, башня «Федерация», офис 67-04"),
    "leninsky":    ("Ленинский",   "119049, г. Москва, Ленинский просп., д. 6, стр. 1, офис 312"),
    "belorussky":  ("Белорусская", "127055, г. Москва, ул. Бутырский Вал, д. 68/70, стр. 1, офис 5"),
}
PIN_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
PHONE_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
MOBILE_SVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="3"/><path d="M11 18h2"/></svg>'
PHONES = {
    "888": ("88007001234",  "8 800 700-12-34",     "Бесплатно по России",       PHONE_SVG),
    "495": ("+74956448120", "+7 (495) 644-81-20",  "Приёмная, Москва",          PHONE_SVG),
    "916": ("+79165214408", "+7 (916) 521-44-08",  "Мобильный, Москва (МТС)",   MOBILE_SVG),
}

def footer(office=None, phone="888"):
    today = TODAY[:4]
    office_html = ""
    if office and office in OFFICES:
        name, addr = OFFICES[office]
        office_html = f"""
    <div class="fc-group">
      <h5>Наш офис</h5>
      <div class="fc-grid">
        <div class="fc-card">
          <span class="fc-ico">{PIN_SVG}</span>
          <div><b>{name}</b><span>{addr}</span></div>
        </div>
      </div>
    </div>"""
    p_href, p_label, p_sub, p_svg = PHONES[phone]
    return f"""<footer class="foot">
  <div class="foot-inner">
    <div class="foot-brand">
      <a href="/" class="brand"><span class="brand-mark">V</span>v2RayTun</a>
      <p>Сайт-навигатор по приложению v2RayTun: подписка, конфигурации, инструкции по запуску на Windows, Android, iOS и TV-приставках.</p>
    </div>
    <div class="foot-col">
      <h5>Загрузка</h5>
      <ul>
        <li><a href="/skachat-v2raytun/">Все платформы</a></li>
        <li><a href="/pk/">Windows / Mac</a></li>
        <li><a href="/android/">Android и APK</a></li>
        <li><a href="/ios/">iPhone / iPad</a></li>
        <li><a href="/tv/">Android TV</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h5>Сервис</h5>
      <ul>
        <li><a href="/podpiska/">Тариф v2RayTun Plus</a></li>
        <li><a href="/konfigi/">Конфигурации</a></li>
        <li><a href="/podklyuchenie/">Подключение</a></li>
      </ul>
    </div>
    <div class="foot-col">
      <h5>Помощь</h5>
      <ul>
        <li><a href="/problemy/">Если не работает</a></li>
        <li><a href="/faq/">Частые вопросы</a></li>
      </ul>
    </div>
  </div>
  <div class="foot-contacts">
    <div class="fc-group">
      <h5>Связаться</h5>
      <div class="fc-grid">
        <a class="fc-card" href="tel:{p_href}">
          <span class="fc-ico">{p_svg}</span>
          <div><b>{p_label}</b><span>{p_sub}</span></div>
        </a>
      </div>
    </div>
{office_html}
  </div>
</footer>
</body></html>"""


def hero(tag, title_pre, title_grad, title_post, lead, primary="active", show_stats=True, show_mockup=True):
    title_html = title_pre
    if title_grad:
        title_html += f' <span class="grad">{title_grad}</span>'
    if title_post:
        title_html += f' {title_post}'
    cta_html = f"""<div class="cta-pair">
      <a href="{CTA_PRIMARY_URL}" class="btn btn-primary">{CTA_PRIMARY}</a>
      <a href="{CTA_SECONDARY_URL}" class="btn btn-ghost">{CTA_SECONDARY}</a>
    </div>"""
    stats_html = ""
    if show_stats:
        stats_html = """<div class="hero-stats">
      <div><strong>6 локаций</strong><span>Европа · США</span></div>
      <div><strong>VLESS Reality</strong><span>протокол</span></div>
      <div><strong>3 устройства</strong><span>в подписке</span></div>
    </div>"""
    mockup_html = ""
    if show_mockup:
        mockup_html = """<div class="mockup">
    <div class="mockup-frame"><div class="mockup-screen">
      <div class="mockup-row"><span class="led"></span><div class="l"><b>Нидерланды</b><span>Reality</span></div><span class="ms">22 ms</span></div>
      <div class="mockup-row"><span class="led"></span><div class="l"><b>Германия</b><span>Reality</span></div><span class="ms">28 ms</span></div>
      <div class="mockup-row"><span class="led"></span><div class="l"><b>Финляндия</b><span>Reality</span></div><span class="ms">19 ms</span></div>
      <div class="mockup-row"><span class="led"></span><div class="l"><b>Польша</b><span>Reality</span></div><span class="ms">25 ms</span></div>
      <div class="mockup-row"><span class="led"></span><div class="l"><b>США</b><span>Reality</span></div><span class="ms">120 ms</span></div>
    </div></div>
  </div>"""
    return f"""<section class="hero">
  <div class="wrap hero-inner">
    <div>
      <span class="hero-tag"><span class="pulse"></span>{tag}</span>
      <h1>{title_html}</h1>
      <p class="lead">{lead}</p>
      {cta_html}
      {stats_html}
    </div>
    {mockup_html}
  </div>
</section>"""


def cta_banner(title, sub):
    return f"""<div class="cta-banner">
  <div>
    <h3>{title}</h3>
    <p>{sub}</p>
  </div>
  <div class="cta-pair">
    <a href="{CTA_PRIMARY_URL}" class="btn btn-primary btn-sm">{CTA_PRIMARY}</a>
    <a href="{CTA_SECONDARY_URL}" class="btn btn-ghost btn-sm">{CTA_SECONDARY}</a>
  </div>
</div>"""


def faq_block(items):
    out = '<div class="faq">'
    for q, a in items:
        out += f'<details><summary>{q}</summary><div class="ans">{a}</div></details>'
    out += '</div>'
    return out


def related_block(url):
    items = RELATED.get(url, [])
    if not items: return ""
    chips = "".join(f'<span class="kw-chip">{html.escape(q)}</span>' for q in items)
    return f"""<section class="section">
  <div class="wrap">
    <span class="eyebrow">Часто ищут</span>
    <h2>Часто спрашивают про v2RayTun</h2>
    <p class="lead" style="margin-bottom:18px">Популярные запросы по приложению v2RayTun — от установки и подписки до решения проблем.</p>
    <div class="kw-cloud">{chips}</div>
  </div>
</section>"""


def page_home():
    url = "/"
    title = "v2RayTun — приложение для подключений на ПК, Android и iPhone"
    desc = ("v2RayTun — клиент для протокола VLESS Reality с готовой подпиской на 5 европейских локаций. "
            "Установка на Windows, Android, iOS и TV-приставку, конфигурация в один тап.")
    parts = [head(title, desc, url), nav(url)]
    parts.append(hero(
        tag="VLESS · Reality · сеть подключений",
        title_pre="v2RayTun —",
        title_grad="приложение",
        title_post="на VLESS Reality для всех платформ",
        lead=("Запускай v2RayTun, забирай рабочий профиль из бота — соединение поднимается за секунды. "
              "Серверы в пяти европейских странах и США, трафик без лимита, до трёх устройств на одну подписку."),
    ))
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Что внутри</span>
      <h2>Почему v2RayTun выбирают чаще остальных</h2>
      <p class="lead">Происходящее под капотом скрыто за плоским тапом «Подключить». Это и есть главная фишка приложения.</p>
    </div>
    <div class="grid-3">
      <div class="feat"><div class="feat-ico">⚡</div><h3>Профиль за полминуты</h3><p>Активация в Telegram-боте занимает меньше времени, чем поиск инструкции. Получаешь рабочую ссылку — открываешь v2RayTun — нажимаешь подключиться.</p></div>
      <div class="feat"><div class="feat-ico">🌍</div><h3>Сеть из 6 локаций</h3><p>Серверы в Нидерландах, Германии, Финляндии, Польше, Франции и США. Один тап — переключение между ними прямо в приложении.</p></div>
      <div class="feat"><div class="feat-ico">📱</div><h3>Любое устройство</h3><p>Сборки под Windows 7/10/11, macOS Intel и Apple Silicon, Android 7+, iOS 14+ и Android TV. Одна подписка покрывает три устройства.</p></div>
      <div class="feat"><div class="feat-ico">🛡️</div><h3>Маскировка VLESS Reality</h3><p>Профиль использует протокол с TLS-маскировкой под обычный браузерный трафик — устойчив к фильтрации в строгих сетях.</p></div>
      <div class="feat"><div class="feat-ico">♾️</div><h3>Без лимитов на трафик</h3><p>Скорость не режется при просмотре YouTube, играх или загрузках. Канал каждого сервера — минимум гигабит.</p></div>
      <div class="feat"><div class="feat-ico">🤝</div><h3>Живая поддержка</h3><p>Если что-то отвалилось — в боте отвечают живые люди, не FAQ-выдача. Среднее время ответа в будни — пара минут.</p></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Как это работает</span>
      <h2>От нуля до защищённого подключения — четыре шага</h2>
    </div>
    <div class="steps">
      <div class="step"><h4>Активация</h4><p>Нажми <i>Получить в Телеграм</i>, дай команду <code>/start</code> и выбери тариф. Бот выдаст ссылку-профиль и подскажет, куда её вставлять.</p></div>
      <div class="step"><h4>Установка v2RayTun</h4><p>Загрузи приложение под свою систему — ссылки на странице <a href="/skachat-v2raytun/">«Скачать»</a>. На iOS — из App Store, на Android — APK или Google Play.</p></div>
      <div class="step"><h4>Импорт профиля</h4><p>Открой v2RayTun и нажми «+ Добавить» → «Из буфера». Полученная ссылка автоматически распарсится — серверы, маскировка, ключи подтянутся сами.</p></div>
      <div class="step"><h4>Подключение</h4><p>Тапни круглую кнопку в центре приложения — соединение поднимется за пару секунд. Когда индикатор стал зелёным, можно открывать любой сайт.</p></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Тарифы</span>
      <h2>Подписка v2RayTun Plus — четыре варианта</h2>
      <p class="lead">Чем длиннее срок — тем ниже цена за месяц. Все тарифы дают одинаковый функционал: 6 локаций, до 3 устройств, поддержка.</p>
    </div>
    <div class="plans">
      <div class="plan">
        <div class="plan-name">На месяц</div>
        <div class="plan-period">Стартовый</div>
        <div class="plan-price">249<span class="cur">₽</span></div>
        <div class="plan-discount" style="color:var(--ink-soft)">Базовая цена</div>
        <ul><li>1 профиль на 3 устройства</li><li>6 локаций: Европа и США</li><li>Без лимита на трафик</li><li>Замена на новый сервер бесплатно</li></ul>
        <a href="/podpiska/" class="btn btn-ghost">Подробнее</a>
      </div>
      <div class="plan">
        <div class="plan-name">На 3 месяца</div>
        <div class="plan-period">Выгодный старт</div>
        <div class="plan-price">599<span class="cur">₽</span></div>
        <div class="plan-discount">Экономия 20% к месячному</div>
        <ul><li>Всё из месячного плана</li><li>Резервный профиль в боте</li><li>Приоритетная очередь поддержки</li><li>Без лимита на трафик</li></ul>
        <a href="/podpiska/" class="btn btn-ghost">Подробнее</a>
      </div>
      <div class="plan featured">
        <div class="plan-name">На полгода</div>
        <div class="plan-period">Оптимальный</div>
        <div class="plan-price">1090<span class="cur">₽</span></div>
        <div class="plan-discount">Экономия 27% к месячному</div>
        <ul><li>Всё из месячного плана</li><li>Резервный профиль в боте</li><li>Приоритетная очередь поддержки</li><li>Доступ к бета-серверам</li></ul>
        <a href="/podpiska/" class="btn btn-primary">Подробнее</a>
      </div>
      <div class="plan">
        <div class="plan-name">На год</div>
        <div class="plan-period">Максимум выгоды</div>
        <div class="plan-price">1890<span class="cur">₽</span></div>
        <div class="plan-discount">Экономия 37% к месячному</div>
        <ul><li>Всё из полугодового плана</li><li>Два резервных профиля</li><li>Гарантия возврата 14 дней</li><li>Промокод на продление</li></ul>
        <a href="/podpiska/" class="btn btn-ghost">Подробнее</a>
      </div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">FAQ</span>
      <h2>Короткие ответы на частые вопросы</h2>
    </div>""")
    parts.append(faq_block([
      ("Что такое v2RayTun и для чего он нужен?",
       "v2RayTun — это клиент, который умеет работать с протоколом VLESS Reality. Приложение хранит твой профиль (ссылку с настройками сервера) и поднимает соединение по этим настройкам в один тап."),
      ("Сколько стоит v2RayTun?",
       "Само приложение бесплатное — скачивается под любую систему. Платный только профиль-подписка, через который идёт трафик. Минимальный тариф 249 ₽ в месяц, годовой — 1890 ₽."),
      ("Есть ли бесплатный v2RayTun?",
       "У сервиса нет бесплатного режима, но есть пробный период три дня — в это время доступны все функции. После окончания пробы профиль превращается в обычный платный."),
      ("Чем v2RayTun отличается от других клиентов VLESS?",
       "Главное отличие — простота: один профиль, который сам понимает на какой сервер пойти, и одна кнопка «Подключить». Не нужно вручную выбирать порт, маскировку или fingerprint."),
      ("Где взять рабочую подписку для v2RayTun?",
       "В боте — нажми кнопку «Получить в Телеграм» в шапке сайта. Бот пришлёт ссылку-профиль, которую открываешь в приложении."),
      ("На скольких устройствах работает один профиль?",
       "До трёх одновременно. Это значит, что ты можешь подключиться с телефона, ноутбука и приставки — все три устройства будут работать через одну подписку."),
    ]))
    parts.append(cta_banner("Готов поднять v2RayTun за минуту?", "Активируй профиль в Telegram-боте — подключение по VLESS Reality сразу будет в приложении."))
    parts.append("</div></section>")
    parts.append(related_block(url))
    parts.append(footer("moscow-city", "888"))
    return "".join(parts)


def page_skachat():
    url = "/skachat-v2raytun/"
    title = "Скачать v2RayTun — официальные сборки для всех платформ"
    desc = ("v2RayTun скачать на ПК Windows, Android APK, iPhone из App Store, Mac и Android TV. "
            "Прямые ссылки на актуальные сборки, описание совместимости, инструкции по запуску.")
    parts = [head(title, desc, url), nav(url)]
    parts.append(hero(
        tag="Загрузка под все системы",
        title_pre="v2RayTun скачать —",
        title_grad="официальные сборки",
        title_post="под Windows, Android, iOS и TV",
        lead=("Под каждую систему — свой установщик. Ниже собраны актуальные версии: прямой APK для Android, "
              "магазинная сборка для iPhone, инсталлер для Windows 7/10/11 и DMG под Mac."),
        show_mockup=False,
    ))
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Платформы</span>
      <h2>v2RayTun для всех платформ — выбери свою</h2>
      <p class="lead">Все варианты загрузки — оригинальные сборки. APK и инсталлеры берутся с актуальной ветки разработки, без переупаковки.</p>
    </div>
    <div class="grid-4">
      <div class="feat"><div class="feat-ico">🪟</div><h3><a href="/pk/">Windows / ПК</a></h3><p>Установщик x64 для Windows 10 и 11. Запускается двойным кликом, иконка появляется в трее.</p><a href="/pk/">v2RayTun скачать на ПК →</a></div>
      <div class="feat"><div class="feat-ico">🤖</div><h3><a href="/android/">Android</a></h3><p>APK напрямую — обновляется быстрее версии Google Play. Совместимость с Android 7 и выше.</p><a href="/android/">Скачать v2RayTun APK →</a></div>
      <div class="feat"><div class="feat-ico">🍎</div><h3><a href="/ios/">iPhone / iPad</a></h3><p>Бесплатно из App Store: поддерживаются все iPhone и iPad с iOS 14.0 и новее.</p><a href="/ios/">v2RayTun на айфон →</a></div>
      <div class="feat"><div class="feat-ico">📺</div><h3><a href="/tv/">Android TV</a></h3><p>Отдельная сборка для Android TV-приставок: интерфейс под пульт, без жестов.</p><a href="/tv/">v2RayTun на TV →</a></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Подробности</span>
      <h2>Куда сохраняется и как запускается</h2>
    </div>
    <div class="grid-3">
      <div class="feat"><h3>v2RayTun скачать на ПК</h3><p>Для Windows 10/11 — установщик примерно 28 МБ. Кладёт исполняемый файл в <code>C:\\Program Files\\v2RayTun\\</code>, профили хранятся в <code>%APPDATA%\\v2RayTun</code>. Запускается из меню «Пуск» или ярлыка на рабочем столе.</p></div>
      <div class="feat"><h3>v2RayTun скачать на андроид</h3><p>APK весит около 18 МБ. Перед установкой включи в настройках Android разрешение «Установка из неизвестных источников» для браузера. После — открой файл и нажми «Установить».</p></div>
      <div class="feat"><h3>Скачать v2RayTun на iPhone</h3><p>Найди приложение в App Store по запросу <i>v2RayTun</i>. Совместимо с iOS 14.0+, требует около 35 МБ свободного места. Установка стандартная — через кнопку «Загрузить».</p></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Перед загрузкой</span>
      <h2>Что важно знать про скачивание v2RayTun</h2>
    </div>
    <div class="grid-2">
      <div class="feat"><h3>Где официально</h3><p>Прямые ссылки на этой странице ведут на сборки с GitHub-релизов разработчика и в магазины приложений Apple/Google. Альтернативные «зеркала» из выдачи могут быть подделкой — лучше не пользоваться.</p></div>
      <div class="feat"><h3>Безопасно ли</h3><p>v2RayTun не содержит рекламы, не собирает аналитику и не запрашивает разрешений сверх необходимых для VPN-туннеля. Исходный код частично открыт на GitHub — можно изучить.</p></div>
    </div>""")
    parts.append(faq_block([
      ("v2RayTun скачать бесплатно — что включено?", "Само приложение всегда бесплатно. Платная — только подписка, через которую идёт трафик. На странице загрузки есть сборки для всех систем без оплаты."),
      ("Можно ли скачать v2RayTun с GitHub?", "Да, GitHub — официальный источник для APK-сборок. Это самый «свежий» канал — обновления туда попадают раньше Google Play."),
      ("Какая последняя версия v2RayTun?", "Обновления выходят 1-2 раза в месяц. На этой странице ссылки ведут на актуальный релиз — версия и дата релиза указаны рядом со ссылкой."),
      ("Что делать, если приложение не загружается?", "Чаще всего помогает смена сети (мобильные данные вместо Wi-Fi) или загрузка через DownloadAccelerator/aria2. Если проблема не уходит, напиши в бота — там пришлют альтернативное зеркало."),
    ]))
    parts.append(cta_banner("Скачал — что дальше?", "Активируй профиль в боте и нажми «Подключить». Соединение поднимется за пару секунд."))
    parts.append("</div></section>")
    parts.append(related_block(url))
    parts.append(footer())
    return "".join(parts)


def page_podpiska():
    url = "/podpiska/"
    title = "Подписка v2RayTun Plus — тарифы от 249 ₽ за месяц"
    desc = ("Подписка v2RayTun Plus открывает доступ к серверам, маскировке и поддержке. "
            "Месяц, полгода и год — у каждого тарифа свои бонусы и цена за месяц.")
    parts = [head(title, desc, url), nav(url)]
    parts.append(hero(
        tag="Подписка v2RayTun Plus",
        title_pre="Подписка v2RayTun Plus —",
        title_grad="три тарифа",
        title_post="на любой бюджет",
        lead=("Подписка — это и есть «доступ к серверам». Сам v2RayTun остаётся бесплатным, "
              "оплачивается только профиль, через который проходит трафик."),
        show_mockup=False,
    ))
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Тарифы</span>
      <h2>Подписка v2RayTun Plus — выбери срок</h2>
      <p class="lead">Чем длиннее срок, тем ниже цена за месяц. Все тарифы включают одинаковый набор: 6 локаций, до 3 устройств, без лимита на трафик.</p>
    </div>
    <div class="plans">
      <div class="plan">
        <div class="plan-name">v2RayTun Plus · 1 месяц</div>
        <div class="plan-period">Стартовый</div>
        <div class="plan-price">249<span class="cur">₽</span></div>
        <div class="plan-discount" style="color:var(--ink-soft)">Базовая цена</div>
        <ul><li>Один профиль · 3 устройства</li><li>6 серверов: Европа и США</li><li>Без лимита на трафик</li><li>Поддержка в чате</li><li>Возврат до 7-го дня</li></ul>
        <a href="https://lk.chekdns.click/" target="_blank" rel="noopener" class="btn btn-ghost">Купить подписку</a>
      </div>
      <div class="plan">
        <div class="plan-name">v2RayTun Plus · 3 месяца</div>
        <div class="plan-period">Выгодный старт</div>
        <div class="plan-price">599<span class="cur">₽</span></div>
        <div class="plan-discount">— 20% к месячному</div>
        <ul><li>Всё, что входит в месячный</li><li>Резервный профиль в боте</li><li>Приоритет в очереди поддержки</li><li>Без лимита на трафик</li><li>Возврат до 7-го дня</li></ul>
        <a href="https://lk.chekdns.click/" target="_blank" rel="noopener" class="btn btn-ghost">Купить подписку</a>
      </div>
      <div class="plan featured">
        <div class="plan-name">v2RayTun Plus · 6 месяцев</div>
        <div class="plan-period">Оптимальный</div>
        <div class="plan-price">1090<span class="cur">₽</span></div>
        <div class="plan-discount">— 27% к месячному</div>
        <ul><li>Всё, что входит в месячный</li><li>Резервный профиль в боте</li><li>Приоритет в очереди поддержки</li><li>Бета-серверы (новые локации первыми)</li><li>Возврат до 7-го дня</li></ul>
        <a href="https://lk.chekdns.click/" target="_blank" rel="noopener" class="btn btn-primary">Купить подписку</a>
      </div>
      <div class="plan">
        <div class="plan-name">v2RayTun Plus · 12 месяцев</div>
        <div class="plan-period">Максимум выгоды</div>
        <div class="plan-price">1890<span class="cur">₽</span></div>
        <div class="plan-discount">— 37% к месячному</div>
        <ul><li>Всё из шестимесячного тарифа</li><li>Два резервных профиля</li><li>Возврат до 14-го дня</li><li>Промокод на следующее продление</li></ul>
        <a href="https://lk.chekdns.click/" target="_blank" rel="noopener" class="btn btn-ghost">Купить подписку</a>
      </div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Как работает</span>
      <h2>Что входит в подписку v2RayTun Plus</h2>
    </div>
    <div class="grid-3">
      <div class="feat"><div class="feat-ico">📦</div><h3>Один профиль на 3 устройства</h3><p>Подключайся одновременно с телефона, ноутбука и приставки. Лимит сессий — три. Если подключиться с четвёртого устройства, самая старая сессия отвалится.</p></div>
      <div class="feat"><div class="feat-ico">♾️</div><h3>Безлимитный трафик</h3><p>Канал каждого сервера — гигабит и выше. На скоростях YouTube 4K, торрентов и игр не упирается.</p></div>
      <div class="feat"><div class="feat-ico">🛟</div><h3>Замена сервера</h3><p>Если конкретный сервер начал проседать, его можно мгновенно заменить через бота — без потери профиля и переустановки приложения.</p></div>
      <div class="feat"><div class="feat-ico">🧪</div><h3>Пробный период 3 дня</h3><p>Можно протестировать каждый тариф трое суток бесплатно. Если не подошло — деньги возвращаются.</p></div>
      <div class="feat"><div class="feat-ico">💬</div><h3>Поддержка живая</h3><p>В чате бота отвечают сотрудники, а не автоответчики. По будням время ответа — 1-5 минут.</p></div>
      <div class="feat"><div class="feat-ico">🔄</div><h3>Гарантия возврата</h3><p>В первые 7 дней подписки (14 — на годовом тарифе) можно отказаться. Деньги вернутся на тот же способ оплаты.</p></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Оплата</span>
      <h2>Как оплатить подписку v2RayTun</h2>
    </div>
    <div class="grid-2">
      <div class="feat"><h3>Российская карта</h3><p>Принимаются карты Мир, Visa, Mastercard от российских банков. Оплата через защищённый шлюз — данные карты на серверах сервиса не остаются.</p></div>
      <div class="feat"><h3>СБП</h3><p>Перевод по QR-коду или ссылке СБП — без ввода реквизитов карты. Зачисление в течение минуты, профиль активируется автоматически.</p></div>
      <div class="feat"><h3>Криптовалюта</h3><p>USDT (TRC-20 и ERC-20) для тех, кто предпочитает анонимные платежи. Курс и реквизиты адреса показываются в боте перед оплатой.</p></div>
      <div class="feat"><h3>Промокод на скидку</h3><p>На странице оплаты есть поле «Промокод» — туда вставляются скидочные коды из соцсетей сервиса. Скидка применяется поверх любого тарифа.</p></div>
    </div>""")
    parts.append(faq_block([
      ("Сколько стоит v2RayTun Plus?", "От 249 ₽ за месяц (если брать самый короткий тариф) до 158 ₽/месяц в эквиваленте годового. Точные цены — выше на странице."),
      ("Есть ли v2RayTun Plus бесплатно?", "Сам v2RayTun — бесплатное приложение. Тариф Plus — платный, бесплатной версии нет, но есть пробные 3 дня с возвратом."),
      ("Что такое v2RayTun Pro?", "Pro — старое название тарифа, сейчас называется Plus. Если видел упоминание Pro в выдаче — это про тот же набор функций."),
      ("Можно ли купить v2RayTun один раз навсегда?", "Нет, серверы стоят денег ежемесячно, поэтому модель — подписочная. Самый длинный тариф — 12 месяцев."),
      ("Как продлить подписку v2RayTun?", "В боте нажми «Мои подписки» → «Продлить». Можно настроить автопродление, тогда списания будут идти автоматически."),
      ("Как вернуть деньги за v2RayTun?", "Напиши в бота «Возврат» в течение 7 дней (или 14 для годового тарифа), укажи причину — деньги вернутся в течение 3 рабочих дней."),
    ]))
    parts.append(cta_banner("Готов к подписке v2RayTun?", "Открой бота, выбери тариф и получи профиль за пару кликов. Деньги вернутся, если не понравится."))
    parts.append("</div></section>")
    parts.append(related_block(url))
    parts.append(footer("leninsky", "495"))
    return "".join(parts)


def page_konfigi():
    url = "/konfigi/"
    title = "Конфигурации для v2RayTun — VLESS Reality профили"
    desc = ("Конфигурация для v2RayTun — это ссылка с настройками сервера и протокола. "
            "Происходит активация в боте, импорт в приложение и подключение в один тап.")
    parts = [head(title, desc, url), nav(url)]
    parts.append(hero(
        tag="Конфиги · профили · ключи",
        title_pre="Конфигурации для v2RayTun —",
        title_grad="готовые профили",
        title_post="VLESS Reality",
        lead=("Конфигурация — это короткая ссылка-профиль, в которой уже прописаны адрес сервера, протокол, "
              "ключи и параметры маскировки. Просто импортируешь в v2RayTun и пользуешься."),
        show_mockup=False,
    ))
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Что в конфиге</span>
      <h2>Что включает рабочий профиль v2RayTun</h2>
      <p class="lead">Один профиль покрывает всю сеть серверов, поддерживает маскировку под обычный браузерный трафик и работает даже в сетях с белыми списками.</p>
    </div>
    <div class="grid-2">
      <div class="feat"><div class="feat-ico">🔗</div><h3>Готовая ссылка-профиль</h3><p>Не нужно вводить адрес и порт вручную — приложение само распарсит ссылку и подтянет настройки. Формат — стандартный <code>vless://</code>, открывается в v2RayTun через буфер обмена.</p></div>
      <div class="feat"><div class="feat-ico">🌐</div><h3>Сеть из 6 серверов</h3><p>Один профиль ведёт сразу ко всем нашим локациям. Переключение между Нидерландами, Германией, Финляндией, Польшей, Францией и США — тапом в приложении.</p></div>
      <div class="feat"><div class="feat-ico">🛡️</div><h3>Маскировка под TLS</h3><p>Профиль использует VLESS Reality — трафик выглядит как обычные HTTPS-запросы к крупным сайтам. Это помогает обходить даже сети с белыми списками.</p></div>
      <div class="feat"><div class="feat-ico">♻️</div><h3>Резервные профили</h3><p>В тарифах на полгода и год — дополнительные профили на запас. Если основной по какой-то причине отвалился, переключаешься на резервный без переустановки.</p></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Получение</span>
      <h2>Как получить рабочую конфигурацию</h2>
    </div>
    <div class="steps">
      <div class="step"><h4>Активация</h4><p>Нажми «Получить в Телеграм» в шапке сайта или зайди в Telegram-бота напрямую. Бот предложит выбрать тариф или активировать пробный период.</p></div>
      <div class="step"><h4>Получение ссылки</h4><p>После оплаты или активации пробы бот пришлёт длинную ссылку, начинающуюся с <code>vless://</code>. Это и есть твой профиль.</p></div>
      <div class="step"><h4>Импорт</h4><p>Скопируй ссылку в буфер. Открой v2RayTun → «+ Добавить» → «Из буфера». Профиль появится в списке профилей приложения.</p></div>
      <div class="step"><h4>Подключение</h4><p>Тапни на профиль, чтобы он стал активным, и нажми круглую кнопку в центре. Соединение поднимется за пару секунд.</p></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Внимание</span>
      <h2>Чем рабочий профиль отличается от публичных списков</h2>
    </div>
    <div class="grid-2">
      <div class="feat"><h3>Срок жизни</h3><p>Публичные конфиги из открытых Telegram-каналов работают часы — потому что одновременно их использует несколько тысяч человек, и серверы быстро отваливаются. Наш профиль выделен под подписку и стабилен весь её срок.</p></div>
      <div class="feat"><h3>Скорость</h3><p>На публичных серверах канал делится между всеми, и YouTube 1080p часто не вытягивает. На наших — гигабитный канал на сервер и ограниченное число клиентов.</p></div>
      <div class="feat"><h3>Поддержка</h3><p>Если у тебя сломался публичный профиль — никто не починит, ищи новый. У нас в боте есть живая поддержка, которая сменит сервер или выдаст резервный.</p></div>
      <div class="feat"><h3>Сети с белыми списками</h3><p>Корпоративные и операторские сети часто пропускают только белые списки IP — там публичные конфиги бесполезны. Наши серверы заведены на адреса, которые проходят такие фильтры.</p></div>
    </div>""")
    parts.append(faq_block([
      ("Где взять рабочий профиль для v2RayTun?", "Через бота — кнопка «Получить в Телеграм» в шапке. Бот пришлёт ссылку, которую открываешь в приложении."),
      ("Как добавить конфигурацию в v2RayTun?", "В приложении тап на «+» → «Из буфера». Если ссылка скопирована в буфер, она вставится автоматически."),
      ("Можно ли использовать один профиль на нескольких устройствах?", "Да, до трёх параллельно. На четвёртом устройстве самая старая сессия отвалится."),
      ("Что такое VLESS Reality?", "Современный протокол маскировки трафика. Соединение выглядит снаружи как обычное TLS-рукопожатие к крупному сайту — поэтому фильтры его пропускают."),
      ("Конфиг перестал работать — что делать?", "В первую очередь переключись на другой сервер в приложении. Если все не отвечают, напиши в бота «Не работает» — выдадут резервный профиль."),
    ]))
    parts.append(cta_banner("Хочешь получить готовую конфигурацию?", "Активируй профиль в боте — приложение сразу подцепит настройки и подключится."))
    parts.append("</div></section>")
    parts.append(related_block(url))
    parts.append(footer())
    return "".join(parts)


def page_podklyuchenie():
    url = "/podklyuchenie/"
    title = "Подключение v2RayTun — как настроить приложение"
    desc = ("Подключение v2RayTun занимает меньше минуты: активация профиля в боте, импорт в приложение, "
            "тап «Подключиться». Пошаговый разбор для всех платформ.")
    parts = [head(title, desc, url), nav(url)]
    parts.append(hero(
        tag="Настройка за минуту",
        title_pre="Подключение v2RayTun —",
        title_grad="за одну минуту",
        title_post="на любой системе",
        lead=("Подключение собирается из двух действий: активация профиля в Telegram-боте "
              "и нажатие одной кнопки в приложении. Ниже — пошаговая инструкция для всех платформ."),
        show_mockup=False,
    ))
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">За минуту</span>
      <h2>Как подключить v2RayTun — общая схема</h2>
    </div>
    <div class="steps">
      <div class="step"><h4>Активация</h4><p>Открываешь Telegram-бота, жмёшь «/start», выбираешь тариф (или пробу). Бот высылает ссылку-профиль формата <code>vless://...</code>.</p></div>
      <div class="step"><h4>Установка</h4><p>Если приложение ещё не стоит — скачиваешь v2RayTun под свою систему со страницы <a href="/skachat-v2raytun/">«Скачать»</a>.</p></div>
      <div class="step"><h4>Импорт</h4><p>Копируешь ссылку из бота в буфер. Открываешь v2RayTun → «+ Добавить» → «Из буфера». Профиль появляется в списке.</p></div>
      <div class="step"><h4>Подключение</h4><p>Тап по профилю — он становится активным. Большая круглая кнопка в центре — нажимаешь, через секунду индикатор зелёный.</p></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">По системам</span>
      <h2>Инструкция по настройке v2RayTun под каждую платформу</h2>
    </div>
    <div class="prose">
      <h3>Подключение v2RayTun на Windows и macOS</h3>
      <p>Запусти установщик, дай разрешение на изменения. Иконка v2RayTun появится в трее (Windows) или в строке меню (macOS). Кликни по иконке — откроется окно с профилями. В первый раз список пустой.</p>
      <p>Перейди в Telegram-бот, скопируй ссылку-профиль. Вернись в v2RayTun, нажми кнопку «+» в правом верхнем углу окна и выбери «Импорт из буфера». Профиль появится в списке. Кликни по нему — он станет активным. Большая круглая кнопка в центре переключает соединение.</p>
      <h3>Подключение v2RayTun на Android</h3>
      <p>Если ставил APK — открой скачанный файл и подтверди установку. После — открой приложение. При первом запуске оно попросит разрешение «Запросить VPN» — это нужно для туннеля, нажми «OK».</p>
      <p>В правом верхнем углу — иконка «+». Тап → «Добавить из буфера». Если ссылка уже скопирована из бота, она вставится. Профиль появится в списке. Тап по нему, потом по большой круглой кнопке снизу.</p>
      <h3>Подключение v2RayTun на iOS</h3>
      <p>Открой v2RayTun из App Store. При первом запуске разрешите профиль VPN в настройках iOS (всплывёт стандартный диалог, нажмите «Разрешить»).</p>
      <p>В правом нижнем углу приложения — иконка «+». Тап на неё → «Из буфера обмена». Если ссылка уже в буфере, она появится как новый профиль. Активируй его и нажми кнопку подключения.</p>
      <h3>Что делать, если что-то пошло не так</h3>
      <p>Если в приложении не вставляется ссылка из буфера — проверь, что ты её действительно скопировал (попробуй вставить в любое текстовое поле и убедись, что она там есть). Если не подключается — открой страницу <a href="/problemy/">«Проблемы»</a>, там разобраны типовые ошибки.</p>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">""")
    parts.append(faq_block([
      ("Как настроить v2RayTun за минуту?", "Активируй профиль в боте, скопируй полученную ссылку, открой v2RayTun, импортируй из буфера, нажми «Подключиться». Это всё."),
      ("Куда вводить ссылку-конфиг в v2RayTun?", "В приложении тап на «+» в углу → выбери «Из буфера обмена» или «Импорт». Поле для ручного ввода тоже есть, но проще через буфер."),
      ("Нужны ли права администратора для v2RayTun?", "На Windows — да, для установки. На Mac, Android и iOS — нет. На Mac, кстати, при первом запуске нужно дать разрешение в Настройках → Конфиденциальность."),
      ("Как обновить v2RayTun?", "На Android и iOS обновления идут через магазин. На ПК — приложение само сообщит о новой версии при запуске и предложит загрузить."),
      ("Где хранятся настройки v2RayTun?", "На Windows — в <code>%APPDATA%\\v2RayTun\\</code>, на Mac — в <code>~/Library/Application Support/v2RayTun/</code>, на Android — в данных приложения. Профили оттуда можно скопировать на другой компьютер."),
    ]))
    parts.append(cta_banner("Готов подключить v2RayTun за минуту?", "Активируй профиль в Telegram-боте и приложение поднимет соединение в один тап."))
    parts.append("</div></section>")
    parts.append(related_block(url))
    parts.append(footer())
    return "".join(parts)


def page_pk():
    url = "/pk/"
    title = "v2RayTun на ПК — установка для Windows 7, 10, 11"
    desc = ("v2RayTun скачать на ПК Windows: установщик x64 для Windows 10/11, версия для Windows 7, "
            "portable-сборка. Установка и настройка приложения для компьютера за минуту.")
    parts = [head(title, desc, url), nav(url)]
    parts.append(hero(
        tag="Windows · ПК · ноутбук",
        title_pre="v2RayTun на ПК —",
        title_grad="установщик",
        title_post="для Windows 7, 10 и 11",
        lead=("v2RayTun скачать на пк можно тремя способами: установщик x64, portable-сборка без инсталляции "
              "и отдельный пакет для Windows 7 с CPU без AVX-инструкций."),
        show_mockup=False,
    ))
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Варианты</span>
      <h2>Версии v2RayTun для Windows</h2>
    </div>
    <div class="grid-3">
      <div class="feat"><div class="feat-ico">⬇️</div><h3>Установщик x64</h3><p>Базовый вариант для Windows 10 и 11. Размер около 28 МБ. Ставится двойным кликом, иконка появляется в системном трее.</p></div>
      <div class="feat"><div class="feat-ico">📦</div><h3>Portable-версия</h3><p>ZIP-архив без установки: распаковал, запустил <code>v2raytun.exe</code>. Удобно, если на компьютере нет прав администратора.</p></div>
      <div class="feat"><div class="feat-ico">🛠️</div><h3>Сборка для Windows 7</h3><p>Отдельный установщик для Windows 7 и старых процессоров без AVX-инструкций. Чуть тяжелее (~32 МБ), но запускается на машинах 2010-2014 годов.</p></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Установка</span>
      <h2>Как поставить v2RayTun на Windows</h2>
    </div>
    <div class="prose">
      <h3>Стандартная установка (x64)</h3>
      <p>Запускаешь скачанный exe. Windows может предупредить «Издатель не проверен» — нажми «Подробнее» → «Выполнить в любом случае». В мастере установки достаточно нажимать «Далее» — нестандартных опций там нет.</p>
      <p>После установки приложение запускается автоматически. Иконка v2RayTun — фиолетовый ромб с буквой V — появляется в трее (рядом с часами). Кликни по ней, чтобы открыть основное окно с профилями.</p>
      <h3>Portable-вариант</h3>
      <p>Распакуй ZIP-архив в любую папку (Документы, рабочий стол, флешка). Запусти <code>v2raytun.exe</code> двойным кликом. Профили и настройки будут храниться в той же папке, рядом с экзешником.</p>
      <h3>Какие требования у v2RayTun на ПК</h3>
      <p>Минимум — Windows 7 SP1 с обновлениями, 2 ГБ оперативной памяти и 100 МБ свободного места на диске. Процессор — любой 64-битный (для x64-версии). На совсем старых машинах без AVX-инструкций нужна отдельная сборка — она тоже доступна на странице загрузки.</p>
      <h3>v2RayTun на ноутбуке</h3>
      <p>На ноутбуке всё работает идентично десктопу. Единственный нюанс — приложение поднимает VPN-туннель, и при подключении к новой сети (например, в кафе) рекомендуется отключать туннель и заново подключаться после авторизации в этой сети. Иначе captive portal не откроется.</p>
      <h3>v2RayTun Plus на пк</h3>
      <p>Подписка Plus работает на ПК так же, как на телефоне: импортируешь профиль из бота, активируешь его и подключаешься. Один профиль покрывает компьютер и до двух дополнительных устройств одновременно.</p>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">""")
    parts.append(faq_block([
      ("v2RayTun скачать на пк Windows — где найти?", "На странице <a href='/skachat-v2raytun/'>«Скачать»</a> есть три варианта: x64-установщик, portable, и сборка для Windows 7. Все ссылки ведут на актуальные релизы."),
      ("Какие требования у v2RayTun на пк?", "Минимум — Windows 7 SP1, 2 ГБ ОЗУ, 100 МБ места. Процессор — любой 64-битный. Для старых CPU без AVX есть отдельная сборка."),
      ("Как настроить v2RayTun на ПК?", "После установки — открой Telegram-бот, скопируй ссылку-профиль, открой v2RayTun, нажми «+» в углу → «Импорт из буфера». Профиль появится — тап по нему, потом по большой кнопке."),
      ("v2RayTun на ноутбуке тормозит — что делать?", "Чаще всего причина в фоновом антивирусе, который проверяет VPN-трафик. Добавь <code>v2raytun.exe</code> в исключения антивируса и сетевого экрана."),
      ("Есть ли v2RayTun Desktop сборка?", "Да, обычный установщик и portable — это и есть Desktop-варианты. Под Linux отдельной сборки пока нет, но работает через Wine/Bottles."),
      ("Можно ли поставить v2RayTun на Windows 7?", "Да, есть специальная сборка для Windows 7 и процессоров без AVX. Она чуть тяжелее, но запускается даже на 14-летнем железе."),
    ]))
    parts.append(cta_banner("Поставил v2RayTun на ПК?", "Активируй профиль в Telegram-боте — соединение поднимется за пару секунд после импорта."))
    parts.append("</div></section>")
    parts.append(related_block(url))
    parts.append(footer())
    return "".join(parts)


def page_android():
    url = "/android/"
    title = "v2RayTun на Android — APK и приложение для смартфона"
    desc = ("v2RayTun скачать на андроид: прямой APK с GitHub-релизов, версия из Google Play. "
            "Установка и настройка приложения на телефон и планшет Android 7+.")
    parts = [head(title, desc, url), nav(url)]
    parts.append(hero(
        tag="Android · APK · Google Play",
        title_pre="v2RayTun на андроид —",
        title_grad="APK и сборка",
        title_post="из Google Play",
        lead=("v2RayTun скачать на андроид можно прямой ссылкой на APK (свежее обновляется) или из Google Play. "
              "Совместимо со всеми смартфонами и планшетами на Android 7.0 и выше."),
        show_mockup=False,
    ))
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Варианты загрузки</span>
      <h2>Где скачать v2RayTun на Android</h2>
    </div>
    <div class="grid-3">
      <div class="feat"><div class="feat-ico">📲</div><h3>Прямой APK</h3><p>Самый свежий вариант. Обновления туда попадают раньше Google Play. Размер примерно 18 МБ, ставится через «Установить из неизвестных источников».</p></div>
      <div class="feat"><div class="feat-ico">🛒</div><h3>Google Play</h3><p>Стандартная установка — кнопка «Загрузить» в магазине. Автообновления, но релизы туда иногда отстают на несколько дней.</p></div>
      <div class="feat"><div class="feat-ico">📺</div><h3>Android TV</h3><p>Отдельная сборка для телевизоров и приставок с интерфейсом под пульт. Подробнее на <a href="/tv/">странице TV</a>.</p></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Установка</span>
      <h2>Как установить v2RayTun на андроид</h2>
    </div>
    <div class="prose">
      <h3>Скачать v2RayTun APK</h3>
      <p>Открой ссылку на APK в браузере телефона. Файл начнёт загружаться — после окончания, нажми на уведомление загрузки или открой папку «Загрузки» в файловом менеджере.</p>
      <p>При первой установке APK Android спросит разрешение «Установка из неизвестных источников» для приложения, из которого ты открыл файл (обычно — браузер или менеджер файлов). Дай разрешение, потом нажми «Установить».</p>
      <h3>Через Google Play</h3>
      <p>Если предпочитаешь магазин — найди «v2RayTun» в Play и нажми «Установить». В Play иногда лежит чуть устаревшая версия — если на телефоне начнутся проблемы с подключением, попробуй обновиться через APK.</p>
      <h3>Настройка v2RayTun на Android</h3>
      <p>При первом запуске приложение попросит «Разрешить VPN-конфигурацию» — это нужно для туннеля, нажми «OK». Дальше — открой Telegram-бота, скопируй ссылку-профиль, вернись в v2RayTun, тап «+ Добавить» → «Из буфера». Профиль появится в списке.</p>
      <p>Тап по профилю — он станет активным. Большая круглая кнопка снизу — нажимаешь, индикатор становится зелёным. Подключение готово.</p>
      <h3>v2RayTun на планшете</h3>
      <p>Интерфейс автоматически масштабируется под планшет — никаких отдельных действий не нужно. Работает на любом Android-планшете с системой 7.0 и новее.</p>
      <h3>Сколько батареи тратит v2RayTun APK</h3>
      <p>В состоянии подключения — примерно 2-4% батареи в час фоновой работы. Это сопоставимо с обычным мессенджером. Если приложение спрашивает разрешение на «Игнорирование оптимизации батареи» — соглашайся, иначе Android может убивать соединение в фоне.</p>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">""")
    parts.append(faq_block([
      ("Скачать v2RayTun apk — это безопасно?", "Да, если брать APK из официального GitHub-репозитория разработчика. Сторонние «зеркала» могут содержать модификации — не пользуйся."),
      ("Какая версия Android нужна для v2RayTun?", "Минимум 7.0 (Nougat). На более старых системах могут быть проблемы с VPN-туннелем."),
      ("v2RayTun не запускается на Android — что делать?", "Чаще всего помогает переустановка с очисткой данных. Если не помогает — отключи в системе MIUI/HyperOS/EMUI «оптимизацию» v2RayTun или добавь его в исключения."),
      ("Скачать v2RayTun apk для Android TV — отдельно?", "Да, у TV-сборки другой интерфейс — под пульт без жестов. <a href='/tv/'>Подробнее на странице TV</a>."),
      ("v2RayTun для смартфона тратит много батареи?", "В подключённом состоянии — 2-4% в час фоновой работы. Это нормально для VPN-клиента."),
    ]))
    parts.append(cta_banner("Скачал v2RayTun на Android?", "Открой Telegram-бот, активируй профиль — соединение появится в приложении за пару секунд."))
    parts.append("</div></section>")
    parts.append(related_block(url))
    parts.append(footer())
    return "".join(parts)


def page_ios():
    url = "/ios/"
    title = "v2RayTun на iPhone — приложение для iOS из App Store"
    desc = ("v2RayTun на iPhone и iPad: установка из App Store, настройка и подключение приложения. "
            "Совместимо с iOS 14.0 и новее, бесплатное приложение, оплачивается только подписка.")
    parts = [head(title, desc, url), nav(url)]
    parts.append(hero(
        tag="iOS · App Store · iPhone и iPad",
        title_pre="v2RayTun на iPhone —",
        title_grad="из App Store",
        title_post="для iOS 14+",
        lead=("v2RayTun на айфон ставится из App Store бесплатно. Приложение совместимо со всеми "
              "iPhone начиная с 6s и iPad начиная с 7-го поколения, требуется iOS 14.0 или новее."),
        show_mockup=False,
    ))
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Варианты установки</span>
      <h2>Как скачать v2RayTun на iPhone</h2>
    </div>
    <div class="grid-3">
      <div class="feat"><div class="feat-ico">📱</div><h3>iPhone</h3><p>Поддерживаются все iPhone начиная с 6s, требуется iOS 14.0 или новее. Установка стандартная — кнопка «Загрузить» в App Store.</p></div>
      <div class="feat"><div class="feat-ico">📱</div><h3>iPad</h3><p>Интерфейс адаптируется под планшетный размер. Поддержка iPad начиная с 7-го поколения и iPad mini 5.</p></div>
      <div class="feat"><div class="feat-ico">🛒</div><h3>App Store</h3><p>Единственный официальный источник — других каналов установки на iOS нет. Найди приложение по запросу <i>v2RayTun</i>.</p></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Установка</span>
      <h2>Установка v2RayTun на айфон и iPad</h2>
    </div>
    <div class="prose">
      <h3>Скачать v2RayTun на iPhone из App Store</h3>
      <p>Открой App Store на телефоне и найди приложение по запросу «v2RayTun». Нужное приложение — иконка-ромб фиолетового цвета. Нажми «Загрузить» (или иконку загрузки), подтверди установку через Face ID или Touch ID.</p>
      <p>После загрузки приложение появится на домашнем экране. При первом запуске v2RayTun попросит «Разрешить VPN-конфигурацию» — это стандартный диалог iOS, нажми «Разрешить».</p>
      <h3>Как настроить v2RayTun на iPhone</h3>
      <p>Открой Telegram-бот, нажми «Получить в Телеграм» в шапке этого сайта или зайди напрямую. Бот пришлёт ссылку-профиль. Скопируй её — она автоматически попадёт в буфер обмена.</p>
      <p>Открой v2RayTun, нажми иконку «+» в правом нижнем углу → «Из буфера обмена». Профиль автоматически добавится в список. Тапни по нему, чтобы он стал активным, и нажми большую круглую кнопку — пойдёт подключение.</p>
      <h3>v2RayTun на айфон бесплатно — что это значит</h3>
      <p>Само приложение бесплатное — за загрузку из App Store ничего платить не нужно. Платная только подписка-профиль, через который идёт трафик. Минимальный тариф — 249 ₽/мес.</p>
      <h3>v2RayTun на iPad</h3>
      <p>На iPad v2RayTun работает так же, как на iPhone — но с увеличенным интерфейсом. Поддерживаются все iPad с iOS 14+. На iPad с M1/M2 (которые могут запускать iPhone-приложения через эмуляцию) — v2RayTun работает нативно как iPad-приложение, с правильной адаптацией под большой экран.</p>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">""")
    parts.append(faq_block([
      ("Скачать v2RayTun на iPhone бесплатно — точно бесплатно?", "Да, само приложение в App Store бесплатное. Оплачивается только подписка-профиль, через который идёт трафик."),
      ("Есть ли v2RayTun для iPhone в формате IPA?", "Нет, на iOS приложения ставятся только через App Store. Сборка устанавливается стандартным способом — через кнопку «Загрузить»."),
      ("Работает ли v2RayTun на iPad?", "Да, поддерживаются все iPad с iOS 14+. Интерфейс адаптируется под планшетный размер автоматически."),
      ("Как настроить v2RayTun на iPhone, если приложение не видит профиль?", "Проверь, что ссылка-профиль действительно в буфере обмена. Попробуй вставить её в Заметки — если там пусто, скопируй ещё раз из бота."),
      ("Можно ли использовать v2RayTun на Apple Watch?", "Нет, отдельной watch-сборки нет. Но трафик с часов, идущий через подключённый iPhone, будет защищён, если на iPhone активен v2RayTun."),
    ]))
    parts.append(cta_banner("Поставил v2RayTun на iPhone?", "Активируй профиль в Telegram-боте и приложение поднимет подключение в один тап."))
    parts.append("</div></section>")
    parts.append(related_block(url))
    parts.append(footer())
    return "".join(parts)


def page_tv():
    url = "/tv/"
    title = "v2RayTun на Android TV — сборка для приставок и смарт-телевизоров"
    desc = ("v2RayTun на TV: отдельная сборка для Android TV-приставок и смарт-телевизоров с интерфейсом под пульт. "
            "Установка APK через ADB, настройка профиля через QR-код.")
    parts = [head(title, desc, url), nav(url)]
    parts.append(hero(
        tag="Android TV · приставки · смарт-ТВ",
        title_pre="v2RayTun на TV —",
        title_grad="отдельная сборка",
        title_post="для Android TV и приставок",
        lead=("На приставках и смарт-телевизорах работает отдельная версия v2RayTun — с интерфейсом под пульт, "
              "без жестов. Поддерживается Android TV 9.0 и новее, включая Xiaomi Mi Box, Nvidia Shield и Chromecast with Google TV."),
        show_mockup=False,
    ))
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Установка</span>
      <h2>Как поставить v2RayTun на Android TV</h2>
    </div>
    <div class="prose">
      <h3>Через файловый менеджер на ТВ</h3>
      <p>На приставке поставь любой Android-файловый менеджер из Play Store на ТВ — подходит «X-plore» или «File Commander». Скачай APK v2RayTun с этого сайта прямо в браузере приставки или перекинь через USB-флешку. Открой файл в файловом менеджере — установка пойдёт стандартным образом.</p>
      <p>Если ТВ отказывается ставить APK — зайди в Настройки → Приложения → Безопасность и включи «Установка из неизвестных источников» для файлового менеджера.</p>
      <h3>Через ADB с компьютера</h3>
      <p>Если на твоей приставке нет браузера или файлового менеджера — установка через ADB. Включи на ТВ режим разработчика (Настройки → О телевизоре → Сборка, нажми 7 раз). Затем в Настройках → Параметры разработчика включи «Отладка по ADB».</p>
      <p>На компьютере с установленным ADB выполни <code>adb connect IP_приставки:5555</code>, потом <code>adb install v2raytun.apk</code>. Через минуту приложение появится в списке установленных.</p>
      <h3>Импорт профиля через QR-код</h3>
      <p>На ТВ нет привычного буфера обмена и неудобно вводить длинные ссылки пультом — поэтому профиль лучше импортировать через QR-код. В Telegram-боте есть команда «Профиль в QR» — она генерит картинку. На ТВ открой v2RayTun, тап «+ Добавить» → «Сканировать QR» и наведи камеру (или используй веб-камеру приставки, если есть).</p>
      <p>Если камеры нет — можно ввести ссылку вручную пультом через экранную клавиатуру. Долго, но работает.</p>
      <h3>Как пользоваться приложением на ТВ</h3>
      <p>Интерфейс TV-сборки упрощён под пульт. Навигация — стрелки и кнопка «OK», без жестов. В центре экрана — большая кнопка подключения, она же — точка фокуса по умолчанию. Сверху — выбор сервера.</p>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">""")
    parts.append(faq_block([
      ("v2RayTun на TV скачать — есть отдельная сборка?", "Да, для Android TV есть отдельный APK с интерфейсом под пульт. Обычная Android-сборка тоже запустится на приставке, но навигация будет неудобной."),
      ("Что нужно для v2RayTun на TV?", "Android TV 9.0 или новее, около 30 МБ свободного места. Подойдут Xiaomi Mi Box, Nvidia Shield, Chromecast with Google TV, а также Android-приставки от Beeline и других провайдеров."),
      ("Можно ли поставить v2RayTun на Smart TV (не Android)?", "Только если у телевизора Android TV. На WebOS (LG), Tizen (Samsung) и других системах v2RayTun не работает — но можно подключить Android-приставку к HDMI и поставить туда."),
      ("Как подключить v2RayTun к Apple TV?", "На Apple TV (tvOS) нет приложения v2RayTun — Apple не разрешает VPN-приложения в tvOS App Store. Альтернатива — настроить VPN на роутере, и весь трафик ТВ пойдёт через туннель."),
      ("Будет ли v2RayTun работать на дешёвой приставке за 1000 рублей?", "Зависит от прошивки. Если на приставке стоит чистый Android TV — да. Если кастомная прошивка типа Tanix или Tanix-X — могут быть проблемы с правами на запуск VPN."),
    ]))
    parts.append(cta_banner("Готов смотреть YouTube без замираний?", "Активируй профиль в Telegram-боте и v2RayTun на приставке поднимет туннель за секунды."))
    parts.append("</div></section>")
    parts.append(related_block(url))
    parts.append(footer())
    return "".join(parts)


def page_problemy():
    url = "/problemy/"
    title = "v2RayTun не работает — разбор типовых проблем и решений"
    desc = ("v2RayTun не работает: типовые причины и решения. Что делать, если приложение не подключается, "
            "соединение рвётся, пинг высокий или TLS-рукопожатие падает с ошибкой.")
    parts = [head(title, desc, url), nav(url)]
    parts.append(hero(
        tag="Диагностика · починка",
        title_pre="v2RayTun не работает?",
        title_grad="Разбор",
        title_post="типовых проблем",
        lead=("Если приложение перестало подключаться или соединение рвётся — ниже разобраны самые частые причины. "
              "В большинстве случаев починка укладывается в две-три минуты."),
        show_mockup=False,
    ))
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Чек-лист</span>
      <h2>Что чаще всего ломается</h2>
    </div>
    <div class="grid-2">
      <div class="feat"><div class="feat-ico">🔄</div><h3>Ошибка TLS-рукопожатия</h3><p>Профиль устарел или сервер на проф-обслуживании. В боте нажми «Обновить профиль» — придёт новая ссылка, в приложении замени старую.</p></div>
      <div class="feat"><div class="feat-ico">⏱️</div><h3>Тайм-аут подключения</h3><p>Сеть оператора режет VLESS-трафик. Помогает смена fingerprint (новый профиль из бота автоматически берёт другой fingerprint), либо смена сервера на менее «горячий».</p></div>
      <div class="feat"><div class="feat-ico">🚫</div><h3>Не подключается совсем</h3><p>Проверь, что в системных настройках VPN-конфигурация v2RayTun существует и активна. На iOS зайди в Настройки → VPN → v2RayTun и убедись, что он включён.</p></div>
      <div class="feat"><div class="feat-ico">🐌</div><h3>Высокий пинг</h3><p>Скорее всего, ты на дальнем сервере. Открой v2RayTun, выбери ближайший географически (Финляндия и Польша — для запада России, Германия — универсально).</p></div>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Разбор</span>
      <h2>Если v2RayTun не работает — подробно</h2>
    </div>
    <div class="prose">
      <h3>v2RayTun не подключается — почему</h3>
      <p>Самая частая причина — устаревший или просроченный профиль. В боте нажми «Мои подписки» → «Обновить профиль». Тебе пришлют свежую ссылку — скопируй её и замени старую в приложении (Долгий тап на старом профиле → «Удалить», потом обычным образом добавь новый из буфера).</p>
      <p>Вторая причина — оператор режет конкретный fingerprint TLS-рукопожатия. Это решается тоже сменой профиля: в новом будет другой fingerprint, который этот оператор пропустит.</p>
      <h3>v2RayTun ошибка ядра (xray)</h3>
      <p>Внутри v2RayTun используется ядро Xray для обработки VLESS-протокола. Иногда оно падает после обновления приложения, если профиль остался от старой версии. Решение: удалить профиль, добавить заново из бота. В 95% случаев помогает.</p>
      <h3>v2RayTun ошибка загрузки гео-файлов</h3>
      <p>Geo-файлы — это списки доменов, которые v2RayTun маршрутизирует напрямую (без VPN-туннеля). Файлы скачиваются с GitHub. Если у тебя в сети заблокирован GitHub — гео-файлы не подтянутся.</p>
      <p>Решение: открой настройки v2RayTun → «Гео-файлы» → выбери альтернативный источник (там есть зеркала Gitee и Gitea). После смены источника перезапусти приложение.</p>
      <h3>Пинг в v2RayTun высокий — что делать</h3>
      <p>Зайди в список серверов и проверь пинг до каждого. Открой настройки маршрутизации и убедись, что включено «Тестировать пинг при подключении» — тогда v2RayTun автоматически выберет самый быстрый сервер. Финляндия обычно дает 15-25 мс для северо-запада, Германия — 25-40 мс, Польша — 18-30 мс.</p>
      <h3>v2RayTun обход белых списков — не получается</h3>
      <p>В корпоративных сетях с белыми списками иногда не пропускают даже VLESS Reality. Проверь в боте раздел «Серверы для строгих сетей» — там есть отдельные конфигурации специально под такие ограничения, использующие другие порты и SNI.</p>
    </div>
  </div>
</section>""")
    parts.append("""<section class="section">
  <div class="wrap">""")
    parts.append(faq_block([
      ("Что делать, если v2RayTun не работает совсем?", "Сначала переустанови приложение и заново импортируй профиль из бота. Если не помогло — напиши в чат бота «Не работает», там разберутся в течение нескольких минут."),
      ("v2RayTun глушилки — как обойти?", "В строгих сетях помогают альтернативные конфиги «для жёстких сетей» — они есть в боте отдельным разделом. Используют нестандартные порты и SNI крупных сайтов."),
      ("Если сервер v2RayTun не работает — что делать?", "Переключись на другой в приложении. Если все недоступны — напиши в бота «Серверы упали», обычно проблема решается в течение 15 минут."),
      ("v2RayTun не запускается после обновления Android — что делать?", "Очисти кэш приложения (Настройки → Приложения → v2RayTun → Очистить кэш), потом перезапусти. Если не помогло — переустанови."),
      ("Можно ли использовать v2RayTun без подписки?", "Без активного профиля приложение не подключится. Но есть пробный период 3 дня — этого хватит, чтобы протестировать."),
    ]))
    parts.append(cta_banner("Не получается разобраться?", "Активируй профиль в Telegram-боте — в чате поддержки помогут с конкретной проблемой за минуты."))
    parts.append("</div></section>")
    parts.append(related_block(url))
    parts.append(footer())
    return "".join(parts)


def page_faq():
    url = "/faq/"
    title = "FAQ v2RayTun — частые вопросы о приложении и подписке"
    desc = ("FAQ v2RayTun: что такое приложение, как настроить, как оплатить подписку, что делать при ошибках. "
            "Короткие ответы на типовые вопросы по приложению, ключам, серверам.")
    parts = [head(title, desc, url), nav(url)]
    parts.append(hero(
        tag="FAQ · справка · справочник",
        title_pre="FAQ v2RayTun —",
        title_grad="частые вопросы",
        title_post="о приложении",
        lead=("Короткие ответы по приложению, подписке, ключам, серверам и оплате. "
              "Если конкретный вопрос не нашёлся — пиши в чат Telegram-бота, там отвечают живые сотрудники."),
        show_mockup=False,
    ))
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Об установке</span>
      <h2>Скачивание и установка</h2>
    </div>""")
    parts.append(faq_block([
      ("Где скачать v2RayTun официально?", "Прямые ссылки на этом сайте — на странице <a href='/skachat-v2raytun/'>«Скачать»</a>. Для Android — APK с GitHub-релизов, для iPhone — App Store, для ПК — установщик с GitHub."),
      ("Какая последняя версия v2RayTun?", "Обновления выходят 1-2 раза в месяц. Версия и дата указаны рядом с каждой ссылкой на странице загрузки."),
      ("Можно ли скачать v2RayTun с GitHub?", "Да, GitHub — официальный канал. APK с GitHub-релизов обновляется быстрее, чем версия в Play Store."),
      ("Безопасно ли скачивание v2RayTun?", "Если брать с этого сайта или официальных магазинов — да. Сторонние «зеркала» и моды лучше не использовать."),
      ("Как установить v2RayTun на старый Android?", "Минимальная версия — Android 7.0. На старых системах подключение по VLESS может работать нестабильно."),
    ]))
    parts.append("</div></section>")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">О подписке</span>
      <h2>Подписка и оплата</h2>
    </div>""")
    parts.append(faq_block([
      ("Сколько стоит v2RayTun?", "Само приложение — бесплатно. Подписка Plus — от 249 ₽ за месяц. На годовом тарифе цена снижается до 158 ₽/месяц в эквиваленте."),
      ("Есть ли v2RayTun бесплатно?", "Бесплатной версии подписки нет, но есть пробный период 3 дня. Можно протестировать перед оплатой."),
      ("Что такое v2RayTun Pro?", "Pro — старое название тарифа. Сейчас он называется Plus, функции те же."),
      ("Что такое пробный период v2RayTun?", "Три дня бесплатного тестирования с полным функционалом. После окончания профиль превращается в обычный платный, если оплачен."),
      ("Как продлить подписку v2RayTun?", "В Telegram-боте — «Мои подписки» → «Продлить». Можно настроить автопродление, тогда списания идут автоматически."),
      ("Как вернуть деньги за v2RayTun?", "Напиши в бота «Возврат» в течение 7 дней (14 для годового тарифа). Деньги вернутся в течение 3 рабочих дней."),
      ("Как оплатить v2RayTun?", "Российская карта, СБП по QR-коду или USDT в крипте. Способ выбираешь в боте перед оплатой."),
    ]))
    parts.append("</div></section>")
    parts.append("""<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">О серверах</span>
      <h2>Серверы и подключение</h2>
    </div>""")
    parts.append(faq_block([
      ("Сколько серверов в v2RayTun?", "Сейчас доступно 6 локаций: Нидерланды, Германия, Финляндия, Польша, Франция и США."),
      ("Как выбрать сервер v2RayTun?", "Самый близкий географически даст самый низкий пинг. Финляндия — для северо-запада, Германия — универсально, Польша — для запада."),
      ("Можно ли переключаться между серверами v2RayTun?", "Да, переключение в приложении — один тап. Без дополнительной подписки."),
      ("Какие протоколы поддерживает v2RayTun?", "v2RayTun работает с VLESS Reality, XRay, VMess и Trojan. Мы используем именно VLESS Reality за устойчивость к фильтрации, но клиент понимает и остальные форматы ссылок-подписок."),
      ("Что такое VLESS Reality?", "Современный протокол маскировки трафика, при котором соединение выглядит как обычное TLS-рукопожатие с крупным сайтом."),
    ]))
    parts.append("</div></section>")
    parts.append("""<section class="section">
  <div class="wrap">""")
    parts.append(cta_banner("Не нашёл ответа?", "Напиши в чат Telegram-бота — там отвечают живые сотрудники, не FAQ-бот."))
    parts.append("</div></section>")
    parts.append(related_block(url))
    parts.append(footer("belorussky", "916"))
    return "".join(parts)


# build
PAGES = [
    ("/", page_home),
    ("/skachat-v2raytun/", page_skachat),
    ("/podpiska/", page_podpiska),
    ("/konfigi/", page_konfigi),
    ("/podklyuchenie/", page_podklyuchenie),
    ("/pk/", page_pk),
    ("/android/", page_android),
    ("/ios/", page_ios),
    ("/tv/", page_tv),
    ("/problemy/", page_problemy),
    ("/faq/", page_faq),
]


def build():
    # clear dist
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST / "assets").mkdir()
    shutil.copy(ROOT / "styles.css", DIST / "assets" / "styles.css")

    # favicon
    favicon = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6366f1"/><stop offset="1" stop-color="#7c3aed"/></linearGradient></defs><rect width="64" height="64" rx="14" fill="url(#g)"/><text x="32" y="42" text-anchor="middle" font-family="Sora,Inter,system-ui" font-size="26" font-weight="700" fill="#0a0b14">V</text></svg>'''
    (DIST / "favicon.svg").write_text(favicon, encoding="utf-8")

    # robots.txt
    robots = f"User-agent: *\nAllow: /\n\nSitemap: https://{DOMAIN}/sitemap.xml\n"
    (DIST / "robots.txt").write_text(robots, encoding="utf-8")

    # sitemap.xml
    sm = ['<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, _ in PAGES:
        sm.append(f"<url><loc>https://{DOMAIN}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>{'1.0' if u == '/' else '0.8'}</priority></url>")
    sm.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")

    # pages
    for u, fn in PAGES:
        path = (DIST / u.strip("/") / "index.html") if u != "/" else (DIST / "index.html")
        path.parent.mkdir(parents=True, exist_ok=True)
        html_text = fn()
        path.write_text(html_text, encoding="utf-8")
        print(f"  → {u}  ({len(html_text)} bytes)")
    print(f"Built {len(PAGES)} pages into {DIST}")


if __name__ == "__main__":
    build()
