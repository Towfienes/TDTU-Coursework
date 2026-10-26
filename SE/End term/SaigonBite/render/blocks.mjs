// Block renderer shared by the Part 1 builder and the consolidated report.
// Kept separate so the consolidated report can reuse Part 1's structured content
// without importing a script that has top-level side effects.

export function renderBlocks(blocks) {
  return blocks.map((b) => {
    switch (b.t) {
      case 'raw': return b.html;
      case 'requirement': return `<div class="requirement"><p class="noindent"><b>${b.id}</b> ${b.statement}</p><p class="noindent">Source: ${b.source}; UC ${b.use_case}; owner ${b.owner}.</p></div>`;
      case 'p': return `<p class="${b.style || ''}">${b.text}</p>`;
      case 'ref': return `<p class="ref">${b.text}</p>`;
      case 'h3': return `<h3>${b.text}</h3>`;
      case 'ul': return `<ul>${b.items.map((i) => `<li>${i}</li>`).join('')}</ul>`;
      case 'ol': return `<ol>${b.items.map((i) => `<li>${i}</li>`).join('')}</ol>`;
      case 'eq': return `<p class="eq">${b.text}</p>`;
      case 'figure':
        return `<div class="figure">${b.svg}</div><p class="caption">${b.caption}</p>`;
      case 'table': {
        const w = b.widths || b.head.map(() => `${Math.floor(100 / b.head.length)}%`);
        const cols = `<colgroup>${w.map((x) => `<col style="width:${x}"/>`).join('')}</colgroup>`;
        const head = `<tr>${b.head.map((h) => `<th>${h}</th>`).join('')}</tr>`;
        const rows = b.rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join('')}</tr>`).join('');
        return `<table>${cols}<thead>${head}</thead><tbody>${rows}</tbody></table>`;
      }
      default: throw new Error(`unknown block ${b.t}`);
    }
  }).join('\n');
}

/** Headings a Part 1 section contributes to a table of contents. */
export function sectionHeadings(s) {
  const out = [];
  if (s.kind === 'chapter') {
    out.push({ level: 1, label: `CHAPTER ${s.number}. ${s.title}`, key: `CHAPTER ${s.number}. ${s.title}` });
  } else if (s.kind === 'appendix' || s.kind === 'references') {
    out.push({ level: 1, label: s.title, key: s.title });
  }
  for (const b of s.blocks) {
    if (b.t === 'h3') out.push({ level: 2, label: b.text, key: b.text });
    if (b.t === 'figure') out.push({ figure: true, caption: b.caption, key: b.caption });
  }
  return out;
}

/** The heading element a Part 1 section starts with. */
export function sectionHeadingHtml(s) {
  if (s.kind === 'chapter') return `<h1 class="chapter">CHAPTER ${s.number}. ${s.title}</h1>`;
  return `<h1 class="chapter">${s.title}</h1>`;
}
