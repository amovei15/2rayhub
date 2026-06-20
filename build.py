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
CSSV = "v3"

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
<meta property="og:site_name" content="2rayhub">
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
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon.svg?v={CSSV}" type="image/svg+xml">
<link rel="stylesheet" href="/assets/app.css?v={CSSV}">{metr}
</head><body>"""

def header():
    nav = "".join(f'<a href="{u}">{esc(t)}</a>' for t, u in NAV)
    return f"""<header class="hp-hdr"><div class="hp-wrap hp-hdr-in">
<a class="hp-logo" href="/"><span class="hp-logo-mark"></span><span class="hp-logo-tx">2rayhub<span class="hp-logo-dot">.</span></span></a>
<nav class="hp-nav">{nav}</nav>
<a class="hp-btn hp-btn-sm" href="{LK}" rel="nofollow noopener">Получить ключ</a>
<button class="hp-burger" aria-label="Меню" onclick="document.body.classList.toggle('hp-open')"><span></span><span></span><span></span></button>
</div><div class="hp-mnav">{nav}</div></header>"""

def cta(big=False):
    lg = " hp-btn-lg" if big else ""
    return f"""<div class="hp-cta">
<a class="hp-btn{lg}" href="{LK}" rel="nofollow noopener">Получить ключ на email</a>
<a class="hp-btn hp-btn-tg{lg}" href="{TG}" rel="nofollow noopener">Получить в Telegram</a></div>"""

def chips(cluster, n=40, title="Что ищут пользователи о v2raytun"):
    ws = kws(cluster, n)
    if not ws: return ""
    items = "".join(f'<li>{esc(w)}</li>' for w in ws)
    return f'<section class="hp-chips"><div class="hp-wrap"><div class="hp-chips-head"><h2 class="hp-h2">{esc(title)}</h2><p>Популярные запросы по бренду v2raytun, под которые на сайте есть ответ.</p></div><div class="hp-chip-group"><ul class="hp-chip-list">{items}</ul></div></div></section>'

def faq(items):
    rows = ""
    for q, a in items:
        rows += f'<details class="hp-faq-i"><summary>{esc(q)}</summary><div>{a}</div></details>'
    import json as _j
    ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in items]}
    return f'<section class="hp-sec"><div class="hp-wrap"><div class="hp-faq"><div class="hp-sec-head hp-sec-head--center"><span class="hp-eyebrow">FAQ</span><h2 class="hp-h2">Частые вопросы о v2raytun</h2></div>{rows}</div></div></section><script type="application/ld+json">{_j.dumps(ld,ensure_ascii=False)}</script>'

def footer():
    cols = ""
    for title, links in FOOT:
        ls = "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for t, u in links)
        cols += f'<div class="hp-fcol"><h4>{esc(title)}</h4><ul>{ls}</ul></div>'
    return f"""<footer class="hp-ftr"><div class="hp-wrap">
<div class="hp-fgrid">
<div class="hp-fbrand"><a class="hp-logo" href="/"><span class="hp-logo-mark"></span><span class="hp-logo-tx">2rayhub<span class="hp-logo-dot">.</span></span></a>
<p>Ключи и конфигурации v2raytun для всех устройств — ПК, Android, iPhone, Mac и Smart TV. Быстрый доступ по email или в Telegram.</p>
{cta()}</div>{cols}</div>
<div class="hp-fbot"><span>© 2026 2rayhub.com</span><span>v2raytun · ключи · конфиги · подписка</span></div>
</div></footer></body></html>"""

def bc_ld(pairs):
    import json as _j
    ld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(pairs)]}
    return f'<script type="application/ld+json">{_j.dumps(ld,ensure_ascii=False)}</script>'

def site_ld():
    import json as _j
    org = {"@context":"https://schema.org","@type":"Organization","name":"2rayhub",
           "url":BASE+"/","logo":BASE+"/og.png","description":"Ключи и конфигурации v2raytun для всех устройств."}
    web = {"@context":"https://schema.org","@type":"WebSite","name":"2rayhub","url":BASE+"/","inLanguage":"ru"}
    return (f'<script type="application/ld+json">{_j.dumps(org,ensure_ascii=False)}</script>'
            f'<script type="application/ld+json">{_j.dumps(web,ensure_ascii=False)}</script>')

def hero():
    quick = [("Скачать","/skachat/"),("Ключи","/klyuchi/"),("Тарифы","#tarify"),("Настройка","/nastrojka/"),
             ("Конфиги","/konfig/"),("Не работает","/oshibki/"),("GitHub","/github/"),("FAQ","/voprosy/")]
    qn = "".join(f'<a href="{u}">{esc(t)}</a>' for t,u in quick)
    dev = """<div class="hp-devices" aria-hidden="true">
<div class="hp-dv"><div class="hp-dv-bar"><span class="hp-dv-dot r"></span><span class="hp-dv-dot y"></span><span class="hp-dv-dot g"></span><span class="hp-dv-ttl">Android</span></div>
<div class="hp-dv-body"><div class="hp-dv-line">v2raytun.apk</div><div class="hp-dv-line k">vless://…@de1 · reality</div><div class="hp-dv-line">скорость: без лимита</div></div></div>
<div class="hp-dv hp-dv-center"><div class="hp-dv-bar"><span class="hp-dv-dot r"></span><span class="hp-dv-dot y"></span><span class="hp-dv-dot g"></span><span class="hp-dv-ttl">v2raytun · подключение</span></div>
<div class="hp-dv-body"><div class="hp-dv-st"><i></i><b>Подключено</b><span>42 ms</span></div>
<div class="hp-dv-line k">ключ активен · VLESS Reality</div>
<div class="hp-dv-line">sni: cloudflare.com · tcp</div>
<div class="hp-dv-stat"><div><b>6</b><span>локаций</span></div><div><b>3</b><span>устройства</span></div><div><b>∞</b><span>трафик</span></div><div><b>1 мин</b><span>выдача</span></div></div></div></div>
<div class="hp-dv"><div class="hp-dv-bar"><span class="hp-dv-dot r"></span><span class="hp-dv-dot y"></span><span class="hp-dv-dot g"></span><span class="hp-dv-ttl">iPhone</span></div>
<div class="hp-dv-body"><div class="hp-dv-line">App Store · v2raytun</div><div class="hp-dv-line k">профиль импортирован</div><div class="hp-dv-line">статус: on</div></div></div></div>"""
    return f"""<section class="hp-hero" id="hero"><div class="hp-wrap">
<span class="hp-pill"><span class="hp-pill-dot"></span>Готовые ключи для v2raytun · VLESS Reality</span>
<h1>v2raytun — рабочие ключи и конфиги <em>за минуту</em></h1>
<p class="hp-lead">Получи готовый ключ v2raytun: вставил конфигурацию в приложение — и подключение работает. ПК (Windows 10/11), Android (APK), iPhone, Mac и Smart TV. Бесплатный пробный ключ — на email или в Telegram. Подписка без ограничений скорости — от 249 ₽.</p>
{cta(big=True)}
<div class="hp-trust"><span>Выдача за 1 минуту</span><span>VLESS Reality</span><span>Без лимита скорости</span><span>Все устройства</span></div>
<div class="hp-quicknav">{qn}</div>
{dev}
</div></section>"""

def stat():
    cells = [("422k","ищут v2raytun в месяц"),("1 мин","выдача ключа"),("5","платформ"),("0 ₽","пробный ключ")]
    c = "".join(f'<div class="hp-stats-i"><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a,b in cells)
    return f'<div class="hp-wrap"><div class="hp-stats"><div class="hp-stats-row">{c}</div></div></div>'

def bento():
    cards = [
        ("🔑","Готовые ключи","Конфигурация v2raytun выдаётся сразу — ничего настраивать вручную не нужно."),
        ("🚀","VLESS Reality","Современный протокол: стабильное соединение и высокая скорость без обрывов."),
        ("📱","Все устройства","Один ключ работает на ПК, Android, iPhone, Mac и Smart TV одновременно."),
        ("🆓","Бесплатный старт","Пробный ключ v2raytun бесплатно — проверь скорость до оплаты подписки."),
        ("♾","Без лимитов","Полная скорость и безлимитный трафик на платной подписке."),
        ("🔄","Автообновление","Подписка обновляет серверы автоматически — ключ всегда рабочий."),
    ]
    c = "".join(f'<div class="hp-feat-i"><div class="hp-feat-ico">{ic}</div><div class="hp-feat-tx"><h3>{esc(t)}</h3><p>{esc(d)}</p></div></div>' for ic,t,d in cards)
    return f'<section class="hp-sec"><div class="hp-wrap"><div class="hp-sec-head hp-sec-head--center"><span class="hp-eyebrow">Почему мы</span><h2 class="hp-h2">Почему ключи v2raytun отсюда</h2><p class="hp-sub">Готовая конфигурация, современный протокол и один ключ сразу на все устройства.</p></div><div class="hp-feat">{c}</div></div></section>'

def sections_grid():
    items = [
        ("/skachat/","💾","Скачать v2raytun","Клиент под свою систему за минуту"),
        ("/na-pk/","💻","v2raytun на ПК","Скачать для Windows 10/11"),
        ("/android/","🤖","v2raytun Android","APK для смартфона и планшета"),
        ("/ios/","🍎","v2raytun iOS","Клиент для iPhone и iPad"),
        ("/mac/","🖥️","v2raytun на Mac","macOS — Intel и Apple Silicon"),
        ("/tv/","📺","v2raytun Smart TV","APK для Android-TV"),
        ("/klyuchi/","🔑","Ключи v2raytun","Рабочие конфиги VLESS Reality"),
        ("/konfig/","🧩","Конфигурации","Готовые конфиги без настройки"),
        ("/podpiska/","🔁","Подписка","Автообновление серверов и ключей"),
        ("/besplatno/","🆓","Бесплатно","Пробный ключ без оплаты"),
        ("/nastrojka/","⚙️","Настройка","Как подключить за 4 шага"),
        ("/oshibki/","🛠️","Не работает","Решение частых проблем"),
        ("/proxy/","🌐","Прокси","VLESS Reality как прокси-туннель"),
        ("/github/","🐙","GitHub","Официальные сборки приложения"),
        ("/tarify/","💎","Тарифы","Месяц, 3, 6 месяцев и год"),
        ("/voprosy/","❓","Вопросы","FAQ по ключам v2raytun"),
    ]
    c = "".join(f'<a class="hp-card hp-card-link" href="{u}"><span class="hp-card-ic">{ic}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for u,ic,t,d in items)
    return f'<section class="hp-sec"><div class="hp-wrap"><div class="hp-sec-head hp-sec-head--center"><span class="hp-eyebrow">Навигация</span><h2 class="hp-h2">Всё о v2raytun — выбери раздел</h2><p class="hp-sub">Скачать клиент под свою систему, получить ключ, настроить или решить проблему — каждой теме посвящена отдельная страница.</p></div><div class="hp-cards">{c}</div></div></section>'

DL = {"ios":"https://apps.apple.com/app/v2raytun/id6476628951",
      "android":"https://play.google.com/store/apps/details?id=com.v2raytun.android",
      "github":"https://github.com/DigneZzZ/v2raytun/releases"}
def downloads(title="Скачать приложение v2raytun", note=True):
    btns = [("📱","App Store","iPhone · iPad",DL["ios"]),
            ("🤖","Google Play","Android",DL["android"]),
            ("💻","GitHub","Windows · Mac · APK",DL["github"])]
    c = "".join(f'<a class="hp-plat-i" href="{u}" target="_blank" rel="nofollow noopener"><span class="ic">{ic}</span><b>{esc(t)}</b><small>{esc(s)}</small></a>' for ic,t,s,u in btns)
    n = '<p class="hp-sub">Скачай официальное приложение под свою систему, затем нажми «Получить ключ» — конфигурация придёт за минуту.</p>' if note else ''
    return f'<section class="hp-sec hp-sec-tight" id="download"><div class="hp-wrap"><div class="hp-sec-head hp-sec-head--center"><span class="hp-eyebrow">Загрузка</span><h2 class="hp-h2">{esc(title)}</h2>{n}</div><div class="hp-plat hp-plat-3">{c}</div></div></section>'

PLAN_FEATS = ["1 профиль на 3 устройства","6 локаций · Европа и США","Без лимита на трафик","Замена сервера бесплатно"]
PLANS = [("На месяц","249 ₽","Стартовый","Базовая цена",PLAN_FEATS,False),
         ("На 3 месяца","599 ₽","Выгодный старт","Экономия 20%",PLAN_FEATS,False),
         ("На полгода","1090 ₽","Оптимальный","Экономия 27%",PLAN_FEATS,True),
         ("Год","1890 ₽","Максимум выгоды","Экономия 37%",PLAN_FEATS,False)]
def tariffs():
    c=""
    for name,price,tier,econ,feats,hit in PLANS:
        fl="".join(f'<li>{esc(f)}</li>' for f in feats)
        badge='<span class="hp-plan-badge">Чаще берут</span>' if hit else ""
        c+=f'<div class="hp-plan{" hp-plan-hit" if hit else ""}">{badge}<div class="hp-plan-tier">{esc(tier)}</div><h3>{esc(name)}</h3><div class="hp-price">{esc(price)}</div><div class="hp-price-sub">{esc(econ)}</div><ul>{fl}</ul><a class="hp-btn hp-btn-block" href="{LK}" rel="nofollow noopener">Купить ключ</a></div>'
    import json as _j
    ld={"@context":"https://schema.org","@type":"Product","name":"Ключ v2raytun","description":"Ключи и подписка v2raytun",
        "offers":{"@type":"AggregateOffer","priceCurrency":"RUB","lowPrice":"249","highPrice":"1890","offerCount":"4"}}
    return f'<section class="hp-sec" id="tarify"><div class="hp-wrap"><div class="hp-sec-head hp-sec-head--center"><span class="hp-eyebrow">Тарифы</span><h2 class="hp-h2">Тарифы на ключи v2raytun</h2><p class="hp-sub">Пробный ключ — бесплатно. Подписка — от 249 ₽: чем дольше период, тем дешевле.</p></div><div class="hp-plans">{c}</div></div></section><script type="application/ld+json">{_j.dumps(ld,ensure_ascii=False)}</script>'

def page(slug, title, desc, h1, body, cluster=None, faqs=None, dl=False):
    path = "/" if slug == "" else f"/{slug}/"
    parts = [head(title, desc, path), header(), '<main>']
    if slug == "":
        parts += [hero(), stat(), bento(), tariffs(), sections_grid(), downloads()]
        if body: parts.append(f'<section class="hp-sec hp-sec-tight"><div class="hp-wrap hp-prose">{body}</div></section>')
        if cluster: parts.append(chips(cluster))
    else:
        parts.append(f'<section class="hp-page-h"><div class="hp-wrap"><nav class="hp-bc"><a href="/">Главная</a> <span class="sep">/</span> <span>{esc(h1)}</span></nav><h1>{esc(h1)}</h1></div></section>')
        parts.append(f'<section class="hp-sec"><div class="hp-wrap hp-prose">{body}</div></section>')
        if slug == "tarify": parts.append(tariffs())
        if dl: parts.append(downloads())
        parts.append(midcta())
        if cluster: parts.append(chips(cluster))
    if faqs: parts.append(faq(faqs))
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
    li="".join(f'<div class="hp-step"><div class="hp-step-n"></div><div class="hp-step-tx"><h3>{esc(t)}</h3><p>{esc(d)}</p></div></div>' for t,d in items)
    return f'<div class="hp-steps">{li}</div>'
def midcta():
    return f"""<section class="hp-cta-mid"><div class="hp-cta-mid-in">
<div class="hp-cta-mid-tx">Получи рабочий ключ v2raytun за минуту</div>
<div class="hp-cta-mid-sub">Пробный ключ — бесплатно, на email или в Telegram. Подписка без лимита скорости — от 249 ₽.</div>
{cta()}</div></section>"""

PAGES = []
# Главная
PAGES.append(dict(slug="", title="Ключи v2raytun — скачать и получить конфиг | 2rayhub",
    desc="Рабочие ключи v2raytun для ПК, Android, iPhone, Mac и TV. Бесплатный пробный ключ, конфигурации VLESS Reality, подписка от 249 ₽.",
    h1="", cluster="Общее",
    body=prose(
        "<b>v2raytun</b> — это приложение-клиент для протокола VLESS/Reality, в которое нужно вставить ключ (конфигурацию) сервера. На 2rayhub.com ты получаешь рабочий ключ v2raytun сразу: на email или в Telegram. Не нужно искать конфиги по форумам — вставил строку в приложение и подключение готово.",
        "Ключи подходят для всех версий v2raytun: на ПК и Windows, на Android (APK), на iPhone и iPad, на Mac и Smart TV. Есть бесплатный пробный ключ, чтобы проверить скорость, и подписка без ограничений.")+
        h2("Приложение v2raytun: куда вставить ключ")+prose("Приложение v2raytun — это клиент, который читает ключ-конфигурацию и устанавливает подключение. Скачай приложение под свою систему, вставь полученный ключ — и v2raytun сам поднимет соединение, без ручной настройки серверов."),
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
    body=prose("Пробный ключ v2raytun — бесплатно. Для постоянного использования выбери подписку: чем дольше период, тем дешевле месяц.","Все тарифы включают один профиль на 3 устройства, 6 локаций (Европа и США), безлимитный трафик и бесплатную замену сервера."),
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
        blocks+=f'<div class="hp-chip-group"><h3>{esc(cl)}</h3><ul class="hp-chip-list">{li}</ul></div>'
    body=prose("Список самых частотных запросов по бренду v2raytun, по которым мы помогаем найти рабочие ключи и конфигурации. Сгруппировано по темам.")+f'<div class="hp-zaprosy">{blocks}</div>'
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
          "author":{"@type":"Organization","name":"2rayhub"},
          "publisher":{"@type":"Organization","name":"2rayhub"}}
    parts = [head(a["title"], a["desc"], path, og_type="article"), header(), '<main>',
        f'<section class="hp-page-h"><div class="hp-wrap"><nav class="hp-bc"><a href="/">Главная</a> <span class="sep">/</span> <a href="/blog/">Блог</a> <span class="sep">/</span> <span>{esc(a["title"])}</span></nav><h1>{esc(a["title"])}</h1><span class="hp-bdate">{esc(a["date"])}</span></div></section>',
        f'<section class="hp-sec"><div class="hp-wrap hp-prose">{a["body"]}</div></section>',
        midcta(),
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
        cards += f'<a class="hp-card hp-card-link" href="/blog/{a["slug"]}/"><span class="hp-bdate">{esc(a["date"])}</span><h3>{esc(a["title"])}</h3><p>{esc(a["excerpt"])}</p><span class="hp-blink">Читать →</span></a>'
    ld = {"@context":"https://schema.org","@type":"Blog","name":"Блог v2raytun","url":BASE+"/blog/",
          "blogPost":[{"@type":"BlogPosting","headline":a["title"],"datePublished":a["date"],"url":BASE+f"/blog/{a['slug']}/"} for a in ARTICLES]}
    parts = [head("Блог v2raytun — статьи о ключах и настройке",
                  "Блог v2raytun: статьи о ключах, конфигурациях, настройке и подписке для всех устройств.","/blog/"),
        header(), '<main>',
        '<section class="hp-page-h"><div class="hp-wrap"><nav class="hp-bc"><a href="/">Главная</a> <span class="sep">/</span> <span>Блог</span></nav><h1>Блог v2raytun</h1></div></section>',
        f'<section class="hp-sec"><div class="hp-wrap"><div class="hp-cards">{cards}</div></div></section>',
        f'<script type="application/ld+json">{_j.dumps(ld,ensure_ascii=False)}</script>',
        bc_ld([("Главная",BASE+"/"),("Блог",BASE+"/blog/")]),
        footer()]
    d = os.path.join(OUT, "blog"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write("\n".join(parts))
    return "/blog/"

CSS = open(os.path.join(ROOT,"style_v3.css"),encoding="utf-8").read()

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
        paths.append(page(p["slug"], p["title"], p["desc"], p["h1"], p["body"], p.get("cluster"), p.get("faqs"), p.get("dl", False)))
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
