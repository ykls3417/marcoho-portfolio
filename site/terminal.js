const commands = ['help', 'whoami', 'about', 'projects', 'skills', 'interests', 'now', 'contact', 'open', 'theme', 'clear'];

// A small portfolio command set. Never evaluates input or runs shell commands.
function resolveCommand(input, content) {
  const [command = '', ...args] = input.trim().toLowerCase().split(/\s+/);
  const argument = args.join(' ');
  if (!command) return { text: '' };
  switch (command) {
    case 'help': return { text: 'whoami / about / projects / skills / interests / now / contact\nopen work | about | experience | contact — jump to a section\ntheme dark | light — change appearance\nclear — clear output\n↑ ↓ recall commands; Tab completes a command.' };
    case 'whoami': return { text: `${content.name} (${content.handle})\n${content.role} · ${content.location}\n${content.intro}` };
    case 'about': return { text: `${content.about}\n\n${content.education}` };
    case 'projects': return { text: content.projects.filter(p => p.name).map(p => `${p.name} — ${p.category}\n${p.description}${p.note ? '\n' + p.note : ''}`).join('\n\n') || 'No projects listed yet.' };
    case 'skills': return { text: content.skills.join(' · ') || 'No skills listed yet.' };
    case 'interests': return { text: content.interests || 'Nothing added yet.' };
    case 'now': return { text: content.now || 'No update added yet.' };
    case 'contact': return { text: [content.email, content.github, content.linkedin].filter(Boolean).join('\n') || 'Contact links are not published yet.' };
    case 'open': {
      const targets = ['work', 'about', 'experience'];
      if ([content.email, content.github, content.linkedin, content.resume_url].some(Boolean)) targets.push('contact');
      return targets.includes(argument) ? { text: `Opening ${argument}.`, target: argument } : { text: `Usage: open ${targets.join(' | ')}` };
    }
    case 'theme': return ['dark', 'light'].includes(argument) ? { text: `Theme: ${argument}`, theme: argument } : { text: 'Usage: theme dark | light' };
    case 'clear': return { clear: true };
    default: return { text: `Unknown command: ${command}. Type help for available commands.` };
  }
}

if (typeof module !== 'undefined') module.exports = { resolveCommand };
if (typeof document !== 'undefined') {
  const content = JSON.parse(document.querySelector('#terminal-data').textContent);
  const form = document.querySelector('#terminal-form');
  const input = document.querySelector('#terminal-input');
  const log = document.querySelector('#terminal-log');
  const shortcuts = document.querySelector('#terminal-shortcuts');
  const history = [];
  let position = 0;
  let draft = '';
  function run(value) {
    const command = value.trim();
    if (!command) return;
    const result = resolveCommand(command, content);
    history.push(command);
    if (history.length > 100) history.shift();
    position = history.length;
    draft = '';
    input.value = '';
    if (result.clear) log.replaceChildren();
    else {
      const entry = document.createElement('div');
      const prompt = document.createElement('p');
      prompt.className = 'command-echo';
      prompt.textContent = `${content.handle}@portfolio ~ $ ${command}`;
      const output = document.createElement('p');
      output.className = 'command-result';
      output.textContent = result.text;
      entry.append(prompt, output);
      log.append(entry);
      if (log.children.length > 40) log.firstElementChild.remove();
    }
    if (result.theme) {
      setTheme(result.theme === 'light');
      try { localStorage.setItem('portfolio-theme', result.theme); } catch { /* Optional preference. */ }
    }
    log.scrollTop = log.scrollHeight;
    if (result.target) {
      const section = document.getElementById(result.target);
      location.hash = result.target;
      section.tabIndex = -1;
      section.focus({ preventScroll: true });
    } else input.focus({ preventScroll: true });
  }
  form.hidden = shortcuts.hidden = document.querySelector('#terminal-hint').hidden = false;
  form.addEventListener('submit', event => { event.preventDefault(); run(input.value); });
  shortcuts.addEventListener('click', event => {
    const button = event.target.closest('button[data-command]');
    if (button) run(button.dataset.command);
  });
  input.addEventListener('keydown', event => {
    if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
      event.preventDefault();
      if (position === history.length) draft = input.value;
      position = Math.max(0, Math.min(history.length, position + (event.key === 'ArrowUp' ? -1 : 1)));
      input.value = history[position] ?? draft;
    } else if (event.key === 'Tab' && !event.shiftKey && input.value.trim()) {
      const matches = commands.filter(c => c.startsWith(input.value.trim().toLowerCase()));
      if (matches.length === 1 && matches[0] !== input.value.trim()) {
        event.preventDefault();
        input.value = matches[0];
      }
    }
  });
}
