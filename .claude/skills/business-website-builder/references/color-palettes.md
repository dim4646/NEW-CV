# Color Palettes

Each "color mood" option from Round 2 maps to a curated palette below. Always provide hex values when filling the prompt template or building the site — never just color names.

Each palette gives: background, surface (cards, lifted areas), text, muted text, accent (primary brand color), accent-hover, border.

## Soft neutrals

```
--bg:           #FAFAF7
--surface:      #FFFFFF
--text:         #1A1A1A
--muted:        #6B6B6B
--accent:       #2D2D2D
--accent-hover: #000000
--border:       #E8E6E1
```

Pairs well with: any business that wants to feel calm, premium, trustworthy. Default for law, consulting, design studios.

## Earthy & natural

```
--bg:           #F5F1EA
--surface:      #FFFBF4
--text:         #2A2118
--muted:        #6B5E4F
--accent:       #8B6F47
--accent-hover: #6B5333
--border:       #E5DCC9
```

Pairs well with: bakeries, cafés, ceramics, artisans, wellness, organic/sustainable brands.

## Cool blues & greens

```
--bg:           #F4F8F7
--surface:      #FFFFFF
--text:         #0F2027
--muted:        #547077
--accent:       #2C7A7B
--accent-hover: #1F5A5B
--border:       #D7E3E1
```

Pairs well with: clinics, healthcare, tech-adjacent services, accountants, anything that wants to feel reliable and clean.

## Warm reds & oranges

```
--bg:           #FFF8F2
--surface:      #FFFFFF
--text:         #2A1B12
--muted:        #7A5C4A
--accent:       #C2410C
--accent-hover: #9A330A
--border:       #F2E1D0
```

Pairs well with: restaurants, food trucks, fitness, energetic services, creative studios.

## Bold black & white

```
--bg:           #FFFFFF
--surface:      #F5F5F5
--text:         #000000
--muted:        #555555
--accent:       #000000
--accent-hover: #333333
--border:       #E0E0E0
```

Pairs well with: fashion, photography, architecture, anything that wants strong editorial presence. Use a distinctive typeface to avoid looking generic.

## Custom (user described it)

If the user described their own palette, derive the seven values yourself, ensuring:
- Body text on background hits at least 4.5:1 contrast (WCAG AA)
- Accent on background hits at least 3:1 contrast for large text / interactive elements
- The palette has one clear "hero" color, not five competing ones

Sanity-check the user's hex values. If they gave a single brand color, build the rest of the palette around it (a tinted near-white background, a slightly darker hover state, a low-saturation muted text, etc.).

## Type pairings (suggestions for Round 2 typography)

- **Clean & modern (sans-serif)**: Inter for everything, OR Inter for body + Space Grotesk for headings.
- **Classic & trustworthy (serif)**: Source Serif Pro or Lora for body + the same for headings (or Playfair Display for headings if a touch more contrast is wanted).
- **Distinctive & characterful (mixed)**: Fraunces for headings + Inter for body. OR for editorial: Tenor Sans for headings + Source Serif Pro for body.
- **No preference**: Default to Inter for everything. Safe, readable, professional.

Always import via `<link>` from fonts.googleapis.com in the layout `<head>`. Use `display=swap` to avoid invisible-text-during-load.
