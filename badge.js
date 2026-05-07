/**
 * RingDesk "Powered by" badge — embeddable on any website.
 * Usage: <script src="https://your-domain.com/badge.js" data-position="bottom-right"></script>
 */
(function () {
  var script = document.currentScript || (function () {
    var scripts = document.getElementsByTagName('script');
    return scripts[scripts.length - 1];
  })();

  var position = (script.getAttribute('data-position') || 'bottom-right').toLowerCase();

  var CSS = [
    '.rd-badge-wrap{position:fixed;z-index:9998;',
    position === 'bottom-left'
      ? 'bottom:18px;left:18px;'
      : 'bottom:18px;right:18px;',
    '}',
    '.rd-badge{display:inline-flex;align-items:center;gap:6px;',
    'background:#111;border:1px solid #222;border-radius:99px;',
    'padding:5px 11px 5px 7px;text-decoration:none;',
    'box-shadow:0 2px 12px rgba(0,0,0,.5);',
    'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;',
    'transition:opacity .15s,transform .15s;cursor:pointer;}',
    '.rd-badge:hover{opacity:.85;transform:translateY(-1px);}',
    '.rd-logo-mark{width:20px;height:20px;border-radius:50%;',
    'background:linear-gradient(135deg,#a78bfa,#7c3aed);',
    'display:flex;align-items:center;justify-content:center;flex-shrink:0;}',
    '.rd-logo-mark svg{width:11px;height:11px;}',
    '.rd-text-wrap{display:flex;flex-direction:column;line-height:1.2;}',
    '.rd-powered{font-size:8px;color:#555;font-weight:600;letter-spacing:.04em;text-transform:uppercase;}',
    '.rd-brand{font-size:11px;color:#e8e8e8;font-weight:800;letter-spacing:-.01em;}',
    '.rd-brand em{font-style:normal;color:#a78bfa;}',
  ].join('');

  var style = document.createElement('style');
  style.textContent = CSS;
  document.head.appendChild(style);

  var wrap = document.createElement('div');
  wrap.className = 'rd-badge-wrap';

  var link = document.createElement('a');
  link.className = 'rd-badge';
  link.href = 'https://ringdesk.ai';
  link.target = '_blank';
  link.rel = 'noopener';
  link.setAttribute('title', 'AI receptionist powered by RingDesk');
  link.innerHTML = [
    '<div class="rd-logo-mark">',
    '<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round">',
    '<path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9a19.79 19.79 0 01-3.07-8.67A2 2 0 012 .18h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/>',
    '</svg>',
    '</div>',
    '<div class="rd-text-wrap">',
    '<span class="rd-powered">Powered by</span>',
    '<span class="rd-brand">Ring<em>Desk</em></span>',
    '</div>',
  ].join('');

  wrap.appendChild(link);
  document.body.appendChild(wrap);
})();
