# Portfolio project: handoff

Last updated: 7 Nov 2026. Owner: Shouvik Sarkar (GitHub `shouviksarkar14`).
Read this file first, then `README.md`. Everything needed to continue the work is in this repo or linked from here.

---

## 1. What this project is

A personal portfolio site for Shouvik Sarkar, a product manager (ex-engineer) looking for PM roles. It shows his work history, two anonymised case studies and his side projects. Three of those side projects run as live demos on the site.

- **Live site:** https://shouvik-sarkar-portfolio.vercel.app
- **Code:** https://github.com/shouviksarkar14/portfolio (this repo)
- **Primary reader:** PM hiring managers. Every content decision is judged against what they need to see in under two minutes.

---

## 2. Current state

| Item | State | Where |
|---|---|---|
| Home page | Live | `/` → `index.html` |
| Switch Board demo | Live, sample data only | `/switchboard/` |
| Casebook Studio demo | Live, 3 original cases | `/casebook/` |
| IIMK course planner | Live, real timetable data | `/planner/` |
| Ideaboard | Card linking out (co-built) | https://ideaboard-three.vercel.app |
| EchoFind | Card linking to its repo | https://github.com/shouviksarkar14/echofind |
| Tremor (own rebuild) | Not started | Placeholder card on the home page |
| Analytics | Script added to every page; **must be switched on in Vercel** | Vercel → portfolio → Analytics → Enable |
| Profile photo | Missing; initials "SS" show instead | Drop a square JPG at `assets/photo.jpg` |

---

## 3. Accounts and services

No secrets are stored in this repo or this file. Log in to each service directly.

### GitHub (account `shouviksarkar14`)
| Repo | Visibility | Purpose |
|---|---|---|
| `portfolio` | Public | This site. Pushing to `main` deploys to production. |
| `echofind` | Public | Hum-and-clue melody search (Next.js + FastAPI). Has its own `README.md` and `docs/HANDOFF.md`. |
| `casebook-studio` | Public | Full Casebook Studio app (Next.js + Supabase login). Contains no case content; cases live in Supabase. |

### Vercel (team `shouvik-s-experiments`)
| Project | Connected to | Production URL | Notes |
|---|---|---|---|
| `portfolio` | GitHub `shouviksarkar14/portfolio`, branch `main` | shouvik-sarkar-portfolio.vercel.app | No build step (framework: none). Analytics not yet enabled. |
| `casebook-studio` | Deployed separately (not from this repo) | casebook-studio-shouvik-s-experiments.vercel.app | Full library behind login. Depends on the Supabase project below. |
| `switch-board-stats` | Unrelated to this site | switch-board-stats.vercel.app | Leave as is. |

### Supabase (region ap-south-1)
| Project | Used by | Status on 7 Nov 2026 |
|---|---|---|
| `casebook-studio` | Full Casebook Studio app (login, cases, bookmarks, progress) | **Paused (inactive).** The full library app will not work until it is restored from the Supabase dashboard. Free-tier projects pause after a period of no use. |
| `waypoint-jobsearch` | Older job-search console ("Waypoint") | Paused. Not used by this site. |

The Casebook app's Supabase URL and anon (publishable) key are in `casebook-studio/lib/env.ts`. The anon key is safe in the browser because Row Level Security protects every table. Never put a service-role key in client code.

### claude.ai (where the source apps live)
The live Switch Board and the original Casebook Studio are **claude.ai artifacts** in Shouvik's account. The live Switch Board keeps its data in the artifact's private database and is filled by a scheduled task that reads Gmail three times a day. That task and data stay on claude.ai. This site only has public demo copies.

---

## 4. Repo layout

```
index.html                 Home page: all CSS and JS inline, no framework
switchboard/index.html     Switch Board demo (generated, see section 6)
casebook/index.html        Casebook Studio demo (generated, see section 6)
planner/index.html         IIMK course planner (Shouvik's file, lightly edited)
assets/*.webp              Card screenshots, 640px wide
vercel.json                cleanUrls + trailingSlash
tools/                     Scripts that rebuild the demo pages and take screenshots
README.md                  Short public description
HANDOFF.md                 This file
```

Plain static HTML. There is no `package.json` and no build. Vercel serves the files as they are.

---

## 5. How to change the site

1. Edit the HTML in this repo.
2. Check it locally: `python3 -m http.server 8765` from the repo root, then open http://localhost:8765.
3. Optional screenshot check (needs Node and Playwright): `FULL=1 node tools/screenshot.js http://localhost:8765/ out.png 1280 900` (add a 7th argument `dark` for dark mode; use width 390 for mobile).
4. Commit and push to `main`. Vercel deploys in about a minute.
5. Check the live URL.

### Design system (home page)
- Layout copied, with permission, from mahirpatrawala.com: a sticky profile column on the left and sections on the right (About, Journey, Selected work, Side projects, Education, Toolstack, Contact).
- Fonts: Bricolage Grotesque (headings) and Figtree (body), from Google Fonts.
- Colours are CSS variables on `:root`, with dark mode under `prefers-color-scheme` and `[data-theme]`. Accent is green (`--accent:#21a179` light, `#3ccf9d` dark). Green was chosen on purpose so the site doesn't copy Mahir's amber.
- A light/system/dark theme toggle saves the choice to `localStorage`.
- Sections fade in on scroll, with a 1.2-second fallback so content always shows.

### Adding a side-project card
Copy an existing `<a class="card">` block inside `#projects`. Pick the right group (Live or Building) and update the group count in `<div class="grp">Live <i>N</i></div>`. For a screenshot, save a 640×400 WebP to `assets/`.

---

## 6. Rebuilding the demo pages

Both demos are generated from the original claude.ai artifact HTML. The scripts reproduce the live files byte for byte (checked on 7 Nov 2026).

**Switch Board**
```
python3 tools/build_switchboard.py <switch-board-artifact.html> switchboard/index.html
```
This keeps the artifact's UI and replaces its database connection with `tools/switchboard-demo-db.js`, an in-browser store seeded with **fictional** companies. Visitors' changes stay in their own browser (`localStorage` key `sb-demo-v1`), and a "Reset sample data" button restores the seed. Never put real application data into the seed.

**Casebook Studio**
```
python3 tools/casebook_demo.py <casebook-studio-artifact.html> casebook/index.html
```
This keeps the artifact's engine and replaces all 251 cases with 3 cases written for the demo: product design, root cause and guesstimate. The script recomputes the guesstimate's arithmetic and fails if the numbers in the text drift.

**Do not publish the 251-case library.** It is derived from published books and IIM club casebooks. It stays behind login in the `casebook-studio` app.

**Course planner** (`planner/index.html`): Shouvik's original file with personal labels removed. "Nitya" became "Sample" / "Sample plan", and the calendar-export identifiers were made generic. A "Built by" link and the analytics script were added.

---

## 7. Content facts (source of truth: PM Core CV v7.1)

Use only these figures. Do not add new numbers without Shouvik confirming them.

**FinIQ Consulting, Product Manager, May 2025 - Sep 2026**
- Started FinIQ's AI product line as a first-year hire. Pitched the roadmap to the CEO, formed a 5 to 7 person cross-functional team, and won Microsoft sponsorship for the AI platform.
- Document-intelligence engine used at 6+ client institutions, on on-premise models. At one client a 30-minute check now takes about a minute at 90% accuracy, freeing ~480 hours a quarter.
- Email-to-order automation: about 85% of requests routed through rules and 15% through AI. Validated in UAT across 150+ orders from 8 client firms. A data-residency requirement blocked rollout in one region for 3 weeks.
- First platform for a client's own end users: paid back a ~USD 1 Mn investment within 30 days.
- AI code reviewer used by ~100 developers across 20+ repositories.

**ZS Associates, Business Technology Solutions Associate, Jun 2021 - May 2023**
- Co-created ZS Data Library: discovery to MVP, then 3 Fortune 500 implementations linked to ~USD 5 Mn in programme revenue.
- Cut onboarding effort by about 80%. ETL over 50+ TB for a drug launch, powering dashboards across 400+ sales territories.

**Internships:** Synergy Consulting (2024): document-translation workflow, 99% less turnaround time, pre-placement offer. JPMorgan Chase (2020): reporting and pitch-deck automation in Python/VBA.

**Education:** IIM Ahmedabad PGP (MBA), 2023-2025. BITS Pilani B.E. Computer Science with a Finance minor, 2017-2021.

**Side projects**
- **Switch Board** (Oct 2026): job-search tracker. Imports applications from Gmail, surfaces follow-ups, tracks which CV went where.
- **Casebook Studio** (Aug 2026): interview cases as click-through decision trees. The full library has 251 cases and is private.
- **Course planner** (Aug 2026): built for one IIM Kozhikode student's elective bidding; **about 50 IIMK students ended up using it**. Covers 186 courses across T4/T5/T6, with live clash detection, substitute finder, saved versions, and XLSX/JPG/PDF/ICS export.
- **Ideaboard**: co-built with Mahir Patrawala and Siddharth.
- **EchoFind** (Oct 2026): hum a tune and say a clue in one recording to find the melody. The catalogue is six original synthetic tunes, with no commercial songs yet. Runs locally, no paid APIs. 34 backend tests pass.
- **Tremor**: original idea and app by Mahir Patrawala; Shouvik has his permission to rebuild it.

**Personal:** sings and plays guitar. Grew up moving around India and taught himself to read Tamil, Bengali and Gujarati from billboards.

---

## 8. Writing rules (Shouvik's standing preferences)

- No em dashes.
- No "X, not Y" constructions, which read as AI-written.
- Never name client banks or financial institutions. Say "client", "enterprise client" or "large financial institution".
- Avoid finance and trading jargon. He wants to be seen as a product PM, not a finance or consulting profile.
- Confident tone, with no evidence labels or hedging on the site.
- Contact section carries a soft signal only: "Exploring my next product role", with no availability dates.
- Show the work before the numbers. Keep it story-like, not lists of facts.
- For job-search advice: lead with the flaw, tag claims by confidence, and hold position under pushback.

---

## 9. Decision log

| Date | Decision | Why |
|---|---|---|
| 2 Nov | Primary reader is PM hiring managers | Site is for the current job search |
| 2 Nov | Two anonymised FinIQ case studies, no client names | Strongest stories; confidentiality |
| 2 Nov | Confident framing, no evidence labels | Shouvik's call |
| 2 Nov | Free Vercel hosting, no paid domain for now | Cost; `shouvik.build` (USD 30/yr) and `shouviksarkar.me` (USD 13.99 first year) were available if wanted later |
| 4 Nov | Copy mahirpatrawala.com's layout | Shouvik's request; Mahir is a friend |
| 4 Nov | Tremor: build his own version | Mahir gave permission |
| 4 Nov | Casebook: public demo with original cases, full library gated | Copyright risk of publishing book-derived cases |
| 6 Nov | Switch Board public copy uses fictional sample data | Real data is personal (Gmail, contacts) |
| 6 Nov | Vercel Web Analytics over GA4 | Already on Vercel; free; no cookie banner needed |
| 6 Nov | FinIQ dates shown as May 2025 - Sep 2026 (CV dates) | Matches CVs; **LinkedIn still shows FinIQ as current, so one of them needs to change** |

---

## 10. Open items (in priority order)

1. **Enable Analytics** in Vercel (one click; Shouvik).
2. **Add a profile photo** at `assets/photo.jpg` (square).
3. **Reconcile FinIQ dates** between the site (Sep 2026 end) and LinkedIn (current).
4. **Decide on the planner's professor names**, which are public on the site. Keep or blank them.
5. **Restore the `casebook-studio` Supabase project** if the full library app should work again.
6. **Build Tremor** as a separate Vercel project, then link its card. Plan: a static frontend plus one serverless function that drafts five leading indicators per stock using an AI API. Shouvik adds the API key as a Vercel environment variable himself, and it must never be committed. Store the watchlist in the browser first and add a database only if needed. Credit Mahir on the page.
7. **EchoFind demo**: it needs a Python backend. Options are a screen recording on the site, or hosting the FastAPI backend (e.g. Render or a Vercel Python function) and the Next.js frontend on Vercel.
8. **Strip the Mac username** from the paths in `echofind/docs/HANDOFF.md`, `CLAUDE_CODE_HANDOFF.md` and `PROGRESS.md` (cosmetic).
9. **Optional custom domain** (see the decision log for prices). Add it in Vercel → portfolio → Domains.

---

## 11. Onboarding another AI assistant

Paste this as the project instruction:

> You are continuing work on Shouvik Sarkar's portfolio site. Read HANDOFF.md in github.com/shouviksarkar14/portfolio first and follow its writing rules (section 8) and content facts (section 7) exactly. Do not invent figures. The site is plain static HTML; changes go live by pushing to `main`. Never commit secrets, real job-application data, or the private 251-case library.

Files worth attaching to the assistant's project knowledge: this `HANDOFF.md`, `index.html`, the PM Core CV, and `echofind/docs/HANDOFF.md` if working on EchoFind.
