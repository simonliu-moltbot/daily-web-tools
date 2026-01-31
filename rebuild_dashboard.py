import os
import glob
import json
import re
from datetime import datetime

# ==========================================
# Configuration & Constants
# ==========================================

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
DASHBOARD_ROOT = SCRIPT_DIR

# URLs (Relative to Dashboard Root for portability, or Absolute if known)
# "Logo -> dashboard root, Home -> user root"
# We'll use relative paths calculated dynamically based on page depth
GITHUB_USER = "simonliu-moltbot"
GITHUB_BASE = f"https://github.com/{GITHUB_USER}"

# Translations
TRANSLATIONS = {
    "nav_home": {"en": "Home", "zh": "首頁"},
    "nav_tools": {"en": "Web Tools", "zh": "網頁工具"},
    "nav_gallery": {"en": "AI Gallery", "zh": "AI 藝廊"},
    "nav_mcp": {"en": "MCP Services", "zh": "MCP 服務"},
    "nav_adk": {"en": "ADK Agents", "zh": "ADK 代理人"},
    "footer_built": {"en": "Built with ❤️ by AI Agent", "zh": "由 AI Agent ❤️ 打造"},
    "footer_updated": {"en": "Last Updated", "zh": "最後更新"},
    "search_placeholder": {"en": "Search projects...", "zh": "搜尋專案..."},
    "view_grid": {"en": "Grid", "zh": "網格"},
    "view_table": {"en": "Table", "zh": "列表"},
    "btn_view": {"en": "View", "zh": "查看"},
    "btn_repo": {"en": "Repo", "zh": "原始碼"},
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
        /* Nordic / Muji Aesthetic */
        body {{
            font-family: 'Inter', 'Noto Sans TC', sans-serif;
            background-color: #faf9f6; /* Off-white / Stone-50-ish but warmer */
            color: #44403c; /* Stone-700 */
        }}
        .glass-panel {{
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(231, 229, 228, 0.8);
        }}
        .card-hover {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .card-hover:hover {{
            transform: translateY(-4px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
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
        /* Table View Styles */
        .view-table .project-card {{
            @apply flex-row items-center p-4 min-h-[80px];
        }}
        .view-table .project-image {{
            @apply w-16 h-16 mr-4 mb-0;
        }}
        .view-table .project-content {{
            @apply flex-row items-center justify-between flex-1;
        }}
        .view-table .project-desc {{
            @apply hidden md:block mr-4 mb-0;
        }}
        .view-table .project-actions {{
            @apply mt-0 w-auto;
        }}
        [v-cloak] {{ display: none; }}
    </style>
    <script>
        // Data passed from Python
        const PROJECT_DATA = {project_json};
        const TRANSLATIONS = {trans_json};
    </script>
</head>
<body class="min-h-screen flex flex-col selection:bg-stone-200 selection:text-stone-900">

    <!-- Navbar -->
    <nav class="sticky top-0 z-50 glass-panel border-b border-stone-200/50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Logo -->
                <div class="flex-shrink-0 flex items-center">
                    <a href="{root}index.html" class="text-lg font-semibold tracking-wide flex items-center gap-2 text-stone-800">
                        SimonLiu <span class="text-stone-400 font-light">| Works</span>
                    </a>
                </div>

                <!-- Desktop Nav -->
                <div class="hidden md:flex space-x-1">
                    {nav_links}
                </div>

                <!-- Right Side: Lang & Mobile Menu -->
                <div class="flex items-center gap-4">
                    <!-- Lang Switcher -->
                    <button id="lang-toggle" class="text-xs font-medium bg-stone-100 hover:bg-stone-200 text-stone-600 px-3 py-1.5 rounded-full transition-colors border border-stone-200">
                        EN / 中文
                    </button>
                    
                    <!-- Mobile Menu Button -->
                    <button id="mobile-menu-btn" class="md:hidden p-2 rounded-md text-stone-500 hover:text-stone-900 hover:bg-stone-100">
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

    <!-- Header / Hero -->
    <header class="bg-white border-b border-stone-100 pt-16 pb-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-7xl mx-auto text-center">
            <h1 class="text-4xl font-light text-stone-900 mb-4 tracking-tight" data-i18n-zh="{title_zh}" data-i18n-en="{title_en}">
                {title_en}
            </h1>
            <p class="max-w-2xl mx-auto text-lg text-stone-500 font-light leading-relaxed" data-i18n-zh="{desc_zh}" data-i18n-en="{desc_en}">
                {desc_en}
            </p>

            <!-- Controls: Search & View Toggle -->
            <div class="mt-10 max-w-xl mx-auto flex flex-col sm:flex-row gap-4 items-center justify-center {hide_controls}">
                <div class="relative w-full">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-stone-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0" />
                        </svg>
                    </div>
                    <input type="text" id="search-input" 
                           class="block w-full pl-10 pr-3 py-2.5 border border-stone-200 rounded-lg leading-5 bg-stone-50 placeholder-stone-400 focus:outline-none focus:bg-white focus:ring-1 focus:ring-stone-400 focus:border-stone-400 sm:text-sm transition-colors"
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

    <!-- Main Content -->
    <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <!-- Projects Container -->
        <div id="projects-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <!-- Content injected by JS -->
        </div>
        
        <!-- Empty State -->
        <div id="empty-state" class="hidden text-center py-20">
            <p class="text-stone-400 text-lg">No projects found.</p>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-stone-200 mt-auto">
        <div class="max-w-7xl mx-auto py-12 px-4 overflow-hidden sm:px-6 lg:px-8">
            <div class="flex justify-center space-x-6 text-stone-400">
               <!-- Social Links could go here -->
            </div>
            <div class="mt-8 text-center text-sm text-stone-400">
                <p data-i18n-key="footer_built">Built with ❤️ by AI Agent</p>
                <p class="mt-2"><span data-i18n-key="footer_updated">Last Updated</span>: {date}</p>
            </div>
        </div>
    </footer>

    <!-- Client-Side Logic -->
    <script>
        // State
        let currentLang = localStorage.getItem('lang') || 'en'; // Default EN
        // Check browser lang only if no preference
        const browserLang = navigator.language || navigator.userLanguage;
        if (!localStorage.getItem('lang')) {{
            currentLang = browserLang.toLowerCase().includes('zh') ? 'zh' : 'en';
        }}
        
        let currentView = localStorage.getItem('view') || 'grid';
        let searchQuery = '';

        // DOM Elements
        const container = document.getElementById('projects-container');
        const emptyState = document.getElementById('empty-state');
        const searchInput = document.getElementById('search-input');
        const langToggle = document.getElementById('lang-toggle');
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');

        // Init
        function init() {{
            renderProjects();
            updateLangUI();
            updateViewUI();
            
            // Listeners
            if (searchInput) {{
                searchInput.addEventListener('input', (e) => {{
                    searchQuery = e.target.value.toLowerCase();
                    renderProjects();
                }});
            }}
            
            langToggle.addEventListener('click', toggleLang);
            
            mobileMenuBtn.addEventListener('click', () => {{
                mobileMenu.classList.toggle('hidden');
            }});
        }}

        // Render Projects
        function renderProjects() {{
            container.innerHTML = '';
            
            const filtered = PROJECT_DATA.filter(p => {{
                const term = searchQuery.toLowerCase();
                const matchTitle = (p.title_en && p.title_en.toLowerCase().includes(term)) || (p.title_zh && p.title_zh.toLowerCase().includes(term));
                const matchDesc = (p.desc_en && p.desc_en.toLowerCase().includes(term)) || (p.desc_zh && p.desc_zh.toLowerCase().includes(term));
                return matchTitle || matchDesc;
            }});

            if (filtered.length === 0) {{
                container.classList.add('hidden');
                emptyState.classList.remove('hidden');
            }} else {{
                container.classList.remove('hidden');
                emptyState.classList.add('hidden');
                
                filtered.forEach(p => {{
                    const card = createCard(p);
                    container.appendChild(card);
                }});
            }}
        }}

        function createCard(p) {{
            const el = document.createElement('div');
            el.className = `project-card group bg-white rounded-xl border border-stone-200 overflow-hidden card-hover flex flex-col relative ${{currentView === 'table' ? 'view-table-item' : ''}}`;
            
            // Image / Icon Area
            let visual = '';
            if (p.image) {{
                visual = `<div class="project-image h-48 w-full bg-stone-100 overflow-hidden relative">
                            <img src="${{p.image}}" alt="${{p.title_en}}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105">
                          </div>`;
            }} else {{
                visual = `<div class="project-image h-32 w-full ${{p.color || 'bg-stone-100'}} flex items-center justify-center text-4xl">
                            ${{p.icon || '📦'}}
                          </div>`;
            }}

            // Content Area
            const title = currentLang === 'zh' ? (p.title_zh || p.title_en) : (p.title_en || p.title_zh);
            const desc = currentLang === 'zh' ? (p.desc_zh || p.desc_en) : (p.desc_en || p.desc_zh);
            const btnText = currentLang === 'zh' ? TRANSLATIONS.btn_view.zh : TRANSLATIONS.btn_view.en;
            
            el.innerHTML = `
                ${{visual}}
                <div class="project-content p-5 flex flex-col flex-1">
                    <div class="mb-auto">
                        <h3 class="text-lg font-bold text-stone-800 mb-2 group-hover:text-stone-600 transition-colors">${{title}}</h3>
                        <p class="project-desc text-sm text-stone-500 line-clamp-3">${{desc}}</p>
                    </div>
                    <div class="project-actions mt-5 pt-4 border-t border-stone-100 flex items-center justify-between">
                        <span class="text-xs font-mono text-stone-400 bg-stone-50 px-2 py-1 rounded">${{p.type}}</span>
                        <a href="${{p.link}}" target="${{p.target || '_blank'}}" class="text-sm font-medium text-stone-800 hover:text-stone-500 flex items-center gap-1 transition-colors">
                            ${{btnText}} <span>&rarr;</span>
                        </a>
                    </div>
                </div>
            `;
            
            return el;
        }}

        // View Toggle
        window.setView = function(mode) {{
            currentView = mode;
            localStorage.setItem('view', mode);
            updateViewUI();
        }}

        function updateViewUI() {{
            const btnGrid = document.getElementById('view-grid');
            const btnTable = document.getElementById('view-table');
            
            if (currentView === 'grid') {{
                container.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6';
                document.body.classList.remove('view-table');
                btnGrid.classList.add('active');
                btnTable.classList.remove('active');
            }} else {{
                container.className = 'flex flex-col gap-4';
                document.body.classList.add('view-table');
                btnGrid.classList.remove('active');
                btnTable.classList.add('active');
            }}
            
            // Re-render to apply structural changes if any
            renderProjects(); 
        }}

        // Language Toggle
        function toggleLang() {{
            currentLang = currentLang === 'zh' ? 'en' : 'zh';
            localStorage.setItem('lang', currentLang);
            updateLangUI();
            renderProjects();
        }}

        function updateLangUI() {{
            document.documentElement.lang = currentLang === 'zh' ? 'zh-TW' : 'en';
            
            // Toggle Button Text
            langToggle.textContent = currentLang === 'zh' ? 'EN' : '中文';

            // Update UI strings
            document.querySelectorAll('[data-i18n-key]').forEach(el => {{
                const key = el.dataset.i18nKey;
                if (TRANSLATIONS[key]) {{
                    el.textContent = TRANSLATIONS[key][currentLang];
                }}
            }});

            // Update Header Title/Desc via data attributes
            document.querySelectorAll('[data-i18n-zh]').forEach(el => {{
                el.textContent = currentLang === 'zh' ? el.dataset.i18nZh : el.dataset.i18nEn;
            }});
            
            // Update Search Placeholder
            if (searchInput) {{
                searchInput.placeholder = TRANSLATIONS.search_placeholder[currentLang];
            }}
        }}

        // Run
        init();
    </script>
</body>
</html>
"""

# ==========================================
# Helpers
# ==========================================

def get_nav_links(root, active_page):
    links = [
        ("nav_home", f"{root}../index.html"), # User root
        ("nav_tools", f"{root}web-tools/index.html"),
        ("nav_gallery", f"{root}gallery/index.html"),
        ("nav_mcp", f"{root}mcp/index.html"),
        ("nav_adk", f"{root}adk/index.html"),
    ]
    
    html_parts = []
    mobile_parts = []
    
    for key, url in links:
        is_active = (key == f"nav_{active_page}")
        active_class = "text-stone-900 bg-stone-100" if is_active else "text-stone-500 hover:text-stone-900 hover:bg-stone-50"
        
        # Desktop
        html_parts.append(f"""
            <a href="{url}" 
               class="px-3 py-2 rounded-md text-sm font-medium transition-colors {active_class}"
               data-i18n-key="{key}">
               {TRANSLATIONS[key]['en']}
            </a>
        """)
        
        # Mobile
        mobile_parts.append(f"""
            <a href="{url}" 
               class="block px-3 py-2 rounded-md text-base font-medium {active_class}"
               data-i18n-key="{key}">
               {TRANSLATIONS[key]['en']}
            </a>
        """)
        
    return "\n".join(html_parts), "\n".join(mobile_parts)

def extract_tool_metadata(tool_dir):
    """
    Parses index.html in the tool directory to extract title and description.
    """
    index_path = os.path.join(tool_dir, "index.html")
    if not os.path.exists(index_path):
        return None
        
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extract Title
    title_match = re.search(r'<title>(.*?)</title>', content)
    full_title = title_match.group(1) if title_match else os.path.basename(tool_dir)
    
    if "|" in full_title:
        parts = full_title.split("|")
        title_zh = parts[0].strip().replace("📅", "").strip() 
        title_en = parts[1].strip()
    else:
        title_zh = full_title
        title_en = full_title
        
    # Extract Description
    desc_match = re.search(r'<meta name="description" content="(.*?)">', content)
    if desc_match:
        desc = desc_match.group(1)
        desc_zh, desc_en = desc, desc
    else:
        desc_zh = "一個實用的網頁工具。"
        desc_en = "A useful web tool."

    return {
        "id": os.path.basename(tool_dir),
        "title_zh": title_zh,
        "title_en": title_en,
        "desc_zh": desc_zh,
        "desc_en": desc_en,
        "link": f"{os.path.basename(tool_dir)}/index.html", 
        "type": "Tool",
        "icon": "🛠️",
        "color": "bg-stone-200"
    }

def scan_tools():
    tools_dir = os.path.join(DASHBOARD_ROOT, "tools")
    projects = []
    
    if os.path.exists(tools_dir):
        for name in os.listdir(tools_dir):
            path = os.path.join(tools_dir, name)
            if os.path.isdir(path):
                meta = extract_tool_metadata(path)
                if meta:
                    meta['link'] = f"../tools/{name}/index.html"
                    projects.append(meta)
    return sorted(projects, key=lambda x: x['id'])

def scan_gallery():
    gallery_dir = os.path.join(DASHBOARD_ROOT, "gallery/images")
    projects = []
    if os.path.exists(gallery_dir):
        for name in os.listdir(gallery_dir):
            if name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                base = os.path.splitext(name)[0]
                parts = base.split('-')
                if len(parts) > 3 and parts[0].isdigit():
                    date_str = f"{parts[0]}-{parts[1]}-{parts[2]}"
                    title_slug = " ".join(parts[3:]).title()
                else:
                    date_str = ""
                    title_slug = base.replace("-", " ").title()
                
                projects.append({
                    "id": base,
                    "title_zh": title_slug,
                    "title_en": title_slug,
                    "desc_zh": f"生成於 {date_str}" if date_str else "AI 生成圖像",
                    "desc_en": f"Generated on {date_str}" if date_str else "AI Generated Image",
                    "link": f"images/{name}",
                    "image": f"images/{name}",
                    "type": "Art",
                    "target": "_blank"
                })
    return sorted(projects, key=lambda x: x['id'], reverse=True)

def scan_repos(prefix, type_label, icon, color):
    projects = []
    for path in glob.glob(os.path.join(PROJECTS_ROOT, f"{prefix}*")):
        if os.path.isdir(path):
            name = os.path.basename(path)
            clean_name = name.replace(prefix, "").replace("-", " ").title()
            
            projects.append({
                "id": name,
                "title_zh": clean_name,
                "title_en": clean_name,
                "desc_zh": f"{type_label} 專案: {clean_name}",
                "desc_en": f"{type_label} project: {clean_name}",
                "link": f"{GITHUB_BASE}/{name}",
                "type": type_label,
                "icon": icon,
                "color": color
            })
    return sorted(projects, key=lambda x: x['id'])

# ==========================================
# Main Generators
# ==========================================

def generate_page(output_path, page_key, data, root_depth="./", header_info=None, hide_controls=""):
    headers = {
        "home": {
            "title_zh": "SimonLiu OpenClaw Works", "title_en": "SimonLiu OpenClaw Works",
            "desc_zh": "AI 工具、服務與藝廊的中心樞紐。", "desc_en": "Central hub for AI tools, services, and galleries."
        },
        "tools": {
            "title_zh": "網頁工具", "title_en": "Web Tools",
            "desc_zh": "解決日常問題的小工具集合。", "desc_en": "Collection of small tools for daily problems."
        },
        "gallery": {
            "title_zh": "AI 藝廊", "title_en": "AI Gallery",
            "desc_zh": "探索台灣風景的 AI 生成藝術。", "desc_en": "AI generated art featuring Taiwan scenery."
        },
        "mcp": {
            "title_zh": "MCP 服務", "title_en": "MCP Services",
            "desc_zh": "為 AI 代理提供數據的後端協議。", "desc_en": "Backend protocols providing data for AI agents."
        },
        "adk": {
            "title_zh": "ADK 代理人", "title_en": "ADK Agents",
            "desc_zh": "使用 Agent Development Kit 構建的自主代理。", "desc_en": "Autonomous agents built with the Agent Development Kit."
        }
    }
    
    h_info = header_info or headers.get(page_key, headers['home'])
    
    nav_html, nav_mobile = get_nav_links(root_depth, page_key)
    
    html = PAGE_TEMPLATE.format(
        page_title=h_info['title_en'],
        title_zh=h_info['title_zh'],
        title_en=h_info['title_en'],
        desc_zh=h_info['desc_zh'],
        desc_en=h_info['desc_en'],
        root=root_depth,
        nav_links=nav_html,
        mobile_nav_links=nav_mobile,
        project_json=json.dumps(data, ensure_ascii=False),
        trans_json=json.dumps(TRANSLATIONS, ensure_ascii=False),
        date=datetime.now().strftime("%Y-%m-%d"),
        hide_controls=hide_controls
    )
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {output_path}")

def main():
    tools_data = scan_tools()
    gallery_data = scan_gallery()
    mcp_data = scan_repos("mcp-", "MCP", "🔌", "bg-blue-100")
    adk_data = scan_repos("adk-", "ADK", "🤖", "bg-purple-100")
    
    generate_page(os.path.join(DASHBOARD_ROOT, "web-tools/index.html"), "tools", tools_data, root_depth="../")
    generate_page(os.path.join(DASHBOARD_ROOT, "gallery/index.html"), "gallery", gallery_data, root_depth="../")
    generate_page(os.path.join(DASHBOARD_ROOT, "mcp/index.html"), "mcp", mcp_data, root_depth="../")
    generate_page(os.path.join(DASHBOARD_ROOT, "adk/index.html"), "adk", adk_data, root_depth="../")
    
    portal_data = [
        {"title_en": "Web Tools", "title_zh": "網頁工具", "desc_en": "Collection of daily useful tools.", "desc_zh": "實用的日常網頁工具。", "link": "web-tools/index.html", "icon": "🛠️", "type": "Section", "target": "_self"},
        {"title_en": "AI Gallery", "title_zh": "AI 藝廊", "desc_en": "Daily AI generated art.", "desc_zh": "每日 AI 生成藝術。", "link": "gallery/index.html", "icon": "🎨", "type": "Section", "target": "_self"},
        {"title_en": "MCP Services", "title_zh": "MCP 服務", "desc_en": "Backend data services for agents.", "desc_zh": "提供 AI 代理的後端服務。", "link": "mcp/index.html", "icon": "🔌", "type": "Section", "target": "_self"},
        {"title_en": "ADK Agents", "title_zh": "ADK 代理人", "desc_en": "Autonomous agents.", "desc_zh": "自主 AI 代理人。", "link": "adk/index.html", "icon": "🤖", "type": "Section", "target": "_self"}
    ]
    
    generate_page(os.path.join(DASHBOARD_ROOT, "index.html"), "home", portal_data, root_depth="./", hide_controls="hidden")

if __name__ == "__main__":
    main()
