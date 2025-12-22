# Everything Machine - Testing Checklist

## Pre-Test Setup

1. Start local web server (required for ES6 modules and fetch)
   ```bash
   python3 -m http.server 8001
   # or
   npx http-server -p 8001
   ```

2. Open in browser: `http://localhost:8001`

3. Open browser DevTools:
   - **Console tab**: Check for errors
   - **Network tab**: Check for failed requests
   - **Sources tab**: Verify modules loaded

4. Check debug logs:
   - EventBus debug mode auto-enabled on localhost
   - Look for `[ComponentName]` prefixed log messages

## Audio System (Music Player)

### Playlist Functionality
- [ ] **Playlist dropdown opens** when clicking list icon
- [ ] **All 3 tracks visible** in dropdown with correct metadata
- [ ] **Album covers displayed** in dropdown
- [ ] **Track durations shown** (not "..." or "Fehler")
- [ ] **Active track highlighted** in playlist

### Playback Controls
- [ ] **Play/pause button toggles** correctly
- [ ] **Play icon changes to pause icon** when playing
- [ ] **Previous button** goes to previous track
- [ ] **Next button** goes to next track
- [ ] **Track auto-advances** when current track ends

### UI Updates
- [ ] **Marquee shows track info** (Artist - Title (Album, Year))
- [ ] **Marquee animates slowly** when paused
- [ ] **Marquee animates quickly** when playing
- [ ] **Marquee speed transition is smooth** (no jumping)
- [ ] **Album cover displays** for current track
- [ ] **Album cover clickable** (opens Spotify for valid IDs)
- [ ] **Time display updates** in format "0:32/3:45"
- [ ] **Time display shows "0:00/..." initially** then updates

### Integration
- [ ] **Playlist dropdown closes** when clicking outside
- [ ] **Playlist dropdown closes** when opening main navigation dropdown
- [ ] **Music continues playing** when navigating between pages

### Console Checks
- [ ] No errors in console
- [ ] See `[MusicPlayer] Initialized successfully`
- [ ] See `playback:play`, `playback:pause` events in debug mode

## Navigation System

### Page Switching
- [ ] **Overview page loads** by default
- [ ] **Clicking "Projektübersicht"** shows overview page
- [ ] **Clicking "Prozess-Logbuch"** shows logbook page
- [ ] **Clicking "Künstler-Dialoge"** shows dialogues page
- [ ] **Only one page visible** at a time
- [ ] **Active menu item highlighted** in dropdown

### Dropdown Behavior
- [ ] **Main dropdown opens** when clicking "Inhalt"
- [ ] **Main dropdown closes** when clicking outside
- [ ] **Main dropdown closes** when opening playlist dropdown
- [ ] **Dropdown items clickable**

### State Persistence
- [ ] **Page selection persists** on refresh (localStorage)
- [ ] **Correct page shown** after refresh

### Console Checks
- [ ] See `[PageNavigator] Initialized`
- [ ] See `[PageNavigator] Navigated to: [pageId]`
- [ ] See `nav:pageChanged` events in debug mode

## Journal System

### Loading
- [ ] **Journal loads** when navigating to "Prozess-Logbuch"
- [ ] **Loading message shown** initially
- [ ] **Timeline appears** with all journal entries
- [ ] **Most recent entry displayed** by default

### Timeline
- [ ] **Timeline items show date** (e.g., "19. Nov 2025")
- [ ] **Timeline items show title**
- [ ] **Active entry highlighted** in timeline
- [ ] **Clicking timeline item** switches entry
- [ ] **Timeline scrolls** to active item horizontally

### Entry Display
- [ ] **Title animates** with typing effect
- [ ] **Blinking caret appears** after typing completes
- [ ] **Content bubbles visible** with proper spacing
- [ ] **Headings render correctly** (different sizes for h1/h2/h3)
- [ ] **Images display** in entries
- [ ] **Markdown formatting works** (bold, italic, links)
- [ ] **World-info dropdowns present** (if applicable)
- [ ] **World-info dropdowns expand** when clicked

### Images & Lightbox
- [ ] **Images clickable** in journal entries
- [ ] **Lightbox opens** when clicking image
- [ ] **Image displays** in lightbox
- [ ] **Navigation arrows visible** (if multiple images in bubble)
- [ ] **Prev/next buttons work** in lightbox
- [ ] **Keyboard navigation works** (arrows, ESC)
- [ ] **Counter shows** "2 / 5" (if multiple images)
- [ ] **Caption displays** (if image has alt text)
- [ ] **Lightbox closes** with ESC or X button

### Layout & Responsiveness
- [ ] **Grid layout adapts** to content height
- [ ] **No overlapping bubbles**
- [ ] **Layout updates** during title typing animation
- [ ] **Layout updates** after images load
- [ ] **Layout updates** on window resize

### Console Checks
- [ ] See `[JournalManager] Loaded X entries`
- [ ] See `[TimelineRenderer] Rendered X timeline items`
- [ ] See `[EntryRenderer] Entry rendered`
- [ ] No fetch errors for journal files

## Cross-Feature Integration

### Music + Navigation
- [ ] **Music continues** when switching pages
- [ ] **Marquee keeps animating** on all pages
- [ ] **Playlist state maintained** when navigating

### Journal + Images
- [ ] **Each bubble has its own gallery**
- [ ] **Gallery doesn't mix images** from different bubbles
- [ ] **Image click doesn't trigger** page navigation

### Dropdowns
- [ ] **Only one dropdown open** at a time
- [ ] **Opening playlist closes** main dropdown
- [ ] **Opening main dropdown closes** playlist
- [ ] **Clicking page closes** both dropdowns

## Performance

### Loading Speed
- [ ] **Initial page load < 2 seconds**
- [ ] **Journal loads < 3 seconds**
- [ ] **Images lazy-load** (check Network tab)
- [ ] **No janky animations** (marquee, typing, grid layout)

### Memory
- [ ] **No memory leaks** (check Performance tab)
- [ ] **EventBus listeners cleaned up** (check in debug logs)
- [ ] **Dispose methods called** when switching pages

## Browser Compatibility

### Desktop Browsers
- [ ] **Chrome** - Full functionality
- [ ] **Firefox** - Full functionality
- [ ] **Safari** - Full functionality
- [ ] **Edge** - Full functionality

### Mobile (if available)
- [ ] **iOS Safari** - Touch gestures, responsive layout
- [ ] **Android Chrome** - Performance on mid-range device

## Accessibility

### Keyboard Navigation
- [ ] **Tab** navigates through interactive elements
- [ ] **Enter/Space** activates buttons
- [ ] **Arrow keys** navigate lightbox
- [ ] **ESC** closes lightbox and dropdowns

### Screen Reader (if available)
- [ ] **Buttons have labels**
- [ ] **Images have alt text**
- [ ] **Page structure makes sense**

## Error Handling

### Network Errors
- [ ] **Journal shows error message** if manifest fails
- [ ] **Music player handles** missing audio files
- [ ] **Images show fallback** on load error

### Edge Cases
- [ ] **Empty playlist doesn't crash**
- [ ] **Missing journal entries handled gracefully**
- [ ] **Invalid localStorage data handled**

## Regression Testing (After Changes)

When making changes to a specific system:

### After Audio Changes
- [ ] Run **Audio System tests** above
- [ ] Verify **Cross-Feature Integration** (music + navigation)

### After Navigation Changes
- [ ] Run **Navigation System tests** above
- [ ] Verify **Cross-Feature Integration** (all dropdowns)

### After Journal Changes
- [ ] Run **Journal System tests** above
- [ ] Verify **Images & Lightbox** functionality
- [ ] Verify **Layout & Responsiveness**

## Debug Checklist

If something doesn't work:

1. **Check Console** for error messages
2. **Check Network tab** for failed requests (404, 500)
3. **Check EventBus logs** (`eventBus.setDebugMode(true)`)
4. **Check module load errors** in Sources tab
5. **Verify DOM elements exist** (right IDs and classes)
6. **Check localStorage** in Application tab
7. **Clear cache** and hard refresh (Cmd/Ctrl + Shift + R)

## Test Pass Criteria

All checkboxes must be checked for a passing test. If any fail:

1. **Document the failure** (screenshot + console errors)
2. **Create issue** or note in IMPLEMENTATION.md
3. **Fix the issue**
4. **Re-test**
5. **Only commit when all tests pass**

## Commit Message Template

```
[System] Brief description

- Detailed change 1
- Detailed change 2

Tested: [List what you tested]
- Audio: Play/pause, track switching, marquee animation
- Navigation: Page switching, dropdown behavior
- Journal: Entry loading, timeline, image lightbox
- Integration: Music + navigation, dropdowns

All tests passing ✓
```

