import { esc } from './lib.mjs';

export const SIGNATURE_CSS = `
.signoff { margin-top: 30pt; font-size: 13pt; break-inside: avoid; }
.signature-heading { width: 84mm; margin-left: auto; text-align: center; font-style: italic; }
.signature-grid { display: flex; justify-content: space-around; flex-wrap: nowrap; margin-top: 3mm; }
.signature-column { flex: 0 0 auto; text-align: center; }
.signature-space { height: 30mm; }
.signature-name { display: block; white-space: nowrap; }
.signoff[data-count="1"] .signature-grid { width: 84mm; margin-left: auto; }
.signoff[data-count="5"] .signature-name { font-size: 11pt; }
`;

export function signatureBlock(names, date) {
  if (names.length < 1 || names.length > 5) throw new RangeError('Signature layout supports 1–5 authors');
  return `<div class="signoff" data-count="${names.length}">
    <div class="signature-heading">
      <div>Ho Chi Minh City, ${esc(date)}</div>
      <div>${names.length === 1 ? 'Author' : 'Authors'}</div>
      <div>(Signature and full name)</div>
    </div>
    <div class="signature-grid">${names.map(name => `<div class="signature-column">
      <div class="signature-space"></div><span class="signature-name">${esc(name)}</span>
    </div>`).join('')}</div>
  </div>`;
}
