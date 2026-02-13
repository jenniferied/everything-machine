#!/usr/bin/env python3
"""Generate Anhang (appendix) from journal markdown files.

Parses journal entries, extracts article text and chat transcripts,
outputs Pandoc markdown with LaTeX raw blocks for chat bubbles.
"""

import re
import os
import sys
import hashlib
import subprocess
from html.parser import HTMLParser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSION_DIR = os.path.join(SCRIPT_DIR, "..")
REPO_ROOT = os.path.normpath(os.path.join(SUBMISSION_DIR, "..", ".."))
JOURNAL_DIR = os.path.join(REPO_ROOT, "journal")
IMG_CACHE_DIR = os.path.join(SUBMISSION_DIR, "_img_cache")

# Max pixel width for optimized images.
# 1200px covers 60% of A4 text width at ~200 DPI — sharp enough for print.
MAX_IMG_WIDTH = 1200


def optimize_image(src_rel_path):
    """Resize image for print and cache the result. Returns path usable by LaTeX."""
    abs_src = os.path.normpath(os.path.join(REPO_ROOT, src_rel_path))
    if not os.path.exists(abs_src):
        return src_rel_path  # fallback to original

    os.makedirs(IMG_CACHE_DIR, exist_ok=True)

    ext = os.path.splitext(src_rel_path)[1].lower()
    # Use content hash for cache filename
    cache_name = hashlib.md5(src_rel_path.encode()).hexdigest() + ext
    cache_path = os.path.join(IMG_CACHE_DIR, cache_name)

    # Skip if cache is newer than source
    if os.path.exists(cache_path) and os.path.getmtime(cache_path) >= os.path.getmtime(abs_src):
        return f"_img_cache/{cache_name}"

    # Get current width
    try:
        result = subprocess.run(
            ["sips", "-g", "pixelWidth", abs_src],
            capture_output=True, text=True,
        )
        width = int(result.stdout.strip().split()[-1])
    except (ValueError, IndexError):
        return src_rel_path

    if width <= MAX_IMG_WIDTH:
        # Already small enough — just copy
        subprocess.run(["cp", abs_src, cache_path], capture_output=True)
    else:
        # Resize with sips (nearest-neighbor not available, but lanczos is fine for photos)
        subprocess.run(
            ["sips", "--resampleWidth", str(MAX_IMG_WIDTH), abs_src, "--out", cache_path],
            capture_output=True,
        )

    return f"_img_cache/{cache_name}"

# Journal files in chronological order with metadata
JOURNALS = [
    {
        "file": "journal-2025-11-15-referenzen-sammeln.md",
        "nr": 1,
        "datum": "15. November 2025",
        "titel": "Referenzen für Kepler sammeln",
        "tools": "Pinterest, Google Drive",
        "modalitaet": "---",
    },
    {
        "file": "journal-2025-11-16-comfyui-consistent-character.md",
        "nr": 2,
        "datum": "16. November 2025",
        "titel": "ComfyUI Consistent Character Workflow",
        "tools": "ComfyUI, Flux, IP-Adapter",
        "modalitaet": "Bild",
    },
    {
        "file": "journal-2025-11-18-marble-worldlabs.md",
        "nr": 3,
        "datum": "18. November 2025",
        "titel": "Marble von Worldlabs",
        "tools": "Marble, Claude",
        "modalitaet": "3D",
    },
    {
        "file": "journal-2025-11-19-cursor-build.md",
        "nr": 4,
        "datum": "19. November 2025",
        "titel": "Website mit Cursor aufsetzen",
        "tools": "Cursor, Claude",
        "modalitaet": "Code",
    },
    {
        "file": "journal-2026-01-11-ki-verstehen.md",
        "nr": 5,
        "datum": "11. Januar 2026",
        "titel": "KI wirklich verstehen -- Teil 1",
        "tools": "Claude (Voice)",
        "modalitaet": "Dialog",
    },
    {
        "file": "journal-2026-01-12-suno-experiment.md",
        "nr": 6,
        "datum": "12. Januar 2026",
        "titel": "Suno-Experiment",
        "tools": "Suno AI",
        "modalitaet": "Audio",
    },
    {
        "file": "journal-2026-01-25-recherche-kepler-zweiter-versuch.md",
        "nr": 7,
        "datum": "25. Januar 2026",
        "titel": "Kepler-Recherche, zweiter Versuch",
        "tools": "Claude, Semantic Scholar, GitHub",
        "modalitaet": "Recherche",
    },
]


def escape_latex(text):
    """Escape LaTeX special characters in plain text."""
    # Order matters: & first, then others
    text = text.replace("\\", "\\textbackslash{}")
    text = text.replace("&", "\\&")
    text = text.replace("%", "\\%")
    text = text.replace("$", "\\$")
    text = text.replace("#", "\\#")
    text = text.replace("_", "\\_")
    text = text.replace("{", "\\{")
    text = text.replace("}", "\\}")
    text = text.replace("~", "\\textasciitilde{}")
    text = text.replace("^", "\\textasciicircum{}")
    return text


def html_to_latex(html_text):
    """Convert HTML to LaTeX-safe text with emphasis preserved.

    Escapes special chars first, then adds LaTeX formatting commands.
    """
    # Extract emphasis/bold spans before stripping HTML
    em_spans = []
    strong_spans = []

    def save_em(m):
        idx = len(em_spans)
        em_spans.append(m.group(1))
        return f"@@EM{idx}@@"

    def save_strong(m):
        idx = len(strong_spans)
        strong_spans.append(m.group(1))
        return f"@@STRONG{idx}@@"

    text = re.sub(r"<em>(.*?)</em>", save_em, html_text)
    text = re.sub(r"<strong>(.*?)</strong>", save_strong, text)

    # Strip <p> tags
    text = re.sub(r"<p>", "", text)
    text = re.sub(r"</p>", "\n\n", text)
    # Strip remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Escape LaTeX special chars in the plain text
    text = escape_latex(text)

    # Restore emphasis/bold with LaTeX commands
    for i, em in enumerate(em_spans):
        text = text.replace(f"@@EM{i}@@", f"\\emph{{{escape_latex(em)}}}")
    for i, s in enumerate(strong_spans):
        text = text.replace(f"@@STRONG{i}@@", f"\\textbf{{{escape_latex(s)}}}")

    # Clean up whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_chat_messages(html_block):
    """Parse HTML chat transcript into list of (role, text) tuples and section headers."""
    elements = []

    # Find section headers: <div class="transcript-section-header">...</div> or <h4>...</h4>
    # and chat messages: <div class="chat-message claude/user">...<div class="chat-bubble">...</div>...</div>

    # Split by chat-message divs and section headers
    # Process line by line for robustness
    lines = html_block.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Section header (div variant)
        m = re.match(r'<div class="transcript-section-header">(.*?)</div>', line)
        if m:
            elements.append(("section", m.group(1).strip()))
            i += 1
            continue

        # Section header (h4 variant)
        m = re.match(r"<h4>(.*?)</h4>", line)
        if m:
            elements.append(("section", m.group(1).strip()))
            i += 1
            continue

        # Chat message start
        m = re.match(r'<div class="chat-message (claude|user)">', line)
        if m:
            role = m.group(1)
            # Collect all lines until closing </div> for the chat-message
            bubble_html = ""
            depth = 1
            i += 1
            in_bubble = False
            while i < len(lines) and depth > 0:
                cline = lines[i]
                if '<div class="chat-bubble">' in cline:
                    in_bubble = True
                    # Get content after the opening tag on same line
                    after = re.sub(r'.*<div class="chat-bubble">', "", cline)
                    # Check if bubble closes on same line
                    if "</div>" in after:
                        # Count divs
                        pass
                    bubble_html += after + "\n"
                    i += 1
                    continue
                if in_bubble:
                    bubble_html += cline + "\n"
                # Track depth for the outer chat-message div
                depth += cline.count("<div")
                depth -= cline.count("</div>")
                i += 1

            # Extract text from bubble
            # Remove the chat-bubble closing div and outer div
            bubble_html = re.sub(r"</div>\s*</div>\s*$", "", bubble_html.strip())
            bubble_html = re.sub(r"</div>\s*$", "", bubble_html.strip())
            text = html_to_latex(bubble_html)
            if text:
                elements.append((role, text))
            continue

        i += 1

    return elements


def parse_inline_chat_messages(text):
    """Parse inline chat messages (Journal 5 style) from article text.

    Returns list of (type, content) where type is 'text', 'claude', 'user', or 'chat-intro'.
    Uses line-by-line parsing for robustness with multi-line HTML blocks.
    """
    elements = []
    lines = text.split("\n")
    i = 0
    text_buffer = []

    def flush_text():
        t = "\n".join(text_buffer).strip()
        if t:
            elements.append(("text", t))
        text_buffer.clear()

    while i < len(lines):
        line = lines[i]

        # Chat-intro div
        m = re.match(r'\s*<div class="chat-intro">', line)
        if m:
            flush_text()
            intro_lines = []
            # Check if it closes on the same line
            if "</div>" in line[m.end():]:
                inner = re.sub(r'.*<div class="chat-intro">', "", line)
                inner = re.sub(r"</div>.*$", "", inner)
                elements.append(("chat-intro", inner.strip()))
                i += 1
                continue
            # Multi-line: collect until </div>
            intro_lines.append(line[m.end():])
            i += 1
            while i < len(lines) and "</div>" not in lines[i]:
                intro_lines.append(lines[i])
                i += 1
            if i < len(lines):
                intro_lines.append(re.sub(r"</div>.*$", "", lines[i]))
                i += 1
            inner = "\n".join(intro_lines).strip()
            inner = re.sub(r"<[^>]+>", "", inner).strip()
            elements.append(("chat-intro", inner))
            continue

        # Chat message div
        m = re.match(r'\s*<div class="chat-message (claude|user)">', line)
        if m:
            flush_text()
            role = m.group(1)
            bubble_html = ""
            depth = 1
            i += 1
            in_bubble = False
            while i < len(lines) and depth > 0:
                cline = lines[i]
                if '<div class="chat-bubble">' in cline:
                    in_bubble = True
                    after = re.sub(r'.*<div class="chat-bubble">', "", cline)
                    bubble_html += after + "\n"
                    i += 1
                    continue
                if in_bubble:
                    bubble_html += cline + "\n"
                depth += cline.count("<div")
                depth -= cline.count("</div>")
                i += 1
            # Clean bubble
            bubble_html = re.sub(r"</div>\s*</div>\s*$", "", bubble_html.strip())
            bubble_html = re.sub(r"</div>\s*$", "", bubble_html.strip())
            converted = html_to_latex(bubble_html)
            if converted:
                elements.append((role, converted))
            continue

        text_buffer.append(line)
        i += 1

    flush_text()
    return elements


def _flush_images(img_buffer, cleaned):
    """Output buffered images as grouped LaTeX figures (side-by-side when consecutive)."""
    if not img_buffer:
        return
    if len(img_buffer) == 1:
        path, alt = img_buffer[0]
        opt = optimize_image(path)
        caption = f"\\caption{{{escape_latex(alt)}}}\n" if alt else ""
        cleaned.append(
            f"```{{=latex}}\n\\begin{{figure}}[H]\n\\centering\n"
            f"\\includegraphics[width=0.6\\textwidth]{{{opt}}}\n"
            f"{caption}\\end{{figure}}\n```"
        )
    else:
        # Group into rows of up to 3
        rows = [img_buffer[i : i + 3] for i in range(0, len(img_buffer), 3)]
        row_strs = []
        for row in rows:
            n = len(row)
            w = "0.45" if n == 2 else "0.3"
            cells = []
            for path, alt in row:
                opt = optimize_image(path)
                cap = f"\\\\[2pt]{{\\small\\color{{darktext!70}} {escape_latex(alt)}}}" if alt else ""
                cells.append(
                    f"\\begin{{minipage}}{{{w}\\textwidth}}\n\\centering\n"
                    f"\\includegraphics[width=\\textwidth]{{{opt}}}"
                    f"{cap}\n\\end{{minipage}}"
                )
            row_strs.append("\\hfill\n".join(cells))
        body = "\n\n\\vspace{4pt}\n\n".join(row_strs)
        cleaned.append(
            f"```{{=latex}}\n\\begin{{figure}}[H]\n\\centering\n"
            f"{body}\n\\end{{figure}}\n```"
        )
    img_buffer.clear()


def clean_article_text(text, journal_nr):
    """Clean article markdown text for PDF appendix."""
    lines = text.split("\n")
    cleaned = []
    skip_first_heading = True
    img_buffer = []  # collect consecutive images for side-by-side layout

    for line in lines:
        # Collect images into buffer (flushed when non-image content appears)
        m_img = re.match(r"!\[(.*?)\]\((.*?)\)", line)
        if m_img:
            img_path = m_img.group(2)
            ext = os.path.splitext(img_path)[1].lower()
            if ext in (".mp3", ".mp4", ".wav"):
                continue  # skip audio/video files
            img_buffer.append((img_path, m_img.group(1)))
            continue

        # Blank lines don't break image groups
        if line.strip() == "" and img_buffer:
            continue

        # Any other content: flush buffered images first
        _flush_images(img_buffer, cleaned)

        # Remove WORLD_INFO blocks
        if "[WORLD_INFO:" in line:
            continue

        # Remove audio viewer divs
        if "<div data-audio-viewer" in line or "data-audio-viewer" in line:
            continue
        # Skip lines that are part of audio viewer JSON
        if re.match(r'\s+data-(prompt|artist|tracks)=', line):
            continue
        if line.strip().startswith('{"src":') or line.strip() == "]'>":
            continue
        if line.strip() == "</div>" and cleaned and any(
            "data-audio-viewer" in c for c in cleaned[-10:]
        ):
            continue

        # Remove **Keywords:** line
        if line.strip().startswith("**Keywords:**"):
            continue

        # Remove first heading (redundant with our own heading)
        if skip_first_heading and re.match(r"^# ", line):
            skip_first_heading = False
            continue

        # Remove date line (bold date after title)
        if re.match(r"^\*\*\d+\.\s+(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s+\d{4}\*\*", line):
            continue
        # Also handle date with parenthetical update note
        if re.match(r"^\*\*\d+\.\s+\w+\s+\d{4}\*\*\s*\*?\(", line):
            continue

        # Shift heading levels: ## -> ####
        if re.match(r"^###\s", line):
            line = "#####" + line[3:]
        elif re.match(r"^##\s", line):
            line = "####" + line[2:]

        cleaned.append(line)

    # Flush any remaining buffered images
    _flush_images(img_buffer, cleaned)

    result = "\n".join(cleaned)

    # Remove audio-viewer div blocks (multiline)
    result = re.sub(
        r'<div data-audio-viewer.*?</div>\s*', "", result, flags=re.DOTALL
    )

    # Remove empty </div> that might be left over
    result = re.sub(r"^\s*</div>\s*$", "", result, flags=re.MULTILINE)

    return result.strip()


def process_journal_5(text):
    """Special handling for Journal 5 which has inline chat messages in article."""
    # Split at the reflexion separator
    parts = re.split(r"\n---\n\s*## Reflexion", text, maxsplit=1)
    if len(parts) < 2:
        parts = re.split(r"\n---\n", text, maxsplit=1)

    article_raw = parts[0] if parts else text

    # Parse inline chat elements
    elements = parse_inline_chat_messages(article_raw)

    # Build output
    output_parts = []
    for etype, content in elements:
        if etype == "text":
            cleaned = clean_article_text(content, 5)
            if cleaned.strip():
                output_parts.append(cleaned)
        elif etype == "chat-intro":
            # Convert to italic markdown
            plain = re.sub(r"<[^>]+>", "", content).strip()
            output_parts.append(f"*{plain}*")
        elif etype in ("claude", "user"):
            env = "claudemsg" if etype == "claude" else "usermsg"
            # content is already LaTeX-escaped from html_to_latex
            text = content.replace("\n\n", "\\par\n")
            output_parts.append(
                f"```{{=latex}}\n\\begin{{{env}}}\n{text}\n\\end{{{env}}}\n```"
            )

    return "\n\n".join(output_parts)


def process_journal(journal_meta):
    """Process a single journal file and return (article_md, transcript_latex)."""
    filepath = os.path.join(JOURNAL_DIR, journal_meta["file"])

    if not os.path.exists(filepath):
        print(f"WARNING: {filepath} not found", file=sys.stderr)
        return "", ""

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Special case: Journal 5 has inline chat in article
    if journal_meta["nr"] == 5:
        article_md = process_journal_5(content)
        # Still extract the interview-transcript section
        transcript_match = re.search(
            r'<div class="interview-transcript">(.*?)</div>\s*$',
            content,
            re.DOTALL,
        )
        transcript_latex = ""
        if transcript_match:
            elements = parse_chat_messages(transcript_match.group(1))
            transcript_latex = build_transcript_latex(elements)
        return article_md, transcript_latex

    # Split at reflexion section
    # Find the --- before ## Reflexion
    reflexion_split = re.split(r"\n---\n\s*(?=## Reflexion)", content, maxsplit=1)
    article_raw = reflexion_split[0] if reflexion_split else content

    # Clean article text
    article_md = clean_article_text(article_raw, journal_meta["nr"])

    # Extract interview transcript
    transcript_match = re.search(
        r'<div class="interview-transcript">(.*?)</div>\s*$',
        content,
        re.DOTALL,
    )

    transcript_latex = ""
    if transcript_match:
        elements = parse_chat_messages(transcript_match.group(1))
        transcript_latex = build_transcript_latex(elements)

    return article_md, transcript_latex


def build_transcript_latex(elements):
    """Build LaTeX chat bubble code from parsed elements."""
    if not elements:
        return ""

    parts = []
    for etype, content in elements:
        if etype == "section":
            escaped_title = escape_latex(content)
            parts.append(f"\\chatsection{{{escaped_title}}}")
        elif etype in ("claude", "user"):
            env = "claudemsg" if etype == "claude" else "usermsg"
            # content is already LaTeX-escaped from html_to_latex
            text = content.replace("\n\n", "\\par\n")
            parts.append(f"\\begin{{{env}}}\n{text}\n\\end{{{env}}}")

    return "\n".join(parts)


def generate_anhang():
    """Generate the full appendix markdown."""
    out = []

    out.append("\\newpage\n")
    out.append("# Anhang\n")
    out.append("## Anhang A: Verzeichnis der Journal-Einträge\n")
    out.append(
        "Die folgende Tabelle gibt einen Überblick über die im Rahmen dieser Arbeit "
        "erstellten Journal-Einträge. Jeder Eintrag dokumentiert ein Experiment oder "
        "eine Arbeitsphase und wurde im Anschluss einer strukturierten KI-gestützten "
        "Reflexion unterzogen (siehe Anhang B).\n"
    )

    # Generate table
    out.append("| Nr. | Datum | Titel | Tools | Modalität |")
    out.append("|-----|-------|-------|-------|-----------|")
    for j in JOURNALS:
        out.append(
            f"| {j['nr']} | {j['datum']} | {j['titel']} | {j['tools']} | {j['modalitaet']} |"
        )
    out.append("")
    out.append(
        "Die vollständigen Journal-Einträge mit Abbildungen sind auf der Projektwebsite "
        "einsehbar: https://jnfrmeier.github.io/everything-machine/"
    )

    out.append("\n\\newpage\n")
    out.append("## Anhang B: Journal-Einträge und Reflexionsinterviews\n")
    out.append(
        "Die folgenden Texte und Transkripte dokumentieren die Journal-Einträge und die "
        "strukturierten Reflexionen, die nach jedem Eintrag im Dialog mit Claude (Anthropic) "
        "entstanden sind. Eingebettete Audio- und Videomedien wurden für die Druckversion entfernt; "
        "die vollständigen Einträge finden sich auf der Projektwebsite.\n"
    )

    for j in JOURNALS:
        print(f"Processing Journal {j['nr']}: {j['titel']}...", file=sys.stderr)
        article_md, transcript_latex = process_journal(j)

        out.append(f"### Journal-Eintrag {j['nr']}: {j['titel']} ({j['datum']})\n")

        if article_md:
            out.append(article_md)
            out.append("")

        if transcript_latex:
            out.append("#### Reflexionsinterview\n")
            out.append("```{=latex}")
            out.append(transcript_latex)
            out.append("```")
            out.append("")

        out.append("\\newpage\n")

    # Eidesstattliche Erklärung
    out.append("# Eidesstattliche Erklärung\n")
    out.append(
        "Ich versichere hiermit, dass ich die vorliegende Arbeit selbstständig verfasst "
        "und keine anderen als die angegebenen Quellen und Hilfsmittel benutzt habe. "
        "Alle Stellen der Arbeit, die wörtlich oder sinngemäß aus Veröffentlichungen "
        "oder aus anderweitigen fremden Äußerungen entnommen wurden, sind als solche "
        "einzeln kenntlich gemacht.\n"
    )
    out.append(
        "Der Einsatz generativer KI-Systeme (Claude, Cursor) bei der Erstellung dieser "
        "Arbeit ist im Abschnitt \"Einsatz von KI in dieser Arbeit\" vollständig offengelegt.\n"
    )
    out.append("\\vspace{2cm}\n")
    out.append("Detmold, Februar 2026\n")
    out.append("\\vspace{2cm}\n")
    out.append("\\noindent\\rule{6cm}{0.4pt}\n")
    out.append("Jennifer Meier")

    return "\n".join(out)


if __name__ == "__main__":
    print(generate_anhang())
