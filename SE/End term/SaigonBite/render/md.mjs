// A deliberately small Markdown subset -> HTML converter.
// Handles exactly what the project documents use: headings, paragraphs, ordered and
// unordered lists, pipe tables, block quotes, fenced code, inline emphasis and images.
// Images whose target ends in .svg are inlined so Chromium vectorises them.

const inline = (s) => s
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/`([^`]+)`/g, '<code>$1</code>')
  .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  .replace(/(^|[^*])\*([^*]+)\*/g, '$1<em>$2</em>')
  .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

const cells = (line) => line.replace(/^\||\|$/g, '').split('|').map((c) => c.trim());

/** Read an SVG file and strip the XML prologue so it can sit inline in HTML. */
export function inlineSvg(svgText) {
  return svgText
    .replace(/<\?xml[^>]*\?>/g, '')
    .replace(/<!DOCTYPE[^>]*>/gi, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .trim();
}

/**
 * Convert Markdown to an HTML fragment.
 * `images` maps a relative src to inline SVG markup.
 * Returns { html, headings, figures } so a table of contents and a list of figures
 * can be derived from the same pass that produced the body.
 */
export function markdownToHtml(md, { images = {}, figureIndex = [] } = {}) {
  const lines = md.replace(/\r\n/g, '\n').split('\n');
  const out = [];
  const headings = [];
  const figures = [];
  let i = 0;
  let chapterCount = 0;

  const flushParagraph = (buf) => {
    if (!buf.length) return;
    out.push(`<p>${inline(buf.join(' '))}</p>`);
    buf.length = 0;
  };
  const para = [];

  while (i < lines.length) {
    const line = lines[i];

    // fenced code
    if (/^```/.test(line)) {
      flushParagraph(para);
      const body = [];
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) body.push(lines[i++]);
      i++;
      out.push(`<pre><code>${body.join('\n').replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')}</code></pre>`);
      continue;
    }

    // headings
    const h = line.match(/^(#{1,4})\s+(.*)$/);
    if (h) {
      flushParagraph(para);
      const level = h[1].length;
      const text = h[2].trim();
      if (level === 1) {
        chapterCount++;
        out.push(`<h1 class="chapter">${inline(text)}</h1>`);
        headings.push({ level: 1, label: text });
      } else if (level === 2) {
        out.push(`<h2>${inline(text)}</h2>`);
        headings.push({ level: 2, label: text });
      } else {
        out.push(`<h3>${inline(text)}</h3>`);
        headings.push({ level: 3, label: text });
      }
      i++;
      continue;
    }

    // image on its own line -> figure or plain image
    const img = line.match(/^!\[([^\]]*)\]\(([^)]+)\)\s*$/);
    if (img) {
      flushParagraph(para);
      const [, alt, src] = img;
      const key = src.split('/').pop();
      const svg = images[key];
      if (svg) {
        out.push(`<div class="figure">${inlineSvg(svg)}</div>`);
      } else {
        out.push(`<div class="figure"><img src="${src}" alt="${inline(alt)}" style="max-width:100%"/></div>`);
      }
      const cap = alt.trim();
      if (/^Figure\s/i.test(cap)) {
        out.push(`<p class="caption">${inline(cap)}</p>`);
        const id = (cap.match(/^Figure\s+([\d.]+)/) || [, ''])[1];
        figures.push({ id, caption: cap });
      } else if (cap) {
        out.push(`<p class="caption">${inline(cap)}</p>`);
      }
      i++;
      continue;
    }

    // table
    if (/^\|/.test(line) && i + 1 < lines.length && /^\|[\s:|-]+\|?\s*$/.test(lines[i + 1])) {
      flushParagraph(para);
      const head = cells(line);
      i += 2;
      const rows = [];
      while (i < lines.length && /^\|/.test(lines[i])) rows.push(cells(lines[i++]));
      out.push('<table><thead><tr>'
        + head.map((c) => `<th>${inline(c)}</th>`).join('')
        + '</tr></thead><tbody>'
        + rows.map((r) => `<tr>${r.map((c) => `<td>${inline(c)}</td>`).join('')}</tr>`).join('')
        + '</tbody></table>');
      continue;
    }

    // block quote
    if (/^>\s?/.test(line)) {
      flushParagraph(para);
      const body = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) body.push(lines[i++].replace(/^>\s?/, ''));
      out.push(`<blockquote><p>${inline(body.join(' '))}</p></blockquote>`);
      continue;
    }

    // lists
    if (/^[-*+]\s+/.test(line) || /^\d+\.\s+/.test(line)) {
      flushParagraph(para);
      const ordered = /^\d+\.\s+/.test(line);
      const items = [];
      const re = ordered ? /^\d+\.\s+/ : /^[-*+]\s+/;
      while (i < lines.length && re.test(lines[i])) {
        let item = lines[i++].replace(re, '');
        // continuation lines that are indented
        while (i < lines.length && /^\s{2,}\S/.test(lines[i])) item += ' ' + lines[i++].trim();
        items.push(item);
      }
      const tag = ordered ? 'ol' : 'ul';
      out.push(`<${tag}>${items.map((t) => `<li>${inline(t)}</li>`).join('')}</${tag}>`);
      continue;
    }

    if (!line.trim()) { flushParagraph(para); i++; continue; }

    para.push(line.trim());
    i++;
  }
  flushParagraph(para);

  return { html: out.join('\n'), headings, figures };
}
