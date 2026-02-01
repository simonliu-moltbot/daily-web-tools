#!/usr/bin/env python3
import os, glob, json, re
from datetime import datetime

# ==========================================
# Configuration
# ==========================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DASHBOARD_ROOT = SCRIPT_DIR

GITHUB_USER = "simonliu-moltbot"
GITHUB_BASE = f"https://github.com/{GITHUB_USER}"
BASE_URL = "https://simonliu-moltbot.github.io/daily-web-tools/"
ENTRY_URL = "https://simonliu-moltbot.github.io/"

TRANSLATIONS = {
    "nav_home": {"en": "Home", "zh": "首頁"},
    "nav_tools": {"en": "Web Tools", "zh": "工具集"},
    "nav_gallery": {"en": "AI Gallery", "zh": "藝術畫廊"},
    "nav_mcp": {"en": "MCP Services", "zh": "MCP 服務"},
    "nav_adk": {"en": "ADK Agents", "zh": "ADK 代理"},
    "footer_built": {"en": "Built with ❤️ by AI Agent", "zh": "由 AI Agent 打造"},
    "footer_updated": {"en": "Last Updated", "zh": "最後更新"},
    "search_placeholder": {"en": "Search projects...", "zh": "檢索項目..."},
    "btn_view": {"en": "View", "zh": "進入"},
}

# ==========================================
# Template (Vanilla CSS only, NO @apply)
# ==========================================

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} | SimonLiu OpenClaw Works</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', 'Noto Sans TC', sans-serif; background-color: #faf9f6; color: #44403c; }}
        .glass-panel {{ background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(231, 229, 228, 0.5); }}
        .muji-table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 0.875rem; }}
        .muji-table th {{ padding: 1rem; font-weight: 500; color: #a8a29e; border-bottom: 1px solid #e7e5e4; text-transform: uppercase; letter-spacing: 0.1em; font-size: 10px; }}
        .muji-table td {{ padding: 1rem; border-bottom: 1px solid #f5f5f4; vertical-align: middle; }}
        .muji-table tr:hover td {{ background-color: rgba(250, 249, 246, 0.5); }}
        .btn-toggle {{ padding: 0.375rem 0.75rem; border-radius: 0.375rem; font-size: 0.875rem; transition: all 0.2s; }}
        .btn-toggle.active {{ background-color: #292524; color: white; }}
        .btn-toggle:not(.active) {{ color: #78716c; }}
        .btn-toggle:not(.active):hover {{ background-color: #e7e5e4; }}
    </style>
    <script>
        const PROJECT_DATA = {project_json};
        const TRANSLATIONS = {trans_json};
    </script>
</head>
<body class="min-h-screen flex flex-col selection:bg-stone-200">

    <nav class="sticky top-0 z-50 glass-panel">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
            <a href="{dashboard_url}" class="text-lg font-bold tracking-tight text-stone-900">
                SimonLiu OpenClaw Works
            </a>
            <div class="hidden md:flex space-x-1">
                {nav_links}
            </div>
            <div class="flex items-center gap-3">
                <button id="lang-toggle" class="text-[10px] font-bold bg-stone-100 px-2.5 py-1.5 rounded-full border border-stone-200 hover:bg-stone-200 transition-colors">
                    EN / 中文
                </button>
                <button id="mobile-menu-btn" class="md:hidden p-1 text-stone-500 hover:text-stone-900">
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
                </button>
            </div>
        </div>
        <div id="mobile-menu" class="hidden md:hidden border-t border-stone-100 bg-white/95 backdrop-blur-sm px-2 py-3 space-y-1">
            {mobile_nav_links}
        </div>
    </nav>

    <header class="bg-white border-b border-stone-100 pt-16 pb-12 px-4 text-center">
        <h1 class="text-4xl font-light text-stone-900 mb-4 tracking-tight" data-i18n-zh="{title_zh}" data-i18n-en="{title_en}">{title_en}</h1>
        <p class="max-w-2xl mx-auto text-lg text-stone-500 font-light leading-relaxed" data-i18n-zh="{desc_zh}" data-i18n-en="{desc_en}">{desc_en}</p>
        <div class="mt-10 max-w-xl mx-auto flex flex-col sm:flex-row gap-4 items-center justify-center {hide_controls}">
            <div class="relative w-full">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="h-5 w-5 text-stone-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0" stroke-width="2"/></svg>
                </div>
                <input type="text" id="search-input" class="block w-full pl-10 pr-3 py-2.5 border border-stone-200 rounded-lg bg-stone-50 text-sm focus:outline-none focus:ring-1 focus:ring-stone-400 transition-colors">
            </div>
            <div class="flex items-center bg-stone-100 p-1 rounded-lg border border-stone-200 shrink-0">
                <button id="view-grid" class="btn-toggle" onclick="setView('grid')"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" stroke-width="2"/></svg></button>
                <button id="view-table" class="btn-toggle" onclick="setView('table')"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16" stroke-width="2"/></svg></button>
            </div>
        </div>
    </header>

    <main class="flex-1 w-full max-w-7xl mx-auto px-4 py-12"><div id="projects-container"></div><div id="empty-state" class="hidden text-center py-20 text-stone-400 text-lg">No projects found.</div></main>

    <footer class="bg-white border-t border-stone-200 py-12 text-center text-sm text-stone-400">
        <p data-i18n-key="footer_built">Built with ❤️ by AI Agent</p>
        <p class="mt-2"><span data-i18n-key="footer_updated">Last Updated</span>: {date}</p>
    </footer>

    <script>
        let currentLang = localStorage.getItem('lang') || 'en', currentView = localStorage.getItem('view') || 'grid', searchQuery = '';
        const container = document.getElementById('projects-container'), empty = document.getElementById('empty-state'), searchInput = document.getElementById('search-input');

        function init() {{
            updateLangUI(); updateViewUI();
            if (searchInput) searchInput.addEventListener('input', e => {{ searchQuery = e.target.value.toLowerCase(); render(); }});
            document.getElementById('lang-toggle').addEventListener('click', () => {{ currentLang = currentLang==='zh'?'en':'zh'; localStorage.setItem('lang', currentLang); updateLangUI(); render(); }});
            document.getElementById('mobile-menu-btn').addEventListener('click', () => document.getElementById('mobile-menu').classList.toggle('hidden'));
        }}

        function render() {{
            const filtered = PROJECT_DATA.filter(p => {{
                const term = searchQuery.toLowerCase();
                return (p.title_en + p.title_zh + p.desc_en + p.desc_zh).toLowerCase().includes(term);
            }});
            if (!filtered.length) {{ container.innerHTML = ''; empty.classList.remove('hidden'); return; }}
            empty.classList.add('hidden');
            if (currentView === 'grid') renderGrid(filtered); else renderTable(filtered);
        }}

        function renderGrid(projects) {{
            container.className = 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6';
            container.innerHTML = projects.map(p => {{
                const t = currentLang==='zh'?(p.title_zh||p.title_en):(p.title_en||p.title_zh), d = currentLang==='zh'?(p.desc_zh||p.desc_en):(p.desc_en||p.desc_zh);
                const visual = p.image ? `<div class="h-48 overflow-hidden"><img src="${{p.image}}" class="w-full h-full object-cover transition-transform group-hover:scale-105"></div>` : `<div class="h-32 flex items-center justify-center text-4xl bg-stone-100">${{p.icon||'📦'}}</div>`;
                return `<div class="bg-white rounded-xl border border-stone-200 overflow-hidden flex flex-col group shadow-sm hover:shadow-md transition-all">
                    ${{visual}}<div class="p-5 flex flex-col flex-1"><h3 class="text-lg font-bold text-stone-800 mb-2">${{t}}</h3><p class="text-xs text-stone-500 line-clamp-3 mb-5">${{d}}</p>
                    <div class="mt-auto pt-4 border-t border-stone-50 flex items-center justify-between"><span class="text-[10px] font-mono text-stone-400 uppercase">${{p.type}}</span>
                    <a href="${{p.link}}" target="${{p.target||'_blank'}}" class="text-xs font-bold text-stone-900 hover:text-stone-500">${{TRANSLATIONS.btn_view[currentLang]}} &rarr;</a></div></div></div>`;
            }}).join('');
        }}

        function renderTable(projects) {{
            container.className = 'overflow-x-auto bg-white rounded-xl border border-stone-200 shadow-sm';
            const h = currentLang==='zh'?['圖標','名稱','描述','操作']:['Icon','Name','Description','Action'];
            container.innerHTML = `<table class="muji-table"><thead><tr><th class="w-12 text-center">${{h[0]}}</th><th class="w-1/4">${{h[1]}}</th><th>${{h[2]}}</th><th class="w-24 text-center">${{h[3]}}</th></tr></thead><tbody>` + 
                projects.map(p => {{
                    const t = currentLang==='zh'?(p.title_zh||p.title_en):(p.title_en||p.title_zh), d = currentLang==='zh'?(p.desc_zh||p.desc_en):(p.desc_en||p.desc_zh);
                    const icon = p.image ? `<img src="${{p.image}}" class="w-8 h-8 rounded object-cover mx-auto">` : `<span class="text-xl">${{p.icon||'📦'}}</span>`;
                    return `<tr><td class="text-center">${{icon}}</td><td class="font-medium text-stone-800">${{t}}</td><td class="text-stone-500 text-xs">${{d}}</td><td class="text-center">
                    <a href="${{p.link}}" target="${{p.target||'_blank'}}" class="text-[11px] font-bold text-stone-600 hover:text-stone-900 underline underline-offset-4 decoration-stone-200">${{TRANSLATIONS.btn_view[currentLang]}}</a></td></tr>`;
                }}).join('') + '</tbody></table>';
        }}

        function setView(m) {{ currentView=m; localStorage.setItem('view',m); updateViewUI(); }}
        function updateViewUI() {{
            document.getElementById('view-grid').classList.toggle('active', currentView==='grid');
            document.getElementById('view-table').classList.toggle('active', currentView==='table');
            render();
        }}
        function updateLangUI() {{
            document.documentElement.lang = currentLang==='zh'?'zh-TW':'en';
            document.getElementById('lang-toggle').textContent = currentLang==='zh'?'EN':'中文';
            document.querySelectorAll('[data-i18n-key]').forEach(el => {{ el.textContent = TRANSLATIONS[el.dataset.i18nKey][currentLang]; }});
            document.querySelectorAll('[data-i18n-zh]').forEach(el => {{ el.textContent = currentLang==='zh'?el.dataset.i18nZh:el.dataset.i18nEn; }});
            if (searchInput) searchInput.placeholder = TRANSLATIONS.search_placeholder[currentLang];
        }}
        init();
    </script>
</body>
</html>
"""

def get_nav_links(active_page):
    links = [("nav_home", ENTRY_URL), ("nav_tools", "web-tools/index.html"), ("nav_gallery", "gallery/index.html"), ("nav_mcp", "mcp/index.html"), ("nav_adk", "adk/index.html")]
    html, mob = [], []
    for k, u in links:
        is_a = (k == f"nav_{active_page}")
        cls = "text-stone-900 bg-stone-100 font-bold" if is_a else "text-stone-500 hover:text-stone-900"
        url = u if "://" in u else BASE_URL + u
        html.append(f'<a href="{url}" class="px-3 py-2 rounded-md text-xs font-medium transition-colors {cls}" data-i18n-key="{k}">{TRANSLATIONS[k]["en"]}</a>')
        mob.append(f'<a href="{url}" class="block px-3 py-2 rounded-md text-sm font-medium {cls}" data-i18n-key="{k}">{TRANSLATIONS[k]["en"]}</a>')
    return "\n".join(html), "\n".join(mob)

def extract_tool_metadata(tool_dir):
    index_path = os.path.join(tool_dir, "index.html")
    if not os.path.exists(index_path): return None
    with open(index_path, "r", encoding="utf-8") as f: content = f.read()
    tm = re.search(r'<title>(.*?)</title>', content)
    ft = tm.group(1) if tm else os.path.basename(tool_dir)
    tz, te = (ft.split("|") + [ft])[:2] if "|" in ft else (ft, ft)
    dm = re.search(r'<meta name="description" content="(.*?)">', content)
    d = dm.group(1) if dm else "Tool"
    return {"title_zh": tz.strip().replace("📅","").strip(), "title_en": te.strip(), "desc_zh": d, "desc_en": d, "link": f"../tools/{os.path.basename(tool_dir)}/index.html", "type": "Tool", "icon": "🛠️"}

def scan_tools():
    tools_dir = os.path.join(DASHBOARD_ROOT, "tools")
    res = []
    if os.path.exists(tools_dir):
        for n in os.listdir(tools_dir):
            path = os.path.join(tools_dir, n)
            if os.path.isdir(path) and os.path.exists(os.path.join(path, "index.html")):
                meta = extract_tool_metadata(path)
                if meta: res.append(meta)
    return sorted(res, key=lambda x: x['title_en'])

def scan_gallery():
    g_dir = os.path.join(DASHBOARD_ROOT, "gallery/images")
    res = []
    if os.path.exists(g_dir):
        for n in os.listdir(g_dir):
            if n.lower().endswith(('.png','.jpg','.jpeg','.webp')):
                pts = os.path.splitext(n)[0].split('-')
                dt = "-".join(pts[:3]) if len(pts)>3 else ""
                ti = " ".join(pts[3:] if len(pts)>3 else pts).title()
                res.append({"title_zh": ti, "title_en": ti, "desc_zh": f"生成於 {dt}", "desc_en": f"Generated on {dt}", "link": f"images/{n}", "image": f"images/{n}", "type": "Art", "target": "_blank"})
    return sorted(res, key=lambda x: x['desc_en'], reverse=True)

def scan_repos(prefix, type_label, icon):
    res = []
    for path in glob.glob(os.path.join(PROJECTS_ROOT, f"{prefix}*")):
        if os.path.isdir(path):
            n = os.path.basename(path)
            c = n.replace(prefix, "").replace("-", " ").title()
            res.append({"title_zh": c, "title_en": c, "desc_zh": f"{type_label} Project: {c}", "desc_en": f"{type_label} Project: {c}", "link": f"{GITHUB_BASE}/{n}", "type": type_label, "icon": icon})
    return sorted(res, key=lambda x: x['title_en'])

def generate_page(out, key, data, header_info=None, hide=""):
    hdrs = {
        "home": {"title_zh": "SimonLiu OpenClaw Works", "title_en": "SimonLiu OpenClaw Works", "desc_zh": "AI 中心樞紐。", "desc_en": "AI Central Hub."},
        "tools": {"title_zh": "🇹🇼 台灣日常工具集", "title_en": "🇹🇼 Daily Taiwan Web Tools", "desc_zh": "解決台灣生活痛點的實用小工具。", "desc_en": "Useful tools for daily life in Taiwan."},
        "gallery": {"title_zh": "藝術畫廊", "title_en": "AI Gallery", "desc_zh": "AI 藝術。", "desc_en": "AI Art."},
        "mcp": {"title_zh": "MCP 服務", "title_en": "MCP Services", "desc_zh": "後端服務。", "desc_en": "Backend services."},
        "adk": {"title_zh": "ADK 代理人", "title_en": "ADK Agents", "desc_zh": "自主代理。", "desc_en": "Autonomous agents."}
    }
    h = header_info or hdrs.get(key, hdrs['home'])
    nav, mob = get_nav_links(key)
    html = PAGE_TEMPLATE.format(
        page_title=h['title_en'], title_zh=h['title_zh'], title_en=h['title_en'],
        desc_zh=h['desc_zh'], desc_en=h['desc_en'], dashboard_url=BASE_URL + "index.html",
        nav_links=nav, mobile_nav_links=mob, project_json=json.dumps(data, ensure_ascii=False),
        trans_json=json.dumps(TRANSLATIONS, ensure_ascii=False),
        date=datetime.now().strftime("%Y-%m-%d"), hide_controls=hide
    )
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f: f.write(html)

def main():
    tools, gallery = scan_tools(), scan_gallery()
    mcp = scan_repos("mcp-", "MCP", "🔌")
    adk = scan_repos("adk-", "ADK", "🤖")
    generate_page(os.path.join(DASHBOARD_ROOT, "web-tools/index.html"), "tools", tools)
    generate_page(os.path.join(DASHBOARD_ROOT, "gallery/index.html"), "gallery", gallery)
    generate_page(os.path.join(DASHBOARD_ROOT, "mcp/index.html"), "mcp", mcp)
    generate_page(os.path.join(DASHBOARD_ROOT, "adk/index.html"), "adk", adk)
    p = [
        {"title_en": "Web Tools", "title_zh": "網頁工具", "desc_en": "Daily tools.", "desc_zh": "日常工具。", "link": "web-tools/index.html", "icon": "🛠️", "type": "Section", "target": "_self"},
        {"title_en": "AI Gallery", "title_zh": "AI 藝廊", "desc_en": "AI art.", "desc_zh": "AI 藝術。", "link": "gallery/index.html", "icon": "🎨", "type": "Section", "target": "_self"},
        {"title_en": "MCP Services", "title_zh": "MCP 服務", "desc_en": "Backend.", "desc_zh": "後端服務。", "link": "mcp/index.html", "icon": "🔌", "type": "Section", "target": "_self"},
        {"title_en": "ADK Agents", "title_zh": "ADK 代理人", "desc_en": "Agents.", "desc_zh": "代理人。", "link": "adk/index.html", "icon": "🤖", "type": "Section", "target": "_self"}
    ]
    generate_page(os.path.join(DASHBOARD_ROOT, "index.html"), "home", p, hide="hidden")

if __name__ == "__main__": main()
