# Testing Instructions for Layout Fixes

## Quick Test (Manual)

### Step 1: Open the Page
1. Start a local server (required for loading journal files):
   ```bash
   # Option 1: Python
   python3 -m http.server 8000
   
   # Option 2: Node.js
   npx http-server -p 8000
   
   # Option 3: PHP
   php -S localhost:8000
   ```

2. Open in browser: `http://localhost:8000/index.html`

### Step 2: Navigate to Logbook
1. Click "Inhalt" dropdown
2. Select "Prozess-Logbuch"
3. Wait for page to load and animation to start

### Step 3: Observe the Animation
Watch for these behaviors:

#### ✅ GOOD SIGNS (What you SHOULD see):
- Title types out character by character
- Title bubble grows smoothly
- Bubbles below the title move DOWN gradually
- Bubbles in right column(s) stay FIXED (don't move)
- No sudden jumps or repositioning
- Smooth, continuous movement
- No scroll position jumping
- Layout updates happen every few characters (subtle)

#### ❌ BAD SIGNS (What you should NOT see):
- Bubbles jumping UP suddenly
- Bubbles changing columns (repacking)
- Scroll position jumping/resetting
- Jittery or stuttering movement
- Bubbles overlapping
- Large gaps appearing/disappearing
- Final "jump" when animation completes

### Step 4: Test Different Scenarios
1. **Scroll during animation**: Scroll up/down while typing happens - should not jump
2. **Hover during animation**: Hover over bubbles - should not cause jumping
3. **Different entries**: Select different timeline entries - all should behave consistently
4. **Window resize**: Resize browser window - layout should adjust smoothly

## Automated Test

### Step 1: Open Test File
1. Make sure local server is running (same as above)
2. Open in browser: `http://localhost:8000/test-layout.html`

### Step 2: Wait for Test to Complete
- Test runs automatically
- Status shows "Running..." then "Test complete!"
- Takes about 10-30 seconds depending on title length

### Step 3: Review Results

#### In the Test Page:
- **Summary Table**: Shows counts of issues detected
- **Issues List**: Detailed description of each problem found
- **Log Output**: Timestamped events during test

#### Expected Results:
```
Total Issues: 0
Bubbles Moved Up: 0
Scroll Jumps: 0
Repacking Detected: No
Bubbles Not Moving Down: 0
```

#### If Issues Found:
- Download JSON results (click button)
- Check console for detailed logs
- Share results for further debugging

### Step 4: Interpret Test Results

#### Issue Types:

**bubble_moved_up**
- Bubble moved UP when it should stay fixed
- Usually indicates repacking or layout conflict
- Should be 0

**scroll_jump**
- Scroll position changed unexpectedly
- Should be 0

**repacking**
- Bubble changed columns (left position changed)
- Should be 0

**bubble_not_moving_down**
- Bubble below title didn't move down when title grew
- May indicate layout not updating
- Should be 0

## What to Report if Issues Persist

If you still see issues, please report:

1. **Browser**: Chrome, Firefox, Safari, etc. (version number)
2. **Screen size**: e.g., 1920x1080, 1440x900
3. **Which entry**: Which timeline entry shows the problem
4. **Specific issue**: Describe what you see (with screenshot if possible)
5. **Test results**: Download and share the JSON from automated test
6. **Console errors**: Open browser DevTools > Console, copy any errors

## Expected Timeline

If all fixes are working:
- ⏱️ **0s**: Page loads, bubbles appear
- ⏱️ **0.3s**: Typing animation starts
- ⏱️ **2-5s**: Title types out, bubbles move down smoothly
- ⏱️ **5s+**: Animation completes, final layout settles
- ⏱️ **5.3s+**: All movement stops, layout is stable

## Performance Benchmarks

On a modern browser (Chrome/Firefox):
- Animation should run at 60fps
- No dropped frames
- Smooth, continuous motion
- CPU usage < 20% during animation
- No memory leaks (check DevTools > Performance)

## Debugging Tips

### If Bubbles Still Jump:
1. Check console for warnings/errors
2. Run automated test to get metrics
3. Try different browser
4. Check if Grid layout is being applied (DevTools > Elements)

### If Scroll Still Jumps:
1. Check if scroll position is at top (0px)
2. Try scrolling down before animation starts
3. Check console for scroll events
4. Verify `overflow-anchor: none` is applied

### If Performance is Poor:
1. Check number of bubbles (should be 2-4)
2. Check image sizes (large images slow down layout)
3. Check CPU usage (DevTools > Performance)
4. Try in incognito mode (disable extensions)

## Contact/Feedback

If you encounter issues:
1. Run the automated test
2. Download JSON results
3. Take screenshots
4. Report with details above

