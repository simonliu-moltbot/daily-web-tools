#!/usr/bin/env python3
import os, glob, json, re
from datetime import datetime

# ==========================================
# Configuration & Constants
# ==========================================

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DASHBOARD_ROOT = SCRIPT_DIR

GITHUB_USER = "simonliu-moltbot"
GITHUB_BASE = f"https://github.com/{GITHUB_USER}"

# Absolute Links as requested
ROOT_URL = "https://simonliu-moltbot.github.io/"
DASHBOARD_URL = "https://simonliu-moltbot.github.io/daily-web-tools/index.html"

# Translations
TRANSLATIONS = {
    "nav_home": {"en": "Home", "zh": "首頁"},
    "nav_tools": {"en": "Web Tools", "zh": "工具集"},
    "nav_gallery": {"en": "AI Gallery", "zh": "藝術畫廊"},
    "nav_mcp": {"en": "MCP Services", "zh": "MCP 服務"},
    "nav_adk": {"en": "ADK Agents", "zh": "ADK 代理"},
    "footer_built": {"en": "Built with ❤️ by AI Agent", "zh": "由 AI Agent 打造"},
    "footer_updated": {"en": "Last Updated", "zh": "最後更新"},
    "search_placeholder": {"en": "Search projects...", "zh": "檢索項目..."},
    "view_grid": {"en": "Grid", "zh": "網格"},
    "view_table": {"en": "Table", "zh": "列表"},
    "btn_view": {"en": "View", "zh": "進入"},
}

# ==========================================
# HTML Templates (Nordic/Muji Style)
# ==========================================

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} | SimonLiu OpenClaw Works</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', 'Noto Sans TC', sans-serif;
            background-color: #faf9f6;
            color: #44403c;
        }}
        .glass-panel {{
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(12px);
            border-b: 1px solid rgba(231, 229, 228, 0.5);
        }}
        .card-hover {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .card-hover:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        }}
        .btn-toggle {{
            @apply px-3 py-1.5 rounded-md text-sm transition-all duration-200;
        }}
        .btn-toggle.active {{
            @apply bg-stone-800 text-white shadow-sm;
        }}
        .btn-toggle:not(.active) {{
            @apply text-stone-500 hover:bg-stone-200;
        }}
        
        /* Proper Table Styles */
        .muji-table {{
            @apply w-full border-collapse text-left text-sm;
        }}
        .muji-table th {{
            @apply py-4 px-4 font-medium text-stone-400 border-b border-stone-200 uppercase tracking-widest text-[10px];
        }}
        .muji-table td {{
            @apply py-4 px-4 border-b border-stone-100 align-middle;
        }}
        .muji-table tr:hover td {{
            @apply bg-stone-50/50;
        }}
    </style>
    <script>
        const PROJECT_DATA = {project_json};
        const TRANSLATIONS = {trans_json};
    </script>
</head>
<body class="min-h-screen flex flex-col selection:bg-stone-200 selection:text-stone-900">

    <!-- Navbar -->
    <nav class="sticky top-0 z-50 glass-panel">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Logo: Always links to Dashboard Index -->
                <div class="flex-shrink-0 flex items-center">
                    <a href="{dashboard_url}" class="text-lg font-semibold tracking-wide flex items-center gap-2 text-stone-800">
                        SimonLiu <span class="text-stone-400 font-light">OpenClaw Works</span>
                    </a>
                </div>

                <!-- Desktop Nav -->
                <div class="hidden md:flex space-x-1">
                    {nav_links}
                </div>

                <!-- Right Side: Lang & Mobile Menu -->
                <div class="flex items-center gap-4">
                    <button id="lang-toggle" class="text-[10px] font-bold bg-stone-100 hover:bg-stone-200 text-stone-600 px-3 py-1.5 rounded-full transition-colors border border-stone-200">
                        EN / 中文
                    </button>
                    <button id="mobile-menu-btn" class="md:hidden p-2 rounded-md text-stone-500 hover:text-stone-900">
                        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Mobile Menu -->
        <div id="mobile-menu" class="hidden md:hidden border-t border-stone-200 bg-white/95 backdrop-blur-sm">
            <div class="px-2 pt-2 pb-3 space-y-1">
                {mobile_nav_links}
            </div>
        </div>
    </nav>

    <!-- Header -->
    <header class="bg-white border-b border-stone-100 pt-16 pb-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-7xl mx-auto text-center">
            <h1 class="text-4xl font-light text-stone-900 mb-4 tracking-tight" data-i18n-zh="{title_zh}" data-i18n-en="{title_en}">
                {title_en}
            </h1>
            <p class="max-w-2xl mx-auto text-lg text-stone-500 font-light leading-relaxed" data-i18n-zh="{desc_zh}" data-i18n-en="{desc_en}">
                {desc_en}
            </p>

            <!-- Controls -->
            <div class="mt-10 max-w-xl mx-auto flex flex-col sm:flex-row gap-4 items-center justify-center {hide_controls}">
                <div class="relative w-full">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-stone-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0" />
                        </svg>
                    </div>
                    <input type="text" id="search-input" 
                           class="block w-full pl-10 pr-3 py-2.5 border border-stone-200 rounded-lg bg-stone-50 text-sm focus:outline-none focus:bg-white focus:ring-1 focus:ring-stone-400 transition-colors"
                           placeholder="Search projects...">
                </div>
                
                <div class="flex items-center bg-stone-100 p-1 rounded-lg border border-stone-200 shrink-0">
                    <button id="view-grid" class="btn-toggle active" onclick="setView('grid')">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
                    </button>
                    <button id="view-table" class="btn-toggle" onclick="setView('table')">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <!-- Main -->
    <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div id="projects-container"></div>
        <div id="empty-state" class="hidden text-center py-20">
            <p class="text-stone-400 text-lg">No projects found.</p>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-stone-200 mt-auto py-12 text-center text-sm text-stone-400">
        <p data-i18n-key="footer_built">Built with ❤️ by AI Agent</p>
        <p class="mt-2"><span data-i18n-key="footer_updated">Last Updated</span>: {date}</p>
    </footer>

    <script>
        let currentLang = localStorage.getItem('lang') || 'en';
        let currentView = localStorage.getItem('view') || 'grid';
        let searchQuery = '';

        const container = document.getElementById('projects-container');
        const emptyState = document.getElementById('empty-state');
        const searchInput = document.getElementById('search-input');

        function init() {{
            updateLangUI();
            updateViewUI();
            if (searchInput) searchInput.addEventListener('input', e => {{ searchQuery = e.target.value.toLowerCase(); renderProjects(); }});
            document.getElementById('lang-toggle').addEventListener('click', toggleLang);
            document.getElementById('mobile-menu-btn').addEventListener('click', () => document.getElementById('mobile-menu').classList.toggle('hidden'));
        }}

        function renderProjects() {{
            const filtered = PROJECT_DATA.filter(p => {{
                const term = searchQuery.toLowerCase();
                return (p.title_en + p.title_zh + p.desc_en + p.desc_zh).toLowerCase().includes(term);
            }});

            if (filtered.length === 0) {{
                container.innerHTML = '';
                emptyState.classList.remove('hidden');
                return;
            }}
            emptyState.classList.add('hidden');
            if (currentView === 'grid') renderGridView(filtered); else renderTableView(filtered);
        }}

        function renderGridView(projects) {{
            container.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6';
            container.innerHTML = projects.map(p => {{
                const title = currentLang === 'zh' ? (p.title_zh || p.title_en) : (p.title_en || p.title_zh);
                const desc = currentLang === 'zh' ? (p.desc_zh || p.desc_en) : (p.desc_en || p.desc_zh);
                const visual = p.image ? 
                    `<div class="h-48 w-full bg-stone-100 overflow-hidden relative"><img src="${{p.image}}" class="w-full h-full object-cover transition-transform group-hover:scale-105"></div>` : 
                    `<div class="h-32 w-full ${{p.color || 'bg-stone-100'}} flex items-center justify-center text-4xl">${{p.icon || '📦'}}</div>`;
                
                return `<div class="project-card group bg-white rounded-xl border border-stone-200 overflow-hidden card-hover flex flex-col relative">
                    ${{visual}}
                    <div class="p-5 flex flex-col flex-1">
                        <div class="mb-auto">
                            <h3 class="text-lg font-bold text-stone-800 mb-2 group-hover:text-stone-600 transition-colors">${{title}}</h3>
                            <p class="text-xs text-stone-500 line-clamp-3">${{desc}}</p>
                        </div>
                        <div class="mt-5 pt-4 border-t border-stone-100 flex items-center justify-between">
                            <span class="text-[10px] font-mono text-stone-400 bg-stone-50 px-2 py-1 rounded border border-stone-100 uppercase">${{p.type}}</span>
                            <a href="${{p.link}}" target="${{p.target || '_blank'}}" class="text-xs font-bold text-stone-900 hover:text-stone-500 transition-colors">${{TRANSLATIONS.btn_view[currentLang]}} &rarr;</a>
                        </div>
                    </div>
                </div>`;
            }}).join('');
        }}

        function renderTableView(projects) {{
            container.className = 'overflow-x-auto bg-white rounded-xl border border-stone-200 shadow-sm';
            const headers = currentLang === 'zh' ? ['圖標', '名稱', '描述', '操作'] : ['Icon', 'Name', 'Description', 'Action'];
            
            let tableHtml = `<table class="muji-table">
                <thead><tr>
                    <th class="w-12 text-center">${{headers[0]}}</th>
                    <th class="w-1/4">${{headers[1]}}</th>
                    <th>${{headers[2]}}</th>
                    <th class="w-24 text-center">${{headers[3]}}</th>
                </tr></thead>
                <tbody>`;

            tableHtml += projects.map(p => {{
                const title = currentLang === 'zh' ? (p.title_zh || p.title_en) : (p.title_en || p.title_zh);
                const desc = currentLang === 'zh' ? (p.desc_zh || p.desc_en) : (p.desc_en || p.desc_zh);
                const icon = p.image ? `<img src="${{p.image}}" class="w-8 h-8 rounded-md object-cover mx-auto">` : `<span class="text-xl">${{p.icon || '📦'}}</span>`;
                return `<tr>
                    <td class="text-center">${{icon}}</td>
                    <td class="font-medium text-stone-800">${{title}}</td>
                    <td class="text-stone-500 text-xs">${{desc}}</td>
                    <td class="text-center">
                        <a href="${{p.link}}" target="${{p.target || '_blank'}}" class="text-[11px] font-bold text-stone-600 hover:text-stone-900 underline decoration-stone-200 underline-offset-4 transition-colors">
                            ${{TRANSLATIONS.btn_view[currentLang]}}
                        </a>
                    </td>
                </tr>`;
            }}).join('');

            container.innerHTML = tableHtml + '</tbody></table>';
        }}

        function setView(mode) {{ currentView = mode; localStorage.setItem('view', mode); updateViewUI(); }}
        function updateViewUI() {{
            document.getElementById('view-grid').classList.toggle('active', currentView === 'grid');
            document.getElementById('view-table').classList.toggle('active', currentView === 'table');
            renderProjects();
        }}
        function toggleLang() {{ currentLang = currentLang === 'zh' ? 'en' : 'zh'; localStorage.setItem('lang', currentLang); updateLangUI(); renderProjects(); }}
        function updateLangUI() {{
            document.documentElement.lang = currentLang === 'zh' ? 'zh-TW' : 'en';
            document.getElementById('lang-toggle').textContent = currentLang === 'zh' ? 'EN' : '中文';
            document.querySelectorAll('[data-i18n-key]').forEach(el => {{ el.textContent = TRANSLATIONS[el.dataset.i18nKey][currentLang]; }});
            document.querySelectorAll('[data-i18n-zh]').forEach(el => {{ el.textContent = currentLang === 'zh' ? el.dataset.i18nZh : el.dataset.i18nEn; }});
            if (searchInput) searchInput.placeholder = TRANSLATIONS.search_placeholder[currentLang];
        }}
        init();
    </script>
</body>
</html>
"""

def get_nav_links(active_page):
    links = [
        ("nav_home", ROOT_URL),
        ("nav_tools", "web-tools/index.html"),
        ("nav_gallery", "gallery/index.html"),
        ("nav_mcp", "mcp/index.html"),
        ("nav_adk", "adk/index.html"),
    ]
    html, mobile = [], []
    base = "https://simonliu-moltbot.github.io/daily-web-tools/"
    for key, url in links:
        is_active = (key == f"nav_{active_page}")
        cls = "text-stone-900 bg-stone-100 font-bold" if is_active else "text-stone-500 hover:text-stone-900"
        target_url = url if "://" in url else base + url
        html.append(f'<a href="{target_url}" class="px-3 py-2 rounded-md text-xs font-medium transition-colors {cls}" data-i18n-key="{key}">{TRANSLATIONS[key]["en"]}</a>')
        mobile.append(f'<a href="{target_url}" class="block px-3 py-2 rounded-md text-sm font-medium {cls}" data-i18n-key="{key}">{TRANSLATIONS[key]["en"]}</a>')
    return "\n".join(html), "\n".join(mobile)

def extract_tool_metadata(tool_dir):
    index_path = os.path.join(tool_dir, "index.html")
    if not os.path.exists(index_path): return None
    with open(index_path, "r", encoding="utf-8") as f: content = f.read()
    title_match = re.search(r'<title>(.*?)</title>', content)
    full_title = title_match.group(1) if title_match else os.path.basename(tool_dir)
    title_zh, title_en = (full_title.split("|") + [full_title])[:2] if "|" in full_title else (full_title, full_title)
    desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
    desc = desc_match.group(1) if desc_match else "A useful web tool."
    return {"title_zh": title_zh.strip(), "title_en": title_en.strip(), "desc_zh": desc, "desc_en": desc, "link": f"../tools/{os.path.basename(tool_dir)}/index.html", "type": "Tool", "icon": "🛠️"}

def scan_tools():
    tools_dir = os.path.join(DASHBOARD_ROOT, "tools")
    projects = []
    if os.path.exists(tools_dir):
        for name in os.listdir(tools_dir):
            path = os.path.join(tools_dir, name)
            if os.path.isdir(path) and os.path.exists(os.path.join(path, "index.html")):
                meta = extract_tool_metadata(path)
                if meta: projects.append(meta)
    return sorted(projects, key=lambda x: x['title_en'])

def scan_gallery():
    gallery_dir = os.path.join(DASHBOARD_ROOT, "gallery/images")
    projects = []
    if os.path.exists(gallery_dir):
        for name in os.listdir(gallery_dir):
            if name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                base = os.path.splitext(name)[0]
                parts = base.split('-')
                date_str = f"{parts[0]}-{parts[1]}-{parts[2]}" if len(parts) > 3 else ""
                title = " ".join(parts[3:] if len(parts) > 3 else parts).title()
                projects.append({"title_zh": title, "title_en": title, "desc_zh": f"生成於 {date_str}", "desc_en": f"Generated on {date_str}", "link": f"images/{name}", "image": f"images/{name}", "type": "Art", "target": "_blank"})
    return sorted(projects, key=lambda x: x['desc_en'], reverse=True)

def scan_repos(prefix, type_label, icon, color):
    projects = []
    for path in glob.glob(os.path.join(PROJECTS_ROOT, f"{prefix}*")):
        if os.path.isdir(path):
            name = os.path.basename(path)
            clean = name.replace(prefix, "").replace("-", " ").title()
            projects.append({"title_zh": clean, "title_en": clean, "desc_zh": f"{type_label} Project: {clean}", "desc_en": f"{type_label} Project: {clean}", "link": f"{GITHUB_BASE}/{name}", "type": type_label, "icon": icon, "color": color})
    return sorted(projects, key=lambda x: x['title_en'])

def generate_page(output_path, page_key, data, header_info=None, hide_controls=""):
    headers = {
        "home": {"title_zh": "SimonLiu OpenClaw Works", "title_en": "SimonLiu OpenClaw Works", "desc_zh": "AI 中心樞紐。", "desc_en": "AI Central Hub."},
        "tools": {"title_zh": "網頁工具集", "title_en": "Web Tools", "desc_zh": "實用工具。", "desc_en": "Useful tools."},
        "gallery": {"title_zh": "藝術畫廊", "title_en": "AI Gallery", "desc_zh": "AI 生成藝術。", "desc_en": "AI generated art."},
        "mcp": {"title_zh": "MCP 服務", "title_en": "MCP Services", "desc_zh": "後端服務協定。", "desc_en": "Backend protocol services."},
        "adk": {"title_zh": "ADK 代理人", "title_en": "ADK Agents", "desc_zh": "自主 AI 代理。", "desc_en": "Autonomous agents."}
    }
    h = header_info or headers.get(page_key, headers['home'])
    nav, mobile = get_nav_links(page_key)
    html = PAGE_TEMPLATE.format(
        page_title=h['title_en'], title_zh=h['title_zh'], title_en=h['title_en'],
        desc_zh=h['desc_zh'], desc_en=h['desc_en'], dashboard_url=DASHBOARD_URL,
        nav_links=nav, mobile_nav_links=mobile, project_json=json.dumps(data, ensure_ascii=False),
        trans_json=json.dumps(TRANSLATIONS, ensure_ascii=False),
        date=datetime.now().strftime("%Y-%m-%d"), hide_controls=hide_controls
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f: f.write(html)

def main():
    tools = scan_tools()
    gallery = scan_gallery()
    mcp = scan_repos("mcp-", "MCP", "🔌", "bg-blue-50")
    adk = scan_repos("adk-", "ADK", "🤖", "bg-purple-50")
    
    generate_page(os.path.join(DASHBOARD_ROOT, "web-tools/index.html"), "tools", tools)
    generate_page(os.path.join(DASHBOARD_ROOT, "gallery/index.html"), "gallery", gallery)
    generate_page(os.path.join(DASHBOARD_ROOT, "mcp/index.html"), "mcp", mcp)
    generate_page(os.path.join(DASHBOARD_ROOT, "adk/index.html"), "adk", adk)
    
    portal_data = [
        {"title_en": "Web Tools", "title_zh": "網頁工具", "desc_en": "Daily tools.", "desc_zh": "日常工具。", "link": "web-tools/index.html", "icon": "🛠️", "type": "Section", "target": "_self"},
        {"title_en": "AI Gallery", "title_zh": "AI 藝廊", "desc_en": "AI generated art.", "desc_zh": "AI 藝術。", "link": "gallery/index.html", "icon": "🎨", "type": "Section", "target": "_self"},
        {"title_en": "MCP Services", "title_zh": "MCP 服務", "desc_en": "Backend.", "desc_zh": "後端服務。", "link": "mcp/index.html", "icon": "🔌", "type": "Section", "target": "_self"},
        {"title_en": "ADK Agents", "title_zh": "ADK 代理人", "desc_en": "Agents.", "desc_zh": "代理人。", "link": "adk/index.html", "icon": "🤖", "type": "Section", "target": "_self"}
    ]
    generate_page(os.path.join(DASHBOARD_ROOT, "index.html"), "home", portal_data, hide_controls="hidden")

if __name__ == "__main__":
    main()
