// Preference stays on this browser; all portfolio content works without JavaScript.
const toggle = document.querySelector('#theme');
const root = document.documentElement;
function setTheme(light) {
  root.dataset.theme = light ? 'light' : 'dark';
  toggle.setAttribute('aria-pressed', String(light));
  toggle.textContent = light ? 'Dark mode' : 'Light mode';
}
try { setTheme(localStorage.getItem('portfolio-theme') === 'light'); } catch { setTheme(false); }
toggle.hidden = false;
toggle.addEventListener('click', () => {
  const light = root.dataset.theme !== 'light';
  setTheme(light);
  try { localStorage.setItem('portfolio-theme', light ? 'light' : 'dark'); } catch { /* Storage is optional. */ }
});
