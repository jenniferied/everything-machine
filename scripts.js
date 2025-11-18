const pages = document.querySelectorAll('.page-content');
const dropdown = document.getElementById('dropdown-menu');
const dropdownItems = dropdown.querySelectorAll('.dropdown-item');
const toggleButton = document.getElementById('contents-toggle');

// --- Erweiterte Player & Playlist Logic ---

// SVG Icons für die Playlist (als Strings)
const iconSong = `<svg class="playlist-icon" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
    <path d="M6 13c0 1.105-1.12 2-2.5 2S1 14.105 1 13c0-1.104 1.12-2 2.5-2s2.5.896 2.5 2zm9-2c0 1.105-1.12 2-2.5 2s-2.5-.895-2.5-2 1.12-2 2.5-2 2.5.895 2.5 2z"/>
    <path fill-rule="evenodd" d="M14 11V2h1v9h-1zM6 3v10H5V3h1z"/>
    <path d="M5 2.905a1 1 0 0 1 .9-.995l8-.8a1 1 0 0 1 1.1.995V3h-1V2.11l-8 .8A1 1 0 0 1 5 2.905z"/>
</svg>`;
const iconAlbum = `<svg class="playlist-icon" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16">
    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
    <path d="M8 4a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM4 8a4 4 0 1 1 8 0 4 4 0 0 1-8 0z"/>
    <path d="M8 10a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/>
</svg>`;

// --- PLAYLIST: EINZIGE QUELLE FÜR ALLE AUDIO-DATEN ---
// Füge hier Songs hinzu - alles andere wird automatisch generiert!
const playlist = [
    {
        artist: "Kepler",
        title: "Deine Moves",
        album: "BLUE EDITION",
        year: "2023",
        src: "assets/audio/06_Deine_Moves_Master_Song.mp3",
        cover: "assets/images/06_Deine_Moves_Cover.png",
        spotifyID: "15LqPeE0iqNMV31haEobtl"
    },
    {
        artist: "Kepler",
        title: "Es tut mir Leid",
        album: "Es tut mir Leid (Single)",
        year: "2023",
        src: "assets/audio/kepler_preview_2.mp3",
        cover: "assets/images/10_Es_Tut_Mir_Leid_Cover.png",
        spotifyID: "YOUR_SONG_ID_2"
    },
    {
        artist: "Kepler",
        title: "Für mich",
        album: "Für mich (Single)",
        year: "2023",
        src: "assets/audio/kepler_preview_3.mp3",
        cover: "assets/images/10_Es_Tut_Mir_Leid_Cover.png", // Fallback, falls kein Cover vorhanden
        spotifyID: "YOUR_SONG_ID_3"
    }
    // Füge hier mehr Songs hinzu - nur diese Liste muss aktualisiert werden!
];
let currentTrackIndex = 0;
let isPlaying = false;

// Player-Elemente holen
const audioPlayer = document.getElementById('audio-player');
const playPauseButton = document.getElementById('play-pause-button');
const marqueeContent = document.getElementById('marquee-content');
const playlistToggleBtn = document.getElementById('playlist-toggle-btn');
const playlistDropdown = document.getElementById('playlist-dropdown');
const timeDisplay = document.getElementById('time-display');
const albumCover = document.getElementById('album-cover');

// --- NEUE FUNKTION: Zeitformatierung ---
// Formatiert Sekunden (z.B. 32.123) in "m:ss" (z.B. "0:32")
function formatTime(seconds) {
    if (isNaN(seconds) || seconds === Infinity) {
        return '...';
    }
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
}

// Funktion zum Abspielen
function playTrack() {
    audioPlayer.play();
    playPauseButton.classList.add('playing');
    if (marqueeContent) marqueeContent.style.animationPlayState = 'running';
    isPlaying = true;
}

// Funktion zum Pausieren
function pauseTrack() {
    audioPlayer.pause();
    playPauseButton.classList.remove('playing');
    if (marqueeContent) marqueeContent.style.animationPlayState = 'paused';
    isPlaying = false;
}

// Funktion zum Umschalten (Play/Pause)
function togglePlay() {
    if (isPlaying) {
        pauseTrack();
    } else {
        playTrack();
    }
}

// Funktion zum Aktualisieren des Marquee-Texts
function updateMarquee(track) {
    if (!marqueeContent) return;
    
    const newText = `${track.artist} - ${track.title} (${track.album}, ${track.year})`;
    const newLink = `https://open.spotify.com/track/${track.spotifyID || 'YOUR_ARTIST_ID'}`;
    
    // Marquee-Content dynamisch generieren (für Scroll-Effekt dupliziert)
    marqueeContent.innerHTML = `
        <a href="${newLink}" target="_blank" title="${track.artist} auf Spotify öffnen">${newText}</a>
        <span class="mx-4">|</span>
        <a href="${newLink}" target="_blank" title="${track.artist} auf Spotify öffnen">${newText}</a>
    `;
}

// Funktion zum Aktualisieren der Zeit-Anzeige
function updateTimeDisplay() {
    if (!timeDisplay || !audioPlayer) return;
    
    const currentTime = audioPlayer.currentTime || 0;
    const duration = audioPlayer.duration || 0;
    
    const currentTimeFormatted = formatTime(currentTime);
    const durationFormatted = formatTime(duration);
    
    timeDisplay.textContent = `${currentTimeFormatted}/${durationFormatted}`;
}

// Funktion zum Aktualisieren des Albumcovers
function updateAlbumCover(track) {
    if (!albumCover) return;
    
    if (track.cover) {
        albumCover.src = track.cover;
        albumCover.alt = `${track.album} Cover`;
        albumCover.style.display = 'block';
        // Fallback bei Fehler
        albumCover.onerror = function() {
            this.style.display = 'none';
        };
    } else {
        albumCover.style.display = 'none';
    }
}

// Funktion zum Laden eines Tracks
function loadTrack(index) {
    currentTrackIndex = index;
    const track = playlist[index];
    
    audioPlayer.src = track.src;
    audioPlayer.load();

    // Marquee-Text aktualisieren
    updateMarquee(track);
    
    // Albumcover aktualisieren
    updateAlbumCover(track);
    
    // Zeit-Anzeige zurücksetzen
    if (timeDisplay) {
        timeDisplay.textContent = '0:00/0:00';
    }

    // "Active" Status in der Playlist aktualisieren
    document.querySelectorAll('.playlist-item').forEach((item, i) => {
        if (i === index) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

// Nächsten Track abspielen (für 'ended' Event)
function playNextTrack() {
    currentTrackIndex = (currentTrackIndex + 1) % playlist.length; // Loop
    loadTrack(currentTrackIndex);
    playTrack();
}

// --- ANGEPASSTE FUNKTION: Playlist-Dropdown füllen ---
function populatePlaylist() {
    if (!playlistDropdown) return;
    let html = '';
    
    // 1. HTML-Struktur aufbauen (mit Album-Cover-Icon und Platzhaltern für die Dauer)
    playlist.forEach((song, index) => {
        html += `
            <button class="playlist-item" data-index="${index}">
                ${iconSong}
                <img src="${song.cover || 'assets/images/06_Deine_Moves_Cover.png'}" 
                     alt="${song.album}" 
                     class="album-cover-icon"
                     onerror="this.style.display='none'">
                <div class="song-details">
                    <span class="song-title">${song.title}</span>
                    <span class="album-info">
                        ${iconAlbum}
                        <span style="margin-left: 4px;">${song.album}</span>
                    </span>
                </div>
                <!-- Dauer-Span bekommt eine einzigartige ID -->
                <span class="duration" id="duration-${index}">...</span>
            </button>
        `;
    });
    playlistDropdown.innerHTML = html;

    // 2. Metadaten (Dauer) für jeden Song asynchron laden
    playlist.forEach((song, index) => {
        const tempAudio = new Audio(); // Temporäres Audio-Objekt
        tempAudio.src = song.src;
        
        // Event-Listener, der feuert, wenn die Metadaten geladen sind
        tempAudio.addEventListener('loadedmetadata', () => {
            const formattedTime = formatTime(tempAudio.duration);
            const durationSpan = document.getElementById(`duration-${index}`);
            if (durationSpan) {
                durationSpan.textContent = formattedTime;
            }
        });
        // Fehlerbehandlung (falls die Datei nicht gefunden wird)
        tempAudio.addEventListener('error', () => {
            const durationSpan = document.getElementById(`duration-${index}`);
            if (durationSpan) {
                durationSpan.textContent = 'Fehler';
            }
        });
    });

    // 3. Klick-Events für Playlist-Items hinzufügen (wie zuvor)
    playlistDropdown.querySelectorAll('.playlist-item').forEach(item => {
        item.addEventListener('click', () => {
            const index = parseInt(item.dataset.index, 10);
            loadTrack(index);
            playTrack();
            playlistDropdown.classList.remove('show'); // Dropdown schließen
            playlistToggleBtn.classList.remove('active');
        });
    });
}

// --- Event Listeners für den Player ---
if (playPauseButton) {
    playPauseButton.addEventListener('click', togglePlay);
    audioPlayer.addEventListener('ended', playNextTrack);
    audioPlayer.addEventListener('play', () => isPlaying = true);
    audioPlayer.addEventListener('pause', () => isPlaying = false);
    
    // Zeit-Anzeige aktualisieren
    audioPlayer.addEventListener('loadedmetadata', () => {
        updateTimeDisplay();
    });
    audioPlayer.addEventListener('timeupdate', () => {
        updateTimeDisplay();
    });
    audioPlayer.addEventListener('durationchange', () => {
        updateTimeDisplay();
    });
}

// Event Listener für Playlist-Dropdown
if (playlistToggleBtn) {
    playlistToggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        playlistDropdown.classList.toggle('show');
        playlistToggleBtn.classList.toggle('active');
        // Schließe das "Inhalt"-Dropdown, falls es offen ist
        dropdown.classList.remove('show');
    });
}
        
// --- Ende Player Logic ---


// Flag, um zu verfolgen, ob Journal-Einträge bereits geladen wurden
let journalEntriesLoaded = false;

function showPage(pageId, clickedElement) {
    // Alle Seiten ausblenden
    pages.forEach(page => {
        page.classList.remove('active');
    });
    // Ziel-Seite einblenden
    document.getElementById('page-' + pageId).classList.add('active');

    // "active" Status im Dropdown aktualisieren
    dropdownItems.forEach(item => {
        item.classList.remove('active');
    });
    if (clickedElement) {
        clickedElement.classList.add('active');
    }
    
    // "active" Status auf dem Haupt-Toggle-Button aktualisieren
    toggleButton.classList.add('active');

    // Dropdown schließen
    
    // Journal-Einträge laden, wenn Logbuch-Seite angezeigt wird
    if (pageId === 'logbook' && !journalEntriesLoaded) {
        loadJournalEntries();
        journalEntriesLoaded = true;
    }
    
    // Lightbox-Funktionalität für die aktuelle Seite initialisieren
    setTimeout(() => {
        initializeImageLightbox();
    }, 100);
    
    // Aktive Seite in localStorage speichern
    localStorage.setItem('activePage', pageId);
    
    dropdown.classList.remove('show');
}

// Logik zum Öffnen/Schließen des Dropdowns
toggleButton.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.classList.toggle('show');
    // Schließe das "Playlist"-Dropdown, falls es offen ist
    if (playlistDropdown) playlistDropdown.classList.remove('show');
    if (playlistToggleBtn) playlistToggleBtn.classList.remove('active');
});

// Logik zum Schließen der Dropdowns bei Klick daneben
window.addEventListener('click', (e) => {
    if (!toggleButton.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove('show');
    }
    if (playlistToggleBtn && !playlistToggleBtn.contains(e.target) && !playlistDropdown.contains(e.target)) {
        playlistDropdown.classList.remove('show');
        playlistToggleBtn.classList.remove('active');
    }
});

// --- JOURNAL-LOGBUCH SYSTEM ---

// Liste der Journal-Dateien (wird automatisch erweitert, wenn neue hinzugefügt werden)
const journalFiles = [
    'journal/journal-2025-11-15-comfyui-consistent-character.md',
    'journal/journal-2025-11-18-marble-worldlabs.md',
    'journal/journal-2025-11-19-cursor-build.md'
];

// Funktion zum Erstellen einer Welt-Info-Dropdown-Komponente
function createWorldInfoDropdown(worldData) {
    const id = `world-info-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const hasLink = worldData.link && worldData.link.trim() !== '';
    const hasVrLink = worldData.vrLink && worldData.vrLink.trim() !== '';
    
    return `
        <div class="world-info-container">
            ${hasLink || hasVrLink ? `
                <div class="world-info-links">
                    ${hasLink ? `
                        <a href="${worldData.link}" target="_blank" rel="noopener noreferrer" class="world-info-link">
                            Welt öffnen →
                        </a>
                    ` : ''}
                    ${hasVrLink ? `
                        <a href="${worldData.vrLink}" target="_blank" rel="noopener noreferrer" class="world-info-link world-info-link-vr">
                            VR-Modus öffnen →
                        </a>
                    ` : ''}
                </div>
            ` : ''}
            <div class="world-info-toggle" onclick="toggleWorldInfo('${id}')">
                <span class="world-info-toggle-title">${worldData.title || 'Welt-Info'}</span>
                <span class="world-info-toggle-icon">▼</span>
            </div>
            <div class="world-info-dropdown" id="${id}">
                <div class="world-info-details">
                    ${worldData.model ? `<p><strong>Model:</strong> ${worldData.model}</p>` : ''}
                    ${worldData.seed !== undefined ? `<p><strong>Seed:</strong> ${worldData.seed}</p>` : ''}
                    ${worldData.publicMode !== undefined ? `<p><strong>Public mode:</strong> ${worldData.publicMode ? 'Yes' : 'No'}</p>` : ''}
                </div>
                ${worldData.description ? `
                    <div class="world-info-description">
                        <strong>World Guide:</strong>
                        <p>${worldData.description}</p>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

// Funktion zum Toggle der Welt-Info-Dropdown
function toggleWorldInfo(id) {
    const dropdown = document.getElementById(id);
    const toggle = dropdown.previousElementSibling;
    if (dropdown && toggle) {
        dropdown.classList.toggle('show');
        toggle.classList.toggle('active');
    }
}

// Einfacher Markdown-Parser
function parseMarkdown(markdown, title = null, date = null, time = null) {
    let html = markdown;
    
    // Welt-Info-Dropdown-Komponenten verarbeiten (Format: [WORLD_INFO:...])
    // Syntax: [WORLD_INFO:title|model|seed|publicMode|previewImage|link|vrLink|description]
    // Die Beschreibung kommt am Ende, damit sie Pipes enthalten kann
    // WICHTIG: Diese müssen VOR der Abschnitts-Aufteilung verarbeitet werden
    const worldInfoPlaceholder = '___WORLD_INFO_PLACEHOLDER___';
    const worldInfoMap = new Map();
    let worldInfoCounter = 0;
    
    const worldInfoRegex = /\[WORLD_INFO:([^\]]+)\]/g;
    markdown = markdown.replace(worldInfoRegex, (match, data) => {
        // Teile die Daten auf
        const parts = data.split('|');
        const worldData = {
            title: parts[0] || '',
            model: parts[1] || '',
            seed: parts[2] || '',
            publicMode: parts[3] === 'true' || parts[3] === '1',
            previewImage: parts[4] || '',
            link: parts[5] || '',
            vrLink: parts[6] || '',
            description: parts.slice(7).join('|') || ''
        };
        const placeholder = `${worldInfoPlaceholder}${worldInfoCounter}${worldInfoPlaceholder}`;
        worldInfoMap.set(placeholder, createWorldInfoDropdown(worldData));
        worldInfoCounter++;
        return placeholder;
    });

    const restoreWorldInfoBlocks = (text) => {
        if (!text) return text;
        worldInfoMap.forEach((componentHTML, placeholder) => {
            if (text.includes(placeholder)) {
                text = text.split(placeholder).join(componentHTML);
            }
        });
        return text;
    };

    const convertMarkdownLinks = (text) => {
        if (!text) return text;
        return text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, label, rawUrl) => {
            let href = rawUrl.trim();
            if (!/^https?:\/\//i.test(href)) {
                href = `https://${href}`;
            }
            const safeLabel = label.trim();
            return `<a href="${href}" target="_blank" rel="noopener noreferrer" class="link-pill link-inline">${safeLabel}</a>`;
        });
    };

    const formatParagraphs = (paragraphs, useFullWidthImages = false) => {
        return paragraphs.map(para => {
            if (!para || !para.trim()) return '';
            let processed = para.trim();
            processed = restoreWorldInfoBlocks(processed);
            processed = processed.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            processed = processed.replace(/\*(.*?)\*/g, '<em>$1</em>');
            // Prüfen, ob der gesamte Absatz nur ein Bild ist (ohne weiteren Text)
            const imageOnlyMatch = processed.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
            if (imageOnlyMatch) {
                // Standalone Bild - immer als Full-Width rendern (mit Caption als <figure>)
                const caption = imageOnlyMatch[1] || '';
                processed = `<figure class="image-figure my-4">
                    <img src="${imageOnlyMatch[2]}" alt="${caption}" class="img-100 rounded-sm h-auto" />
                    ${caption ? `<figcaption class="image-caption">${caption}</figcaption>` : ''}
                </figure>`;
            } else {
                // Bilder innerhalb von Text - Bild-Klasse basierend auf Parameter
                const imageClass = useFullWidthImages ? 'img-100' : 'img-50';
                processed = processed.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, `<img src="$2" alt="$1" class="${imageClass} my-4 rounded-sm h-auto" />`);
            }
            processed = convertMarkdownLinks(processed);
            // Wenn der gesamte Absatz nur ein Bild ist, ohne <p> Tag rendern
            if (processed.match(/^<figure/)) {
                return processed;
            }
            return '<p class="mb-4">' + processed + '</p>';
        }).filter(Boolean).join('\n');
    };
    
    // Markdown in Abschnitte aufteilen (jede Überschrift wird ein Bubble)
    const lines = markdown.split('\n');
    const sections = [];
    let currentSection = { heading: null, headingLevel: null, content: [] };
    let currentParagraph = [];
    let hasSections = false;
    let introText = [];
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmed = line.trim();
        
        // Überschrift erkennen (#, ## oder ###) - alle Überschriften verarbeiten
        const headingMatch = trimmed.match(/^(#{1,3})\s+(.+)$/);
        if (headingMatch) { // Alle Überschriften (#, ##, ###)
            hasSections = true;
            // Aktuellen Abschnitt abschließen
            if (currentParagraph.length > 0) {
                if (currentSection.heading) {
                    currentSection.content.push(currentParagraph.join(' '));
                } else {
                    // Text vor der ersten Überschrift
                    introText.push(currentParagraph.join(' '));
                }
                currentParagraph = [];
            }
            if (currentSection.heading || currentSection.content.length > 0) {
                sections.push(currentSection);
            }
            
            // Neuen Abschnitt starten
            const headingLevel = headingMatch[1].length;
            // Überschrift-Text extrahieren - sicherstellen, dass kein # enthalten ist
            let headingText = headingMatch[2].trim();
            // Falls doch ein # am Anfang ist, entfernen
            headingText = headingText.replace(/^#+\s*/, '').trim();
            
            currentSection = {
                heading: headingText,
                headingLevel: headingLevel,
                content: []
            };
            continue;
        }
        
        // Falls eine Zeile mit # beginnt, aber nicht als Überschrift erkannt wurde, entferne das #
        // (Fallback für fehlerhafte Formatierung)
        if (trimmed.startsWith('#') && !trimmed.match(/^#{1,3}\s+/)) {
            // Zeile beginnt mit #, aber ist keine gültige Überschrift - entferne das #
            currentParagraph.push(trimmed.replace(/^#+\s*/, ''));
            continue;
        }
        
        // Leere Zeile - Absatz beenden
        if (trimmed === '') {
            if (currentParagraph.length > 0) {
                if (currentSection.heading) {
                    currentSection.content.push(currentParagraph.join(' '));
                } else {
                    introText.push(currentParagraph.join(' '));
                }
                currentParagraph = [];
            }
            continue;
        }
        
        // Normale Zeile zum Absatz hinzufügen
        currentParagraph.push(trimmed);
    }
    
    // Letzten Absatz und Abschnitt hinzufügen
    if (currentParagraph.length > 0) {
        if (currentSection.heading) {
            currentSection.content.push(currentParagraph.join(' '));
        } else {
            introText.push(currentParagraph.join(' '));
        }
    }
    if (currentSection.heading || currentSection.content.length > 0) {
        sections.push(currentSection);
    }
    
    // Wenn keine Überschriften gefunden wurden, Fallback zum alten Verhalten
    if (!hasSections || sections.length === 0) {
        // Zuerst Fettdruck und Kursiv behandeln
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Bilder behandeln - Standard 50% Breite
        html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" class="img-50 my-6 rounded-sm h-auto" />');

        // Markdown-Links verarbeiten
        html = convertMarkdownLinks(html);
        
        // Überschriften
        html = html.replace(/^### (.*$)/gim, '<h3 class="text-xl font-bold mt-6 mb-3 text-accent">$1</h3>');
        html = html.replace(/^## (.*$)/gim, '<h2 class="text-2xl font-bold mt-8 mb-4">$1</h2>');
        html = html.replace(/^# (.*$)/gim, '<h1 class="text-3xl font-bold mt-8 mb-4">$1</h1>');
        
        // Absätze
        const processedLines = html.split('\n');
        const finalLines = [];
        let para = [];
        
        for (const line of processedLines) {
            const trimmed = line.trim();
            if (trimmed === '') {
                if (para.length > 0) {
                    finalLines.push('<p class="mb-4">' + para.join(' ') + '</p>');
                    para = [];
                }
            } else if (trimmed.match(/^<h[1-6]/) || trimmed.match(/^<img/)) {
                if (para.length > 0) {
                    finalLines.push('<p class="mb-4">' + para.join(' ') + '</p>');
                    para = [];
                }
                finalLines.push(trimmed);
            } else {
                para.push(trimmed);
            }
        }
        if (para.length > 0) {
            finalLines.push('<p class="mb-4">' + para.join(' ') + '</p>');
        }
        html = finalLines.join('\n');
    } else {
        // Grid-Container mit Bubbles erstellen
        let gridHTML = '<div class="content-grid">';
        
        // Überschrift mit Datum/Zeit in der ersten Bubble
        let firstBubbleContent = '';
        if (title && date) {
            const dateStr = formatDate(date);
            const timeStr = time || '10:30';
            firstBubbleContent = `
                <div class="journal-header">
                    <h1 class="journal-title">${title}</h1>
                    <div class="journal-date-time">${dateStr} · ${timeStr}</div>
                </div>
            `;
        }
        
        // Intro-Text am Anfang anzeigen (falls vorhanden) - mit fullwidth Bildern
        if (introText.length > 0) {
            firstBubbleContent += formatParagraphs(introText, true);
        }

        let remainingSections = [...sections];
        let mergedSection = null;

        if (remainingSections.length > 0 && remainingSections[0].headingLevel === 1) {
            mergedSection = remainingSections.shift();
        } else if (introText.length === 0 && remainingSections.length > 0) {
            mergedSection = remainingSections.shift();
        }

        if (mergedSection) {
            firstBubbleContent += formatParagraphs(mergedSection.content);
        }
        
        // Erste Bubble mit Überschrift und/oder Intro-Text
        if (firstBubbleContent) {
            gridHTML += `
                <div class="content-bubble bubble-large">
                    <div class="bubble-content">
                        ${firstBubbleContent}
                    </div>
                </div>
            `;
        }
        
        remainingSections.forEach((section) => {
            // Inhalt formatieren
            let sectionContent = formatParagraphs(section.content);
            
            const headingClass = section.headingLevel === 2 ? 'text-2xl' : 'text-xl';
            const bubbleSize = section.headingLevel === 2 ? 'bubble-large' : 'bubble-medium';
            
            // Überschrift richtig escapen (aber nicht das "#" Zeichen)
            let headingText = section.heading || 'Abschnitt';
            // Entferne eventuelle "#" am Anfang
            headingText = headingText.replace(/^#+\s*/, '').trim();
            headingText = headingText.replace(/</g, '&lt;').replace(/>/g, '&gt;');
            
            gridHTML += `
                <div class="content-bubble ${bubbleSize}">
                    <h${section.headingLevel || 2} class="${headingClass} font-bold mb-4 text-accent bubble-section-title bubble-heading-level-${section.headingLevel || 2}">${headingText}</h${section.headingLevel || 2}>
                    <div class="bubble-content">
                        ${sectionContent}
                    </div>
                </div>
            `;
        });
        
        gridHTML += '</div>';
        html = gridHTML;
        
        // URL/Link-Verarbeitung NACH dem Grid-HTML (damit es die HTML-Struktur nicht zerstört)
        // Aber nur auf Text-Inhalt anwenden, nicht auf bereits verarbeitete HTML-Tags
        // Das wird später in der Funktion gemacht
    }
    
    // URLs in Links umwandeln (als Pills) - nach Absatz-Verarbeitung
    // Erkennt URLs in Text (http://, https://, www.), aber nicht in bereits existierenden Links
    // Wir müssen zuerst alle bereits existierenden Links markieren, dann URLs konvertieren, dann Markierungen entfernen
    const linkPlaceholder = '___LINK_PLACEHOLDER___';
    const linkMap = new Map();
    let linkCounter = 0;
    
    // Temporär alle existierenden Links, Bilder und WORLD_INFO Dropdowns ersetzen
    html = html.replace(/<a[^>]*>.*?<\/a>/gi, (match) => {
        const placeholder = `${linkPlaceholder}${linkCounter}${linkPlaceholder}`;
        linkMap.set(placeholder, match);
        linkCounter++;
        return placeholder;
    });
    html = html.replace(/<img[^>]*>/gi, (match) => {
        const placeholder = `${linkPlaceholder}${linkCounter}${linkPlaceholder}`;
        linkMap.set(placeholder, match);
        linkCounter++;
        return placeholder;
    });
    // WORLD_INFO Dropdowns schützen (multiline match)
    html = html.replace(/<div class="world-info-container">[\s\S]*?<\/div>/gi, (match) => {
        const placeholder = `${linkPlaceholder}${linkCounter}${linkPlaceholder}`;
        linkMap.set(placeholder, match);
        linkCounter++;
        return placeholder;
    });
    
    // URLs in Links umwandeln (als Pills)
    const urlRegex = /(https?:\/\/[^\s<>"{}|\\^`\[\]]+|www\.[^\s<>"{}|\\^`\[\]]+)/gi;
    html = html.replace(urlRegex, (url) => {
        const href = url.startsWith('http') ? url : `https://${url}`;
        const displayUrl = url.length > 50 ? url.substring(0, 47) + '...' : url;
        return `<a href="${href}" target="_blank" rel="noopener noreferrer" class="link-pill">${displayUrl}</a>`;
    });
    
    // Platzhalter wieder durch ursprüngliche Links ersetzen
    linkMap.forEach((originalLink, placeholder) => {
        html = html.replace(placeholder, originalLink);
    });
    
    return html;
}

// Datum aus Dateinamen extrahieren (Format: journal-YYYY-MM-DD-...)
function extractDate(filename) {
    const match = filename.match(/journal-(\d{4})-(\d{2})-(\d{2})/);
    if (match) {
        return new Date(parseInt(match[1]), parseInt(match[2]) - 1, parseInt(match[3]));
    }
    return new Date(0); // Fallback für ungültige Daten
}

// Datum formatieren (z.B. "15. Nov 2025")
function formatDate(date) {
    const months = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'];
    return `${date.getDate()}. ${months[date.getMonth()]} ${date.getFullYear()}`;
}

// Titel aus Markdown extrahieren (erste Zeile mit #)
function extractTitle(markdown) {
    const match = markdown.match(/^# (.+)$/m);
    return match ? match[1] : 'Unbenannter Eintrag';
}

// Globale Variable für alle geladenen Einträge
let allJournalEntries = [];
let currentEntryIndex = 0;

// Journal-Einträge laden und anzeigen
async function loadJournalEntries() {
    const container = document.getElementById('logbook-container');
    const timelineList = document.getElementById('timeline-list');
    
    if (!container || !timelineList) {
        console.error('Logbook-Container oder Timeline-Liste nicht gefunden');
        return;
    }
    
    // Loading-State anzeigen
    container.innerHTML = '<div class="logbook-entry"><p class="text-gray-400">Lade Journal-Einträge...</p></div>';
    timelineList.innerHTML = '';
    
    const entries = [];
    
    console.log('Lade Journal-Einträge:', journalFiles);
    
    // Alle Journal-Dateien laden
    for (const filename of journalFiles) {
        try {
            console.log(`Versuche ${filename} zu laden...`);
            const response = await fetch(filename);
            if (!response.ok) {
                console.warn(`Konnte ${filename} nicht laden: ${response.status} ${response.statusText}`);
                continue;
            }
            
            let markdown = await response.text();
            console.log(`${filename} erfolgreich geladen (${markdown.length} Zeichen)`);
            
            const date = extractDate(filename);
            const title = extractTitle(markdown);
            
            // Realistische Zeit generieren basierend auf dem Datum
            // 15. Nov: 14:15, 18. Nov: 10:30
            let time = '10:30';
            if (date.getDate() === 15) {
                time = '14:15';
            } else if (date.getDate() === 18) {
                time = '10:30';
            }
            
            // Datum-Zeile entfernen (Format: **DD. Monat YYYY** oder ähnlich)
            markdown = markdown.replace(/^\*\*.*?\d{1,2}\.\s+\w+\s+\d{4}.*?\*\*\s*$/gm, '');

            // Erste H1-Überschrift entfernen, damit sie nicht doppelt erscheint
            let headingRemoved = false;
            markdown = markdown.replace(/^# .+$/m, (match) => {
                if (headingRemoved) return match;
                headingRemoved = true;
                return '';
            }).trimStart();
            
            let html = parseMarkdown(markdown, title, date, time);
            
            entries.push({
                filename,
                date,
                title,
                html,
                formattedDate: formatDate(date)
            });
        } catch (error) {
            console.error(`Fehler beim Laden von ${filename}:`, error);
        }
    }
    
    console.log(`${entries.length} Einträge geladen`);
    
    if (entries.length === 0) {
        container.innerHTML = '<div class="logbook-entry"><p class="text-gray-400">Keine Journal-Einträge gefunden.</p></div>';
        return;
    }
    
    // Nach Datum sortieren (neueste zuerst für horizontale Timeline)
    entries.sort((a, b) => b.date - a.date);
    
    // Globale Variable speichern
    allJournalEntries = entries;
    
    // Timeline generieren
    generateTimeline(entries);
    
    // Ersten Eintrag anzeigen
    currentEntryIndex = 0;
    displayEntry(0);
}

// Timeline generieren
function generateTimeline(entries) {
    const timelineList = document.getElementById('timeline-list');
    if (!timelineList) return;
    
    let timelineHTML = '';
    entries.forEach((entry, index) => {
        timelineHTML += `
            <div class="timeline-item" data-index="${index}" onclick="selectEntry(${index})">
                <div class="timeline-item-date">${entry.formattedDate}</div>
                <div class="timeline-item-title">${entry.title}</div>
            </div>
        `;
    });
    
    timelineList.innerHTML = timelineHTML;
}

// Eintrag auswählen und anzeigen
function selectEntry(index) {
    if (index < 0 || index >= allJournalEntries.length) return;
    
    currentEntryIndex = index;
    displayEntry(index);
    
    // Active-Status in Timeline aktualisieren
    document.querySelectorAll('.timeline-item').forEach((item, i) => {
        if (i === index) {
            item.classList.add('active');
            // Scroll zu aktivem Item (horizontal)
            const timelineContainer = document.getElementById('timeline-sidebar');
            if (timelineContainer && item) {
                const itemLeft = item.offsetLeft;
                const itemWidth = item.offsetWidth;
                const containerWidth = timelineContainer.offsetWidth;
                const scrollLeft = itemLeft - (containerWidth / 2) + (itemWidth / 2);
                timelineContainer.scrollTo({
                    left: scrollLeft,
                    behavior: 'smooth'
                });
            }
        } else {
            item.classList.remove('active');
        }
    });
}

// Optimale Spaltenanzahl für Grid berechnen
function calculateOptimalColumns(bubbleCount, containerWidth) {
    if (containerWidth >= 1200) {
        return Math.min(3, Math.max(1, bubbleCount));
    }
    
    if (containerWidth >= 768) {
        return Math.min(2, Math.max(1, bubbleCount));
    }
    
    return 1;
}

// Global flag to track if user is actively scrolling
let isUserScrolling = false;
let scrollTimeout = null;

// Global flag to track if typing animation is active
let isTypingAnimationActive = false;

// Smart Grid Layout optimieren
function optimizeGridLayout(preserveScroll = true) {
    const grid = document.querySelector('.content-grid');
    if (!grid) return;
    
    const bubbles = grid.querySelectorAll('.content-bubble');
    if (bubbles.length === 0) return;
    
    // Find the scrollable container (logbook-main)
    const scrollContainer = grid.closest('.logbook-main') || window;
    
    // Don't preserve scroll if user is actively scrolling or typing animation is active
    if (preserveScroll && (isUserScrolling || isTypingAnimationActive)) {
        preserveScroll = false;
    }
    
    // Store scroll position relative to a reference element (second bubble or first if only one)
    // This prevents jumping when the first bubble (title) changes height during typing
    let referenceElement = bubbles.length > 1 ? bubbles[1] : bubbles[0];
    let referenceTop = 0;
    let currentScrollTop = 0;
    if (preserveScroll && referenceElement) {
        currentScrollTop = scrollContainer === window 
            ? window.pageYOffset 
            : scrollContainer.scrollTop;
        // Store the reference element's position relative to the scroll container
        const containerRect = scrollContainer === window 
            ? { top: 0 } 
            : scrollContainer.getBoundingClientRect();
        const referenceRect = referenceElement.getBoundingClientRect();
        referenceTop = referenceRect.top - containerRect.top + currentScrollTop;
    }
    
    const containerWidth = grid.offsetWidth || window.innerWidth;
    const optimalColumns = calculateOptimalColumns(bubbles.length, containerWidth);
    
    // Grid-Spalten dynamisch setzen
    grid.style.gridTemplateColumns = `repeat(${optimalColumns}, minmax(0, 1fr))`;
    grid.style.gridAutoFlow = optimalColumns > 1 ? 'row dense' : 'row';

    // Reset all gridRowEnd before recalculating to avoid stale values
    bubbles.forEach(bubble => bubble.style.gridRowEnd = 'auto');

    // Read gap and grid-auto-rows from computed styles
    const styles = window.getComputedStyle(grid);
    const rowGap = parseFloat(styles.rowGap) || 0;
    const rowHeight = parseFloat(styles.gridAutoRows) || 0.2 * 16; // Default to 0.2rem in px (assuming 16px base)
    
    // Ensure we have valid values
    if (rowHeight <= 0 || rowGap < 0) {
        console.warn('grid-auto-rows or rowGap is invalid');
        return;
    }
    
    // Calculate total row size: rowHeight + rowGap
    const totalRowSize = rowHeight + rowGap;
    
    // Recalculate spans for all bubbles
    // Formula: We need N rows such that: bubbleHeight <= N * rowHeight + (N - 1) * rowGap
    // Which simplifies to: N >= (bubbleHeight + rowGap) / (rowHeight + rowGap)
    bubbles.forEach(bubble => {
        // Use offsetHeight for more accurate measurement (excludes margins)
        const bubbleHeight = bubble.offsetHeight;
        
        // Calculate span: ceil ensures we have enough space
        const span = Math.max(1, Math.ceil((bubbleHeight + rowGap) / totalRowSize));
        bubble.style.gridRowEnd = `span ${span}`;
    });
    
    // Force a reflow to ensure all spans are applied before next calculation
    void grid.offsetHeight;
    
    // Restore scroll position relative to reference element
    // Only if user is not actively scrolling
    if (preserveScroll && referenceElement && !isUserScrolling) {
        requestAnimationFrame(() => {
            // Double-check user is still not scrolling
            if (isUserScrolling) return;
            
            const containerRect = scrollContainer === window 
                ? { top: 0 } 
                : scrollContainer.getBoundingClientRect();
            const referenceRect = referenceElement.getBoundingClientRect();
            const newReferenceTop = referenceRect.top - containerRect.top + (scrollContainer === window ? window.pageYOffset : scrollContainer.scrollTop);
            const delta = newReferenceTop - referenceTop;
            
            // Only restore if delta is significant (more than 1px) to avoid micro-adjustments
            if (Math.abs(delta) > 1) {
                const newScroll = currentScrollTop + delta;
                
                if (scrollContainer === window) {
                    window.scrollTo(0, newScroll);
                } else {
                    scrollContainer.scrollTop = newScroll;
                }
            }
        });
    }
}

// Eintrag anzeigen
function displayEntry(index) {
    const container = document.getElementById('logbook-container');
    if (!container || !allJournalEntries[index]) return;
    
    const entry = allJournalEntries[index];
    
    // Direkt den HTML-Inhalt einfügen (ohne logbook-entry Wrapper)
    // Der parseMarkdown erstellt bereits das content-grid
    let html = entry.html;
    
    // Falls noch kein content-grid vorhanden ist (Fallback), eines hinzufügen
    if (!html.includes('content-grid')) {
        html = `<div class="content-grid">${html}</div>`;
    }
    
    container.innerHTML = html;

    const gridElement = container.querySelector('.content-grid');
    const requestOptimize = () => {
        window.requestAnimationFrame(() => optimizeGridLayout());
    };
    if (gridElement) {
        const mediaElements = gridElement.querySelectorAll('img, video');
        mediaElements.forEach(element => {
            if (element.complete || element.readyState >= 2) {
                requestOptimize();
            } else {
                element.addEventListener('load', requestOptimize, { once: true });
                element.addEventListener('error', requestOptimize, { once: true });
            }
        });
    }

    // Initial layout optimization before typing animation starts
    setTimeout(() => {
        optimizeGridLayout(false);
    }, 0);

    // Typing Effekt bei erster Bubble (Titel)
    const titleElement = container.querySelector('.journal-title');
    if (titleElement) {
        const text = titleElement.dataset.fullText || titleElement.textContent.trim();
        titleElement.textContent = '';
        titleElement.classList.add('journal-title-typing');

        const typedSpan = document.createElement('span');
        typedSpan.className = 'journal-title-text';
        titleElement.appendChild(typedSpan);

        const caret = document.createElement('span');
        caret.className = 'journal-title-caret';
        titleElement.appendChild(caret);

        let idx = 0;
        
        // Set typing animation flag to prevent layout updates during animation
        // Set after initial layout is done
        setTimeout(() => {
            isTypingAnimationActive = true;
        }, 100);

        const typeNext = () => {
            if (idx < text.length) {
                typedSpan.textContent += text[idx];
                idx += 1;
                // No layout updates during typing to prevent scroll jumping
                setTimeout(typeNext, 55 + Math.random() * 45);
            } else {
                caret.classList.add('blink');
                // Animation complete - reset flag and optimize layout once
                isTypingAnimationActive = false;
                
                // Optimize layout after animation completes
                requestAnimationFrame(() => {
                    optimizeGridLayout(false); // Don't preserve scroll, let user's position stay
                });
                
                // Additional layout pass after a short delay to ensure final spacing is correct
                setTimeout(() => {
                    optimizeGridLayout(false);
                }, 200);
            }
        };
        setTimeout(typeNext, 300);
    }
    
    // Layout wird bereits vor der Typing-Animation optimiert (siehe oben)
    
    // Lightbox-Funktionalität für Bilder initialisieren
    initializeImageLightbox();
    
    // (Kein automatischer Scroll nach oben, um "Jumping" zu vermeiden)
}

// Standardmäßig die 'overview'-Seite anzeigen
document.addEventListener('DOMContentLoaded', () => {
    // Prüfe localStorage für gespeicherte aktive Seite
    const savedPage = localStorage.getItem('activePage');
    const pageToShow = savedPage || 'overview';
    
    // Alle Seiten ausblenden
    pages.forEach(page => {
        page.classList.remove('active');
    });
    
    // Gespeicherte Seite anzeigen
    document.getElementById('page-' + pageToShow).classList.add('active');
    
    // Den passenden Menüpunkt auch als "active" markieren
    const activeMenuItem = dropdown.querySelector(`[data-page="${pageToShow}"]`);
    if (activeMenuItem) {
        dropdownItems.forEach(item => {
            item.classList.remove('active');
        });
        activeMenuItem.classList.add('active');
    } else {
        // Fallback: overview markieren
        dropdown.querySelector('[data-page="overview"]').classList.add('active');
    }

    // Player initialisieren
    if (typeof populatePlaylist === 'function') {
        populatePlaylist();
        loadTrack(0); // Ersten Track laden (initialisiert auch den Marquee)
        
        // Zeit-Anzeige nach dem Laden der Metadaten aktualisieren
        if (audioPlayer) {
            audioPlayer.addEventListener('loadedmetadata', () => {
                updateTimeDisplay();
            }, { once: true });
        }
    }
    
    // Journal-Einträge laden, wenn Logbuch-Seite aktiv ist
    if (pageToShow === 'logbook') {
        loadJournalEntries();
        journalEntriesLoaded = true;
    }
    
    // Window Resize Handler für Layout-Optimierung
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            optimizeGridLayout();
        }, 150);
    });
    
    // Track user scrolling to prevent scroll position restoration during active scrolling
    const logbookMain = document.querySelector('.logbook-main');
    if (logbookMain) {
        const handleScrollStart = () => {
            isUserScrolling = true;
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                isUserScrolling = false;
            }, 150); // Reset flag 150ms after scrolling stops
        };
        
        logbookMain.addEventListener('scroll', handleScrollStart, { passive: true });
        logbookMain.addEventListener('wheel', handleScrollStart, { passive: true });
        logbookMain.addEventListener('touchmove', handleScrollStart, { passive: true });
    }
    
    // Lightbox-Funktionalität initialisieren
    setTimeout(() => {
        initializeImageLightbox();
    }, 100);
});

// --- IMAGE LIGHTBOX / GALLERY SYSTEM ---

let currentImageGallery = [];
let currentImageIndex = 0;

// Initialisiert die Lightbox-Funktionalität für alle Bilder
function initializeImageLightbox() {
    // Alle Bubbles finden
    const bubbles = document.querySelectorAll('.content-bubble');
    
    bubbles.forEach(bubble => {
        // Alle Bilder in dieser Bubble finden
        const images = bubble.querySelectorAll('img:not([data-lightbox-initialized])');
        
        if (images.length === 0) return;
        
        // Gallery-Array für diese Bubble erstellen
        const gallery = Array.from(bubble.querySelectorAll('img')).map(img => {
            // Caption finden (kann in figcaption oder alt-Attribut sein)
            let caption = '';
            const figure = img.closest('figure');
            if (figure) {
                const figcaption = figure.querySelector('figcaption');
                if (figcaption) {
                    caption = figcaption.textContent.trim();
                }
            }
            if (!caption) {
                caption = img.getAttribute('alt') || '';
            }
            
            return {
                src: img.src,
                alt: img.getAttribute('alt') || '',
                caption: caption
            };
        });
        
        // Click-Handler für jedes Bild hinzufügen (nur für noch nicht initialisierte)
        images.forEach((img, index) => {
            // Index im gesamten Gallery-Array finden
            const allImages = Array.from(bubble.querySelectorAll('img'));
            const actualIndex = allImages.indexOf(img);
            
            img.addEventListener('click', (e) => {
                e.stopPropagation();
                openLightbox(gallery, actualIndex);
            });
            
            // Markieren als initialisiert
            img.setAttribute('data-lightbox-initialized', 'true');
        });
    });
    
    // Auch für Bilder außerhalb von Bubbles (z.B. in overview-Seite)
    const standaloneImages = document.querySelectorAll('#page-overview img:not([data-lightbox-initialized]), #page-dialogues img:not([data-lightbox-initialized])');
    standaloneImages.forEach(img => {
        // Nur wenn nicht bereits in einer Bubble
        if (!img.closest('.content-bubble')) {
            const gallery = [{
                src: img.src,
                alt: img.getAttribute('alt') || '',
                caption: img.getAttribute('alt') || ''
            }];
            
            img.addEventListener('click', (e) => {
                e.stopPropagation();
                openLightbox(gallery, 0);
            });
            
            // Markieren als initialisiert
            img.setAttribute('data-lightbox-initialized', 'true');
        }
    });
}

// Öffnet die Lightbox mit einer Gallery
function openLightbox(gallery, startIndex = 0) {
    if (!gallery || gallery.length === 0) return;
    
    currentImageGallery = gallery;
    currentImageIndex = Math.max(0, Math.min(startIndex, gallery.length - 1));
    
    const overlay = document.getElementById('image-lightbox-overlay');
    const image = document.getElementById('image-lightbox-image');
    const caption = document.getElementById('image-lightbox-caption');
    const counter = document.getElementById('image-lightbox-counter');
    const prevBtn = overlay.querySelector('.image-lightbox-nav.prev');
    const nextBtn = overlay.querySelector('.image-lightbox-nav.next');
    
    // Bild und Caption aktualisieren
    updateLightboxContent();
    
    // Navigation-Buttons anzeigen/verstecken
    if (gallery.length > 1) {
        prevBtn.style.display = 'flex';
        nextBtn.style.display = 'flex';
        counter.style.display = 'block';
    } else {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
        counter.style.display = 'none';
    }
    
    // Overlay anzeigen
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Scroll verhindern
    
    // Keyboard-Navigation
    window.addEventListener('keydown', handleLightboxKeyboard);
}

// Aktualisiert den Inhalt der Lightbox
function updateLightboxContent() {
    if (currentImageGallery.length === 0) return;
    
    const item = currentImageGallery[currentImageIndex];
    const image = document.getElementById('image-lightbox-image');
    const caption = document.getElementById('image-lightbox-caption');
    const counter = document.getElementById('image-lightbox-counter');
    
    image.src = item.src;
    image.alt = item.alt;
    
    if (item.caption) {
        caption.textContent = item.caption;
        caption.style.display = 'block';
    } else {
        caption.style.display = 'none';
    }
    
    if (currentImageGallery.length > 1) {
        counter.textContent = `${currentImageIndex + 1} / ${currentImageGallery.length}`;
    }
}

// Schließt die Lightbox
function closeLightbox() {
    const overlay = document.getElementById('image-lightbox-overlay');
    overlay.classList.remove('active');
    document.body.style.overflow = ''; // Scroll wieder erlauben
    
    // Keyboard-Listener entfernen
    window.removeEventListener('keydown', handleLightboxKeyboard);
    
    currentImageGallery = [];
    currentImageIndex = 0;
}

// Navigiert in der Gallery
function navigateLightbox(direction) {
    if (currentImageGallery.length === 0) return;
    
    currentImageIndex += direction;
    
    // Loop durch die Gallery
    if (currentImageIndex < 0) {
        currentImageIndex = currentImageGallery.length - 1;
    } else if (currentImageIndex >= currentImageGallery.length) {
        currentImageIndex = 0;
    }
    
    updateLightboxContent();
}

// Keyboard-Navigation für Lightbox
function handleLightboxKeyboard(e) {
    const overlay = document.getElementById('image-lightbox-overlay');
    if (!overlay.classList.contains('active')) return;
    
    switch(e.key) {
        case 'Escape':
            closeLightbox();
            break;
        case 'ArrowLeft':
            navigateLightbox(-1);
            e.preventDefault();
            break;
        case 'ArrowRight':
            navigateLightbox(1);
            e.preventDefault();
            break;
    }
}

// Click auf Overlay schließt Lightbox
document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.getElementById('image-lightbox-overlay');
    if (overlay) {
        overlay.addEventListener('click', (e) => {
            // Nur schließen, wenn direkt auf Overlay geklickt wurde
            if (e.target === overlay) {
                closeLightbox();
            }
        });
    }
});