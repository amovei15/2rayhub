#!/usr/bin/env python3
# 2rayhub.com — статический генератор. Дизайн: charcoal + amber/gold, "key-vault".
import json, os, re, html, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
DOMAIN = "2rayhub.com"
BASE = f"https://{DOMAIN}"
NOINDEX = False                     # апрув получен — индексируем
LK = "https://lk.chekdns.click/?utm_source=2rayhub"
TG = "https://t.me/tgbpn_bot?start=utm_v2ray2tuncom"
INDEXNOW_KEY = "8b3d1f6a9c2e47d05a8f1b6c3e9d2a74"
METRIKA_ID = ""
YA_VERIFY = "3faddb3cefb5ec4f"
CSSV = "5"

KW = json.load(open(os.path.join(ROOT, "keywords.json"), encoding="utf-8"))
TOP = KW["hero"]
BYC = KW["clusters"]
TOTAL_KW = KW.get("total", sum(len(v) for v in BYC.values()))

def kws(cluster, n=40):
    items = BYC.get(cluster, [])
    return [i["q"] for i in items[:n]]

NAV = [
    ("Ключи", "/klyuchi/"), ("Скачать", "/skachat/"), ("ПК", "/na-pk/"),
    ("Android", "/android/"), ("iPhone", "/ios/"), ("Конфиги", "/konfig/"),
    ("Тарифы", "/tarify/"), ("Блог", "/blog/"), ("Вопросы", "/voprosy/"),
]
FOOT = [
    ("Платформы", [("Скачать", "/skachat/"), ("На ПК / Windows", "/na-pk/"),
        ("Android / APK", "/android/"), ("iPhone / iOS", "/ios/"), ("Mac", "/mac/"), ("Smart TV", "/tv/")]),
    ("Ключи", [("Ключи v2raytun", "/klyuchi/"), ("Бесплатно", "/besplatno/"),
        ("Конфигурации", "/konfig/"), ("Подписка", "/podpiska/"), ("Прокси", "/proxy/")]),
    ("Помощь", [("Настройка", "/nastrojka/"), ("Не работает", "/oshibki/"),
        ("GitHub", "/github/"), ("Блог", "/blog/"), ("Все запросы", "/zaprosy/")]),
]

def esc(s): return html.escape(s, quote=True)

def head(title, desc, path, og_type="website"):
    robots = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else '<meta name="robots" content="index,follow">'
    ya = f'\n<meta name="yandex-verification" content="{YA_VERIFY}">' if YA_VERIFY else ""
    metr = ""
    if METRIKA_ID:
        metr = f"""<script>(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return}}}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})(window,document,"script","https://mc.yandex.ru/metrika/tag.js","ym");ym({METRIKA_ID},"init",{{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true}});</script>"""
    canon = BASE + path
    og = f"""<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="v2ray2tun">
<meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}/og.png">"""
    return f"""<!doctype html><html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
{robots}{ya}
<link rel="canonical" href="{canon}">
{og}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.svg?v={CSSV}" type="image/svg+xml">
<link rel="stylesheet" href="/assets/app.css?v={CSSV}">{metr}
</head><body>"""

def header():
    nav = "".join(f'<a href="{u}">{esc(t)}</a>' for t, u in NAV)
    return f"""<header class="vk-hdr"><div class="vk-wrap vk-hdr-in">
<a class="vk-logo" href="/"><span class="vk-logo-mk">v2</span>raytun<span class="vk-logo-dot">·keys</span></a>
<nav class="vk-nav">{nav}</nav>
<a class="vk-btn vk-btn-sm" href="{LK}">Получить ключ</a>
<button class="vk-burger" aria-label="Меню" onclick="document.body.classList.toggle('vk-open')"><span></span><span></span><span></span></button>
</div><div class="vk-mnav">{nav}</div></header>"""

def cta(big=False):
    cls = " vk-cta-big" if big else ""
    return f"""<div class="vk-cta{cls}">
<a class="vk-btn" href="{LK}">🔑 Получить ключ на email</a>
<a class="vk-btn vk-btn-tg" href="{TG}">✈ Получить ключ в Telegram</a></div>"""

def chips(cluster, n=40, title="Популярные запросы"):
    ws = kws(cluster, n)
    if not ws: return ""
    items = "".join(f'<li>{esc(w)}</li>' for w in ws)
    return f'<section class="vk-chips"><h2>{esc(title)}</h2><ul class="vk-chip-list">{items}</ul></section>'

def faq(items):
    rows = ""
    for q, a in items:
        rows += f'<details class="vk-faq-i"><summary>{esc(q)}</summary><div>{a}</div></details>'
    import json as _j
    ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in items]}
    return f'<section class="vk-faq"><h2>Частые вопросы</h2>{rows}</section><script type="application/ld+json">{_j.dumps(ld,ensure_ascii=False)}</script>'

def footer():
    cols = ""
    for title, links in FOOT:
        ls = "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for t, u in links)
        cols += f'<div class="vk-fcol"><h4>{esc(title)}</h4><ul>{ls}</ul></div>'
    return f"""<footer class="vk-ftr"><div class="vk-wrap">
<div class="vk-fgrid">
<div class="vk-fbrand"><a class="vk-logo" href="/"><span class="vk-logo-mk">v2</span>raytun<span class="vk-logo-dot">·keys</span></a>
<p>Ключи и конфигурации v2raytun для всех устройств. Быстрый доступ по email или в Telegram.</p>
{cta()}</div>{cols}</div>
<div class="vk-fbot"><span>© 2026 2rayhub.com</span><span>v2raytun · ключи · конфиги · подписка</span></div>
</div></footer></body></html>"""

def bc_ld(pairs):
    import json as _j
    ld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(pairs)]}
    return f'<script type="application/ld+json">{_j.dumps(ld,ensure_ascii=False)}</script>'

def site_ld():
    import json as _j
    org = {"@context":"https://schema.org","@type":"Organization","name":"v2ray2tun",
           "url":BASE+"/","logo":BASE+"/og.png","description":"Ключи и конфигурации v2raytun для всех устройств."}
    web = {"@context":"https://schema.org","@type":"WebSite","name":"v2ray2tun","url":BASE+"/","inLanguage":"ru"}
    return (f'<script type="application/ld+json">{_j.dumps(org,ensure_ascii=False)}</script>'
            f'<script type="application/ld+json">{_j.dumps(web,ensure_ascii=False)}</script>')

def hero():
    key = "vless://2b9f4c1a-7e3d-48a6-b1c2-9f8e7d6c5b4a@de1.2rayhub.com:443?security=reality&sni=cloudflare.com&type=tcp#v2raytun-key"
    tops = " · ".join([t["q"] for t in TOP[:6]])
    return f"""<section class="vk-hero"><div class="vk-wrap vk-hero-in">
<div class="vk-hero-l">
<span class="vk-tag">Ключи v2raytun · VLESS Reality</span>
<h1>Ключи v2raytun — рабочие конфиги для всех устройств</h1>
<p class="vk-lead">Получи готовый ключ v2raytun за минуту: вставил конфигурацию в приложение — и подключение работает. ПК, Android, iPhone, Mac и TV. Бесплатный пробный ключ и подписка без ограничений скорости.</p>
{cta(big=True)}
<div class="vk-trust"><span>⚡ Выдача за 1 минуту</span><span>🛡 VLESS Reality</span><span>♾ Без лимита скорости</span></div>
</div>
<div class="vk-hero-r">
<div class="vk-keycard">
<div class="vk-keycard-top"><span class="vk-dot"></span> ключ активен <span class="vk-kc-badge">Reality</span></div>
<div class="vk-keystr"><code>{esc(key)}</code></div>
<div class="vk-keycard-bot"><span>скопируй и вставь в v2raytun</span><span class="vk-kc-copy">Скопировать</span></div>
</div>
<div class="vk-hero-tags">{esc(tops)}</div>
</div>
</div></section>"""

def stat():
    cells = [("422k","ищут v2raytun в месяц"),("1 мин","выдача ключа"),("5","платформ"),("0 ₽","пробный ключ")]
    c = "".join(f'<div class="vk-stat-i"><b>{a}</b><span>{esc(b)}</span></div>' for a,b in cells)
    return f'<section class="vk-stat"><div class="vk-wrap vk-stat-in">{c}</div></section>'

def bento():
    cards = [
        ("🔑","Готовые ключи","Конфигурация v2raytun выдаётся сразу — ничего настраивать вручную не нужно."),
        ("🚀","VLESS Reality","Современный протокол: стабильное соединение и высокая скорость без обрывов."),
        ("📱","Все устройства","Один ключ работает на ПК, Android, iPhone, Mac и Smart TV одновременно."),
        ("🆓","Бесплатный старт","Пробный ключ v2raytun бесплатно — проверь скорость до оплаты подписки."),
        ("♾","Без лимитов","Полная скорость и безлимитный трафик на платной подписке."),
        ("🔄","Автообновление","Подписка обновляет серверы автоматически — ключ всегда рабочий."),
    ]
    c = "".join(f'<div class="vk-bento-i"><span class="vk-bi-ic">{ic}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for ic,t,d in cards)
    return f'<section class="vk-sec"><div class="vk-wrap"><h2 class="vk-h2">Почему ключи v2raytun отсюда</h2><div class="vk-bento">{c}</div></div></section>'

def platforms():
    items = [("Скачать","/skachat/","💾"),("ПК / Windows","/na-pk/","🖥"),("Android / APK","/android/","🤖"),
             ("iPhone / iOS","/ios/","📱"),("Mac","/mac/","🍎"),("Smart TV","/tv/","📺")]
    c = "".join(f'<a class="vk-plat-i" href="{u}"><span>{ic}</span><b>{esc(t)}</b></a>' for t,u,ic in items)
    return f'<section class="vk-sec"><div class="vk-wrap"><h2 class="vk-h2">v2raytun на твоё устройство</h2><div class="vk-plat">{c}</div></div></section>'

DL = {"ios":"https://apps.apple.com/app/v2raytun/id6476628951",
      "android":"https://play.google.com/store/apps/details?id=com.v2raytun.android",
      "github":"https://github.com/DigneZzZ/v2raytun/releases"}
def downloads(title="Скачать приложение v2raytun", note=True):
    btns = [("📱","App Store","iPhone и iPad",DL["ios"]),
            ("🤖","Google Play","Android",DL["android"]),
            ("💻","GitHub Releases","Windows, Mac, Linux, APK",DL["github"])]
    c = "".join(f'<a class="vk-dl-i" href="{u}" target="_blank" rel="nofollow noopener"><span class="vk-dl-ic">{ic}</span><b>{esc(t)}</b><small>{esc(s)}</small></a>' for ic,t,s,u in btns)
    n = '<p class="vk-sub">Скачай официальное приложение под свою систему, затем нажми «Получить ключ» — конфигурация придёт за минуту.</p>' if note else ''
    return f'<section class="vk-sec" id="download"><div class="vk-wrap"><h2 class="vk-h2">{esc(title)}</h2>{n}<div class="vk-dl">{c}</div></div></section>'

PLAN_FEATS = ["1 профиль на 3 устройства","6 локаций · Европа и США","Без лимита на трафик","Замена сервера бесплатно"]
PLANS = [("На месяц","249 ₽","Стартовый","Базовая цена",PLAN_FEATS,False),
         ("На 3 месяца","599 ₽","Выгодный старт","Экономия 20%",PLAN_FEATS,False),
         ("На полгода","1090 ₽","Оптимальный","Экономия 27%",PLAN_FEATS,True),
         ("Год","1890 ₽","Максимум выгоды","Экономия 37%",PLAN_FEATS,False)]
def tariffs():
    c=""
    for name,price,tier,econ,feats,hit in PLANS:
        fl="".join(f'<li>{esc(f)}</li>' for f in feats)
        badge="<span class=vk-plan-badge>Чаще берут</span>" if hit else ""
        c+=f'<div class="vk-plan{" vk-plan-hit" if hit else ""}">{badge}<div class="vk-plan-tier">{esc(tier)}</div><h3>{esc(name)}</h3><div class="vk-price">{esc(price)}</div><div class="vk-price-sub">{esc(econ)}</div><ul>{fl}</ul><a class="vk-btn vk-btn-block" href="{LK}">Купить ключ</a></div>'
    import json as _j
    ld={"@context":"https://schema.org","@type":"Product","name":"Ключ v2raytun","description":"Ключи и подписка v2raytun",
        "offers":{"@type":"AggregateOffer","priceCurrency":"RUB","lowPrice":"249","highPrice":"1890","offerCount":"4"}}
    return f'<section class="vk-sec" id="tarify"><div class="vk-wrap"><h2 class="vk-h2">Тарифы на ключи v2raytun</h2><p class="vk-sub">Пробный ключ — бесплатно. Подписка — от 249 ₽.</p><div class="vk-plans">{c}</div></div></section><script type="application/ld+json">{_j.dumps(ld,ensure_ascii=False)}</script>'

def page(slug, title, desc, h1, body, cluster=None, faqs=None, dl=False):
    path = "/" if slug == "" else f"/{slug}/"
    parts = [head(title, desc, path), header(), '<main>']
    if slug == "":
        parts += [hero(), stat(), bento(), platforms(), downloads(), body, tariffs()]
        if cluster: parts.append(chips(cluster))
    else:
        parts.append(f'<section class="vk-page-h"><div class="vk-wrap"><nav class="vk-bc"><a href="/">Главная</a> / <span>{esc(h1)}</span></nav><h1>{esc(h1)}</h1></div></section>')
        parts.append(f'<section class="vk-sec"><div class="vk-wrap vk-prose">{body}</div></section>')
        if dl: parts.append(downloads())
        parts.append(f'<div class="vk-wrap">{cta(big=True)}</div>')
        if cluster: parts.append(chips(cluster))
    if faqs: parts.append(f'<div class="vk-wrap">{faq(faqs)}</div>')
    if slug == "":
        parts.append(site_ld())
    else:
        parts.append(bc_ld([("Главная", BASE+"/"), (h1, BASE+path)]))
    parts.append(footer())
    out_dir = OUT if slug == "" else os.path.join(OUT, slug)
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write("\n".join(parts))
    return path

def prose(*paras): return "".join(f"<p>{p}</p>" for p in paras)
def h2(t): return f'<h2>{esc(t)}</h2>'
def steps(items):
    li="".join(f'<li><b>{esc(t)}</b> {esc(d)}</li>' for t,d in items)
    return f'<ol class="vk-steps">{li}</ol>'

PAGES = []
# Главная
PAGES.append(dict(slug="", title="Ключи v2raytun — скачать и получить конфиг | v2ray2tun",
    desc="Рабочие ключи v2raytun для ПК, Android, iPhone, Mac и TV. Бесплатный пробный ключ, конфигурации VLESS Reality, подписка от 249 ₽.",
    h1="", cluster="Общее",
    body='<section class="vk-sec"><div class="vk-wrap vk-prose">'+prose(
        "<b>v2raytun</b> — это приложение-клиент для протокола VLESS/Reality, в которое нужно вставить ключ (конфигурацию) сервера. На 2rayhub.com ты получаешь рабочий ключ v2raytun сразу: на email или в Telegram. Не нужно искать конфиги по форумам — вставил строку в приложение и подключение готово.",
        "Ключи подходят для всех версий v2raytun: на ПК и Windows, на Android (APK), на iPhone и iPad, на Mac и Smart TV. Есть бесплатный пробный ключ, чтобы проверить скорость, и подписка без ограничений.")+
        h2("Приложение v2raytun: куда вставить ключ")+prose("Приложение v2raytun — это клиент, который читает ключ-конфигурацию и устанавливает подключение. Скачай приложение под свою систему, вставь полученный ключ — и v2raytun сам поднимет соединение, без ручной настройки серверов.")+'</div></section>',
    faqs=[("Что такое ключ v2raytun?","Ключ — это строка-конфигурация вида <code>vless://…</code>, которую вставляют в приложение v2raytun. Она содержит адрес сервера и параметры подключения."),
          ("Где взять ключ v2raytun бесплатно?","Нажми «Получить ключ» — пробный ключ выдаётся бесплатно на email или в Telegram, без оплаты."),
          ("На каких устройствах работает?","На ПК/Windows, Android, iPhone/iOS, Mac и Smart TV. Один ключ можно использовать на нескольких устройствах.")]))
# Ключи (центр)
PAGES.append(dict(slug="klyuchi", title="Ключи v2raytun — бесплатные ключи и конфиги подключения",
    desc="Получи ключ v2raytun: бесплатные ключи, ключи подключения, конфигурации VLESS Reality. Выдача за минуту на email или в Telegram.",
    h1="Ключи v2raytun", cluster="Ключи/конфиги/сервера",
    body=prose("Ключ v2raytun — это готовая конфигурация сервера, которую вставляют в приложение. На этой странице ты можешь получить рабочие ключи v2raytun: бесплатный пробный ключ и ключи подключения по подписке.")+
        h2("Ключи для v2raytun — где взять рабочие")+prose("Рабочие ключи для v2raytun выдаются прямо здесь: нажми «Получить ключ», и конфигурация придёт на email или в Telegram. Это и есть ключ для подключения v2raytun — копируешь строку и вставляешь в приложение.")+
        h2("Бесплатные ключи v2raytun")+prose("Бесплатный ключ выдаётся сразу для проверки скорости. Его достаточно, чтобы оценить стабильность соединения до оформления подписки.")+
        h2("Ключи подключения и конфигурации")+prose("Ключ подключения содержит адрес сервера, протокол (VLESS Reality), SNI и параметры шифрования. Просто скопируй строку и добавь её в v2raytun — вручную ничего вводить не нужно.")+
        steps([("Получи ключ —","нажми «Получить ключ на email» или открой Telegram-бота."),("Скопируй конфигурацию —","строку вида vless://…"),("Вставь в v2raytun —","приложение само распознает сервер."),("Подключись —","нажми кнопку подключения, ключ активен.")]),
    faqs=[("Чем ключ отличается от подписки?","Ключ — это один сервер. Подписка — ссылка, которая автоматически обновляет список ключей и серверов."),
          ("Сколько действует бесплатный ключ?","Пробного ключа хватает на ознакомление; для постоянного использования подойдёт подписка от 249 ₽.")]))
# Скачать
PAGES.append(dict(slug="skachat", title="Скачать v2raytun — официальное приложение и ключ",
    desc="Скачать v2raytun на ПК, Android и iPhone и сразу получить рабочий ключ. Ссылки на приложение и готовая конфигурация.",
    h1="Скачать v2raytun", cluster="Скачать", dl=True,
    body=prose("Чтобы пользоваться ключами, сначала скачай приложение v2raytun под свою систему, а затем вставь полученную конфигурацию.")+
        h2("Где скачать v2raytun")+prose("Приложение доступно для ПК/Windows, Android (APK), iPhone/iOS, Mac и Smart TV. Скачивай только из официальных источников — так ключ и подключение будут работать корректно.")+
        h2("Скачал — получи ключ")+prose("После установки приложения нажми «Получить ключ»: пробная конфигурация придёт на email или в Telegram, и её останется вставить в v2raytun."),
    faqs=[("Скачать v2raytun бесплатно?","Само приложение бесплатное. Здесь ты дополнительно получаешь рабочий ключ к нему."),
          ("Откуда скачивать?","С официальных страниц приложения для вашей платформы — раздел GitHub и страницы платформ помогут.")]))
# На ПК
PAGES.append(dict(slug="na-pk", title="v2raytun на ПК и Windows — скачать и ключ",
    desc="v2raytun на ПК и Windows: как скачать приложение на компьютер и получить рабочий ключ-конфигурацию. Пошаговая настройка.",
    h1="v2raytun на ПК и Windows", cluster="ПК/Windows", dl=True,
    body=prose("v2raytun на ПК работает в Windows как обычное приложение: скачай клиент, добавь ключ-конфигурацию и подключись.")+
        h2("Как установить v2raytun на пк")+steps([("Скачай v2raytun для Windows —","установи приложение на компьютер."),("Получи ключ —","нажми «Получить ключ на email»."),("Добавь конфигурацию —","вставь строку vless:// в v2raytun."),("Подключись —","выбери сервер и нажми «Подключить».")])+
        h2("v2raytun скачать на пк бесплатно")+prose("Клиент для ПК бесплатный, пробный ключ тоже. Для постоянной работы на компьютере подойдёт подписка без ограничения скорости."),
    faqs=[("v2raytun на пк github?","Сборки клиента для ПК публикуются в том числе на GitHub — см. страницу GitHub."),
          ("Работает на Windows 10 и 11?","Да, приложение работает на актуальных версиях Windows.")]))
# Android
PAGES.append(dict(slug="android", title="v2raytun на Android — скачать APK и получить ключ",
    desc="v2raytun на Android: скачать APK, добавить ключ-конфигурацию и подключиться. Бесплатный пробный ключ для телефона.",
    h1="v2raytun на Android (APK)", cluster="Android", dl=True,
    body=prose("На Android v2raytun устанавливается как обычное приложение или из APK. После установки добавь ключ — и подключение готово.")+
        h2("Скачать v2raytun на андроид")+prose("Скачай APK или приложение для Android, открой его и вставь полученную конфигурацию v2raytun.")+
        steps([("Установи APK v2raytun —","разреши установку, если нужно."),("Получи ключ —","на email или в Telegram."),("Импортируй конфигурацию —","вставь vless:// или ссылку-подписку."),("Подключись —","нажми кнопку подключения.")]),
    faqs=[("v2raytun apk скачать бесплатно?","Да, приложение для Android бесплатное, пробный ключ тоже."),
          ("Безопасно ли ставить APK?","Скачивай APK только из официальных источников приложения.")]))
# iOS
PAGES.append(dict(slug="ios", title="v2raytun на iPhone и iOS — ключ и настройка",
    desc="v2raytun на iPhone и iPad: как получить ключ и добавить конфигурацию на iOS. Пошаговая инструкция и пробный ключ.",
    h1="v2raytun на iPhone (iOS)", cluster="iOS", dl=True,
    body=prose("На iPhone и iPad v2raytun работает через приложение для iOS. Получи ключ и добавь его в клиент — настройка занимает минуту.")+
        h2("v2raytun на айфон — как настроить")+steps([("Установи v2raytun для iOS —","из App Store или по ссылке приложения."),("Получи ключ —","нажми «Получить ключ на email»."),("Добавь конфигурацию —","вставь ссылку-подписку или vless://."),("Подключись —","разреши профиль конфигурации и подключись.")]),
    faqs=[("Работает на iPad?","Да, приложение и ключи работают и на iPhone, и на iPad."),
          ("Нужен ли отдельный ключ для iOS?","Нет, один ключ v2raytun работает на всех платформах.")]))
# Mac
PAGES.append(dict(slug="mac", title="v2raytun на Mac — скачать и добавить ключ",
    desc="v2raytun на Mac (macOS): как скачать клиент и добавить ключ-конфигурацию. Пробный ключ и подписка.",
    h1="v2raytun на Mac", cluster="Mac", dl=True,
    body=prose("На macOS v2raytun устанавливается как десктоп-приложение. Скачай клиент для Mac, добавь полученный ключ и подключись.")+
        steps([("Скачай v2raytun для Mac —","установи приложение."),("Получи ключ —","на email или в Telegram."),("Вставь конфигурацию —","строку vless:// в приложение."),("Подключись —","выбери сервер и подключайся.")]),
    faqs=[("Работает на Apple Silicon?","Да, клиент поддерживает Mac на M-чипах и Intel.")]))
# TV
PAGES.append(dict(slug="tv", title="v2raytun на Smart TV и Android TV — ключ",
    desc="v2raytun на телевизоре: как добавить ключ-конфигурацию на Android TV. Инструкция и пробный ключ.",
    h1="v2raytun на Smart TV", cluster="TV", dl=True,
    body=prose("На Android TV v2raytun ставится как приложение из магазина или APK. Добавь ключ-конфигурацию — и подключение работает на телевизоре.")+
        steps([("Установи v2raytun на ТВ —","через магазин приложений или APK."),("Получи ключ —","на email или в Telegram."),("Импортируй конфигурацию —","удобнее по ссылке-подписке."),("Подключись —","выбери сервер на пульте.")]),
    faqs=[("Подойдёт любой телевизор?","Нужен Android TV или приставка на Android. Один ключ работает и на ТВ, и на телефоне.")]))
# Конфигурации
PAGES.append(dict(slug="konfig", title="Конфигурации v2raytun — конфиги VLESS Reality",
    desc="Конфигурации и конфиги v2raytun: что это, как добавить и где взять рабочие конфиги VLESS Reality. Готовые конфигурации за минуту.",
    h1="Конфигурации v2raytun", cluster="Ключи/конфиги/сервера",
    body=prose("Конфигурация v2raytun (конфиг) — это и есть ключ: строка с адресом сервера и параметрами VLESS Reality. Здесь ты получаешь готовые рабочие конфиги без ручной настройки.")+
        h2("Как добавить конфигурацию")+steps([("Получи конфиг —","на email или в Telegram."),("Скопируй строку —","vless://… или ссылку-подписку."),("Вставь в v2raytun —","приложение распознает сервер автоматически."),("Подключись —","конфигурация активна.")])+
        h2("Конфигурации для v2raytun бесплатно")+prose("Пробная конфигурация выдаётся бесплатно. Платная подписка добавляет несколько серверов и автообновление конфигов."),
    faqs=[("Конфиг и ключ — одно и то же?","Да, в v2raytun это синонимы: строка-конфигурация и есть ключ подключения."),
          ("Конфиги обновляются?","По подписке список серверов и конфигов обновляется автоматически.")]))
# Подписка
PAGES.append(dict(slug="podpiska", title="Подписка v2raytun — ключи с автообновлением",
    desc="Подписка v2raytun: одна ссылка с автообновлением серверов и ключей. Тарифы от 249 ₽, пробный доступ бесплатно.",
    h1="Подписка v2raytun", cluster="Ключи/конфиги/сервера",
    body=prose("Подписка v2raytun — это ссылка, которую добавляют в приложение один раз. Она сама обновляет список серверов и ключей, поэтому подключение всегда рабочее.")+
        h2("Чем подписка лучше одного ключа")+prose("Один ключ — один сервер. Подписка даёт несколько серверов сразу и автоматически заменяет нерабочие, без ручного переноса конфигов.")+
        h2("Подписка v2raytun бесплатно")+prose("Попробовать можно бесплатно — пробный доступ. Полная подписка без ограничений скорости стоит от 249 ₽."),
    faqs=[("Как добавить подписку?","Скопируй ссылку-подписку и вставь её в v2raytun — приложение загрузит все серверы."),
          ("Сколько устройств?","Подписку можно использовать на ПК, телефоне и ТВ одновременно.")]))
# Бесплатно
PAGES.append(dict(slug="besplatno", title="v2raytun бесплатно — бесплатный ключ и конфиг",
    desc="v2raytun бесплатно: пробный ключ и конфигурация без оплаты. Проверь скорость, потом оформи подписку. Выдача за минуту.",
    h1="v2raytun бесплатно", cluster="Бесплатно",
    body=prose("Получить v2raytun бесплатно можно прямо здесь: пробный ключ выдаётся без оплаты, чтобы ты проверил скорость и стабильность.")+
        h2("Что входит в бесплатный доступ")+prose("Бесплатный ключ — это рабочая конфигурация для проверки. Скорость и серверы ограничены, но этого достаточно, чтобы оценить v2raytun перед подпиской.")+
        h2("Бесплатные ключи и конфиги")+prose("Нажми «Получить ключ» — бесплатный ключ придёт на email или в Telegram. Без регистрации и привязки карты."),
    faqs=[("Правда бесплатно?","Да, пробный ключ бесплатный и без карты."),
          ("В чём ограничения?","Бесплатный доступ ограничен по скорости и числу серверов; подписка снимает лимиты.")]))
# Настройка
PAGES.append(dict(slug="nastrojka", title="Настройка v2raytun — как настроить и подключить",
    desc="Как настроить v2raytun: пошаговая инструкция добавления ключа и подключения на ПК, Android и iPhone.",
    h1="Настройка v2raytun", cluster="Настройка/как",
    body=prose("Настройка v2raytun сводится к двум шагам: добавить ключ-конфигурацию и нажать «Подключить». Вручную вводить адреса серверов не нужно.")+
        steps([("Установи приложение —","для своей платформы."),("Получи ключ —","на email или в Telegram."),("Добавь конфигурацию —","вставь vless:// или ссылку-подписку."),("Подключись —","выбери сервер и активируй соединение.")])+
        h2("Как подключить v2raytun")+prose("Если используешь подписку — достаточно одной ссылки: приложение само загрузит серверы. Для одного ключа просто вставь строку конфигурации."),
    faqs=[("Нужно ли что-то прописывать вручную?","Нет, вся конфигурация уже в ключе — приложение читает её автоматически."),
          ("Как сменить сервер?","В списке серверов выбери другой — по подписке их несколько.")]))
# Ошибки
PAGES.append(dict(slug="oshibki", title="v2raytun не работает — что делать",
    desc="v2raytun не работает или не подключается: частые причины и решения. Как обновить ключ и восстановить подключение.",
    h1="v2raytun не работает — решение", cluster="Не работает/ошибки",
    body=prose("Если v2raytun не работает или не подключается, чаще всего дело в устаревшем ключе или выбранном сервере. Ниже — что проверить по порядку.")+
        steps([("Обнови ключ —","получи свежую конфигурацию, старый сервер мог смениться."),("Смени сервер —","выбери другой в списке (по подписке их несколько)."),("Проверь время —","некорректное системное время ломает Reality-подключение."),("Переустанови приложение —","если ничего не помогло, поставь актуальную версию.")]),
    faqs=[("Почему перестал работать ключ?","Сервер мог обновиться. По подписке ключи обновляются автоматически — это надёжнее одного ключа."),
          ("Подключается, но нет интернета?","Смени сервер и проверь, что выбран рабочий профиль конфигурации.")]))
# GitHub
PAGES.append(dict(slug="github", title="v2raytun GitHub — официальные сборки и ключ",
    desc="v2raytun на GitHub: где брать официальные сборки приложения и как получить рабочий ключ-конфигурацию к нему.",
    h1="v2raytun GitHub", cluster="Бренд/офиц/github", dl=True,
    body=prose("Официальные сборки клиента v2raytun публикуются в том числе на GitHub. Оттуда удобно скачивать версии для ПК и Android.")+
        h2("Скачал с GitHub — нужен ключ")+prose("Само приложение из GitHub не содержит серверов: к нему нужна конфигурация. Получи рабочий ключ здесь и вставь его в v2raytun."),
    faqs=[("Где официальный v2raytun?","Официальное приложение распространяется через магазины и GitHub-релизы; ключи к нему ты получаешь на этом сайте.")]))
# Прокси
PAGES.append(dict(slug="proxy", title="v2raytun прокси — proxy-конфигурация и ключ",
    desc="v2raytun прокси: как работает proxy-подключение через VLESS Reality и где взять ключ-конфигурацию.",
    h1="v2raytun прокси (proxy)", cluster="Прокси/proxy",
    body=prose("v2raytun работает как прокси-клиент: ключ-конфигурация направляет трафик через сервер по протоколу VLESS Reality. Получи рабочий proxy-ключ и подключайся.")+
        h2("Как получить proxy-ключ")+prose("Нажми «Получить ключ» — конфигурация прокси придёт на email или в Telegram, её останется вставить в приложение."),
    faqs=[("Это socks-прокси?","v2raytun использует протокол VLESS/Reality; для приложений это работает как защищённый прокси-туннель.")]))
# Тарифы (отдельная)
PAGES.append(dict(slug="tarify", title="Тарифы v2raytun — цены на ключи и подписку",
    desc="Тарифы на ключи v2raytun: пробный ключ бесплатно, подписка от 249 ₽. На месяц, 3 месяца, полгода и год.",
    h1="Тарифы на ключи v2raytun", cluster="Ключи/конфиги/сервера",
    body=prose("Пробный ключ v2raytun — бесплатно. Для постоянного использования выбери подписку: чем дольше период, тем дешевле месяц.")+
        '<div class="vk-plans">'+"".join(
            (lambda name,price,tier,econ,feats,hit: f'<div class="vk-plan{" vk-plan-hit" if hit else ""}">{"<span class=vk-plan-badge>Чаще берут</span>" if hit else ""}<div class="vk-plan-tier">{esc(tier)}</div><h3>{esc(name)}</h3><div class="vk-price">{esc(price)}</div><div class="vk-price-sub">{esc(econ)}</div><ul>{"".join(f"<li>{esc(f)}</li>" for f in feats)}</ul><a class="vk-btn vk-btn-block" href="{LK}">Купить ключ</a></div>')(*p)
            for p in PLANS)+'</div>',
    faqs=[("Есть ли пробный период?","Да, пробный ключ выдаётся бесплатно до оплаты."),
          ("Как оплатить?","Оплата происходит в личном кабинете после получения ключа.")]))
# Вопросы
PAGES.append(dict(slug="voprosy", title="Вопросы о ключах v2raytun — FAQ",
    desc="Частые вопросы о ключах v2raytun: что такое ключ, где взять бесплатно, как настроить на разных устройствах.",
    h1="Вопросы и ответы о v2raytun", cluster="Настройка/как",
    body=prose("Здесь собраны частые вопросы о ключах и конфигурациях v2raytun."),
    faqs=[("Что такое ключ v2raytun?","Строка-конфигурация vless://… с адресом сервера и параметрами, которую вставляют в приложение."),
          ("Где скачать v2raytun?","Приложение — из официальных источников и GitHub; ключ к нему — на этом сайте."),
          ("Как получить ключ бесплатно?","Нажми «Получить ключ» — пробный ключ придёт на email или в Telegram без оплаты."),
          ("Чем ключ отличается от подписки?","Ключ — один сервер; подписка — ссылка с автообновлением нескольких серверов."),
          ("Работает на всех устройствах?","Да: ПК, Android, iPhone, Mac и Smart TV."),
          ("Что делать, если не работает?","Обнови ключ и смени сервер — см. страницу «Не работает».")]))

def zaprosy_page():
    blocks=""
    order=sorted(BYC.items(), key=lambda x:-sum(i['f'] for i in x[1]))
    for cl, items in order:
        li="".join(f'<li>{esc(i["q"])}</li>' for i in items)
        blocks+=f'<div class="vk-zcol"><h3>{esc(cl)} <span>{len(items)}</span></h3><ul>{li}</ul></div>'
    body=prose("Список самых частотных запросов по бренду v2raytun, по которым мы помогаем найти рабочие ключи и конфигурации. Сгруппировано по темам.")+f'<div class="vk-zgrid">{blocks}</div>'
    return dict(slug="zaprosy", title="Запросы v2raytun — список ключевых тем",
        desc="Частотные запросы по v2raytun: скачать, на пк, ключи, конфигурации, android, ios и другие темы по бренду.",
        h1="Популярные запросы v2raytun", body=body, cluster=None)
PAGES.append(zaprosy_page())

# ---------- БЛОГ ----------
ARTICLES = [
 dict(slug="chto-takoe-klyuch-v2raytun", date="2026-05-27",
   title="Что такое ключ v2raytun и как он устроен",
   desc="Простыми словами: что такое ключ v2raytun, из чего состоит конфигурация vless:// и чем ключ отличается от подписки.",
   excerpt="Разбираем, что такое ключ v2raytun, из чего состоит строка конфигурации и чем ключ отличается от подписки.",
   body=prose("Ключ v2raytun — это строка-конфигурация, которую вставляют в приложение, чтобы подключиться к серверу. Внешне она выглядит как <code>vless://…</code> и содержит всё необходимое для подключения.")+
        h2("Из чего состоит ключ")+prose("В ключе зашиты адрес сервера и порт, идентификатор пользователя, протокол VLESS и параметры Reality — современного механизма маскировки трафика. Благодаря этому подключение работает стабильно и быстро, как обычный прокси.")+
        h2("Ключ, конфиг и подписка")+prose("«Ключ» и «конфигурация» в v2raytun — это одно и то же: одна строка для одного сервера. Подписка — ссылка, которая отдаёт сразу несколько ключей и обновляет их автоматически.")+
        h2("Как получить рабочий ключ")+prose("Нажми «Получить ключ» — пробный ключ придёт на email или в Telegram. Скопируй строку, вставь в v2raytun, и приложение само распознает сервер.")),
 dict(slug="kak-dobavit-klyuch-v2raytun", date="2026-05-27",
   title="Как добавить ключ v2raytun на ПК, Android и iPhone",
   desc="Пошагово: как добавить ключ-конфигурацию v2raytun на ПК и Windows, на Android (APK) и на iPhone/iOS.",
   excerpt="Пошаговая инструкция, как вставить ключ v2raytun в приложение на ПК, Android и iPhone за минуту.",
   body=prose("Добавить ключ v2raytun одинаково просто на любой системе: получаешь конфигурацию и вставляешь её в приложение. Разберём по платформам.")+
        h2("На ПК и Windows")+steps([("Скачай v2raytun для Windows","и установи приложение."),("Получи ключ","на email или в Telegram."),("Вставь конфигурацию","строку vless:// в приложение."),("Подключись","выбери сервер и нажми «Подключить».")])+
        h2("На Android")+prose("Установи приложение или APK, открой его и импортируй ключ — удобнее по ссылке-подписке, тогда серверы обновляются сами.")+
        h2("На iPhone и iPad")+prose("Поставь v2raytun для iOS, добавь ключ или подписку, разреши профиль конфигурации и подключайся. Один ключ работает на всех устройствах одновременно.")),
 dict(slug="besplatnyj-klyuch-ili-podpiska", date="2026-05-27",
   title="Бесплатный ключ или подписка v2raytun — что выбрать",
   desc="Сравниваем бесплатный ключ v2raytun и платную подписку: скорость, серверы, автообновление и когда что выгоднее.",
   excerpt="Чем бесплатный ключ v2raytun отличается от подписки и в каком случае стоит платить — короткое сравнение.",
   body=prose("Перед оплатой логично попробовать бесплатный ключ v2raytun, а затем решить, нужна ли подписка. Сравним варианты.")+
        h2("Бесплатный ключ")+prose("Бесплатный ключ выдаётся сразу и подходит, чтобы проверить скорость и стабильность. Минусы — ограничение скорости и один сервер: если он перегружен, подключение замедляется.")+
        h2("Подписка")+prose("Подписка снимает лимиты: полная скорость, несколько серверов и автоматическое обновление ключей. Если перестал работать один сервер, приложение само переключится на рабочий.")+
        h2("Что выбрать")+prose("Для разового использования хватит бесплатного ключа. Для постоянной работы выгоднее подписка — от 249 ₽, а при оплате за год месяц выходит дешевле всего.")),
]

def article_page(a):
    import json as _j
    path = f"/blog/{a['slug']}/"
    ld = {"@context":"https://schema.org","@type":"BlogPosting","headline":a["title"],
          "datePublished":a["date"],"dateModified":a["date"],"description":a["desc"],
          "mainEntityOfPage":BASE+path,"inLanguage":"ru",
          "author":{"@type":"Organization","name":"v2ray2tun"},
          "publisher":{"@type":"Organization","name":"v2ray2tun"}}
    parts = [head(a["title"], a["desc"], path, og_type="article"), header(), '<main>',
        f'<section class="vk-page-h"><div class="vk-wrap"><nav class="vk-bc"><a href="/">Главная</a> / <a href="/blog/">Блог</a> / <span>{esc(a["title"])}</span></nav><span class="vk-bdate">{esc(a["date"])}</span><h1>{esc(a["title"])}</h1></div></section>',
        f'<section class="vk-sec"><div class="vk-wrap vk-prose">{a["body"]}</div></section>',
        f'<div class="vk-wrap">{cta(big=True)}</div>',
        f'<script type="application/ld+json">{_j.dumps(ld,ensure_ascii=False)}</script>',
        bc_ld([("Главная",BASE+"/"),("Блог",BASE+"/blog/"),(a["title"],BASE+path)]),
        footer()]
    d = os.path.join(OUT, "blog", a["slug"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write("\n".join(parts))
    return path

def blog_index_page():
    import json as _j
    cards = ""
    for a in ARTICLES:
        cards += f'<a class="vk-bcard" href="/blog/{a["slug"]}/"><span class="vk-bdate">{esc(a["date"])}</span><h3>{esc(a["title"])}</h3><p>{esc(a["excerpt"])}</p><span class="vk-blink">Читать →</span></a>'
    ld = {"@context":"https://schema.org","@type":"Blog","name":"Блог v2raytun","url":BASE+"/blog/",
          "blogPost":[{"@type":"BlogPosting","headline":a["title"],"datePublished":a["date"],"url":BASE+f"/blog/{a['slug']}/"} for a in ARTICLES]}
    parts = [head("Блог v2raytun — статьи о ключах и настройке",
                  "Блог v2raytun: статьи о ключах, конфигурациях, настройке и подписке для всех устройств.","/blog/"),
        header(), '<main>',
        '<section class="vk-page-h"><div class="vk-wrap"><nav class="vk-bc"><a href="/">Главная</a> / <span>Блог</span></nav><h1>Блог v2raytun</h1></div></section>',
        f'<section class="vk-sec"><div class="vk-wrap"><div class="vk-blog-grid">{cards}</div></div></section>',
        f'<script type="application/ld+json">{_j.dumps(ld,ensure_ascii=False)}</script>',
        bc_ld([("Главная",BASE+"/"),("Блог",BASE+"/blog/")]),
        footer()]
    d = os.path.join(OUT, "blog"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write("\n".join(parts))
    return "/blog/"

CSS = """
:root{--bg:#0d0e12;--bg2:#15171e;--panel:#191c24;--line:#262a35;--tx:#e9eaf0;--mut:#9aa0ab;
--amb:#8b5cf6;--amb2:#7c3aed;--tg:#27a7e7;--rad:16px}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--tx);font:16px/1.65 'Onest',system-ui,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:clip}
a{color:inherit;text-decoration:none}
.vk-wrap{max-width:1140px;margin:0 auto;padding:0 20px}
h1{font-size:clamp(28px,5vw,46px);line-height:1.1;font-weight:800;letter-spacing:-.02em}
h2{font-size:clamp(22px,3vw,30px);font-weight:700;letter-spacing:-.01em}
h3{font-size:19px;font-weight:700}
.vk-h2{text-align:center;margin-bottom:8px}
.vk-sub{text-align:center;color:var(--mut);margin-bottom:28px}
/* header */
.vk-hdr{position:sticky;top:0;z-index:50;background:rgba(13,14,18,.85);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.vk-hdr-in{display:flex;align-items:center;gap:18px;height:64px}
.vk-logo{font-weight:800;font-size:20px;letter-spacing:-.02em}
.vk-logo-mk{background:linear-gradient(135deg,var(--amb),var(--amb2));-webkit-background-clip:text;background-clip:text;color:transparent}
.vk-logo-dot{color:var(--mut);font-weight:600;font-size:14px}
.vk-nav{display:flex;gap:20px;margin-left:auto;font-size:15px;font-weight:500}
.vk-nav a{color:var(--mut);transition:.15s}.vk-nav a:hover{color:var(--tx)}
.vk-btn{display:inline-flex;align-items:center;gap:8px;justify-content:center;background:linear-gradient(135deg,var(--amb),var(--amb2));color:#1a1205;font-weight:700;padding:12px 20px;border-radius:12px;border:0;cursor:pointer;transition:.15s;white-space:nowrap}
.vk-btn:hover{transform:translateY(-1px);box-shadow:0 8px 24px rgba(124,58,237,.28)}
.vk-btn-sm{padding:9px 16px;font-size:14px}
.vk-btn-tg{background:linear-gradient(135deg,#2aa9e8,#1f7fc0);color:#fff}
.vk-btn-block{width:100%}
.vk-burger{display:none;margin-left:8px;background:0;border:0;flex-direction:column;gap:5px;cursor:pointer}
.vk-burger span{width:24px;height:2px;background:var(--tx);border-radius:2px}
.vk-mnav{display:none}
/* hero */
.vk-hero{padding:54px 0 36px;border-bottom:1px solid var(--line);background:radial-gradient(900px 420px at 78% -10%,rgba(124,58,237,.10),transparent 60%)}
.vk-hero-in{display:grid;grid-template-columns:1.05fr .95fr;gap:42px;align-items:center}
.vk-tag{display:inline-block;font-size:13px;font-weight:600;color:var(--amb);border:1px solid rgba(139,92,246,.3);background:rgba(139,92,246,.07);padding:6px 12px;border-radius:999px;margin-bottom:16px}
.vk-lead{color:var(--mut);font-size:18px;margin:16px 0 24px;max-width:560px}
.vk-cta{display:flex;gap:12px;flex-wrap:wrap}
.vk-cta-big .vk-btn{padding:15px 24px;font-size:16px}
.vk-trust{display:flex;gap:18px;flex-wrap:wrap;margin-top:20px;color:var(--mut);font-size:14px}
.vk-keycard{background:linear-gradient(160deg,#1b1f29,#13151c);border:1px solid var(--line);border-radius:20px;padding:20px;box-shadow:0 24px 60px rgba(0,0,0,.45);position:relative;overflow:hidden}
.vk-keycard:before{content:"";position:absolute;inset:0;background:radial-gradient(400px 120px at 90% 0,rgba(139,92,246,.14),transparent 60%);pointer-events:none}
.vk-keycard-top{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--mut);font-weight:600}
.vk-dot{width:9px;height:9px;border-radius:50%;background:#3ddc8b;box-shadow:0 0 10px #3ddc8b}
.vk-kc-badge{margin-left:auto;font-size:11px;color:var(--amb);border:1px solid rgba(139,92,246,.4);padding:2px 8px;border-radius:6px}
.vk-keystr{margin:14px 0;background:#0c0d11;border:1px solid var(--line);border-radius:12px;padding:14px;font-family:'JetBrains Mono',monospace;font-size:12.5px;line-height:1.6;color:#cfe3ff;word-break:break-all;max-height:120px;overflow:hidden}
.vk-keystr code{color:#8fd0ff}
.vk-keycard-bot{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:var(--mut)}
.vk-kc-copy{color:var(--amb);font-weight:600;border:1px solid rgba(139,92,246,.35);padding:5px 12px;border-radius:8px}
.vk-hero-tags{margin-top:14px;color:var(--mut);font-size:12.5px;font-family:'JetBrains Mono',monospace;opacity:.8}
/* stat */
.vk-stat{border-bottom:1px solid var(--line)}
.vk-stat-in{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;padding:26px 0}
.vk-stat-i{text-align:center}.vk-stat-i b{display:block;font-size:26px;font-weight:800;color:var(--amb)}
.vk-stat-i span{color:var(--mut);font-size:14px}
/* sections */
.vk-sec{padding:46px 0}
.vk-bento{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:24px}
.vk-bento-i{background:var(--panel);border:1px solid var(--line);border-radius:var(--rad);padding:22px;transition:.15s}
.vk-bento-i:hover{border-color:rgba(139,92,246,.4);transform:translateY(-2px)}
.vk-bi-ic{font-size:26px}.vk-bento-i h3{margin:10px 0 6px}.vk-bento-i p{color:var(--mut);font-size:14.5px}
.vk-plat{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-top:24px}
.vk-plat-i{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 10px;text-align:center;transition:.15s}
.vk-plat-i:hover{border-color:rgba(139,92,246,.4);color:var(--amb)}
.vk-plat-i span{font-size:24px;display:block;margin-bottom:8px}.vk-plat-i b{font-size:14px;font-weight:600}
/* tariffs */
.vk-plans{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:24px}
.vk-plan{background:var(--panel);border:1px solid var(--line);border-radius:var(--rad);padding:24px 20px;position:relative;display:flex;flex-direction:column}
.vk-plan-hit{border-color:var(--amb);box-shadow:0 0 0 1px var(--amb),0 18px 40px rgba(124,58,237,.16)}
.vk-plan-badge{position:absolute;top:-11px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,var(--amb),var(--amb2));color:#fff;font-size:12px;font-weight:700;padding:4px 14px;border-radius:999px;white-space:nowrap}
.vk-plan-tier{font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--amb);margin-bottom:4px}
.vk-plan h3{font-size:19px}
.vk-price{font-size:32px;font-weight:800;margin:8px 0 2px}.vk-price-sub{color:#7ee0a8;font-size:13px;font-weight:600;margin-bottom:16px}
.vk-plan:first-child .vk-price-sub{color:var(--mut);font-weight:500}
/* downloads */
.vk-dl{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px}
.vk-dl-i{display:flex;flex-direction:column;align-items:flex-start;gap:2px;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px 22px;transition:.15s}
.vk-dl-i:hover{border-color:var(--amb);transform:translateY(-2px);box-shadow:0 14px 30px rgba(124,58,237,.14)}
.vk-dl-ic{font-size:30px;margin-bottom:6px}
.vk-dl-i b{font-size:17px}.vk-dl-i small{color:var(--mut);font-size:13px}
.vk-plan ul{list-style:none;margin:0 0 18px}.vk-plan li{padding:7px 0 7px 24px;position:relative;font-size:14.5px;border-bottom:1px solid var(--line)}
.vk-plan li:before{content:"✓";position:absolute;left:0;color:var(--amb);font-weight:700}
.vk-plan .vk-btn-block{margin-top:auto}
/* page */
.vk-page-h{padding:40px 0 8px;border-bottom:1px solid var(--line);background:radial-gradient(700px 300px at 80% -20%,rgba(124,58,237,.08),transparent)}
.vk-bc{font-size:13px;color:var(--mut);margin-bottom:12px}.vk-bc a{color:var(--amb)}
.vk-prose{max-width:780px}.vk-prose p{margin:0 0 16px;color:#cfd2db}.vk-prose h2{margin:30px 0 12px}
.vk-prose code{background:#0c0d11;border:1px solid var(--line);padding:1px 6px;border-radius:5px;font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--amb)}
.vk-steps{counter-reset:s;list-style:none;margin:8px 0 8px}
.vk-steps li{counter-increment:s;position:relative;padding:12px 0 12px 44px;border-bottom:1px solid var(--line);color:var(--mut)}
.vk-steps li b{color:var(--tx)}
.vk-steps li:before{content:counter(s);position:absolute;left:0;top:12px;width:28px;height:28px;border-radius:8px;background:rgba(139,92,246,.12);color:var(--amb);font-weight:700;display:grid;place-items:center;font-size:14px}
/* chips */
.vk-chips{max-width:1140px;margin:0 auto;padding:10px 20px 46px}
.vk-chips h2{margin-bottom:16px;font-size:22px}
.vk-chip-list{list-style:none;display:flex;flex-wrap:wrap;gap:8px}
.vk-chip-list li{background:var(--panel);border:1px solid var(--line);color:var(--mut);font-size:13.5px;padding:7px 13px;border-radius:999px}
/* zaprosy */
.vk-zgrid{columns:3;column-gap:18px;margin-top:8px}
.vk-zcol{break-inside:avoid;margin-bottom:18px;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.vk-zcol h3{font-size:15px;color:var(--amb);margin-bottom:8px;display:flex;justify-content:space-between}
.vk-zcol h3 span{color:var(--mut);font-weight:500}
.vk-zcol ul{list-style:none}.vk-zcol li{font-size:13px;color:var(--mut);padding:3px 0;border-bottom:1px solid rgba(38,42,53,.6)}
/* faq */
.vk-faq{max-width:820px;margin:10px auto 30px}
.vk-faq h2{margin-bottom:16px}
.vk-faq-i{background:var(--panel);border:1px solid var(--line);border-radius:12px;margin-bottom:10px;padding:0 18px}
.vk-faq-i summary{cursor:pointer;padding:15px 0;font-weight:600;list-style:none;display:flex;justify-content:space-between;align-items:center}
.vk-faq-i summary:after{content:"⌄";color:var(--amb);font-size:20px;transition:.2s}
.vk-faq-i[open] summary:after{transform:rotate(180deg)}
.vk-faq-i div{padding:0 0 16px;color:var(--mut);font-size:15px}
.vk-faq-i code{color:var(--amb);font-family:'JetBrains Mono',monospace;font-size:13px}
/* footer */
.vk-ftr{border-top:1px solid var(--line);background:#0a0b0e;padding:44px 0 24px;margin-top:20px}
.vk-fgrid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:28px}
.vk-fbrand p{color:var(--mut);font-size:14px;margin:12px 0 16px;max-width:300px}
.vk-fbrand .vk-cta{flex-direction:column}.vk-fbrand .vk-btn{width:100%}
.vk-fcol h4{font-size:14px;margin-bottom:12px}.vk-fcol ul{list-style:none}
.vk-fcol li{margin-bottom:8px}.vk-fcol a{color:var(--mut);font-size:14px}.vk-fcol a:hover{color:var(--amb)}
.vk-fbot{display:flex;justify-content:space-between;color:var(--mut);font-size:13px;border-top:1px solid var(--line);margin-top:30px;padding-top:18px}
/* mobile */
@media(max-width:900px){
 .vk-nav{display:none}.vk-burger{display:flex}
 .vk-hero-in{grid-template-columns:1fr;gap:28px}
 .vk-bento{grid-template-columns:1fr}
 .vk-plans{grid-template-columns:repeat(2,1fr)}
 .vk-dl{grid-template-columns:1fr}
 .vk-plat{grid-template-columns:repeat(3,1fr)}
 .vk-stat-in{grid-template-columns:repeat(2,1fr);gap:22px}
 .vk-fgrid{grid-template-columns:1fr 1fr}
 .vk-zgrid{columns:1}
 .vk-plan-hit{transform:none}
 body.vk-open .vk-mnav{display:flex;flex-direction:column;border-top:1px solid var(--line);padding:8px 20px 14px}
 body.vk-open .vk-mnav a{padding:11px 0;color:var(--mut);border-bottom:1px solid var(--line)}
 .vk-hdr .vk-btn-sm{display:none}
}
/* blog */
.vk-blog-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.vk-bcard{background:var(--panel);border:1px solid var(--line);border-radius:var(--rad);padding:22px;display:flex;flex-direction:column;gap:8px;transition:.15s}
.vk-bcard:hover{border-color:rgba(139,92,246,.4);transform:translateY(-2px)}
.vk-bdate{font-size:12.5px;color:var(--mut);font-family:'JetBrains Mono',monospace}
.vk-bcard h3{font-size:18px;line-height:1.3}
.vk-bcard p{color:var(--mut);font-size:14.5px;flex:1;margin:0}
.vk-blink{color:var(--amb);font-weight:600;font-size:14px}
.vk-page-h .vk-bdate{display:block;margin-bottom:8px}
@media(max-width:560px){.vk-plat{grid-template-columns:repeat(2,1fr)}.vk-plans{grid-template-columns:1fr}.vk-fbot{flex-direction:column;gap:6px}.vk-fgrid{grid-template-columns:1fr;gap:22px}}
@media(max-width:900px){.vk-blog-grid{grid-template-columns:1fr}}
"""

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8b5cf6"/><stop offset="1" stop-color="#7c3aed"/></linearGradient></defs><rect width="64" height="64" rx="14" fill="#0d0e12"/><circle cx="24" cy="28" r="11" fill="none" stroke="url(#g)" stroke-width="5"/><path d="M31 33 L48 50 M44 46 l6 -6 M40 42 l5 -5" stroke="url(#g)" stroke-width="5" stroke-linecap="round" fill="none"/></svg>'''

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    open(os.path.join(OUT, "assets", "app.css"), "w", encoding="utf-8").write(CSS)
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(FAVICON)
    open(os.path.join(OUT, f"{INDEXNOW_KEY}.txt"), "w").write(INDEXNOW_KEY)
    og_src = os.path.join(ROOT, "og.png")
    if os.path.exists(og_src): shutil.copy(og_src, os.path.join(OUT, "og.png"))
    paths = []
    for p in PAGES:
        paths.append(page(p["slug"], p["title"], p["desc"], p["h1"], p["body"], p.get("cluster"), p.get("faqs")))
    paths.append(blog_index_page())
    for a in ARTICLES:
        paths.append(article_page(a))
    # robots
    if NOINDEX:
        robots = "User-agent: *\nDisallow: /\n"
    else:
        robots = f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n"
    open(os.path.join(OUT, "robots.txt"), "w").write(robots)
    # sitemap
    urls = "".join(f"<url><loc>{BASE}{p}</loc></url>" for p in paths)
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    print(f"built {len(paths)} pages -> {OUT}")
    # QA
    print("NOINDEX =", NOINDEX, "| pages:", len(paths))
    for p in PAGES:
        t = p["title"]
        if len(t) > 60: print("  ⚠ title>60:", len(t), t)

if __name__ == "__main__":
    build()
