# Player Play-State Preservation Problem

## Problembeschreibung

Der Audio-Player spielt automatisch ab, wenn der Song gewechselt wird (Forward/Backward), obwohl der vorherige Song pausiert war. Der Play/Pause-Status wird nicht korrekt erhalten.

## Erwartetes Verhalten

1. **Wenn Song pausiert ist und Forward/Backward gedrückt wird:**
   - Neuer Song wird geladen
   - Song bleibt **pausiert** (spielt NICHT automatisch)
   - Zeit wird auf 0:00 zurückgesetzt
   - Button zeigt "Play" (nicht "Pause")

2. **Wenn Song spielt und Forward/Backward gedrückt wird:**
   - Neuer Song wird geladen
   - Song spielt **automatisch weiter**
   - Zeit wird auf 0:00 zurückgesetzt
   - Button zeigt "Pause" (nicht "Play")

3. **Wenn Song endet (ended Event):**
   - Nächster Song wird geladen
   - Song spielt **automatisch weiter** (weil vorheriger Song spielte)

4. **Beim Klick auf Playlist-Item:**
   - Song wird geladen
   - Song spielt **automatisch** (erwartetes Verhalten)

## Aktuelles Verhalten (BUG)

- Song wird automatisch abgespielt, auch wenn vorheriger Song pausiert war
- Play-State wird nicht erhalten

## Relevante Code-Stellen

### 1. State-Variablen

```javascript
let currentTrackIndex = 0;
let isPlaying = false; // Globale Variable für Play-Status
```

### 2. Play/Pause Funktionen

```javascript
// Funktion zum Abspielen
function playTrack() {
    audioPlayer.play();
    playPauseButton.classList.add('playing');
    changeMarqueeSpeed(7);
    isPlaying = true;
}

// Funktion zum Pausieren
function pauseTrack() {
    audioPlayer.pause();
    playPauseButton.classList.remove('playing');
    changeMarqueeSpeed(40);
    isPlaying = false;
}
```

### 3. loadTrack() Funktion (HAUPTPROBLEM)

```javascript
function loadTrack(index, preservePlayState = true) {
    currentTrackIndex = index;
    const track = playlist[index];
    
    // WICHTIG: Speichere Play-Status BEVOR wir irgendetwas ändern
    const wasPlaying = !audioPlayer.paused;
    
    // Bestimme ob Track spielen soll
    const shouldPlay = preservePlayState ? wasPlaying : true;
    
    // Pausiere aktuellen Track, bevor wir wechseln
    audioPlayer.pause();
    
    // Lade neuen Track
    audioPlayer.src = track.src;
    audioPlayer.load();
    
    // Zeit auf 0:00 zurücksetzen
    audioPlayer.currentTime = 0;
    
    // Stelle sicher, dass Audio pausiert ist (falls load() es geändert hat)
    if (!shouldPlay) {
        audioPlayer.pause();
    }

    // ... weitere Updates (Marquee, Cover, etc.)
    
    // Update isPlaying Variable
    isPlaying = shouldPlay;
    
    // Update Button-Status
    if (shouldPlay) {
        playPauseButton.classList.add('playing');
    } else {
        playPauseButton.classList.remove('playing');
    }
    
    // Wenn Track spielen soll, starte Playback
    if (shouldPlay) {
        audioPlayer.play().catch(err => {
            // Error handling
        });
    } else {
        // Stelle sicher, dass es pausiert bleibt
        audioPlayer.pause();
    }
}
```

### 4. Forward/Backward Funktionen

```javascript
// Vorherigen Track abspielen
function playPreviousTrack() {
    const wasPlaying = !audioPlayer.paused;
    currentTrackIndex = (currentTrackIndex - 1 + playlist.length) % playlist.length;
    loadTrack(currentTrackIndex, true); // preservePlayState = true
}

// Nächsten Track abspielen
function playNextTrack(autoPlay = false) {
    currentTrackIndex = (currentTrackIndex + 1) % playlist.length;
    loadTrack(currentTrackIndex, !autoPlay); // preservePlayState = !autoPlay
}
```

### 5. Event Listeners

```javascript
audioPlayer.addEventListener('ended', () => playNextTrack(true)); // autoPlay = true
audioPlayer.addEventListener('play', () => {
    isPlaying = true;
    playPauseButton.classList.add('playing');
    changeMarqueeSpeed(7);
});
audioPlayer.addEventListener('pause', () => {
    isPlaying = false;
    playPauseButton.classList.remove('playing');
    changeMarqueeSpeed(40);
});
```

### 6. Alle loadTrack() Aufrufe

- `playPreviousTrack()` → `loadTrack(index, true)` - State erhalten
- `playNextTrack(false)` → `loadTrack(index, true)` - State erhalten
- `playNextTrack(true)` → `loadTrack(index, false)` - Immer spielen
- Playlist-Item Klick → `loadTrack(index, false)` - Immer spielen
- Initial Load → `loadTrack(0, true)` - State erhalten (sollte pausiert sein)

## Mögliche Ursachen

1. **Timing-Problem**: `audioPlayer.load()` könnte den Player in einen State versetzen, der automatisch spielt
2. **Event-Konflikt**: `play` Event könnte durch `load()` oder `currentTime = 0` ausgelöst werden
3. **Asynchrones Verhalten**: `audioPlayer.play()` könnte asynchron sein und trotz `pause()` danach ausgeführt werden
4. **Browser-Auto-Play**: Browser könnte Auto-Play-Verhalten haben
5. **State-Synchronisation**: `isPlaying` Variable und `audioPlayer.paused` könnten nicht synchron sein

## Bekannte Browser-Verhalten

- `audioPlayer.load()` kann den Player in einen "ready" State versetzen
- `audioPlayer.currentTime = 0` kann Events auslösen
- `audioPlayer.play()` ist asynchron und gibt ein Promise zurück
- Manche Browser haben Auto-Play-Policies, die Play verhindern können

## Debugging-Strategie

1. **State-Tracking**: Logge alle State-Änderungen
2. **Event-Monitoring**: Überwache alle Audio-Events (play, pause, loadstart, etc.)
3. **Timing-Analyse**: Prüfe, ob Events in falscher Reihenfolge feuern
4. **Explicit State Management**: Verwende einen zentralen State-Manager statt mehrere Quellen

## Mögliche Lösungsansätze

1. **State vor load() speichern und nach load() explizit wiederherstellen**
2. **Event-Listener temporär entfernen während load()**
3. **Promise-basiertes State-Management** für asynchrone Operationen
4. **Zentraler State-Manager** statt mehrerer State-Quellen
5. **Debouncing/Throttling** für State-Änderungen
6. **Explicit pause() nach jedem load() und dann conditional play()**

## Technische Details

- **Audio-Element**: `<audio id="audio-player" src="" preload="metadata"></audio>`
- **Playlist**: Array von Track-Objekten mit `src`, `cover`, `spotifyID`, etc.
- **Player-Buttons**: Previous, Play/Pause, Next, Playlist-Toggle
- **Animation**: Marquee scrollt mit unterschiedlicher Geschwindigkeit je nach Play-Status

## Zusätzliche Anforderungen

- Zeit wird auf 0:00 zurückgesetzt beim Track-Wechsel ✓ (funktioniert)
- Marquee-Animation passt Geschwindigkeit an Play-Status an ✓ (funktioniert)
- Button-Status wird aktualisiert ✓ (funktioniert)
- Play-State wird NICHT erhalten ✗ (BUG)

