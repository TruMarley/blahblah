(function() {
  'use strict';

  // Read config from the script tag
  var scripts = document.getElementsByTagName('script');
  var thisScript = scripts[scripts.length - 1];
  var shopId = thisScript.getAttribute('data-shop') || 'demo';
  var color = thisScript.getAttribute('data-color') || '#7c3aed';
  var position = thisScript.getAttribute('data-position') || 'bottom-left';
  var label = thisScript.getAttribute('data-label') || 'Book Now';

  // Avoid double-init
  if (document.getElementById('rd-widget-btn')) return;

  // Inject styles
  var style = document.createElement('style');
  style.textContent = [
    '#rd-widget-btn {',
    '  position: fixed;',
    '  ' + (position.includes('left') ? 'left: 24px;' : 'right: 24px;'),
    '  ' + (position.includes('top') ? 'top: 24px;' : 'bottom: 24px;'),
    '  z-index: 99999;',
    '  background: ' + color + ';',
    '  color: #fff;',
    '  border: none;',
    '  border-radius: 50px;',
    '  padding: 14px 22px;',
    '  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;',
    '  font-size: 15px;',
    '  font-weight: 700;',
    '  cursor: pointer;',
    '  box-shadow: 0 4px 20px rgba(0,0,0,0.3);',
    '  display: flex;',
    '  align-items: center;',
    '  gap: 8px;',
    '  transition: transform 0.2s, box-shadow 0.2s;',
    '  text-decoration: none;',
    '}',
    '#rd-widget-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.35); }',
    '#rd-widget-panel {',
    '  position: fixed;',
    '  ' + (position.includes('left') ? 'left: 24px;' : 'right: 24px;'),
    '  ' + (position.includes('top') ? 'top: 90px;' : 'bottom: 90px;'),
    '  z-index: 99998;',
    '  width: 300px;',
    '  background: #111;',
    '  border: 1px solid #2a2a2a;',
    '  border-radius: 16px;',
    '  overflow: hidden;',
    '  display: none;',
    '  box-shadow: 0 8px 40px rgba(0,0,0,0.5);',
    '  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;',
    '}',
    '#rd-widget-panel.rd-open { display: block; }',
    '.rd-panel-header { background: ' + color + '; padding: 1rem 1.25rem; color: #fff; }',
    '.rd-panel-title { font-weight: 800; font-size: 15px; }',
    '.rd-panel-sub { font-size: 12px; opacity: 0.8; margin-top: 2px; }',
    '.rd-panel-body { padding: 1.25rem; }',
    '.rd-field { margin-bottom: 0.75rem; }',
    '.rd-field label { display: block; font-size: 11px; font-weight: 600; color: #888; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }',
    '.rd-field input, .rd-field select { width: 100%; background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 8px; padding: 9px 11px; color: #e8e8e8; font-size: 14px; font-family: inherit; outline: none; box-sizing: border-box; }',
    '.rd-submit { width: 100%; background: ' + color + '; color: #fff; border: none; border-radius: 8px; padding: 11px; font-size: 14px; font-weight: 700; cursor: pointer; font-family: inherit; }',
    '.rd-submit:hover { opacity: 0.9; }',
    '.rd-success { text-align: center; padding: 1.5rem; color: #22c55e; font-size: 14px; font-weight: 600; display: none; }',
  ].join('\n');
  document.head.appendChild(style);

  // Build the button
  var btn = document.createElement('button');
  btn.id = 'rd-widget-btn';
  btn.innerHTML = '✂️ ' + label;
  document.body.appendChild(btn);

  // Build the panel
  var panel = document.createElement('div');
  panel.id = 'rd-widget-panel';
  panel.innerHTML = [
    '<div class="rd-panel-header">',
    '  <div class="rd-panel-title">Book an Appointment</div>',
    '  <div class="rd-panel-sub">Powered by RingDesk AI</div>',
    '</div>',
    '<div class="rd-panel-body">',
    '  <form id="rd-book-form">',
    '    <div class="rd-field"><label>Your Name</label><input type="text" id="rd-name" placeholder="Marcus Johnson" required></div>',
    '    <div class="rd-field"><label>Phone Number</label><input type="tel" id="rd-phone" placeholder="(786) 555-0100" required></div>',
    '    <div class="rd-field"><label>Service</label><select id="rd-service"><option>Haircut ($30)</option><option>Fade ($35)</option><option>Beard Trim ($20)</option><option>Full Cut + Beard ($50)</option></select></div>',
    '    <div class="rd-field"><label>Preferred Day</label><select id="rd-day"><option>Today</option><option>Tomorrow</option><option>This Week</option><option>Flexible</option></select></div>',
    '    <button type="submit" class="rd-submit">Request Booking →</button>',
    '  </form>',
    '  <div class="rd-success" id="rd-success">✓ Request sent! We\'ll text you to confirm your appointment.</div>',
    '</div>',
  ].join('\n');
  document.body.appendChild(panel);

  // Toggle
  btn.addEventListener('click', function() {
    panel.classList.toggle('rd-open');
  });

  // Form submit
  document.getElementById('rd-book-form').addEventListener('submit', function(e) {
    e.preventDefault();
    this.style.display = 'none';
    document.getElementById('rd-success').style.display = 'block';
  });

  // Close panel when clicking outside
  document.addEventListener('click', function(e) {
    if (!btn.contains(e.target) && !panel.contains(e.target)) {
      panel.classList.remove('rd-open');
    }
  });
})();
