# Marco portfolio

A restrained terminal-inspired static portfolio. No npm, frontend framework, external fonts, analytics, or runtime services. GitHub Pages builds it with Python's standard library.

## Edit words and placeholders

Edit **content.json**. Most portfolio copy is here; fixed navigation/section labels and terminal captions live in **build.py**.

- `headline`: use `\n` for a new line.
- `intro`, `about`, `personal_note`: your own sentences; personal note starts blank.
- `projects`: replace entries, add objects, or remove them. The current public projects have repository URLs; the extra placeholder is blank.
- The last project starts blank and is hidden. Set `show_empty_project` to `true` to display a quiet “Next experiment” slot.
- `github` links to your account. `email`, `linkedin`, and `resume_url` remain blank. Contact section appears once at least one is filled. No dead links.
- `resume_url`: put a public-safe PDF in `site/`, then use `resume.pdf`. Original CV was not copied.
- `experience`, `education`, `skills`: starter facts based on your CV. Review dates before publishing.
- Quotes inside JSON text must be escaped as `\"`. Keep commas between fields.

To start entirely blank, empty the text fields and use `[]` for `projects`, `experience`, and `skills`; the layout remains available in the template.

## Edit appearance

Open **site/theme.css**. First `:root` block controls dark colors, fonts, maximum page width, spacing, and corners. The next block controls light colors. Layout rules follow in the same file. Change section order or labels in **build.py**.

## Preview

Run from this folder:

```sh
python3 build.py
python3 -m http.server 4173 --directory site
```

Open http://localhost:4173. Run the build again after changing content, then refresh. CSS edits only need refresh. `site/index.html` is generated; edit the source instead.

Check before publishing:

```sh
python3 check.py
```

## GitHub and deployment

Repository: https://github.com/ykls3417/marcoho-portfolio

GitHub Pages is configured to deploy through `.github/workflows/pages.yml`. Pushes to `main` run checks, build the HTML, and publish `site/`. The Actions run reports the deployment URL and result.

Edit `content.json` or `site/theme.css` with GitHub's web editor and commit to `main` to update the site. For local edits, run the checks and build, commit, then `git push`. Command-line pushes require your own GitHub authentication; the initial files were uploaded through the signed-in web session.

Only `site/` is uploaded as the website artifact. Relative asset URLs support repository subpaths. To host elsewhere, upload the contents of `site/` after building.

## Design and content references

- [Terminal CSS](https://terminalcss.xyz/): monospace details, thin rules, simple terminal framing; inspiration only, no dependency or copied code.
- [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages): official publishing flow.
- Local employment CV: professional background, education, roles, and final-year project.
- Local Charamelt README: editable video creation workflow.

Design choice: graphite background, soft green accent, generous space, normal navigation, optional terminal commands alongside normal navigation, no glitching or flashing. UI/UX skill results were broader than this brief; terminal styling follows the reference and the requested restrained direction, with the skill's contrast, focus, responsive, and reduced-motion guidance.

## Interactive terminal

The header and prompt use `handle` (`marcoho`). Edit `interests`, `now`, and `terminal_welcome` in content.json to change the personal copy and terminal greeting. Command responses read the same content as the page.

Commands: `help`, `whoami`, `about`, `projects`, `skills`, `interests`, `now`, `contact`, `open work|about|experience|contact`, `theme dark|light`, `clear`. Contact navigation appears only when a contact link is set. Up/down recalls session history; Tab completes a unique command prefix and otherwise moves focus normally. This is a portfolio command interface, not a server shell.

Run `node check-terminal.cjs` for the command regression check. Browser history is session-only; only theme preference persists.
