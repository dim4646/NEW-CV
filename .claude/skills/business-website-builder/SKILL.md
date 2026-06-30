---
name: business-website-builder
description: Guide non-technical small business owners through creating a presentational website (Home, About, Services, Contact, plus optional extras like Gallery, FAQ, Pricing, Testimonials, Team, or static News) using Astro. Runs a friendly interview covering brand colors (sampling from a logo, taking hex values, or suggesting from moods), uploaded logos and photos with per-image placement, and per-page content. Works in three environments — local Claude Code (terminal + localhost preview), claude.ai chat (sandboxed, returns a zip), and claude.ai/code (cloud sessions with GitHub PR + Netlify auto-deploy). Trigger whenever a non-developer wants a website, landing page, or online presence for their business — phrases like "build me a website", "I need a site for my shop/clinic/studio", "help me make a business website", "create a website for my company", or any time someone uploads no code and asks for a site. Also trigger on Claude Code + website together.
---

# Business Website Builder

This skill walks a non-technical small business owner through building a clean, professional 4-page website (Home, About, Services, Contact) using Astro. The user does not need to know HTML, CSS, or design — Claude asks plain-language questions and produces either a paste-ready prompt for Claude Code or a fully built project.

## Audience and tone

Assume the user is a small business owner — a hairdresser, a lawyer, a bakery owner, a physiotherapist, a tutor — who can install software with step-by-step guidance but does not write code. Avoid jargon. When a technical term is unavoidable, define it in one short sentence the first time it appears. Do not assume they know what a "framework", "static site", or "deployment" is.

Be warm and patient. This person is doing something brave. Celebrate small wins ("Great, that's the hardest part done").

## How the skill ends

The interview produces a fully built Astro project. *How* and *where* that project gets built depends on which environment the skill is running in. There are three:

- **Local Claude Code** (running on the user's own machine, terminal-based): build directly into a folder in their current working directory, run `npm install` and `npm run dev`, and tell the user to open `localhost:4321` to see the site before deploying.
- **Claude.ai chat** (web/mobile chat, sandboxed): build the project in the sandbox, zip it, hand it over via `present_files`. The user unzips and runs it locally themselves to preview, then deploys.
- **Claude.ai/code** (cloud Claude Code, sessions started from claude.ai/code): build directly into the cloned GitHub repository, commit on a branch, and let the user create a PR. Once the repo is connected to Netlify, **the live site IS the preview** — every merged PR auto-deploys. No localhost needed.

Detect the environment before building — see "Environment detection" below.

## The interview

Ask questions in small batches, not all at once. The user is more likely to finish if it feels like a conversation than a form. Use the `ask_user_input_v0` tool for any question with a small set of clear options — it makes selection easier on mobile.

Group the interview into five short rounds. After each round, briefly reflect back what you heard ("Got it — a family-run bakery in Thessaloniki, focused on traditional Greek pastries") so the user feels heard and can correct misunderstandings early.

### Round 1 — The basics

Ask in prose (these need free-text answers):

- What's the business called?
- In one or two sentences, what does the business do?
- Where is it based? (city / region / online-only)
- Who's the typical customer? ("Anyone passing by", "young families", "other businesses", etc. — plain language is fine)

### Round 2 — Brand feel

This round has two sub-steps because the color question branches.

**2a. Vibe and typography** — use `ask_user_input_v0`:

- **Vibe**: Modern & minimal / Warm & friendly / Bold & energetic / Elegant & refined / Playful & quirky
- **Typography feel**: Clean & modern (sans-serif) / Classic & trustworthy (serif) / Distinctive & characterful (mixed) / No preference

**2b. Colors** — ask first whether they already have brand colors. Use `ask_user_input_v0`:

- **Do you have brand colors already?**: Yes, I have specific colors / I have a logo and want colors that match it / No, please suggest some

Then branch:

- **"Yes, I have specific colors"** → ask in prose: "Great — share what you have. Hex codes (`#2C7A7B`) are most precise, but plain descriptions work too (`a deep forest green`, `the orange from my logo`). One main color is enough; I'll build the rest of the palette around it."
- **"I have a logo and want colors that match it"** → ask them to upload the logo if they haven't already (see Round 4). Once it's uploaded, sample the dominant colors yourself and propose a palette: "Based on your logo, I'm thinking [main color] as the accent with [neutral] for backgrounds. Sound right, or want something different?"
- **"No, please suggest some"** → fall back to the mood picker. Use `ask_user_input_v0`:
  - **Color mood**: Soft neutrals / Earthy & natural / Cool blues & greens / Warm reds & oranges / Bold black & white

For all three branches, the final output is a full 7-value palette derived per `references/color-palettes.md`. Always confirm the chosen palette back to the user with the actual hex values before moving on, so they have a chance to course-correct.

### Round 3 — Content for each page

For each of the four pages, ask what should appear. Keep it conversational — don't dump all questions at once.

- **Home**: A short tagline (5–10 words), and 3 short reasons customers choose them
- **About**: The story — when did it start, who runs it, what makes it personal? (3–6 sentences is fine; the user can ramble and Claude will tighten it)
- **Services**: A list of 3–8 services with a one-line description each. If the user gives names only, prompt for the one-liner.
- **Contact**: Phone, email, physical address (if any), opening hours (if any), and which social links to include (Instagram, Facebook, LinkedIn, TikTok — only what they actually use)

If the user gets stuck on any of these, offer to draft something based on what they've already said, then let them edit.

### Round 3.5 — Any other pages?

Ask: "Beyond Home, About, Services, and Contact — do you want any other pages?" Use `ask_user_input_v0`:

- **Extra pages**: No, four is enough / Yes, add more (multi-select next)

If yes, follow up with a multi-select listing the common additions, plus an "Other" option:

- Gallery / Portfolio (photos of work)
- FAQ (common questions and answers)
- Pricing
- Testimonials (real ones the user provides)
- Blog / News
- Booking / Appointments
- Team (staff bios)
- Other (free text)

**Cap the total at 7 pages.** If the user picks more, gently push back: "Let's start with the most important 3 — we can always add more later. Which matter most right now?"

**Refuse two specific additions:**
- **Blog/News** as a full system → this needs a content backend and is out of scope. Offer a static "Latest News" page instead, where they manually edit posts as `.astro` files. Tell them honestly that a real blog needs a separate conversation.
- **Booking/Appointments** with real availability → this needs a third-party service (Calendly, SimplyBook, etc.). Offer to embed their existing booking link as a button, but don't build a custom system.

For each extra page they confirm, ask one short follow-up question to gather content:

- **Gallery**: How many images, and do they have them? (If no images, skip this page.)
- **FAQ**: Ask for 3–8 question-and-answer pairs in prose.
- **Pricing**: Ask for the structure — flat list, tiered packages, or "contact for a quote"?
- **Testimonials**: Ask them to paste 3–6 real testimonials with attribution. Refuse to invent them.
- **Latest News (static blog substitute)**: Ask for 1–3 starter posts, each with a title, date, and 2–4 paragraphs.
- **Team**: Ask for each person's name, role, and one-sentence bio. Photos optional (see Round 4).
- **Other**: Ask what's on it and what content goes there.

Reflect the full final page list back: "Got it — your site will have: Home, About, Services, Contact, Gallery, and FAQ. Six pages total." Wait for confirmation.
### Round 4 — Imagery and logo

This round has two goals: collect any visual assets the user already has, and figure out where each one should go on the site.

**4a. What do they have?** Ask in prose: "Do you have any of these you'd like to use? Upload whatever you have — no need for everything." Suggest specifically:

- A logo (any format — PNG, SVG, JPG)
- Photos of the storefront, workspace, or interior
- Photos of products or finished work
- Team or staff photos
- A profile photo of the owner (for solo businesses)

If the user uploads files, look at each one and confirm what you see ("I see a logo in dark green, a photo that looks like a café interior, and three product shots"). This catches mis-uploads early.

**4b. Where does each one go?** For every uploaded image, ask the user where they want it placed. Don't assume — a logo *usually* goes in the header but the user might also want it big on the homepage hero. Default suggestions to offer:

- **Logo** → header (always), favicon (recommended), and optionally footer
- **Storefront/interior photo** → homepage hero background, or About page
- **Product photos** → Services page (one per service if numbers match), or Gallery if they added one
- **Team photos** → Team page if they added one, or About page
- **Owner profile photo** → About page

Confirm placements back to the user: "So the logo goes in the header and as the favicon, the storefront shot is the homepage hero, and the three product photos go next to your three services. Sound right?"

**4c. Gaps.** For any page that needs imagery and doesn't have a real photo, ask: "Want me to use a decorative placeholder (gradient, pattern, or geometric shape — clearly not a real photo), or leave that section image-free for now?"

**Hard rules:**
- Never generate fake photos of people, real-looking storefronts that don't exist, or anything that could be mistaken for a real place.
- Never use stock photos of strangers.
- Placeholders are gradients, SVG patterns, or geometric shapes only — and should look obviously decorative.
- If the user uploads a photo of a real person and asks to use it, confirm they have permission (one quick question is enough — don't lecture).

**File handling on claude.ai:** Uploaded images live in `/mnt/user-data/uploads/`. Copy each one into the project's `public/images/` folder with a clear name (`logo.svg`, `storefront.jpg`, `service-haircut.jpg`, etc.) and reference them in the `.astro` files as `/images/<filename>`.

**File handling in Claude Code:** Ask the user where they have the images on their machine, or to drop them into a folder you tell them about. Then copy them into the project's `public/images/` folder with the same naming convention. Reference them in the `.astro` files as `/images/<filename>`.

### Round 5 — Practical bits

Use `ask_user_input_v0`:

- **Language**: English / Greek / Both (with a language switcher) / Other (free-text)
- **Contact form**: Yes, simple form that opens the user's email client (mailto) / No, just show contact info / Yes, real form that sends email (note: requires a small extra service)
- **Domain**: I already have one / I want to buy one / I'll figure it out later

That's the end of the interview — once these are answered, start building.

## Environment detection

Before building, figure out which of the three environments you're in. Run these checks in order and stop at the first match:

1. **Check for the claude.ai sandbox.** Run `ls /mnt/user-data/outputs/ 2>&1`. If the path exists AND a `present_files` tool is in your toolset, you're on **claude.ai chat**. Stop here.

2. **Check for claude.ai/code (cloud Claude Code).** Run `echo $CLAUDE_CODE_REMOTE`. If it prints `true`, you're on **claude.ai/code**. Also confirm the working directory is inside a git repository with `git rev-parse --is-inside-work-tree 2>/dev/null` — claude.ai/code always clones a repo. Stop here.

3. **Otherwise, you're in local Claude Code** (the user's own terminal). Bash runs on their machine, you can write anywhere, no sandbox.

If you can't tell after these checks, ask the user once: "Quick check — are you running this in your terminal (local Claude Code), on claude.ai chat, or at claude.ai/code (the cloud sessions surface)?" Then proceed accordingly.

## Special handling for claude.ai/code

Before doing anything else in claude.ai/code, **check whether the user actually wants to use this surface**. The cloud-sessions workflow is built around GitHub repos and PRs — great if the user already has a GitHub account and is comfortable with merging PRs, hard otherwise.

Tell the user honestly: "I see you're on claude.ai/code. This works best if you already have a GitHub account and are OK with the GitHub + PR flow — I'll commit your site to a branch, you merge the PR, and your site auto-deploys to Netlify on every change. If that sounds fine, we'll continue. If it sounds confusing, you might prefer running the local Claude Code in your terminal — same skill, but with a localhost preview and no GitHub needed. Which do you want?"

If they want to switch surfaces, give them a one-line out and stop: "No problem. Close this session, install Claude Code locally with `npm install -g @anthropic-ai/claude-code`, run `claude` in an empty folder, and ask me to build your business website. I'll handle it from there."

If they confirm GitHub is fine, continue with the build.

## Building the site — common steps (all environments)

Regardless of environment, do these first:

1. **Read `/mnt/skills/public/frontend-design/SKILL.md`** (claude.ai) or your equivalent `frontend-design` skill (Claude Code). This is non-negotiable — it defines design tokens, layout grids, and styling conventions. Skipping it produces generic-looking output.
2. **For Astro syntax/API questions**, check whether an `astro-docs` MCP is available via `tool_search`. Use it. If not present, web-search `docs.astro.build`. Never trust training-data memory for Astro specifics — Astro evolves quickly. Note: on claude.ai/code, MCP servers only load if they're declared in the repo's `.mcp.json` — you can't add them via `claude mcp add` because that writes to user-local config that isn't carried into the cloud session. If `astro-docs` isn't present in the cloud session, just web-search the docs.
3. **Decide on a project folder name** — a slug derived from the business name (e.g. "Maria's Bakery" → `marias-bakery-site`). Lowercase, hyphens, no spaces.
4. **Build the Astro project** following `references/astro-structure.md`. Bake the user's content directly into the `.astro` files. No placeholders. No invented content. Use the exact color palette hex values from Round 2. Add SEO basics (per-page `<title>`, `<meta description>`, Open Graph + Twitter card tags, `lang` attribute, `public/robots.txt`, `public/sitemap.xml`). Make it responsive (mobile-first, breakpoint at 768px).
5. **Place uploaded images** per the placement decisions from Round 4. Copy from `/mnt/user-data/uploads/` (claude.ai) or wherever the user uploaded them (Claude Code) into the project's `public/images/` folder.

Then branch on environment:

## Building — Local Claude Code path

The user's terminal is the workspace. They want to see the site running.

1. **Build directly into the user's current working directory.** Create the folder there: `./<business-slug>-site/`. Don't put it anywhere weird — they ran `claude` from where they want the project.
2. **Install dependencies.** Run `npm install` in the project folder. This may take a minute. Tell the user what's happening so they don't think it's frozen ("Installing Astro and its dependencies — this takes about a minute").
3. **Start the dev server.** Run `npm run dev` (in the background, since the dev server is long-running). Astro typically serves on `http://localhost:4321`.
4. **Tell the user to open `http://localhost:4321` in their browser** to see the site. Make this clear and prominent — it's the payoff for the whole interview.
5. **Wait for their feedback.** Ask: "Take a look — does this match what you had in mind? Anything you want changed before we put it on the internet?" Edit-and-reload is fast in Astro, so iterate based on their response.
6. **When they're happy, walk them through deployment** (see "Deployment" section below).

If `npm install` or `npm run dev` fails, surface the error to the user and fix it. Don't ignore failures.

## Building — Claude.ai path

The sandbox can't show the user a running site. Best you can do is hand over a working project they can run locally.

1. **Build the project at `/home/claude/<business-slug>-site/`.**
2. **Don't run `npm install` or `npm run dev`** — the dev server wouldn't be reachable from the user's browser anyway, and `node_modules` would bloat the zip pointlessly. The user installs deps locally.
3. **Zip the project**: `cd /home/claude && zip -r <business-slug>-site.zip <business-slug>-site/`.
4. **Move the zip to `/mnt/user-data/outputs/`** and present it via `present_files`.
5. **Walk the user through running it locally** so they see it before deploying:
   - Unzip wherever they like (Desktop is fine).
   - Install Node.js from nodejs.org (LTS) if they don't have it.
   - Open a terminal, `cd` into the unzipped folder.
   - Run `npm install`, then `npm run dev`.
   - Open `http://localhost:4321` in their browser.
6. **Then walk them through deployment** (see "Deployment" section below).

## Building — Claude.ai/code path (GitHub-first)

You're inside a cloned GitHub repo. The user's preview will be the live Netlify site, not localhost. The flow is: build into the repo on a new branch → commit → push → user creates a PR and merges → Netlify auto-deploys.

1. **Verify the repo state.** Run `git status` and `pwd`. Confirm with the user: "I'll build your site into this repo: `<repo path>`. Is that right?"
   - **If the repo isn't empty** (has existing files unrelated to the website): ask whether to put the site in a subfolder (e.g. `site/`) or whether they made a new empty repo for this. Don't overwrite their existing work.
2. **Create a new branch.** Use a descriptive name: `git checkout -b add-business-website`.
3. **Build the Astro project** in the repo (root if empty, subfolder if not). Same steps as the common build above — frontend-design skill, content from interview, SEO, responsive, etc.
4. **Add a `netlify.toml`** at the repo root (or in the site subfolder if applicable) so Netlify auto-detects build settings:
   ```toml
   [build]
     command = "npm run build"
     publish = "dist"
   ```
   If the site is in a subfolder, set `base` too:
   ```toml
   [build]
     base = "site"
     command = "npm run build"
     publish = "dist"
   ```
5. **Add a brief `README.md`** at the repo root describing what the site is, who it's for, and how to run it locally. Non-tech users may forget what's in their own repo a month from now — write it for that future self.
6. **Commit everything** with a clear message: `git add -A && git commit -m "Add business website (Astro)"`.
7. **Push the branch**: `git push -u origin add-business-website`.
8. **Tell the user the next steps** — keep this short and concrete. They need to:
   - **Open a Pull Request on GitHub.** GitHub usually shows a "Compare & pull request" banner right after a push. They click it, write a one-line description (or just accept the default), and create the PR.
   - **Connect Netlify to the repo (one-time setup, only on the first build).** Go to netlify.com, sign in (free tier), click "Add new site" → "Import from Git" → connect GitHub → pick this repo. Netlify reads `netlify.toml` and figures out the rest. Default branch will deploy automatically.
   - **Merge the PR.** Once Netlify is connected, every merge to the main branch triggers a fresh deploy. The first one takes ~1–2 minutes; the user will see the live URL in Netlify's dashboard.
9. **Don't run `npm install`, `npm run dev`, or `npm run build` here.** None of them help — the user can't reach a dev server in this VM, and the build runs on Netlify after merge anyway. Just commit valid Astro source.

After the PR is merged and Netlify is connected, **the live URL becomes the preview**. Any future change goes through the same loop: open a new claude.ai/code session, ask for the change, get a PR, merge it, the live site updates. The user never touches a terminal or localhost.

## Deployment (local Claude Code and claude.ai chat)

This section is for users who built the site locally or got a zip from claude.ai chat. **For claude.ai/code users, deployment happens via merging the PR + Netlify auto-deploy** — see the previous section, no extra steps here.

Once the user has seen the site locally and is happy with it:

**Easiest path — Netlify Drop (no terminal beyond `npm run build`):**
1. In the project folder, run `npm run build`. This produces a `dist/` folder.
2. Go to **netlify.com/drop** in a browser. Drag the `dist/` folder onto the page. The site is live in about 30 seconds at a `something-random.netlify.app` URL.
3. Sign into Netlify in the same browser to claim the site, rename the URL, and keep it permanent.

**Claude Code path with Netlify MCP (preferred for local Claude Code users — handles redeploys and edits later):**
1. Add the Netlify MCP one time: `claude mcp add netlify npx -- -y @netlify/mcp`
2. In the project folder, ask Claude Code: "Deploy this to Netlify." It handles auth (browser popup the first time) and the upload.
3. Future changes: edit in the same folder via Claude Code, then ask "redeploy to Netlify."

**GitHub-connected path (if the user wants long-term auto-deploy without claude.ai/code):**
1. The user creates a GitHub repo and pushes the project to it.
2. In Netlify: Add new site → Import from Git → pick the repo. Netlify auto-detects Astro builds.
3. From then on, any push to the main branch auto-deploys. This matches the claude.ai/code workflow.

## Custom domain (all environments)

Optional but recommended for real businesses. Same steps regardless of how the site got deployed:

1. Buy from a registrar — namecheap.com, porkbun.com (international), or papaki.gr / top.host (for `.gr`). Roughly $10–15/year for `.com`, €15–20/year for `.gr`. Pick something short and memorable.
2. In Netlify: site → Domain settings → Add a domain. Netlify gives DNS values; paste them into the registrar's control panel. HTTPS is automatic — no action needed for the padlock icon.
3. In local Claude Code with the Netlify MCP, you can also ask "help me connect my domain to Netlify" and it'll walk you through the DNS step.

## Editing the site later

Tell the user how to make changes after the initial build:

- **Local Claude Code users**: re-open their terminal, `cd` into the project folder, run `claude`, describe what they want changed ("update the phone number on the contact page", "add a new service called X", "make the homepage hero darker"). Then `npm run dev` to preview, or ask Claude Code to redeploy.
- **Claude.ai chat users**: come back to claude.ai, attach the project zip (or the relevant `.astro` file), describe the change. They'll get an updated zip back. To make this less painful long-term, suggest they install Claude Code at some point.
- **Claude.ai/code users**: open a new claude.ai/code session on the same repo, describe the change. They get a PR. Merge it. Netlify auto-deploys. No terminal, no localhost — they can do this from their phone if they want.

## Things to never do

- Never invent reviews, testimonials, awards, or quotes from real or fake customers. If the user wants testimonials, ask them to provide real ones.
- Never use stock photos of people who don't exist or AI-generated photos of real-looking places. Placeholder visuals should be clearly decorative (gradients, patterns, geometric shapes, abstract SVGs).
- Never include tracking, analytics, or third-party scripts the user didn't ask for.
- Never use lorem ipsum in the final output. If a section has no content, ask the user for it or omit the section entirely.
- Never add a fake company history ("founded in 1952"). If the user didn't say when it started, leave that out.

## Edge cases

- **The user has no idea what they want for "vibe" or "colors"**: Offer to suggest based on the type of business (a law firm probably wants "elegant & refined / soft neutrals"; a bakery probably wants "warm & friendly / earthy"). Suggest, then confirm.
- **The user's business has no physical location**: Skip the address field on Contact; replace with "Available across [region]" or "Online" depending on what they said in Round 1.
- **The user wants a blog with real posts and a CMS**: Out of scope. Offer a static "Latest News" page they edit by hand (see Round 3.5). Tell them honestly that a real blog with admin UI needs a separate conversation.
- **The user wants real booking/appointments with availability**: Out of scope. Offer to embed their Calendly/SimplyBook link as a button instead.
- **The user wants more than 7 pages**: Push back gently. Help them pick the most important ones; the rest can be added later.
- **The user gives content in a language other than what they picked**: Match the language they wrote in. Don't translate without permission.

## Reference files

- `references/astro-structure.md` — File layout and per-page content patterns for the Astro project
- `references/color-palettes.md` — Curated palettes for each color mood option, with hex values
