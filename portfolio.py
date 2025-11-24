from __future__ import annotations

from html import escape
from pathlib import Path
from string import Template
import json

# Data populated from the original Flask app.
PORTFOLIO = {
    "name": "Mariyam Sohail",
    "tagline": "MS Data Science | AI Engineer | Math Educator",
    "sections": [
        {
            "id": "education",
            "title": "Education",
            "items": [
                {
                    "title": "MS in Data Science — Information Technology University",
                    "subtitle": "Aug 2024 – Present",
                    "description": "Coursework: Machine Learning, Deep Learning, Reinforcement Learning, Big Data, Statistics.",
                    "badge": "MS Data Science",
                },
                {
                    "title": "BS in Mathematics — University of Central Punjab",
                    "subtitle": "Oct 2019 – June 2023",
                    "description": "CGPA: 3.66. Coursework includes Linear Algebra, Differential Equations, Calculus.",
                    "badge": "BS Mathematics",
                },
            ],
        },
        {
            "id": "experience",
            "title": "Experience",
            "items": [
                {
                    "title": "AI Engineer — Clab AI",
                    "subtitle": "Aug 2025 – Present",
                    "description": "Built specialized AI agents, RAG pipelines (LangChain, OpenAI embeddings, ChromaDB). Streamlit tools for PMs.",
                    "badge": "AI Engineer",
                },
                {
                    "title": "Visiting Lecturer — Lahore School of Innovation & Technology",
                    "subtitle": "July 2024 – Present",
                    "description": "Taught Applied Mathematics and Statistics; designed analytically rigorous assessments.",
                    "badge": "Lecturer",
                },
            ],
        },
        {
            "id": "projects",
            "title": "Projects",
            "items": [
                {
                    "title": "Floww LLM — Multi-Model Chat App",
                    "subtitle": "Full-stack AI chat app",
                    "description": "Dynamic flow logic, file uploads, multi-LLM integration (LangChain, OpenRouter).",
                    "badge": "Full-Stack",
                },
                {
                    "title": "Image Captioning (ResNet + LSTM)",
                    "subtitle": "Deep Learning project",
                    "description": "Image captioning pipeline with ResNet-50 encoder and multi-layer LSTM decoder.",
                    "badge": "CV / NLP",
                },
                {
                    "title": "Transformer for StackOverflow Text Gen",
                    "subtitle": "From-scratch transformer",
                    "description": "Decoder-only transformer with masked attention and top-k sampling for code Q&A.",
                    "badge": "NLP",
                },
            ],
        },
        {
            "id": "skills",
            "title": "Skills",
            "items": [
                {"title": "Python", "subtitle": "NumPy, Pandas, PyTorch"},
                {"title": "Machine Learning", "subtitle": "Scikit-learn, PyTorch"},
                {"title": "LLM Tooling", "subtitle": "LangChain, OpenRouter, ChromaDB"},
                {"title": "Web / Tools", "subtitle": "Streamlit, Flask, Git, VS Code"},
            ],
        },
        {
            "id": "achievements",
            "title": "Achievements",
            "items": [
                {
                    "title": "3rd — National Mathenasium Competition",
                    "subtitle": "Mar 2023",
                },
                {
                    "title": "Poster Presentation — UCP Research Forum",
                    "subtitle": "Jun 2022",
                },
            ],
        },
    ],
    "contact": {
        "email": "mariyamsohail2011@gmail.com",
        "location": "Lahore",
        "github": "github.com/yourusername",
        "linkedin": "linkedin.com/in/mariyamsohail",
    },
}


HTML_TEMPLATE = Template(
    """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>$name — Portfolio</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <style>
    :root{
      --bg:#0b0f14;
      --card:#0f1720;
      --accent:#e50914;
      --muted:#9aa4b2;
      --white:#eef2f5;
    }
    *{box-sizing:border-box;font-family:Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;}
    body{margin:0;background:linear-gradient(180deg,#071018 0%, #0b0f14 100%);color:var(--white);min-height:100vh;}
    header{display:flex;align-items:center;justify-content:space-between;padding:18px 32px;border-bottom:1px solid rgba(255,255,255,0.03)}
    .brand{display:flex;gap:14px;align-items:center}
    .logo{background:var(--accent);width:46px;height:30px;border-radius:4px;display:flex;align-items:center;justify-content:center;font-weight:700}
    .title{font-size:18px;font-weight:600}
    .tag{color:var(--muted);font-size:13px}
    main{padding:28px 32px;}
    .hero{display:flex;gap:24px;align-items:center;margin-bottom:28px}
    .hero-left{flex:1}
    .hero-right{width:320px}
    .hero h1{margin:0;font-size:34px}
    .hero p{color:var(--muted);margin:8px 0 0}
    .row{margin:18px 0}
    .row-title{display:flex;align-items:center;gap:12px;margin-bottom:10px}
    .row-title h2{margin:0;font-size:18px}
    .carousel{display:flex;gap:12px;overflow-x:auto;padding-bottom:6px;scroll-behavior:smooth}
    .carousel::-webkit-scrollbar{height:10px}
    .carousel::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.08);border-radius:8px}
    .tile{min-width:220px;height:130px;background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.005));border-radius:8px;padding:12px;position:relative;cursor:pointer;transition:transform .18s ease, box-shadow .18s ease}
    .tile:hover{transform:translateY(-10px) scale(1.03);box-shadow:0 10px 30px rgba(0,0,0,0.6)}
    .tile-badge{position:absolute;right:10px;top:10px;background:rgba(255,255,255,0.06);padding:6px 8px;border-radius:6px;font-size:12px;color:var(--muted)}
    .tile h3{margin:0 0 6px 0;font-size:16px}
    .tile p{margin:0;color:var(--muted);font-size:13px;line-height:1.2}
    .small{font-size:13px;color:var(--muted)}
    .chip{display:inline-block;padding:6px 10px;border-radius:999px;background:rgba(255,255,255,0.03);font-size:13px;margin-right:8px}
    .modal{position:fixed;inset:0;display:none;align-items:center;justify-content:center;background:rgba(2,6,9,0.6);z-index:40}
    .modal.open{display:flex}
    .modal-card{width:min(880px,96%);background:linear-gradient(180deg,#0f1720,#0b1116);padding:20px;border-radius:10px;box-shadow:0 20px 40px rgba(0,0,0,0.7);color:var(--white)}
    .modal-header{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
    .close-btn{border:none;background:transparent;color:var(--muted);font-size:20px;cursor:pointer}
    @media (max-width:900px){
      .hero{flex-direction:column;align-items:flex-start}
      .hero-right{width:100%}
      .tile{min-width:170px;height:120px}
    }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="logo">M</div>
      <div>
        <div class="title">$name</div>
        <div class="tag">$tagline</div>
      </div>
    </div>
    <nav style="display:flex;gap:12px;align-items:center">
      <a href="#projects" style="color:var(--muted);text-decoration:none">Projects</a>
      <a href="#experience" style="color:var(--muted);text-decoration:none">Experience</a>
      <a href="#contact" style="color:var(--muted);text-decoration:none">Contact</a>
    </nav>
  </header>

  <main>
    <section class="hero" aria-label="hero">
      <div class="hero-left">
        <h1>From Equations to Intelligence</h1>
        <p class="small">Browse my professional journey like a streaming catalog — each profile is a deep-dive into a skill, project, or role.</p>
        <div style="margin-top:12px">
          <span class="chip">Open to work</span>
          <span class="chip">Research &amp; ML</span>
          <span class="chip">Teaching</span>
        </div>
      </div>
      <div class="hero-right">
        <div style="background:linear-gradient(180deg,#0b1116,#071018);padding:14px;border-radius:8px">
          <div style="font-weight:600">$name</div>
          <div class="small">$tagline</div>
          <div style="margin-top:10px;color:var(--muted);font-size:13px">
            $location · $email
            <div style="margin-top:8px">
              <a href="https://$github" target="_blank" style="color:var(--muted);text-decoration:none;margin-right:10px">GitHub</a>
              <a href="https://$linkedin" target="_blank" style="color:var(--muted);text-decoration:none">LinkedIn</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    $sections

    <section id="contact" style="margin-top:28px">
      <h2>Contact</h2>
      <p class="small">Email: <a href="mailto:$email">$email</a> · Location: $location</p>
    </section>
  </main>

  <div id="modal" class="modal" role="dialog" aria-modal="true">
    <div class="modal-card" id="modalCard">
      <div class="modal-header">
        <div>
          <h3 id="md-title">Title</h3>
          <div class="small" id="md-sub">Subtitle</div>
        </div>
        <div>
          <button class="close-btn" id="modalClose" aria-label="close">✕</button>
        </div>
      </div>
      <div id="md-body" style="margin-top:12px;color:var(--muted)"></div>
    </div>
  </div>

  <script>
    const DATA = $data_json;
    document.querySelectorAll('.tile').forEach(tile => {
      tile.addEventListener('click', () => {
        const sectionId = tile.getAttribute('data-section');
        const idx = parseInt(tile.getAttribute('data-index'));
        const section = DATA.sections.find(s => s.id === sectionId);
        const item = section.items[idx];
        document.getElementById('md-title').innerText = item.title;
        document.getElementById('md-sub').innerText = item.subtitle || '';
        const desc = item.description || (item.subtitle ? item.subtitle : '');
        document.getElementById('md-body').innerText = desc;
        document.getElementById('modal').classList.add('open');
      });
    });

    document.getElementById('modalClose').addEventListener('click', () => {
      document.getElementById('modal').classList.remove('open');
    });
    document.getElementById('modal').addEventListener('click', (e) => {
      if(e.target === document.getElementById('modal')) document.getElementById('modal').classList.remove('open');
    });

    document.querySelectorAll('.carousel').forEach(car => {
      car.addEventListener('keydown', (e) => {
        if(e.key === 'ArrowRight') car.scrollBy({left:260, behavior:'smooth'});
        if(e.key === 'ArrowLeft') car.scrollBy({left:-260, behavior:'smooth'});
      });
    });

    document.querySelectorAll('.carousel').forEach(car => {
      let pressed = false, startX = 0, scrollLeft = 0;
      car.addEventListener('mousedown', e => { pressed = true; startX = e.pageX - car.offsetLeft; scrollLeft = car.scrollLeft; car.style.cursor='grabbing' });
      car.addEventListener('mouseleave', () => { pressed=false; car.style.cursor='default' });
      car.addEventListener('mouseup', () => { pressed=false; car.style.cursor='default' });
      car.addEventListener('mousemove', e => {
        if(!pressed) return;
        e.preventDefault();
        const x = e.pageX - car.offsetLeft;
        const walk = (x - startX) * 1.1;
        car.scrollLeft = scrollLeft - walk;
      });
    });
  </script>
</body>
</html>
"""
)


def _render_tile(section_id: str, index: int, item: dict[str, str]) -> str:
    desc = ""
    if item.get("description"):
        desc = (
            '<p style="margin-top:8px;color:var(--muted);font-size:12px;max-height:40px;overflow:hidden">'
            f"{escape(item['description'])}"
            "</p>"
        )
    badge = escape(item.get("badge", ""))
    return (
        '        <div class="tile" role="button" data-section="'
        f"{escape(section_id)}"
        '" data-index="'
        f"{index}"
        '">\n'
        f'          <div class="tile-badge">{badge}</div>\n'
        f"          <h3>{escape(item['title'])}</h3>\n"
        f"          <p>{escape(item.get('subtitle', ''))}</p>\n"
        f"{desc}\n"
        "        </div>"
    )


def _render_section(section: dict[str, str]) -> str:
    tiles = "\n".join(
        _render_tile(section["id"], idx, item)
        for idx, item in enumerate(section["items"])
    )
    return f"""
    <section class="row" id="{escape(section["id"])}">
      <div class="row-title">
        <h2>{escape(section["title"])}</h2>
        <div class="small" style="margin-left:auto">Press ← → to scroll</div>
      </div>
      <div class="carousel" tabindex="0" data-section="{escape(section["id"])}">
{tiles}
      </div>
    </section>"""


def build_static_site(output_file: Path) -> None:
    sections_html = "\n".join(
        _render_section(section) for section in PORTFOLIO["sections"]
    )
    html = HTML_TEMPLATE.substitute(
        name=escape(PORTFOLIO["name"]),
        tagline=escape(PORTFOLIO["tagline"]),
        email=escape(PORTFOLIO["contact"]["email"]),
        location=escape(PORTFOLIO["contact"]["location"]),
        github=escape(PORTFOLIO["contact"]["github"]),
        linkedin=escape(PORTFOLIO["contact"]["linkedin"]),
        sections=sections_html,
        data_json=json.dumps(PORTFOLIO, indent=2),
    )
    output_file.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build_static_site(Path(__file__).with_name("index.html"))
