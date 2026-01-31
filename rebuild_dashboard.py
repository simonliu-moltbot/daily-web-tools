import os
import glob
import re
from datetime import datetime

# Configuration
PROJECTS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DASHBOARD_ROOT = os.path.abspath(os.path.dirname(__file__))
GITHUB_BASE = "https://github.com/simonliu-moltbot"

NAV_TEMPLATE = """
    <!-- Top Navigation Bar -->
    <nav class="bg-stone-900 text-white shadow-lg z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                
                <!-- Logo -->
                <div class="flex-shrink-0 flex items-center">
                    <a href="{root}index.html" class="text-xl font-bold tracking-wider leading-tight flex items-center gap-2">
                        SimonLiu <span class="text-stone-400 text-base font-normal">OpenClaw Works</span>
                    </a>
                </div>

                <!-- Desktop Navigation -->
                <div class="hidden md:block">
                    <div class="ml-10 flex items-baseline space-x-4">
                        <a href="{root}index.html" class="px-3 py-2 rounded-md text-sm font-medium {nav_home_class} hover:bg-stone-700 hover:text-white transition-colors">Home</a>
                        <a href="{root}web-tools/index.html" class="px-3 py-2 rounded-md text-sm font-medium {nav_tools_class} hover:bg-stone-700 hover:text-white transition-colors">Web Tools</a>
                        <a href="{root}gallery/index.html" class="px-3 py-2 rounded-md text-sm font-medium {nav_gallery_class} hover:bg-stone-700 hover:text-white transition-colors">AI Gallery</a>
                        <a href="{root}mcp/index.html" class="px-3 py-2 rounded-md text-sm font-medium {nav_mcp_class} hover:bg-stone-700 hover:text-white transition-colors">MCP Services</a>
                        <a href="{root}adk/index.html" class="px-3 py-2 rounded-md text-sm font-medium {nav_adk_class} hover:bg-stone-700 hover:text-white transition-colors">ADK Agents</a>
                    </div>
                </div>

                <!-- Mobile Menu Button -->
                <div class="-mr-2 flex md:hidden">
                    <button type="button" onclick="document.getElementById('mobile-menu').classList.toggle('hidden')" class="bg-stone-800 inline-flex items-center justify-center p-2 rounded-md text-stone-400 hover:text-white hover:bg-stone-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-stone-800 focus:ring-white" aria-controls="mobile-menu" aria-expanded="false">
                        <span class="sr-only">Open main menu</span>
                        <svg class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Menu -->
        <div class="hidden md:hidden bg-stone-800 border-t border-stone-700" id="mobile-menu">
            <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
                <a href="{root}index.html" class="block px-3 py-2 rounded-md text-base font-medium text-stone-300 hover:text-white hover:bg-stone-700">Home</a>
                <a href="{root}web-tools/index.html" class="block px-3 py-2 rounded-md text-base font-medium text-stone-300 hover:text-white hover:bg-stone-700">Web Tools</a>
                <a href="{root}gallery/index.html" class="block px-3 py-2 rounded-md text-base font-medium text-stone-300 hover:text-white hover:bg-stone-700">AI Gallery</a>
                <a href="{root}mcp/index.html" class="block px-3 py-2 rounded-md text-base font-medium text-stone-300 hover:text-white hover:bg-stone-700">MCP Services</a>
                <a href="{root}adk/index.html" class="block px-3 py-2 rounded-md text-base font-medium text-stone-300 hover:text-white hover:bg-stone-700">ADK Agents</a>
            </div>
        </div>
    </nav>
"""

FOOTER_TEMPLATE = """
                <div class="mt-12 text-center text-stone-400 text-sm border-t border-stone-200 pt-8">
                    <p>Built with ❤️ by AI Agent</p>
                    <p class="mt-1">Last Updated: {date}</p>
                </div>
"""

HTML_SKELETON = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | SimonLiu OpenClaw Works</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans TC', sans-serif; }}
        .project-card {{ transition: all 0.3s ease; }}
        .project-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
    </style>
</head>
<body class="bg-stone-50 min-h-screen flex flex-col">

    {nav}

    <div class="flex-1 flex flex-col w-full">
        
        <header class="bg-white border-b border-stone-200 px-6 py-10 md:px-8 shadow-sm">
            <div class="max-w-7xl mx-auto">
                <h2 class="text-3xl font-bold text-stone-800">{header_title}</h2>
                <p class="text-stone-500 mt-3 text-lg">
                    {header_desc}
                </p>
            </div>
        </header>

        <main class="flex-1 p-4 md:p-8">
            <div class="max-w-7xl mx-auto pb-12">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {content}
                </div>

                {footer}
            </div>
        </main>
    </div>

</body>
</html>
"""

def get_nav(root="./", active="home"):
    classes = {
        "nav_home_class": "text-stone-300",
        "nav_tools_class": "text-stone-300",
        "nav_gallery_class": "text-stone-300",
        "nav_mcp_class": "text-stone-300",
        "nav_adk_class": "text-stone-300"
    }
    # Set active class
    active_key = f"nav_{active}_class"
    if active_key in classes:
        classes[active_key] = "bg-stone-800 text-white border border-stone-700"
    
    return NAV_TEMPLATE.format(root=root, **classes)

def get_footer():
    return FOOTER_TEMPLATE.format(date=datetime.now().strftime("%Y-%m-%d"))

def scan_projects(prefix):
    projects = []
    for path in glob.glob(os.path.join(PROJECTS_ROOT, f"{prefix}*")):
        if os.path.isdir(path):
            name = os.path.basename(path)
            projects.append(name)
    return sorted(projects)

def create_card(title, desc, link, icon="📦", color="bg-gray-500", label="View Repo"):
    return f"""
    <div class="project-card bg-white rounded-xl overflow-hidden border border-stone-100 shadow-sm flex flex-col">
        <div class="h-2 {color}"></div>
        <div class="p-6 flex-1 flex flex-col">
            <div class="text-3xl mb-4">{icon}</div>
            <h3 class="text-xl font-bold text-stone-800 mb-2">{title}</h3>
            <p class="text-stone-500 text-sm mb-6 flex-1">
                {desc}
            </p>
            <a href="{link}" target="_blank" class="block w-full text-center bg-stone-800 hover:bg-stone-900 text-white font-medium py-2 rounded-lg transition-colors">
                {label} ↗
            </a>
        </div>
    </div>
    """

def generate_mcp_page():
    projects = scan_projects("mcp-")
    cards = []
    for p in projects:
        # Simple heuristic for description based on name
        clean_name = p.replace("mcp-", "").replace("-", " ").title()
        desc = f"Model Context Protocol server for {clean_name}."
        link = f"{GITHUB_BASE}/{p}"
        cards.append(create_card(p, desc, link, icon="🔌", color="bg-blue-600"))
    
    html = HTML_SKELETON.format(
        title="MCP Services",
        nav=get_nav(root="../", active="mcp"),
        header_title="MCP Services",
        header_desc="Model Context Protocol servers providing data and tools to AI agents.",
        content="\n".join(cards),
        footer=get_footer()
    )
    
    with open(os.path.join(DASHBOARD_ROOT, "mcp/index.html"), "w") as f:
        f.write(html)
    print("Generated mcp/index.html")

def generate_adk_page():
    projects = scan_projects("adk-")
    cards = []
    for p in projects:
        clean_name = p.replace("adk-", "").replace("-", " ").title()
        desc = f"Agent Development Kit project for {clean_name}."
        link = f"{GITHUB_BASE}/{p}"
        cards.append(create_card(p, desc, link, icon="🤖", color="bg-purple-600"))
    
    html = HTML_SKELETON.format(
        title="ADK Agents",
        nav=get_nav(root="../", active="adk"),
        header_title="ADK Agents",
        header_desc="Autonomous agents built with the Agent Development Kit.",
        content="\n".join(cards),
        footer=get_footer()
    )
    
    with open(os.path.join(DASHBOARD_ROOT, "adk/index.html"), "w") as f:
        f.write(html)
    print("Generated adk/index.html")

def patch_web_tools_page():
    path = os.path.join(DASHBOARD_ROOT, "web-tools/index.html")
    with open(path, "r") as f:
        content = f.read()
    
    # Replace Nav
    nav = get_nav(root="../", active="tools")
    # Regex to replace existing nav
    content = re.sub(r'<nav.*?</nav>', nav, content, flags=re.DOTALL)
    
    # Fix links (tools/ -> ../tools/)
    # But be careful not to break other things.
    # The links are like href="tools/..."
    # We want href="../tools/..."
    content = content.replace('href="tools/', 'href="../tools/')
    
    # Fix AI Gallery link specifically if it was hardcoded differently
    # In index.html it was tools/ai-gallery/index.html -> now ../gallery/index.html
    # But we just moved ai-gallery to gallery.
    # So if link was tools/ai-gallery/index.html, replacing tools/ with ../tools/ makes it ../tools/ai-gallery/index.html
    # But the folder is actually ../gallery/index.html
    # So we need to fix that.
    content = content.replace('href="../tools/ai-gallery/index.html"', 'href="../gallery/index.html"')
    
    # Also update the footer date
    content = re.sub(r'Last Updated: <script>.*?</script>', f'Last Updated: {datetime.now().strftime("%Y-%m-%d")}', content)

    # Remove the AI Gallery card from the grid since it has its own section now?
    # User said "Web Tools" list. Gallery is separate.
    # Let's try to remove the specific AI Gallery card.
    # Pattern: <!-- Tool: AI Gallery --> ... </div> (closing div of the card)
    # This might be tricky with regex.
    # Let's leave it for now, or just let it link to the gallery. 
    # Actually, the user wants "AI Gallery" in Top Nav. 
    # Having it as a card in Web Tools is duplicate but harmless.
    # I'll update the title/header to "Web Tools" if it isn't already.
    
    with open(path, "w") as f:
        f.write(content)
    print("Patched web-tools/index.html")

def patch_gallery_page():
    path = os.path.join(DASHBOARD_ROOT, "gallery/index.html")
    with open(path, "r") as f:
        content = f.read()
    
    # Replace Nav
    nav = get_nav(root="../", active="gallery")
    content = re.sub(r'<nav.*?</nav>', nav, content, flags=re.DOTALL)
    
    # Fix Home link in Logo if regex didn't catch it (it did)
    
    with open(path, "w") as f:
        f.write(content)
    print("Patched gallery/index.html")

def generate_portal_page():
    # Home Portal
    cards = []
    
    # Web Tools
    cards.append(create_card(
        "Web Tools", 
        "Collection of daily useful tools for Taiwan life.", 
        "web-tools/index.html", 
        icon="🛠️", 
        color="bg-amber-500", 
        label="Open Tools"
    ))
    
    # AI Gallery
    cards.append(create_card(
        "AI Gallery", 
        "Daily AI generated art featuring Taiwan scenery.", 
        "gallery/index.html", 
        icon="🎨", 
        color="bg-pink-500", 
        label="Enter Gallery"
    ))
    
    # MCP
    cards.append(create_card(
        "MCP Services", 
        "Backend data services for AI agents.", 
        "mcp/index.html", 
        icon="🔌", 
        color="bg-blue-500", 
        label="Browse Services"
    ))
    
    # ADK
    cards.append(create_card(
        "ADK Agents", 
        "Autonomous agents performing daily tasks.", 
        "adk/index.html", 
        icon="🤖", 
        color="bg-purple-500", 
        label="View Agents"
    ))
    
    html = HTML_SKELETON.format(
        title="Home",
        nav=get_nav(root="./", active="home"),
        header_title="SimonLiu OpenClaw Works",
        header_desc="Central hub for all AI-powered tools, services, and galleries.",
        content="\n".join(cards),
        footer=get_footer()
    )
    
    with open(os.path.join(DASHBOARD_ROOT, "index.html"), "w") as f:
        f.write(html)
    print("Generated index.html")

if __name__ == "__main__":
    generate_mcp_page()
    generate_adk_page()
    patch_web_tools_page()
    patch_gallery_page()
    generate_portal_page()
