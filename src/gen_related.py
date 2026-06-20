# Regenerates related.py (keyword chips per page) from v2raytun_core.xlsx.
# Chips show keyword text only (answers no longer rendered).
import openpyxl, re
XLSX = "/root/.claude-lab/pfseopapa/v2raytun_core.xlsx"
N = 40
wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
ws = wb["v2raytun (расшир., без vpn)"]
rows = [(int(f or 0), str(q).strip(), str(c).strip())
        for f,q,c in list(ws.iter_rows(values_only=True))[1:] if q]
rows.sort(key=lambda r: -r[0])

# primary cluster -> page
CLUSTER_PAGE = {
    'Общее': '/',
    'Бренд/офиц/github': '/',
    'Скачать': '/skachat-v2raytun/',
    'Бесплатно': '/skachat-v2raytun/',
    'Прокси/proxy': '/podpiska/',
    'Ключи/конфиги/сервера': '/konfigi/',
    'Настройка/как': '/podklyuchenie/',
    'ПК/Windows': '/pk/',
    'Mac': '/pk/',
    'Android': '/android/',
    'iOS': '/ios/',
    'TV': '/tv/',
    'Не работает/ошибки': '/problemy/',
}
# keyword-filter pages (no dedicated cluster)
IOS = re.compile(r'\b(ios|айфон|iphone|ipad|айпад|эпл|apple)\b', re.I)
TV  = re.compile(r'(\btv\b|телевизор|приставк|смарт.?тв|android tv|androidtv|тиви)', re.I)

def cap(q): return q[0].upper()+q[1:] if q else q

pages = {u: [] for u in ['/','/skachat-v2raytun/','/podpiska/','/konfigi/',
            '/podklyuchenie/','/pk/','/android/','/ios/','/tv/','/problemy/','/faq/']}
seen = {u: set() for u in pages}

def add(u, q):
    k=q.lower()
    if k in seen[u] or len(pages[u])>=N: return
    seen[u].add(k); pages[u].append(cap(q))

# filter pages first (highest-freq matches)
for f,q,c in rows:
    if IOS.search(q): add('/ios/', q)
    if TV.search(q):  add('/tv/', q)
# cluster pages
for f,q,c in rows:
    u = CLUSTER_PAGE.get(c)
    if u: add(u, q)
# faq: top up with broad top queries if under N
for f,q,c in rows:
    add('/faq/', q)

out = ["# auto-generated from v2raytun_core.xlsx (top by frequency, per-cluster -> page)",
       "# regenerate: python gen_related.py  (chips: keyword text only)",
       "RELATED = {"]
for u in pages:
    out.append(f"    {u!r}: [")
    for q in pages[u]:
        out.append(f"        {q!r},")
    out.append("    ],")
out.append("}")
open("related.py","w",encoding="utf-8").write("\n".join(out)+"\n")
print("counts:", {u:len(v) for u,v in pages.items()})
