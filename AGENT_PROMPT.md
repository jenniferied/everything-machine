# Agent Prompt: Complete Redesign of Scroll + Typing Animation + Bubble Layout System

## Context
The `page-logbook` view renders Markdown entries as "content bubbles" arranged in a masonry-style CSS grid with a horizontal timeline selector. Entries live in `journal/` (now includes `journal-2025-11-19-cursor-build.md`). Layout logic is in `style.css` and `scripts.js` (`parseMarkdown`, `displayEntry`, `optimizeGridLayout`).

## Current Critical Problems (UPDATED - Situation has worsened)
1. **Bubbles jump/repack during typing animation**
   - Bubbles in right columns move UP when they should stay in place
   - Only bubbles below the title should move DOWN as title grows
   - Current implementation makes it WORSE - bubbles are repacking incorrectly

2. **Scroll position jumps at animation end**
   - When typing animation completes, scroll position jumps
   - Even with delays and explicit positioning, the problem persists

3. **Fundamental CSS Grid issue**
   - `grid-auto-flow: row dense` repacks bubbles when any height changes
   - Switching to `row` during animation helps but doesn't fully solve it
   - Explicit `grid-row-start` positioning was added but problems persist

4. **Layout updates cause repacking**
   - Even incremental updates to single bubble cause other bubbles to move
   - The grid layout system fundamentally fights against dynamic content changes

## Previously Attempted Approaches (DO NOT REPEAT)

### Scroll Position Preservation Attempts
1. **Absolute scroll position storage** - Stored `scrollTop` before layout, restored after. FAILED: Relative position changed when content height changed.
2. **Relative to reference element** - Stored position relative to second bubble or first bubble. FAILED: Still jumped when reference moved.
3. **Relative to stable container** - Stored position relative to `.logbook-entry-container`. FAILED: Still jumped.
4. **Scroll tracking with flags** - Added `isUserScrolling` flag to detect active scrolling. PARTIAL: Helped but didn't solve core issue.
5. **Scroll restoration with double requestAnimationFrame** - Used nested RAF to restore after layout. FAILED: Still jumps.

### Layout Update Strategies
1. **Disable updates during typing** - Set `isTypingAnimationActive` flag, disabled all layout updates. FAILED: Bubbles didn't move live.
2. **Throttled updates (200ms interval)** - Limited layout updates to every 200ms. FAILED: Still caused jumping.
3. **Updates only when not scrolling** - Skip layout updates if `isUserScrolling === true`. PARTIAL: Bubbles don't move when user scrolls.
4. **Scroll position storage during updates** - Store scroll before `gridRowEnd = 'auto'`, restore after. PARTIAL: Still jumps sometimes.
5. **CSS scroll-anchoring** - Added `scroll-anchoring: auto` to `.logbook-main` and `.content-grid`. PARTIAL: Helps but doesn't solve repacking issue.
6. **ResizeObserver for automatic updates** - Used ResizeObserver to detect height changes. PARTIAL: Works but doesn't prevent repacking.
7. **Direct layout updates after each character** - Update layout immediately after each typed character. PARTIAL: Bubbles move but still repack.

### Grid Layout Strategies
1. **Switch to `row` during typing** - Changed `grid-auto-flow` from `row dense` to `row` during animation. PARTIAL: Reduces repacking but doesn't eliminate it.
2. **Explicit `grid-row-start` positioning** - Set explicit row positions for all bubbles to prevent repacking. FAILED: Made situation WORSE - bubbles still move incorrectly.
3. **Incremental updates** - Only update target bubble's span, keep others fixed. PARTIAL: Helps but other bubbles still affected.

### Height Measurement Approaches
1. **getBoundingClientRect().height** - Used initially. FAILED: Included margins, inaccurate.
2. **offsetHeight** - Switched to offsetHeight. IMPROVED: More accurate but still issues.
3. **Temporary pointerEvents disable** - Disabled hover effects during measurement. PARTIAL: Helped but didn't solve.

### Span Calculation Formula
- Current: `span = ceil((bubbleHeight + rowGap) / (rowHeight + rowGap))`
- This formula is mathematically correct but implementation has issues

## Root Cause Analysis (UPDATED)
The fundamental problem is:
1. **CSS Grid `grid-auto-flow: row dense` repacks elements** - When any bubble height changes, Grid tries to fill gaps, causing bubbles to move unexpectedly
2. **Explicit positioning conflicts with Grid's auto-placement** - Setting `grid-row-start` explicitly may conflict with Grid's internal layout algorithm
3. **Multi-column layout complexity** - With 2-3 columns, bubbles in different columns affect each other's positions
4. **Layout recalculation triggers repacking** - Even incremental updates can trigger full Grid recalculation
5. **No reliable way to prevent repacking** - CSS Grid doesn't have a "lock positions" mode

## Current Implementation State (UPDATED - 2025-11-18)
- `optimizeGridLayout()` simplified - removed explicit `grid-row-start` positioning
- Always uses `row` (never `row dense`) to prevent repacking
- Reduced update frequency (every 8 characters instead of every character)
- Two-phase updates: incremental for title bubble, full recalculation in next frame
- Height-change threshold increased to 10px to reduce unnecessary updates
- CSS scroll-anchoring disabled (`overflow-anchor: none`)
- ResizeObserver removed (was causing too many updates)
- 300ms delay before resetting `isTypingAnimationActive` flag

**Result: Significantly improved. Automated test infrastructure created for verification.**

## Required Research (FIRST STEP)
Before implementing, research best practices for:
1. **CSS Grid masonry with dynamic content** - How to handle height changes without scroll jumping
2. **Scroll position preservation during layout changes** - Modern approaches (IntersectionObserver, CSS scroll-anchoring, etc.)
3. **Typing animations with live layout updates** - How other sites handle this
4. **CSS Grid vs Flexbox vs other approaches** - Is Grid the right tool for this?
5. **Browser scroll anchoring** - Can we use native browser features?

## Files to Inspect
- `scripts.js`
  - `optimizeGridLayout()` (lines ~1096-1200) - Current implementation with explicit positioning
  - `displayEntry()` typing block (lines ~1248-1328) - Typing animation with ResizeObserver + direct updates
  - `scheduleLayoutUpdate()` - Batched layout updates during typing
- `style.css`
  - `.content-grid` (lines ~224-235) - Grid setup with `gap: 0.75rem`, `grid-auto-rows: 0.2rem`, `scroll-anchoring: auto`
  - `.content-bubble:hover` (lines ~247-250) - Hover effects that might affect layout
  - `.logbook-main` (lines ~203-210) - Scroll container with `scroll-anchoring: auto`

## Testing Requirements (NEW - HIGH PRIORITY)
Need automated test infrastructure to:
1. Load logbook page automatically
2. Trigger typing animation
3. Measure bubble positions (getBoundingClientRect) at each step
4. Detect when bubbles move incorrectly (compare positions)
5. Measure scroll position changes
6. Output test results (console + optional file)
7. Identify exact failure points (which bubble, when, why)

## Expected Outcome (After Redesign)
1. **Bubbles move live during typing** - As title grows character-by-character, bubbles below smoothly move down
2. **No scroll jumping** - User can scroll freely during animation without position jumping
3. **Consistent vertical spacing** - Vertical gaps always equal horizontal gaps (0.75rem)
4. **No overlaps** - Bubbles never overlap, spacing is always correct
5. **Smooth performance** - No jittering, smooth 60fps experience
6. **Works during hover** - Hovering over bubbles doesn't cause jumping

## Implementation Strategy (UPDATED)
1. **CRITICAL: Add testing infrastructure FIRST** - Cannot debug without automated tests
   - Create test HTML file that automatically runs typing animation
   - Measure bubble positions before/during/after animation
   - Detect when bubbles move incorrectly (jump up, repack)
   - Measure scroll position changes
   - Output test results to console/file

2. **Debug with tests** - Use test results to identify exact failure points
   - Which bubbles move when they shouldn't?
   - When exactly does repacking occur?
   - What triggers scroll jumps?

3. **Consider alternative approaches** - Current Grid-based approach may be fundamentally flawed
   - Absolute positioning with JavaScript?
   - Flexbox with manual positioning?
   - Canvas-based layout?
   - Different Grid strategy (subgrid, explicit tracks)?

4. **Clean implementation** - Once root cause identified, implement clean solution
5. **Test thoroughly** - Use automated tests to verify fix

## Technical Constraints
- Must work on mobile (375px), tablet (768px), and desktop (≥1440px)
- Must maintain responsive column count (1/2/3 columns)
- Must preserve existing visual design (bubble styling, colors, etc.)
- Must work with existing Markdown parsing and entry loading system
