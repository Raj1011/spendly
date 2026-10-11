---
name: spendly-ui-designer
description: Designs and builds production-ready UI pages and components for Spendly, Raj's Flask expense tracker (github.com/Raj1011/spendly), matching its existing design system. Use whenever the user asks to design, create, build, redesign or improve any page, screen, component, form, card, list, modal or layout for Spendly, e.g. "design the dashboard page", "create UI for add expense", "build a component for category breakdown", "improve the profile page", even if Spendly isn't named but the work is clearly in that repo or about the expense tracker.
---

# Spendly UI Designer

Spendly is a Flask + Jinja2 personal expense tracker. Your job is to produce UI that looks like it was always part of the app: calm, card-based, fintech-clean, and built the way the repo already builds things. A beautiful page that ignores the stack (React, Tailwind, a CDN icon script) is a failure here, because the owner would have to throw it away.

## The stack you're designing for

These come from the repo's `CLAUDE.md` and are hard constraints, not preferences:

- **Templates**: Jinja2, every page `{% extends "base.html" %}` and fills `{% block content %}`. Never repeat `<html>/<head>/<nav>/<footer>`.
- **CSS**: one global file, `static/css/style.css`. No per-page CSS files, no Tailwind, no CSS frameworks. Use the `:root` tokens; never hardcode hex values in component rules.
- **JS**: one global file, `static/js/main.js`, vanilla only, no libraries, no build step. Write JS only when the UI genuinely needs it.
- **Links**: always `{{ url_for('endpoint') }}`, never a hardcoded path.
- **Backend**: routes in `app.py` stay thin; SQL lives only in `database/db.py`. No new pip packages.

## Workflow

### 1. Ground yourself in the current repo

The project changes week to week, so read before designing:

- `CLAUDE.md` for current conventions and which routes are real vs stubs.
- `static/css/style.css`: the `:root` block in full, plus any section related to what you're building. Note which recipe classes already exist (a previous run may have added `.card`, `.icon-chip`, space tokens, etc.). Reuse them instead of duplicating.
- `templates/base.html` and the existing template closest to the request.
- The relevant route in `app.py` and helpers in `database/db.py`, to know what data the template can actually receive (expenses have `id, amount, category, date, description`).
- `.claude/specs/` for a spec of this feature, if one exists. If a spec defines the page, follow it.

Then read `references/design-system.md` for tokens, component recipes and category styling.

If you can't reach the repo, say so and ask for the relevant files (or work from `references/design-system.md` and flag that the code must be checked against the live stylesheet).

### 2. Check you have enough visual reference

The canonical references for app-style UI are the landing page hero mock-card (stat tiles + category bars) and the auth/legal cards. Most requests can be designed confidently from those.

Ask for screenshots of the current design before writing code when:
- the user refers to a look you can't see ("like the one I showed", "match my Figma", "the way it looks on my phone"),
- the user wants to change the overall visual direction rather than add a screen,
- what you read in the repo contradicts what they describe (they may have uncommitted work).

Keep the question short and say what you'd do by default if they'd rather not share.

### 3. Design, then build

Plan the screen around the user's main task on it (on a dashboard: "how am I doing this month?"; on add-expense: "log this in 10 seconds"). Decide the hierarchy first: what's the one number or action that should dominate, what's secondary, what can hide behind a click.

Design rules:
- Card-based layout on the `--paper` background, white cards with 1px `--border`, `--radius-md`, soft `--shadow-sm` (`--shadow-md` only for raised/hover elements).
- 8px spacing grid via the `--space-*` tokens (4px only for tight inline gaps like icon-to-label).
- Restraint with colour: ink + green accent for UI, category colours only for category signals, `--danger` only for errors, overspend and destructive actions. Spending increases read as negative (danger), savings/under-budget as positive (hero-accent).
- Amounts in rupees (`₹`), tabular figures, right-aligned in lists.
- Every data view gets its empty state; every form gets its error state; destructive actions get a confirmation and use POST.
- Mobile-first thinking: check both the 900px and 600px breakpoints already used in the stylesheet. Touch targets ≥ 40px. No horizontal scroll at 375px.
- Accessibility: semantic elements (`header`, `section`, `table` for genuinely tabular data, `button` vs `a` correctly), labels on every input, `aria-label` on icon-only buttons, visible `:focus-visible` styles, and contrast of at least 4.5:1 for text.

Icons:
- Use Lucide as **inline SVG through a Jinja macro**, never a CDN `<script>` (that would be a JS library, which the repo forbids).
- The macro file is `assets/_icons.html` in this skill. If `templates/_icons.html` doesn't exist in the repo yet, copy it there. Use it with `{% from "_icons.html" import icon, category_icon %}` then `{{ icon("plus", size=16) }}` or `{{ category_icon(expense.category) }}`.
- Icons should mean something: an action, a category, a status. Don't scatter decorative icons on every heading.
- Need an icon that isn't in the macro? Add its exact markup from the `lucide-static` package (`node_modules/lucide-static/icons/<name>.svg`) or lucide.dev. Never write SVG path data from memory; guessed paths render as broken shapes. Heroicons is fine if the user asks for it, same inline approach.

### 4. Write the code

Where to put things:
- **Template**: new file in `templates/` (or the existing one being redesigned). Use Jinja loops/conditionals over the real context variables, including the empty case.
- **CSS**: append to `style.css` as a new section with the same banner comment style the file uses (`/* --- */ /* Dashboard */ /* --- */`), placed before the `Responsive` section, with its own responsive rules at 900px/600px. Add missing tokens to the existing `:root` once. Class names are flat, descriptive and prefixed by component (`.expense-row`, `.expense-row-amount`), matching the existing `.mock-stat-label` style. No BEM double-underscores, no utility soup.
- **JS** (only if needed): add a clearly commented block inside the existing `DOMContentLoaded` handler in `main.js`, guarded by an element check so it does nothing on other pages.
- **Route/data**: the UI is the deliverable. If the template needs data the route doesn't provide yet, make the minimal change (thin route in `app.py`, query helper in `db.py`, parameterised SQL) or, if that's a bigger feature, list the exact context variables the template expects and suggest writing a spec with the repo's `/create-spec` command.

Keep it lean: no commented-out alternatives, no placeholder lorem, no styles for elements that don't exist. Realistic sample copy (Indian context, rupees) where copy is needed.

If you have the repo checked out, edit the files directly. Otherwise present each file in its own code block.

### 5. Verify before handing over

When the repo is available, check the work actually runs:
- Render the page through Flask's test client (log in or seed a session if the page is behind auth) and confirm a 200 with no template errors, both with data and with an empty state.
- Grep your new CSS for hardcoded hex values and for class names used in the template but never defined (and vice versa).
- If a browser tool is available, look at the page at ~1280px and ~375px wide.

## Response format

Structure every answer like this:

**1. UI structure** (brief)
- Layout: the grid/sections from top to bottom, one line each.
- Key UX decisions: 2–4 bullets explaining the choices that matter (what's emphasised and why, how empty/error/mobile states behave).

**2. Code**, one block (or one edit) per file, labelled with path and whether it's new or modified:
- `templates/<page>.html`
- `static/css/style.css`: the new section (and `:root` additions, if any)
- `templates/_icons.html` if added or extended
- `static/js/main.js`, `app.py`, `database/db.py` only if touched

**3. Notes**, only if there's something worth saying: tokens or icons you added, assumptions about data, how to see it (e.g. "log in as the seed user, then open /dashboard"), one suggested next step.

Skip long preambles and design-philosophy essays. The structure section is a quick map, not a spec.

## Avoid

- Generic or dated UI: heavy gradients, glassmorphism, neon accents, drop-shadow-heavy cards, stock "admin template" sidebars, emoji as icons.
- Random one-off styles: a new colour, radius or shadow that isn't a token. If something genuinely needs a new token, add it to `:root` and say so.
- Unstructured code dumps: every block labelled with its file, CSS in a named section, no giant inline `style=""` attributes (a computed width on a progress bar is fine).
- Clutter: more than one primary action per view, more than ~4 stat tiles in a row, tables with columns nobody needs.
- Breaking the stack: React/JSX, Tailwind classes, CDN JS, per-page CSS/JS files, hardcoded URLs, SQL in routes.