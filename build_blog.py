#!/usr/bin/env python3
"""
ARRUDA CHUDZY ADVOGADAS - Automated Blog Engine & Static Site Generator
Generates:
1. Individual static article pages in `artigos/<slug>.html` (high SEO, Schema.org, OpenGraph)
2. Main blog hub in `blog.html` (interactive search, category filters, responsive cards)
3. Latest 3 articles showcase section in `index.html`
4. Complete search engine `sitemap.xml`
"""

import os
import re
import json
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(REPO_ROOT, "content", "artigos")
ARTICLES_OUT_DIR = os.path.join(REPO_ROOT, "artigos")
BLOG_HTML_PATH = os.path.join(REPO_ROOT, "blog.html")
INDEX_HTML_PATH = os.path.join(REPO_ROOT, "index.html")
SITEMAP_PATH = os.path.join(REPO_ROOT, "sitemap.xml")

AUTHORS_INFO = {
    "Julia de Arruda Souza": {
        "name": "Julia de Arruda Souza",
        "role": "Sócia-Fundadora & Presidente da Com. de Direito da Saúde da OAB Lages",
        "oab": "OAB/SC 72.463",
        "photo": "assets/images/julia-arruda.webp",
        "fallback_photo": "assets/images/julia-arruda.jpg",
        "bio": "Advogada e sócia-fundadora do escritório Arruda Chudzy Advogadas. Presidente da Comissão de Direito da Saúde da OAB Lages (2025–2027), é idealizadora do treinamento Secretárias 360º. Pós-graduada em Direito Médico e da Saúde pela PUC-PR e graduada pela UNIPLAC.",
        "wa_text": "Olá! Li o artigo da Dra. Julia de Arruda Souza no blog e gostaria de agendar uma consulta."
    },
    "Bianca Flor Chudzy": {
        "name": "Bianca Flor Chudzy",
        "role": "Sócia-Fundadora & Secretária da Com. de Direito da Saúde da OAB Lages",
        "oab": "OAB/SC 71.437",
        "photo": "assets/images/bianca-chudzy.webp",
        "fallback_photo": "assets/images/bianca-chudzy.jpg",
        "bio": "Advogada e sócia-fundadora do escritório Arruda Chudzy Advogadas. Secretária da Comissão de Direito da Saúde da OAB Lages (2025–2027), é idealizadora do treinamento Secretárias 360º. Pós-graduanda em Gestão Tributária pela USP e graduada pelo CESUSC.",
        "wa_text": "Olá! Li o artigo da Dra. Bianca Flor Chudzy no blog e gostaria de agendar uma consulta."
    }
}

MONTHS_PT = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

def format_date_pt(date_str):
    try:
        dt = datetime.strptime(date_str.strip()[:10], "%Y-%m-%d")
        return f"{dt.day} de {MONTHS_PT[dt.month]} de {dt.year}"
    except Exception:
        return date_str

def parse_markdown(text):
    """Clean and fast standard-library Markdown to HTML converter."""
    # Convert headings
    lines = text.strip().split("\n")
    html_lines = []
    in_list = False
    in_ordered = False
    in_quote = False
    quote_lines = []

    for line in lines:
        stripped = line.strip()

        # Handle Blockquotes
        if stripped.startswith(">"):
            if not in_quote:
                in_quote = True
                quote_lines = []
            quote_text = stripped.lstrip("> ").strip()
            quote_lines.append(quote_text)
            continue
        elif in_quote:
            quote_html = "<br>".join(quote_lines)
            html_lines.append(f'<blockquote class="article-quote">{inline_markdown(quote_html)}</blockquote>')
            in_quote = False
            quote_lines = []

        # Handle Horizontal Rules
        if stripped in ["---", "***", "___"]:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_ordered:
                html_lines.append("</ol>")
                in_ordered = False
            html_lines.append('<hr class="article-divider">')
            continue

        # Handle Headings
        if stripped.startswith("#### "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f'<h4 class="article-h4">{inline_markdown(stripped[5:])}</h4>')
            continue
        if stripped.startswith("### "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f'<h3 class="article-h3">{inline_markdown(stripped[4:])}</h3>')
            continue
        if stripped.startswith("## "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f'<h2 class="article-h2">{inline_markdown(stripped[3:])}</h2>')
            continue
        if stripped.startswith("# "):
            if in_list: html_lines.append("</ul>"); in_list = False
            html_lines.append(f'<h1 class="article-h1">{inline_markdown(stripped[2:])}</h1>')
            continue

        # Handle Unordered Lists
        if stripped.startswith("* ") or stripped.startswith("- "):
            if not in_list:
                if in_ordered: html_lines.append("</ol>"); in_ordered = False
                html_lines.append('<ul class="article-list">')
                in_list = True
            item_text = stripped[2:].strip()
            html_lines.append(f'<li>{inline_markdown(item_text)}</li>')
            continue
        elif in_list:
            html_lines.append("</ul>")
            in_list = False

        # Handle Ordered Lists
        m_ol = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m_ol:
            if not in_ordered:
                if in_list: html_lines.append("</ul>"); in_list = False
                html_lines.append('<ol class="article-ordered-list">')
                in_ordered = True
            html_lines.append(f'<li>{inline_markdown(m_ol.group(2))}</li>')
            continue
        elif in_ordered:
            html_lines.append("</ol>")
            in_ordered = False

        # Empty line
        if not stripped:
            continue

        # Regular Paragraph
        html_lines.append(f'<p class="article-p">{inline_markdown(stripped)}</p>')

    if in_quote:
        quote_html = "<br>".join(quote_lines)
        html_lines.append(f'<blockquote class="article-quote">{inline_markdown(quote_html)}</blockquote>')
    if in_list:
        html_lines.append("</ul>")
    if in_ordered:
        html_lines.append("</ol>")

    return "\n".join(html_lines)

def inline_markdown(text):
    # Bold **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic *text*
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    # Links [label](url)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text)
    return text

def parse_frontmatter(content):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    yaml_text = parts[1]
    body = parts[2]
    meta = {}
    current_key = None
    for line in yaml_text.split("\n"):
        line_clean = line.rstrip()
        if not line_clean or line_clean.strip().startswith("#"):
            continue
        if line_clean.startswith("  - ") and current_key:
            # list item
            item = line_clean.strip()[2:].strip().strip("\"'")
            if not isinstance(meta[current_key], list):
                meta[current_key] = []
            meta[current_key].append(item)
            continue
        m = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line_clean)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            current_key = key
            if val == "":
                meta[key] = []
            else:
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                meta[key] = val
    return meta, body

def load_all_articles():
    articles = []
    if not os.path.exists(CONTENT_DIR):
        return articles
    for fname in os.listdir(CONTENT_DIR):
        if not fname.endswith(".md"):
            continue
        slug = fname[:-3]
        fpath = os.path.join(CONTENT_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            raw = f.read()
        meta, body = parse_frontmatter(raw)
        title = meta.get("title", slug.replace("-", " ").title())
        date = str(meta.get("date", "2026-10-22"))
        author_name = meta.get("author", "Julia de Arruda Souza")
        category = meta.get("category", "Direito Médico e da Saúde")
        cover_image = meta.get("cover_image", "assets/images/og-preview.jpg")
        excerpt = meta.get("excerpt", "")
        reading_time = meta.get("reading_time", "5 min")
        tags = meta.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        articles.append({
            "slug": slug,
            "title": title,
            "date": date,
            "date_formatted": format_date_pt(date),
            "author": author_name,
            "category": category,
            "cover_image": cover_image,
            "excerpt": excerpt,
            "reading_time": reading_time,
            "tags": tags,
            "body_md": body,
            "body_html": parse_markdown(body)
        })

    # Sort descending by date
    articles.sort(key=lambda a: a["date"], reverse=True)
    return articles

def generate_article_page(article, all_articles):
    author = AUTHORS_INFO.get(article["author"], AUTHORS_INFO["Julia de Arruda Souza"])
    
    # Related articles (up to 2, excluding current)
    related = [a for a in all_articles if a["slug"] != article["slug"]]
    # Prioritize same category
    same_cat = [a for a in related if a["category"] == article["category"]]
    diff_cat = [a for a in related if a["category"] != article["category"]]
    related_picked = (same_cat + diff_cat)[:2]

    related_html_cards = ""
    for rel in related_picked:
        related_html_cards += f'''
          <article class="blog-card">
            <a href="{rel['slug']}.html" class="blog-card-media" aria-label="Ler artigo: {rel['title']}">
              <img src="../{rel['cover_image']}" alt="{rel['title']}" width="400" height="240" loading="lazy">
              <span class="blog-category-badge">{rel['category']}</span>
            </a>
            <div class="blog-card-body">
              <div class="blog-card-meta">
                <span>{rel['date_formatted']}</span> &bull; <span>{rel['reading_time']} de leitura</span>
              </div>
              <h3 class="blog-card-title">
                <a href="{rel['slug']}.html">{rel['title']}</a>
              </h3>
              <p class="blog-card-excerpt">{rel['excerpt'][:130]}...</p>
              <div class="blog-card-footer">
                <span class="blog-author-name">{rel['author']}</span>
                <a href="{rel['slug']}.html" class="blog-read-more">Ler Artigo &rarr;</a>
              </div>
            </div>
          </article>'''

    canonical_url = f"https://arrudachudzy.com.br/artigos/{article['slug']}.html"
    og_image = f"https://arrudachudzy.com.br/{article['cover_image']}"
    wa_share_url = f"https://api.whatsapp.com/send?text={article['title']} - Leia em: {canonical_url}"
    linkedin_share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={canonical_url}"

    # JSON-LD Schema
    schema_ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": article["title"],
        "description": article["excerpt"],
        "image": og_image,
        "datePublished": article["date"],
        "dateModified": article["date"],
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url
        },
        "author": {
            "@type": "Person",
            "name": author["name"],
            "jobTitle": author["role"]
        },
        "publisher": {
            "@type": "LegalService",
            "name": "Arruda Chudzy Advogadas",
            "logo": {
                "@type": "ImageObject",
                "url": "https://arrudachudzy.com.br/assets/images/logo-monogram.svg"
            }
        }
    }

    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{article['title']} | Arruda Chudzy Advogadas</title>
  <meta name="description" content="{article['excerpt']}">
  <meta name="author" content="{author['name']}">
  <link rel="canonical" href="{canonical_url}">

  <!-- Open Graph / WhatsApp / Facebook -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{article['title']} | Arruda Chudzy Advogadas">
  <meta property="og:description" content="{article['excerpt']}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:locale" content="pt_BR">
  <meta property="article:published_time" content="{article['date']}">
  <meta property="article:author" content="{author['name']}">
  <meta property="article:section" content="{article['category']}">

  <!-- Twitter Meta Tags -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{article['title']}">
  <meta name="twitter:description" content="{article['excerpt']}">
  <meta name="twitter:image" content="{og_image}">

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="../assets/images/favicon.svg">
  <link rel="manifest" href="../manifest.json">
  <meta name="theme-color" content="#65194B">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap">

  <!-- Consolidated Stylesheet -->
  <link rel="stylesheet" href="../assets/css/style.css">

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {json.dumps(schema_ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body class="article-page-body">
  <a href="#conteudo-artigo" class="skip-link">Pular para o conteúdo do artigo</a>

  <!-- Header -->
  <header class="site-header" role="banner">
    <div class="container navbar-container">
      <a href="../index.html" class="brand-logo" aria-label="Arruda Chudzy Advogadas - Página Inicial">
        <picture>
          <source type="image/webp" srcset="../assets/images/logo-oficial.webp">
          <img src="../assets/images/logo-oficial.png" alt="Arruda Chudzy Advogadas" class="brand-logo-img" width="160" height="46">
        </picture>
      </a>

      <nav class="nav-menu" role="navigation" aria-label="Navegação Principal">
        <a href="../index.html#inicio" class="nav-link">Início</a>
        <a href="../index.html#sobre" class="nav-link">Sobre</a>
        <a href="../index.html#socias" class="nav-link">Sócias</a>
        <a href="../index.html#atuacao" class="nav-link">Áreas de Atuação</a>
        <a href="../blog.html" class="nav-link active">Blog & Artigos</a>
        <a href="../index.html#eventos" class="nav-link">Eventos</a>
        <a href="../index.html#contato" class="nav-link">Contato</a>
      </nav>

      <div class="nav-actions">
        <a href="https://wa.me/5549999370099" target="_blank" rel="noopener noreferrer" class="nav-cta-btn" aria-label="Falar pelo WhatsApp com o escritório">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.074-2.127-.521-1.625-.675-2.656-2.34-2.736-2.448-.078-.108-.654-.869-.654-1.657 0-.787.413-1.174.558-1.332.144-.158.315-.198.421-.198.106 0 .211.002.304.006.098.004.229-.037.359.274.135.324.461 1.125.501 1.206.04.081.067.176.014.283-.054.108-.081.176-.161.27-.081.095-.17.211-.243.283-.081.081-.165.17-.071.332.095.162.42.34 1.229 1.42.128.114.244.151.343.19.123.048.243.042.335.028.115-.017.359-.147.501-.365.143-.217.143-.404.101-.485-.042-.081-.144-.131-.288-.202z"/></svg>
          <span>WhatsApp</span>
        </a>
      </div>

      <button class="menu-toggle" aria-label="Abrir menu de navegação" aria-expanded="false">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </header>

  <!-- Article Container -->
  <main id="conteudo-artigo" class="article-detail-page">
    <div class="container article-layout-container">
      
      <!-- Breadcrumbs -->
      <nav class="article-breadcrumbs" aria-label="Navegação em trilha">
        <a href="../index.html">Início</a>
        <span class="bc-sep">/</span>
        <a href="../blog.html">Blog &amp; Artigos</a>
        <span class="bc-sep">/</span>
        <span class="bc-current">{article['category']}</span>
      </nav>

      <!-- Article Header -->
      <header class="article-header-block">
        <span class="article-category-pill">{article['category']}</span>
        <h1 class="article-main-title">{article['title']}</h1>
        <p class="article-excerpt-lead">{article['excerpt']}</p>

        <!-- Meta Author Card -->
        <div class="article-meta-bar">
          <div class="article-author-avatar-wrap">
            <picture>
              <source type="image/webp" srcset="../{author['photo']}">
              <img src="../{author['fallback_photo']}" alt="{author['name']}" width="54" height="54" class="article-author-avatar">
            </picture>
          </div>
          <div class="article-author-info">
            <span class="article-author-name">{author['name']} <span class="oab-tag">{author['oab']}</span></span>
            <span class="article-author-sub">{author['role']}</span>
          </div>
          <div class="article-date-read-info">
            <time datetime="{article['date']}">{article['date_formatted']}</time>
            <span class="meta-dot">&bull;</span>
            <span>{article['reading_time']} de leitura</span>
          </div>
        </div>

        <!-- Social Share Bar -->
        <div class="article-share-strip">
          <span class="share-label">Compartilhar:</span>
          <a href="{wa_share_url}" target="_blank" rel="noopener noreferrer" class="share-btn share-wa" aria-label="Compartilhar no WhatsApp">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.074-2.127-.521-1.625-.675-2.656-2.34-2.736-2.448-.078-.108-.654-.869-.654-1.657 0-.787.413-1.174.558-1.332.144-.158.315-.198.421-.198.106 0 .211.002.304.006.098.004.229-.037.359.274.135.324.461 1.125.501 1.206.04.081.067.176.014.283-.054.108-.081.176-.161.27-.081.095-.17.211-.243.283-.081.081-.165.17-.071.332.095.162.42.34 1.229 1.42.128.114.244.151.343.19.123.048.243.042.335.028.115-.017.359-.147.501-.365.143-.217.143-.404.101-.485-.042-.081-.144-.131-.288-.202z"/></svg>
            <span>WhatsApp</span>
          </a>
          <a href="{linkedin_share_url}" target="_blank" rel="noopener noreferrer" class="share-btn share-li" aria-label="Compartilhar no LinkedIn">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
            <span>LinkedIn</span>
          </a>
          <button type="button" class="share-btn share-copy" onclick="navigator.clipboard.writeText(window.location.href); alert('Link copiado para a área de transferência!');" aria-label="Copiar link do artigo">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
            <span>Copiar Link</span>
          </button>
        </div>
      </header>

      <!-- Featured Image -->
      <div class="article-featured-media">
        <img src="../{article['cover_image']}" alt="{article['title']}" width="800" height="480" class="article-featured-img">
      </div>

      <!-- Article Content Body -->
      <article class="article-body-content">
        {article['body_html']}
      </article>

      <!-- Author Bio Footer Box -->
      <div class="article-author-bio-box">
        <picture>
          <source type="image/webp" srcset="../{author['photo']}">
          <img src="../{author['fallback_photo']}" alt="{author['name']}" width="90" height="90" class="bio-avatar">
        </picture>
        <div class="bio-text-col">
          <span class="bio-written-by">Artigo redigido por</span>
          <h3 class="bio-name">{author['name']} <span class="oab-tag-inline">{author['oab']}</span></h3>
          <p class="bio-desc">{author['bio']}</p>
          <div class="bio-actions">
            <a href="https://wa.me/5549999370099?text={author['wa_text']}" target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp" style="font-size: 0.9rem; padding: 12px 24px;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.074-2.127-.521-1.625-.675-2.656-2.34-2.736-2.448-.078-.108-.654-.869-.654-1.657 0-.787.413-1.174.558-1.332.144-.158.315-.198.421-.198.106 0 .211.002.304.006.098.004.229-.037.359.274.135.324.461 1.125.501 1.206.04.081.067.176.014.283-.054.108-.081.176-.161.27-.081.095-.17.211-.243.283-.081.081-.165.17-.071.332.095.162.42.34 1.229 1.42.128.114.244.151.343.19.123.048.243.042.335.028.115-.017.359-.147.501-.365.143-.217.143-.404.101-.485-.042-.081-.144-.131-.288-.202z"/></svg>
              <span>Consultar com a Autora via WhatsApp</span>
            </a>
            <a href="../blog.html" class="btn btn-secondary" style="font-size: 0.9rem; padding: 12px 24px; color: var(--color-primary-dark); border-color: var(--color-primary);">
              <span>Ver mais artigos do blog</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Related Articles Section -->
      {f"""
      <section class="related-articles-section">
        <h2 class="related-section-title">Publicações Relacionadas</h2>
        <div class="blog-grid" style="margin-top: 28px;">
          {related_html_cards}
        </div>
      </section>""" if related_html_cards else ""}

    </div>
  </main>

  <!-- Rodapé Oficial -->
  <footer class="site-footer" role="contentinfo">
    <div class="container">
      <div class="footer-top-grid">
        <div class="footer-brand-col">
          <a href="../index.html" class="brand-logo" style="margin-bottom: 16px;" aria-label="Arruda Chudzy Advogadas">
            <picture>
              <source type="image/webp" srcset="../assets/images/logo-oficial.webp">
              <img src="../assets/images/logo-oficial.png" alt="Arruda Chudzy Advogadas" class="brand-logo-img" width="180" height="53">
            </picture>
          </a>
          <p class="footer-lead-desc">
            Escritório de advocacia com atuação estratégica voltada à segurança jurídica de profissionais da saúde, empresas e pessoas físicas.
          </p>
          <div class="footer-oab-badge" style="gap: 8px;">
            <img src="../assets/images/logo-monogram-oficial.png" alt="AC" width="20" height="20" style="border-radius: 4px; display: inline-block; vertical-align: middle;">
            <span>Arruda Chudzy Advogadas &bull; OAB/SC 12.228</span>
          </div>
        </div>

        <div>
          <h4 class="footer-heading">Navegação</h4>
          <ul class="footer-links-list">
            <li class="footer-link-item"><a href="../index.html#inicio">Início</a></li>
            <li class="footer-link-item"><a href="../index.html#sobre">Sobre o Escritório</a></li>
            <li class="footer-link-item"><a href="../index.html#socias">Nossas Sócias</a></li>
            <li class="footer-link-item"><a href="../index.html#atuacao">Áreas de Atuação</a></li>
            <li class="footer-link-item"><a href="../blog.html">Blog & Artigos</a></li>
            <li class="footer-link-item"><a href="../index.html#contato">Fale Conosco</a></li>
            <li class="footer-link-item"><a href="../politica-de-privacidade.html">Política de Privacidade (LGPD)</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-heading">Áreas de Atuação</h4>
          <ul class="footer-links-list">
            <li class="footer-link-item"><a href="../index.html#atuacao">Direito Médico e da Saúde</a></li>
            <li class="footer-link-item"><a href="../index.html#atuacao">Contratos</a></li>
            <li class="footer-link-item"><a href="../index.html#atuacao">Direito Criminal</a></li>
            <li class="footer-link-item"><a href="../index.html#atuacao">Defesa Ética e CFM/CRM</a></li>
            <li class="footer-link-item"><a href="../index.html#atuacao">Compliance Médico</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-heading">Contato & Redes</h4>
          <div class="footer-contact-info">
            <div class="footer-contact-row">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.074-2.127-.521-1.625-.675-2.656-2.34-2.736-2.448-.078-.108-.654-.869-.654-1.657 0-.787.413-1.174.558-1.332.144-.158.315-.198.421-.198.106 0 .211.002.304.006.098.004.229-.037.359.274.135.324.461 1.125.501 1.206.04.081.067.176.014.283-.054.108-.081.176-.161.27-.081.095-.17.211-.243.283-.081.081-.165.17-.071.332.095.162.42.34 1.229 1.42.128.114.244.151.343.19.123.048.243.042.335.028.115-.017.359-.147.501-.365.143-.217.143-.404.101-.485-.042-.081-.144-.131-.288-.202z"/></svg>
              <div>
                <strong>WhatsApp:</strong><br>
                <a href="https://wa.me/5549999370099" target="_blank" rel="noopener noreferrer">(49) 99937-0099</a>
              </div>
            </div>
            <div class="footer-contact-row">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
              <div>
                <strong>Instagram:</strong><br>
                <a href="https://www.instagram.com/arrudachudzy/" target="_blank" rel="noopener noreferrer">@arrudachudzy</a>
              </div>
            </div>
            <div class="footer-contact-row">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
              <div>
                <strong>Endereço:</strong><br>
                Rua Coronel Córdova, 458, Sala 712<br>
                Edifício Azteca &bull; Centro, Lages - SC
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div>
          &copy; 2026 Arruda Chudzy Advogadas &bull; Todos os direitos reservados.
        </div>
        <div class="footer-bottom-links">
          <a href="../politica-de-privacidade.html" class="footer-privacy-link">Política de Privacidade (LGPD)</a>
          <span style="color: var(--color-support);">&bull;</span>
          <span style="color: var(--color-support);">OAB/SC 12.228</span>
        </div>
      </div>
    </div>
  </footer>

  <!-- Floating WhatsApp -->
  <a href="https://wa.me/5549999370099" target="_blank" rel="noopener noreferrer" class="floating-whatsapp-btn" aria-label="Falar pelo WhatsApp com Arruda Chudzy Advogadas">
    <svg width="34" height="34" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.074-2.127-.521-1.625-.675-2.656-2.34-2.736-2.448-.078-.108-.654-.869-.654-1.657 0-.787.413-1.174.558-1.332.144-.158.315-.198.421-.198.106 0 .211.002.304.006.098.004.229-.037.359.274.135.324.461 1.125.501 1.206.04.081.067.176.014.283-.054.108-.081.176-.161.27-.081.095-.17.211-.243.283-.081.081-.165.17-.071.332.095.162.42.34 1.229 1.42.128.114.244.151.343.19.123.048.243.042.335.028.115-.017.359-.147.501-.365.143-.217.143-.404.101-.485-.042-.081-.144-.131-.288-.202z"/></svg>
  </a>

  <!-- Mobile Menu JS Toggle -->
  <script>
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (menuToggle && navMenu) {{
      menuToggle.addEventListener('click', () => {{
        const open = navMenu.classList.toggle('is-open');
        menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      }});
    }}
  </script>
</body>
</html>'''
    return html

def generate_blog_index(articles):
    categories = sorted(list(set(a["category"] for a in articles)))
    category_buttons_html = '<button type="button" class="blog-filter-btn active" data-filter="all">Todos os Artigos</button>'
    for cat in categories:
        category_buttons_html += f'\n        <button type="button" class="blog-filter-btn" data-filter="{cat}">{cat}</button>'

    cards_html = ""
    for a in articles:
        cards_html += f'''
        <article class="blog-card" data-category="{a['category']}" data-title="{a['title'].lower()}" data-excerpt="{a['excerpt'].lower()}">
          <a href="artigos/{a['slug']}.html" class="blog-card-media" aria-label="Ler artigo: {a['title']}">
            <img src="{a['cover_image']}" alt="{a['title']}" width="400" height="240" loading="lazy">
            <span class="blog-category-badge">{a['category']}</span>
          </a>
          <div class="blog-card-body">
            <div class="blog-card-meta">
              <span>{a['date_formatted']}</span> &bull; <span>{a['reading_time']} de leitura</span>
            </div>
            <h2 class="blog-card-title">
              <a href="artigos/{a['slug']}.html">{a['title']}</a>
            </h2>
            <p class="blog-card-excerpt">{a['excerpt']}</p>
            <div class="blog-card-footer">
              <span class="blog-author-name">{a['author']}</span>
              <a href="artigos/{a['slug']}.html" class="blog-read-more">Ler Artigo &rarr;</a>
            </div>
          </div>
        </article>'''

    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog Jurídico & Artigos | Arruda Chudzy Advogadas - Lages e SC</title>
  <meta name="description" content="Artigos, pareceres e orientações jurídicas sobre Direito Médico, Contratos, Direito Criminal e Compliance em Saúde pelo escritório Arruda Chudzy Advogadas.">
  <link rel="canonical" href="https://arrudachudzy.com.br/blog.html">

  <!-- Open Graph / WhatsApp -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://arrudachudzy.com.br/blog.html">
  <meta property="og:title" content="Blog & Artigos Jurídicos | Arruda Chudzy Advogadas">
  <meta property="og:description" content="Análises técnicas, pareceres e novidades regulatórias sobre Direito Médico, Contratos e Direito Criminal.">
  <meta property="og:image" content="https://arrudachudzy.com.br/assets/images/og-preview.jpg">
  <meta property="og:locale" content="pt_BR">

  <!-- Twitter Meta Tags -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Blog & Artigos Jurídicos | Arruda Chudzy Advogadas">
  <meta name="twitter:description" content="Análises técnicas, pareceres e novidades regulatórias sobre Direito Médico, Contratos e Direito Criminal.">
  <meta name="twitter:image" content="https://arrudachudzy.com.br/assets/images/og-preview.jpg">

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="assets/images/favicon.svg">
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#65194B">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap">

  <!-- Consolidated Stylesheet -->
  <link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="blog-hub-page">
  <a href="#conteudo-blog" class="skip-link">Pular para o conteúdo do blog</a>

  <!-- Header -->
  <header class="site-header" role="banner">
    <div class="container navbar-container">
      <a href="index.html" class="brand-logo" aria-label="Arruda Chudzy Advogadas - Página Inicial">
        <picture>
          <source type="image/webp" srcset="assets/images/logo-oficial.webp">
          <img src="assets/images/logo-oficial.png" alt="Arruda Chudzy Advogadas" class="brand-logo-img" width="160" height="46">
        </picture>
      </a>

      <nav class="nav-menu" role="navigation" aria-label="Navegação Principal">
        <a href="index.html#inicio" class="nav-link">Início</a>
        <a href="index.html#sobre" class="nav-link">Sobre</a>
        <a href="index.html#socias" class="nav-link">Sócias</a>
        <a href="index.html#atuacao" class="nav-link">Áreas de Atuação</a>
        <a href="blog.html" class="nav-link active">Blog &amp; Artigos</a>
        <a href="index.html#eventos" class="nav-link">Eventos</a>
        <a href="index.html#contato" class="nav-link">Contato</a>
      </nav>

      <div class="nav-actions">
        <a href="https://wa.me/5549999370099" target="_blank" rel="noopener noreferrer" class="nav-cta-btn" aria-label="Falar pelo WhatsApp com o escritório">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.074-2.127-.521-1.625-.675-2.656-2.34-2.736-2.448-.078-.108-.654-.869-.654-1.657 0-.787.413-1.174.558-1.332.144-.158.315-.198.421-.198.106 0 .211.002.304.006.098.004.229-.037.359.274.135.324.461 1.125.501 1.206.04.081.067.176.014.283-.054.108-.081.176-.161.27-.081.095-.17.211-.243.283-.081.081-.165.17-.071.332.095.162.42.34 1.229 1.42.128.114.244.151.343.19.123.048.243.042.335.028.115-.017.359-.147.501-.365.143-.217.143-.404.101-.485-.042-.081-.144-.131-.288-.202z"/></svg>
          <span>WhatsApp</span>
        </a>
      </div>

      <button class="menu-toggle" aria-label="Abrir menu de navegação" aria-expanded="false">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </header>

  <!-- Hero do Blog -->
  <section class="blog-hero-section">
    <div class="container text-center">
      <div class="section-tag" style="display: inline-block; margin-bottom: 12px;">Conhecimento Estratégico</div>
      <h1 class="blog-hero-title">Blog Jurídico &amp; Artigos</h1>
      <p class="blog-hero-sub">
        Análises práticas, pareceres técnicos e diretrizes legais com foco em Direito Médico e da Saúde, Contratos e Direito Criminal.
      </p>

      <!-- Barra de Busca Instantânea -->
      <div class="blog-search-wrapper">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="blogSearchInput" class="blog-search-input" placeholder="Buscar por tema, palavra-chave ou legislação..." aria-label="Buscar artigos do blog">
      </div>

      <!-- Filtros de Categorias -->
      <div class="blog-filters-bar" role="tablist">
        {category_buttons_html}
      </div>
    </div>
  </section>

  <!-- Grade de Artigos -->
  <main id="conteudo-blog" class="blog-main-content">
    <div class="container">
      <div class="blog-grid" id="articlesGrid">
        {cards_html}
      </div>

      <!-- Estado Vazio para Busca -->
      <div id="noResultsMsg" class="blog-no-results" style="display: none;">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin: 0 auto 16px; color: var(--color-primary);"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <h3>Nenhum artigo encontrado</h3>
        <p>Não encontramos artigos para a busca realizada. Tente outro termo ou limpe os filtros de categoria.</p>
        <button type="button" class="btn btn-secondary" onclick="resetBlogFilters()" style="margin-top: 16px;">Ver Todos os Artigos</button>
      </div>

      <!-- Banner de Contato Direto -->
      <div class="blog-contact-cta-banner">
        <div class="cta-banner-text">
          <h3>Dúvidas sobre os temas abordados nos artigos?</h3>
          <p>Converse diretamente com as advogadas sócias para avaliar a situação da sua clínica ou demanda jurídica com sigilo e rapidez.</p>
        </div>
        <div class="cta-banner-action">
          <a href="https://wa.me/5549999370099" target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp" style="padding: 16px 32px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.074-2.127-.521-1.625-.675-2.656-2.34-2.736-2.448-.078-.108-.654-.869-.654-1.657 0-.787.413-1.174.558-1.332.144-.158.315-.198.421-.198.106 0 .211.002.304.006.098.004.229-.037.359.274.135.324.461 1.125.501 1.206.04.081.067.176.014.283-.054.108-.081.176-.161.27-.081.095-.17.211-.243.283-.081.081-.165.17-.071.332.095.162.42.34 1.229 1.42.128.114.244.151.343.19.123.048.243.042.335.028.115-.017.359-.147.501-.365.143-.217.143-.404.101-.485-.042-.081-.144-.131-.288-.202z"/></svg>
            <span>Falar pelo WhatsApp</span>
          </a>
        </div>
      </div>
    </div>
  </main>

  <!-- Rodapé Oficial -->
  <footer class="site-footer" role="contentinfo">
    <div class="container">
      <div class="footer-top-grid">
        <div class="footer-brand-col">
          <a href="index.html" class="brand-logo" style="margin-bottom: 16px;" aria-label="Arruda Chudzy Advogadas">
            <picture>
              <source type="image/webp" srcset="assets/images/logo-oficial.webp">
              <img src="assets/images/logo-oficial.png" alt="Arruda Chudzy Advogadas" class="brand-logo-img" width="180" height="53">
            </picture>
          </a>
          <p class="footer-lead-desc">
            Escritório de advocacia com atuação estratégica voltada à segurança jurídica de profissionais da saúde, empresas e pessoas físicas.
          </p>
          <div class="footer-oab-badge" style="gap: 8px;">
            <img src="assets/images/logo-monogram-oficial.png" alt="AC" width="20" height="20" style="border-radius: 4px; display: inline-block; vertical-align: middle;">
            <span>Arruda Chudzy Advogadas &bull; OAB/SC 12.228</span>
          </div>
        </div>

        <div>
          <h4 class="footer-heading">Navegação</h4>
          <ul class="footer-links-list">
            <li class="footer-link-item"><a href="index.html#inicio">Início</a></li>
            <li class="footer-link-item"><a href="index.html#sobre">Sobre o Escritório</a></li>
            <li class="footer-link-item"><a href="index.html#socias">Nossas Sócias</a></li>
            <li class="footer-link-item"><a href="index.html#atuacao">Áreas de Atuação</a></li>
            <li class="footer-link-item"><a href="blog.html">Blog &amp; Artigos</a></li>
            <li class="footer-link-item"><a href="index.html#contato">Fale Conosco</a></li>
            <li class="footer-link-item"><a href="politica-de-privacidade.html">Política de Privacidade (LGPD)</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-heading">Áreas de Atuação</h4>
          <ul class="footer-links-list">
            <li class="footer-link-item"><a href="index.html#atuacao">Direito Médico e da Saúde</a></li>
            <li class="footer-link-item"><a href="index.html#atuacao">Contratos</a></li>
            <li class="footer-link-item"><a href="index.html#atuacao">Direito Criminal</a></li>
            <li class="footer-link-item"><a href="index.html#atuacao">Defesa Ética e CFM/CRM</a></li>
            <li class="footer-link-item"><a href="index.html#atuacao">Compliance Médico</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-heading">Contato &amp; Redes</h4>
          <div class="footer-contact-info">
            <div class="footer-contact-row">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.074-2.127-.521-1.625-.675-2.656-2.34-2.736-2.448-.078-.108-.654-.869-.654-1.657 0-.787.413-1.174.558-1.332.144-.158.315-.198.421-.198.106 0 .211.002.304.006.098.004.229-.037.359.274.135.324.461 1.125.501 1.206.04.081.067.176.014.283-.054.108-.081.176-.161.27-.081.095-.17.211-.243.283-.081.081-.165.17-.071.332.095.162.42.34 1.229 1.42.128.114.244.151.343.19.123.048.243.042.335.028.115-.017.359-.147.501-.365.143-.217.143-.404.101-.485-.042-.081-.144-.131-.288-.202z"/></svg>
              <div>
                <strong>WhatsApp:</strong><br>
                <a href="https://wa.me/5549999370099" target="_blank" rel="noopener noreferrer">(49) 99937-0099</a>
              </div>
            </div>
            <div class="footer-contact-row">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
              <div>
                <strong>Instagram:</strong><br>
                <a href="https://www.instagram.com/arrudachudzy/" target="_blank" rel="noopener noreferrer">@arrudachudzy</a>
              </div>
            </div>
            <div class="footer-contact-row">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
              <div>
                <strong>Endereço:</strong><br>
                Rua Coronel Córdova, 458, Sala 712<br>
                Edifício Azteca &bull; Centro, Lages - SC
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div>
          &copy; 2026 Arruda Chudzy Advogadas &bull; Todos os direitos reservados.
        </div>
        <div class="footer-bottom-links">
          <a href="politica-de-privacidade.html" class="footer-privacy-link">Política de Privacidade (LGPD)</a>
          <span style="color: var(--color-support);">&bull;</span>
          <span style="color: var(--color-support);">OAB/SC 12.228</span>
        </div>
      </div>
    </div>
  </footer>

  <!-- Floating WhatsApp -->
  <a href="https://wa.me/5549999370099" target="_blank" rel="noopener noreferrer" class="floating-whatsapp-btn" aria-label="Falar pelo WhatsApp com Arruda Chudzy Advogadas">
    <svg width="34" height="34" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.074-2.127-.521-1.625-.675-2.656-2.34-2.736-2.448-.078-.108-.654-.869-.654-1.657 0-.787.413-1.174.558-1.332.144-.158.315-.198.421-.198.106 0 .211.002.304.006.098.004.229-.037.359.274.135.324.461 1.125.501 1.206.04.081.067.176.014.283-.054.108-.081.176-.161.27-.081.095-.17.211-.243.283-.081.081-.165.17-.071.332.095.162.42.34 1.229 1.42.128.114.244.151.343.19.123.048.243.042.335.028.115-.017.359-.147.501-.365.143-.217.143-.404.101-.485-.042-.081-.144-.131-.288-.202z"/></svg>
  </a>

  <!-- Mobile Menu & Search Script -->
  <script>
    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (menuToggle && navMenu) {{
      menuToggle.addEventListener('click', () => {{
        const open = navMenu.classList.toggle('is-open');
        menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      }});
    }}

    // Real-time Blog Filter & Search Engine
    const searchInput = document.getElementById('blogSearchInput');
    const filterBtns = document.querySelectorAll('.blog-filter-btn');
    const cards = document.querySelectorAll('.blog-card');
    const noResults = document.getElementById('noResultsMsg');

    let currentFilter = 'all';

    function filterArticles() {{
      const query = (searchInput ? searchInput.value : '').toLowerCase().trim();
      let visibleCount = 0;

      cards.forEach(card => {{
        const cat = card.getAttribute('data-category');
        const title = card.getAttribute('data-title');
        const excerpt = card.getAttribute('data-excerpt');

        const matchesCat = (currentFilter === 'all' || cat === currentFilter);
        const matchesQuery = (!query || title.includes(query) || excerpt.includes(query));

        if (matchesCat && matchesQuery) {{
          card.style.display = 'flex';
          visibleCount++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      if (noResults) {{
        noResults.style.display = (visibleCount === 0) ? 'block' : 'none';
      }}
    }}

    if (filterBtns) {{
      filterBtns.forEach(btn => {{
        btn.addEventListener('click', () => {{
          filterBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          currentFilter = btn.getAttribute('data-filter');
          filterArticles();
        }});
      }});
    }}

    if (searchInput) {{
      searchInput.addEventListener('input', filterArticles);
    }}

    function resetBlogFilters() {{
      if (searchInput) searchInput.value = '';
      currentFilter = 'all';
      if (filterBtns) {{
        filterBtns.forEach(b => {{
          if (b.getAttribute('data-filter') === 'all') b.classList.add('active');
          else b.classList.remove('active');
        }});
      }}
      filterArticles();
    }}
  </script>
</body>
</html>'''
    return html

def update_home_page_blog_section(articles):
    if not os.path.exists(INDEX_HTML_PATH):
        return
    with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Generate 3 latest articles cards
    top3 = articles[:3]
    cards_html = ""
    for a in top3:
        cards_html += f'''
          <article class="blog-card" data-fx="subir">
            <a href="artigos/{a['slug']}.html" class="blog-card-media" aria-label="Ler artigo: {a['title']}">
              <img src="{a['cover_image']}" alt="{a['title']}" width="400" height="240" loading="lazy">
              <span class="blog-category-badge">{a['category']}</span>
            </a>
            <div class="blog-card-body">
              <div class="blog-card-meta">
                <span>{a['date_formatted']}</span> &bull; <span>{a['reading_time']}</span>
              </div>
              <h3 class="blog-card-title">
                <a href="artigos/{a['slug']}.html">{a['title']}</a>
              </h3>
              <p class="blog-card-excerpt">{a['excerpt'][:125]}...</p>
              <div class="blog-card-footer">
                <span class="blog-author-name">{a['author']}</span>
                <a href="artigos/{a['slug']}.html" class="blog-read-more">Ler Artigo &rarr;</a>
              </div>
            </div>
          </article>'''

    new_blog_section = f'''<!-- =====================================================================
         ARTIGOS & CONTEÚDO JURÍDICO (BLOG)
         ===================================================================== -->
    <section id="artigos" class="section" data-fx-fundo="#FAF6F8" data-fx-tinta="#25071B">
      <div class="container">
        <div class="section-header" data-fx="subir">
          <div class="section-tag">Análises &amp; Atualizações</div>
          <h2 class="section-title">Artigos e Conteúdo Estratégico</h2>
          <p class="section-subtitle">
            Orientações práticas e artigos fundamentados em Direito Médico, Contratos e Direito Criminal, elaborados pelas advogadas sócias do escritório.
          </p>
        </div>

        <div class="blog-grid" style="margin-top: 40px;">
          {cards_html}
        </div>

        <div class="text-center" style="margin-top: 48px;" data-fx="subir">
          <a href="blog.html" class="btn btn-secondary" style="color: var(--color-primary-dark); border-color: var(--color-primary); padding: 16px 36px;">
            <span>Acessar Todos os Artigos do Blog</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
          </a>
        </div>
      </div>
    </section>'''

    # Check if section already exists, otherwise insert before #eventos
    if '<section id="artigos"' in html:
        # replace existing section
        pattern = r"<!-- =+\s*ARTIGOS & CONTEÚDO JURÍDICO \(BLOG\).*?</section>"
        html = re.sub(pattern, new_blog_section, html, flags=re.DOTALL)
    else:
        # insert before <section id="eventos"
        target = '<!-- =====================================================================\n         EVENTOS E CONTEÚDO JURÍDICO'
        if target in html:
            html = html.replace(target, new_blog_section + "\n\n    " + target)

    # Ensure navbar in index.html includes Artigos link
    old_nav = '<a href="#atuacao" class="nav-link">Áreas de Atuação</a>\n        <a href="#eventos" class="nav-link">Eventos</a>'
    new_nav = '<a href="#atuacao" class="nav-link">Áreas de Atuação</a>\n        <a href="#artigos" class="nav-link">Artigos</a>\n        <a href="#eventos" class="nav-link">Eventos</a>'
    if old_nav in html and '<a href="#artigos"' not in html:
        html = html.replace(old_nav, new_nav)

    # Ensure footer in index.html includes Blog link
    old_footer_link = '<li class="footer-link-item"><a href="#atuacao">Áreas de Atuação</a></li>\n            <li class="footer-link-item"><a href="#eventos">Eventos & Conteúdo</a></li>'
    new_footer_link = '<li class="footer-link-item"><a href="#atuacao">Áreas de Atuação</a></li>\n            <li class="footer-link-item"><a href="blog.html">Blog & Artigos</a></li>\n            <li class="footer-link-item"><a href="#eventos">Eventos & Conteúdo</a></li>'
    if old_footer_link in html:
        html = html.replace(old_footer_link, new_footer_link)

    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated index.html with blog section and navigation links.")

def update_sitemap(articles):
    today = datetime.now().strftime("%Y-%m-%d")
    urls = [
        ("https://arrudachudzy.com.br/", today, "weekly", "1.0"),
        ("https://arrudachudzy.com.br/blog.html", today, "weekly", "0.9"),
        ("https://arrudachudzy.com.br/politica-de-privacidade.html", today, "monthly", "0.5")
    ]
    for a in articles:
        urls.append((f"https://arrudachudzy.com.br/artigos/{a['slug']}.html", a["date"], "monthly", "0.8"))

    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, changefreq, prio in urls:
        sitemap_xml.append("  <url>")
        sitemap_xml.append(f"    <loc>{loc}</loc>")
        sitemap_xml.append(f"    <lastmod>{lastmod}</lastmod>")
        sitemap_xml.append(f"    <changefreq>{changefreq}</changefreq>")
        sitemap_xml.append(f"    <priority>{prio}</priority>")
        sitemap_xml.append("  </url>")
    sitemap_xml.append("</urlset>\n")

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_xml))
    print(f"Updated sitemap.xml with {len(urls)} URLs.")

def main():
    print("Loading articles from content/artigos...")
    articles = load_all_articles()
    print(f"Found {len(articles)} articles.")

    os.makedirs(ARTICLES_OUT_DIR, exist_ok=True)

    print("Generating individual article pages in artigos/...")
    for a in articles:
        html = generate_article_page(a, articles)
        out_path = os.path.join(ARTICLES_OUT_DIR, f"{a['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f" - Generated: artigos/{a['slug']}.html")

    print("Generating blog hub in blog.html...")
    blog_html = generate_blog_index(articles)
    with open(BLOG_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(blog_html)
    print(" - Generated: blog.html")

    print("Updating home page (index.html)...")
    update_home_page_blog_section(articles)

    print("Updating sitemap.xml...")
    update_sitemap(articles)

    print("\nSUCCESS: All blog pages generated and synced!")

if __name__ == "__main__":
    main()
