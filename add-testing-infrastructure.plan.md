# Add Testing Infrastructure for Layout Debugging

## Goal
Create automated test infrastructure to debug layout issues during typing animation. Test file should automatically detect when bubbles move incorrectly or scroll position jumps.

## Test File: `testing/test-layout.html`

### Features
1. **Auto-load page** - Loads `index.html` directly (same origin)
2. **Auto-navigate** - Automatically navigates to logbook page
3. **Wait for load** - Waits for journal entries to load
4. **Measure initial state** - Records all bubble positions before animation
5. **Trigger animation** - Automatically starts typing animation (or waits for it)
6. **Monitor during animation** - Measures positions at intervals (every 100ms or after layout updates)
7. **Measure final state** - Records positions after animation completes
8. **Detect issues** - Compares positions to detect:
   - Bubbles moving UP when they should stay fixed
   - Bubbles not moving DOWN when title grows
   - Scroll position jumps
   - Repacking (bubbles changing columns)
9. **Output results** - Console logs with colors + optional JSON file with test results

### Implementation Details

#### Test Structure
```javascript
class LayoutTest {
  constructor() {
    this.results = {
      baseline: null,
      duringAnimation: [],
      final: null,
      issues: []
    };
    this.baselinePositions = new Map();
  }
  
  async run() {
    // 1. Wait for page load
    // 2. Navigate to logbook
    // 3. Wait for entries loaded
    // 4. Measure baseline positions
    // 5. Wait for animation to start (or trigger it)
    // 6. Monitor during animation
    // 7. Measure final state
    // 8. Analyze results
    // 9. Output results
  }
  
  measureBubblePositions() {
    // Get all .content-bubble elements
    // Measure getBoundingClientRect() for each
    // Also get computed grid-row-start, grid-row-end
    // Return array of positions
  }
  
  detectIssues(currentPositions, previousPositions) {
    // Compare positions
    // Detect bubbles moving up
    // Detect bubbles not moving down when they should
    // Detect scroll jumps
    // Return array of issues
  }
}
```

#### Position Measurement
- Use `getBoundingClientRect()` for each bubble
- Store: `top`, `left`, `width`, `height`
- Also store: `grid-row-start`, `grid-row-end` (computed styles)
- Store scroll position: `scrollTop` of `.logbook-main`
- Store bubble index and identify by content or DOM order

#### Issue Detection Rules
- **Bubble moved up**: `currentTop < baselineTop - threshold` (5px threshold)
- **Bubble should move down but didn't**: Title bubble grew but bubble below didn't move down
- **Scroll jumped**: `|currentScroll - baselineScroll| > threshold` (10px threshold)
- **Repacking**: Bubble changed column (left position changed by >50px)
- **Bubble in wrong column**: Left position doesn't match expected column

#### Output Format
```json
{
  "testRun": "2025-01-XX...",
  "baseline": {
    "bubbles": [
      {
        "index": 0,
        "top": 100,
        "left": 20,
        "width": 300,
        "height": 150,
        "gridRowStart": "1",
        "gridRowEnd": "span 50"
      }
    ],
    "scroll": 0,
    "titleBubbleHeight": 100
  },
  "duringAnimation": [
    {
      "timestamp": 1234,
      "characterIndex": 5,
      "bubbles": [...],
      "scroll": 0,
      "issues": [
        {
          "type": "bubble_moved_up",
          "bubbleIndex": 2,
          "deltaY": -15,
          "message": "Bubble 2 moved up 15px"
        }
      ]
    }
  ],
  "final": {
    "bubbles": [...],
    "scroll": 0,
    "issues": [...]
  },
  "summary": {
    "totalIssues": 3,
    "bubblesMovedUp": 2,
    "scrollJumps": 1,
    "repackingDetected": false
  }
}
```

## Implementation Steps

1. **Create `testing/test-layout.html`**
   - Standalone HTML file that loads in same window
   - Includes test script inline
   - Can be opened directly in browser

2. **Implement test runner**
   - Wait for DOM ready
   - Wait for journal entries loaded (check for `.content-grid` with bubbles)
   - Measure baseline positions

3. **Hook into typing animation**
   - Option A: Wait for animation to start naturally (observe DOM)
   - Option B: Monkey-patch `displayEntry()` to add test hooks
   - Option C: Use MutationObserver to detect title text changes
   - Best: Use MutationObserver on `.journal-title-text` to detect character additions

4. **Implement monitoring**
   - Use `requestAnimationFrame` loop during animation
   - Measure positions every 100ms or after each detected character
   - Compare with baseline and previous measurement
   - Store results

5. **Implement issue detection**
   - Compare current positions with baseline
   - Detect unexpected movements (up when should stay, not down when should move)
   - Track scroll changes
   - Detect column changes (repacking)

6. **Output results**
   - Console.log with colors (green for pass, red for issues)
   - Visual summary in test page (table or list)
   - Optional: Download JSON file button

## Files to Create
- `testing/test-layout.html` - Main test file (standalone, can be opened in browser)

## Files to Modify (Optional - only if needed)
- `scripts.js` - Add test hooks (only if MutationObserver approach doesn't work)

## Expected Outcome
- Test file that can be opened in browser (`file://` or via local server)
- Automatically detects when typing animation starts
- Monitors layout during animation
- Outputs detailed test results showing:
  - Which bubbles moved incorrectly
  - When they moved (character index or timestamp)
  - Scroll position changes
  - Summary of all issues
- Results visible in console and on page

## Usage
1. Open `testing/test-layout.html` in browser (or serve via local server)
2. Test runs automatically when page loads
3. Check console for detailed results
4. Check page for visual summary
5. Optional: Click button to download JSON results

## Test Scenarios to Cover
1. **Basic typing animation** - Title grows, bubbles below should move down
2. **Scroll during animation** - User scrolls, no jumps should occur
3. **Animation end** - No jump when animation completes
4. **Multi-column layout** - Bubbles in right columns should stay fixed
5. **Hover during animation** - Hovering shouldn't cause jumps

## Success Criteria
- Test file runs without errors
- Test detects when bubbles move incorrectly
- Test detects scroll jumps
- Test output is clear and actionable
- Test can be run multiple times for comparison

