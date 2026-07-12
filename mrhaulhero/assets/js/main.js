/* ============================================================
   Mr Haul Hero — Site JS
   - Mobile menu toggle
   - Service Area dropdown -> accordion on mobile
   - FAQ accordion
   - Footer year
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  /* ---- Mobile menu toggle ---- */
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      links.classList.toggle('open');
      var open = links.classList.contains('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  /* ---- Service Area: hover on desktop, tap-accordion on mobile ---- */
  var navItem = document.querySelector('.nav-item');
  if (navItem) {
    var trigger = navItem.querySelector('a');
    trigger.addEventListener('click', function (e) {
      // Only intercept as accordion when in mobile layout
      if (window.matchMedia('(max-width: 900px)').matches) {
        e.preventDefault();
        navItem.classList.toggle('expanded');
        var expanded = navItem.classList.contains('expanded');
        trigger.setAttribute('aria-expanded', expanded ? 'true' : 'false');
      }
    });
  }

  /* ---- FAQ accordion ---- */
  var faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(function (item) {
    var q = item.querySelector('.faq-q');
    if (!q) return;
    q.setAttribute('role', 'button');
    q.setAttribute('tabindex', '0');
    function toggleItem() {
      item.classList.toggle('open');
      var open = item.classList.contains('open');
      q.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    q.addEventListener('click', toggleItem);
    q.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleItem(); }
    });
  });

  /* ---- File input label feedback ---- */
  var fileInput = document.getElementById('junk-photo');
  var fileLabel = document.querySelector('.field-file-text');
  if (fileInput && fileLabel) {
    fileInput.addEventListener('change', function () {
      if (fileInput.files && fileInput.files.length) {
        fileLabel.textContent = fileInput.files.length === 1
          ? fileInput.files[0].name
          : fileInput.files.length + ' photos selected';
      } else {
        fileLabel.textContent = 'Tap to upload a photo';
      }
    });
  }

  /* ---- Footer year ---- */
  var yr = document.getElementById('year');
  if (yr) { yr.textContent = new Date().getFullYear(); }

});
