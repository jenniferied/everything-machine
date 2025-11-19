# Quick Start Guide

## Getting Started

### 1. Run a Local Server
Since the project uses ES6 modules, you need to run it on a local server:

```bash
# Option 1: Python
python -m http.server 8000

# Option 2: Node.js
npx serve

# Option 3: PHP
php -S localhost:8000
```

Then open `http://localhost:8000` in your browser.

### 2. View the Homepage
The homepage now includes:
- ✅ **Floating animations** on placeholder images (Anime.js)
- ✅ **3D viewer** for Kepler model (Three.js, with WebGL detection)
- ✅ **Point cloud viewer** (Potree placeholder, WebGL2 detection)
- ✅ **AI Attribution footer** (expandable details)
- ✅ **Lazy loading** for all images
- ✅ **Enhanced gallery** with touch gestures

## What Happens on Load

1. **Feature Detection** runs first
   - Checks WebGL, WebGL2 support
   - Detects performance tier (low/medium/high)
   - Checks network speed
   - Respects "reduced motion" preference

2. **Progressive Enhancement**
   - If WebGL is supported → 3D viewer loads
   - If not → Static placeholder image shown
   - Same pattern for all features

3. **Lazy Loading**
   - Images load as you scroll
   - Viewers initialize when visible
   - External libraries load only when needed

## Feature Breakdown

### Floating Animations
- **Where**: Overview page placeholder images
- **Tech**: Anime.js (auto-loads if motion allowed)
- **Fallback**: CSS animations
- **Control**: Respects `prefers-reduced-motion`

### 3D Viewer
- **Where**: Overview page, "Kepler in 3D" section
- **Tech**: Three.js (placeholder cube for now)
- **Controls**: 
  - Mouse: Click + drag to rotate
  - Touch: Swipe to rotate
  - Auto-rotates by default
- **Fallback**: Static image

### Point Cloud Viewer
- **Where**: Overview page, "Point Cloud Exploration" section
- **Tech**: Potree (placeholder for now)
- **Requirements**: WebGL2 + medium+ performance
- **Fallback**: Screenshot

### AI Attribution
- **Where**: Footer of every page
- **Features**:
  - Click badge to expand details
  - Shows all AI models used
  - Lists tools and workflow
- **Accessibility**: Keyboard navigable

## Browser Console

Open DevTools Console to see:
```
[App] Initializing application...
[App] Core services initialized
[App] Capabilities detected: { webgl: true, webgl2: true, performanceTier: 'high', ... }
[App] Controllers initialized
[App] 2 viewers configured
[App] Floating animation setup for 4 elements
[App] Animations started
[App] Application initialized successfully
```

## Customization

### Add Your Own 3D Model
In `js/app.js`, update the 3D viewer configuration:
```javascript
const threeDViewer = new ThreeDViewer(
  threeDContainer,
  {
    modelPath: 'path/to/your/model.glb', // Add your model path
    autoRotate: true,
    cameraDistance: 5
  },
  // ...
);
```

### Modify Floating Animation
In `js/app.js`, adjust animation parameters:
```javascript
const floatingAnimation = new FloatingAnimation(
  floatingElements,
  {
    duration: 3000,    // Animation duration (ms)
    distance: 15,      // Float distance (px)
    rotation: 3,       // Rotation amount (degrees)
    useAnimeJs: true
  },
  this.scriptLoader
);
```

### Customize AI Attribution
In `js/app.js`, modify the AI attribution:
```javascript
const aiAttribution = new AIAttribution(
  footerContainer,
  {
    badge: 'Built with Your AI',
    models: [
      {
        name: 'Your Model',
        provider: 'Provider Name',
        usage: 'What it was used for'
      }
    ],
    tools: [
      { name: 'Tool 1', description: 'Description' }
    ],
    workflow: 'Your workflow description'
  },
  this.eventBus
);
```

## Debugging

### Check Capabilities
In browser console:
```javascript
window.everythingMachineApp.capabilities
```

### Get Application Status
```javascript
window.everythingMachineApp.getStatus()
```

### View Animation Stats
```javascript
window.everythingMachineApp.animationController.getStats()
```

### View Lazy Loading Stats
```javascript
window.everythingMachineApp.lazyLoader.getStats()
```

## Mobile Testing

### iOS Safari
1. Enable Web Inspector in Settings
2. Connect device to Mac
3. Use Safari Developer Tools

### Android Chrome
1. Enable USB Debugging
2. Connect device
3. Use Chrome DevTools remote debugging

### Responsive Design Mode
- Chrome: Cmd/Ctrl + Shift + M
- Firefox: Cmd/Ctrl + Shift + M
- Safari: Develop menu → Enter Responsive Design Mode

## Performance Testing

### Test with Slow Network
1. Open DevTools
2. Network tab → Throttling → Slow 3G
3. Reload page
4. Observe: Lazy loading adapts, lower quality assets

### Test Reduced Motion
1. Enable reduced motion in OS:
   - macOS: System Preferences → Accessibility → Display → Reduce Motion
   - Windows: Settings → Ease of Access → Display → Show animations
2. Reload page
3. Observe: Animations disabled

### Test Low Performance
1. DevTools → Performance tab → CPU throttling → 6x slowdown
2. Observe: Animations auto-throttle to 30fps

## Troubleshooting

### Images Not Loading
- Check browser console for errors
- Verify image paths in `assets/images/`
- Ensure local server is running

### 3D Viewer Not Appearing
- Check console: "WebGL not supported" → Device doesn't support WebGL
- Should show fallback image automatically

### Animations Not Working
- Check console: "Reduced motion enabled" → User preference
- Check console: "Slow network" → Animations disabled for performance

### Module Errors
- Ensure you're using a local server (not `file://`)
- Check that all `.js` files are in the correct paths

## Next Steps

1. ✅ Test in different browsers
2. ✅ Test on mobile devices
3. ✅ Add your own 3D model (replace placeholder)
4. ✅ Add your own point cloud data
5. ✅ Customize AI attribution with your details
6. ✅ Add videos to test Video.js integration

## Need Help?

See `IMPLEMENTATION.md` for detailed architecture documentation.

