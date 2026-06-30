# Astro Project Structure

This is what to create when the user picks "build it now". The user will unzip, run `npm install`, then `npm run dev`.

## Files to create

```
<business-slug>-site/
├── package.json
├── astro.config.mjs
├── tsconfig.json
├── .gitignore
├── README.md
├── public/
│   ├── favicon.svg
│   └── images/                    ← user-uploaded images go here
└── src/
    ├── layouts/
    │   └── Layout.astro
    ├── components/
    │   ├── Header.astro
    │   ├── Footer.astro
    │   └── Hero.astro
    ├── styles/
    │   └── global.css
    └── pages/
        ├── index.astro
        ├── about.astro
        ├── services.astro
        ├── contact.astro
        └── <extra-pages>.astro    ← gallery.astro, faq.astro, etc. as needed
```

## Handling user-uploaded images

If the user uploaded images during Round 4:

1. Copy each from `/mnt/user-data/uploads/` into `public/images/` with clear names (`logo.svg`, `storefront.jpg`, `team-maria.jpg`, `service-haircut.jpg`, etc.).
2. Reference each one in the relevant `.astro` file as `/images/<filename>` (the leading slash is important — it's the public root).
3. Always include meaningful `alt` text. For decorative images, `alt=""` is correct; for content images (logo, team photos, products), describe what the image shows.
4. For the logo specifically: also generate a `favicon.svg` from it if the upload is an SVG, or add a `<link rel="icon" type="image/png" href="/images/logo.png">` if it's a raster format.

If the user uploaded no images, use inline SVG placeholders (gradients, patterns, geometric shapes) — never stock photos, never AI-generated faces or places.

## File contents — exact specs

### package.json

Use the latest Astro version. The cleanest way: instead of writing `package.json` by hand, run `npm create astro@latest` (or `npx create-astro@latest`) to scaffold the project, then customize from there. This ensures the user gets whatever version is current when they build.

If for some reason you're writing `package.json` directly, use `"astro": "latest"` rather than pinning a specific version:

```json
{
  "name": "<business-slug>-site",
  "type": "module",
  "version": "0.0.1",
  "scripts": {
    "dev": "astro dev",
    "start": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "astro": "astro"
  },
  "dependencies": {
    "astro": "latest"
  }
}
```

After install, `npm` will resolve `latest` to a specific version and lock it in `package-lock.json`. The user can upgrade later with `npm update`.

### astro.config.mjs

```js
import { defineConfig } from 'astro/config';

export default defineConfig({
  // Site config goes here when the user has a domain
});
```

### tsconfig.json

```json
{
  "extends": "astro/tsconfigs/strict"
}
```

### .gitignore

Standard Astro gitignore — `node_modules`, `dist`, `.astro`, `.env`, `.DS_Store`.

### README.md

A short, plain-language readme for a non-developer:
- What this is
- How to run locally (`npm install`, `npm run dev`)
- How to build for production (`npm run build` produces a `dist/` folder)
- Where to drop the `dist/` folder for free hosting (Netlify Drop: netlify.com/drop, or Vercel)
- Where to edit content (point them to specific files: "Change your tagline in `src/pages/index.astro` line ~XX")

### src/styles/global.css

Set up CSS custom properties from the chosen palette (see `color-palettes.md`). Include:
- CSS reset (modern minimal one — `*, *::before, *::after { box-sizing: border-box; }`, body margin 0, etc.)
- CSS variables for color, font, spacing scale, max-content-width
- Base typography — body, headings, links
- A `.container` utility for max-width + horizontal padding
- Focus styles (visible outline for keyboard users)
- Smooth scroll, prefers-reduced-motion fallback

### src/layouts/Layout.astro

```astro
---
import Header from '../components/Header.astro';
import Footer from '../components/Footer.astro';
import '../styles/global.css';

interface Props {
  title: string;
  description: string;
  ogImage?: string;
}

const { title, description, ogImage = '/images/og-default.jpg' } = Astro.props;
const canonicalURL = new URL(Astro.url.pathname, Astro.site || 'https://example.com');
---

<!DOCTYPE html>
<html lang="<LANG>">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonicalURL} />

    <!-- Open Graph (Facebook, LinkedIn, WhatsApp link previews) -->
    <meta property="og:type" content="website" />
    <meta property="og:url" content={canonicalURL} />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:image" content={new URL(ogImage, canonicalURL)} />

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={title} />
    <meta name="twitter:description" content={description} />
    <meta name="twitter:image" content={new URL(ogImage, canonicalURL)} />

    <!-- Google Fonts link goes here -->
  </head>
  <body>
    <Header />
    <main><slot /></main>
    <Footer />
  </body>
</html>
```

Pass `title` and `description` from every page. Title format: `Page Name — <Business Name>`, except homepage which is `<Business Name> — <Tagline>`. Description: 140–160 characters, written from the page's actual content (not keyword-stuffed).

### Components and pages

- **Header.astro**: Logo/business name (left), nav links to all pages (right). Mobile: hamburger or stacked. Update the nav array to include any extra pages the user added.
- **Footer.astro**: Compact contact summary, social links, copyright `© <year> <business name>`.
- **Hero.astro**: Reusable hero block taking `title` and `subtitle` props.
- **index.astro**: Hero + "Why us" 3-card section + a final CTA section linking to Contact.
- **about.astro**: Hero + body text + (optional) values/principles.
- **services.astro**: Grid or list of service cards, each with name + description.
- **contact.astro**: Two columns on desktop (info on left, form/CTA on right), stacked on mobile.

### Extra pages — patterns

When the user added extra pages in Round 3.5, build each one with these patterns:

- **gallery.astro**: Responsive image grid using CSS grid (`grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))`). Lightbox-on-click is optional and only worth adding if simple — a plain `<a href="/images/full.jpg" target="_blank">` is fine.
- **faq.astro**: Either a styled list of Q/A pairs, or HTML `<details>`/`<summary>` for native accordions (no JS needed). Prefer `<details>` for accessibility.
- **pricing.astro**: Three layouts depending on what the user provided — flat list (table or grid), tiered packages (3 or 4 cards side by side, "most popular" highlighted if specified), or "contact for a quote" (a single CTA section pointing to the Contact page).
- **testimonials.astro**: Card grid or simple stacked quotes. Always include attribution (name, and role/company if given). Never invent or pad testimonials the user didn't provide.
- **news.astro** (static blog substitute): An index page listing posts with title, date, excerpt. Each post is its own file at `src/pages/news/<slug>.astro` using the same Layout. No dynamic routes, no collections — keep it dead simple so the user can edit posts by hand.
- **team.astro**: Grid of cards, one per person, with photo (or initial-based placeholder), name, role, and bio.
- **other (custom)**: Build per the user's description. If they were vague, default to: hero, body content section, CTA section.

### SEO files (always create both)

- **`public/robots.txt`** — allow all crawlers:
  ```
  User-agent: *
  Allow: /
  Sitemap: https://example.com/sitemap.xml
  ```
  (The user replaces `example.com` with their real domain after deployment. Note this in the README.)
- **`public/sitemap.xml`** — either hand-write a static sitemap listing every page, or use the official `@astrojs/sitemap` integration (check the `astro-docs` MCP for the current install command). For a 4–7 page site, hand-written is fine and avoids one more dependency.

## Critical reminders

- **Read `/mnt/skills/public/frontend-design/SKILL.md` before writing any of these files.** That skill defines the actual design tokens, type scale, and layout conventions for this environment. Without it, the output looks generic.
- **Do not invent content.** Every word on the page should come from the interview answers. If a section has no content, omit it.
- **Decorative imagery only.** Use inline SVG patterns, gradients, or geometric shapes for placeholders. Never use stock photos of people or AI-generated photos of places.
- **Mobile-first.** Default styles are for mobile; use `@media (min-width: 768px)` for desktop overrides.
- **Accessibility basics.** Semantic HTML (`<header>`, `<nav>`, `<main>`, `<footer>`, `<section>`), all images have `alt`, all links are descriptive, color contrast meets WCAG AA.
- **SEO basics on every page.** Unique title and description; Open Graph + Twitter card tags; `lang` on `<html>`; `robots.txt` and `sitemap.xml` in `public/`.

## Packaging (claude.ai only)

In claude.ai, after creating all files, zip the project folder:

```bash
cd /home/claude && zip -r <business-slug>-site.zip <business-slug>-site/
```

Move the zip to `/mnt/user-data/outputs/`, then call `present_files` with the zip path.

In Claude Code, do not zip — the project lives directly in the user's filesystem. Run `npm install` and `npm run dev` instead so they can see the site at `http://localhost:4321`.
