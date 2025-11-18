# Agent Prompt: Stabilize Logbook Masonry Layout & Typing Effect

## Context
The `page-logbook` view renders Markdown entries as “content bubbles” arranged in a masonry-style CSS grid with a horizontal timeline selector. Entries live in `journal/` (now includes `journal-2025-11-18-cursor-build.md`). Layout logic is in `style.css` and `scripts.js` (`parseMarkdown`, `displayEntry`, `optimizeGridLayout`).

## Current Pain Points
1. **Vertical spacing drift during typing animation**
   - The journal title types character-by-character; while it grows, bubbles beneath temporarily jump or leave extra gaps.
   - Need a masonry formula that keeps vertical guters equal to horizontal ones (currently 0.75rem) even as bubble heights change each frame.

2. **Masonry accuracy**
   - CSS sets `grid-auto-rows` to a very small unit; JS must translate real heights into `grid-row-end: span N`.
   - Wrong span math or stale measurements cause bubbles to either overlap or leave inconsistent white space.

3. **General layout constraints**
   - Timeline and grid should hug the edges (≤20px on desktop, none on mobile).
   - Bubbles share the same dark gradient background, centered media, and responsive column count (1/2/3 columns at mobile/tablet/desktop).

## Files / Areas to Inspect
- `scripts.js`
  - `optimizeGridLayout()` → ensure it reads `rowGap` & `gridAutoRows` accurately, resets `gridRowEnd`, and recalculates spans whenever heights change (typing, media load, resize).
  - `displayEntry()` typing block → throttle layout recalcs so scrolling stays smooth, but reflow happens often enough to keep spacing even.
  - `journalFiles` list now includes `journal-2025-11-18-cursor-build.md`.
- `style.css`
  - `.content-grid` gap/padding values, `grid-auto-rows` (tiny base unit ~0.2rem).
  - `.journal-title`, typing caret styles, bubble gradients, responsive paddings.

## Expected Outcome
1. Vertical gaps between stacked bubbles always equal horizontal gaps, even while the title is typing or media inside a bubble finishes loading.
2. No bubble overlaps, no massive voids; masonry fills columns densely on tablet/desktop and gracefully reduces to one column on mobile.
3. Typing animation keeps the caret visually aligned, does not block scrolling, and does not freeze the bubble below.
4. New Markdown entries automatically appear in both timeline and content grid without extra manual tweaks.

## Tips
- Use `requestAnimationFrame` throttling when reacting to frequent height changes.
- When computing spans: `span = ceil((height + rowGap)/(rowHeight + rowGap))`.
- Keep CSS spacings centralized (one source of truth) so tweaking gutter size is easy.
- Verify on real browsers at 375px, 1024px, and ≥1440px widths.