// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Auto-resize textareas
document.querySelectorAll('textarea').forEach(ta => {
  ta.addEventListener('input', () => {
    ta.style.height = 'auto';
    ta.style.height = Math.max(120, ta.scrollHeight) + 'px';
  });
});
