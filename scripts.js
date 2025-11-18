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

// Funktion zum Laden eines Tracks
function loadTrack(index) {
    currentTrackIndex = index;
    const track = playlist[index];
    
    audioPlayer.src = track.src;
    audioPlayer.load();

    // Marquee-Text aktualisieren
    updateMarquee(track);

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
    clickedElement.classList.add('active');
    
    // "active" Status auf dem Haupt-Toggle-Button aktualisieren
    toggleButton.classList.add('active');

    // Dropdown schließen
    
    // Journal-Einträge laden, wenn Logbuch-Seite angezeigt wird
    if (pageId === 'logbook' && !journalEntriesLoaded) {
        loadJournalEntries();
        journalEntriesLoaded = true;
    }
    
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
    'journal/journal-2025-11-18-marble-worldlabs.md'
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
function parseMarkdown(markdown) {
    let html = markdown;
    
    // Welt-Info-Dropdown-Komponenten verarbeiten (Format: [WORLD_INFO:...])
    // Syntax: [WORLD_INFO:title|model|seed|publicMode|previewImage|link|vrLink|description]
    // Die Beschreibung kommt am Ende, damit sie Pipes enthalten kann
    const worldInfoRegex = /\[WORLD_INFO:([^\]]+)\]/g;
    html = html.replace(worldInfoRegex, (match, data) => {
        // Teile die Daten auf
        // Format: title|model|seed|publicMode|previewImage|link|vrLink|description
        const parts = data.split('|');
        
        // Die Teile sind: title, model, seed, publicMode, previewImage, link, vrLink, description
        // Alles nach dem 7. Pipe ist die Beschreibung
        const worldData = {
            title: parts[0] || '',
            model: parts[1] || '',
            seed: parts[2] || '',
            publicMode: parts[3] === 'true' || parts[3] === '1',
            previewImage: parts[4] || '',
            link: parts[5] || '',
            vrLink: parts[6] || '',
            description: parts.slice(7).join('|') || '' // Alles ab Index 7 ist die Beschreibung
        };
        return createWorldInfoDropdown(worldData);
    });
    
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
        
        // Überschrift erkennen (## oder ###)
        const headingMatch = trimmed.match(/^(##+)\s+(.+)$/);
        if (headingMatch) {
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
            const headingText = headingMatch[2];
            currentSection = {
                heading: headingText,
                headingLevel: headingLevel,
                content: []
            };
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
        
        // Bilder behandeln
        html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" class="my-6 rounded-sm w-full h-auto max-w-4xl mx-auto" />');
        
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
        
        // Intro-Text am Anfang anzeigen (falls vorhanden)
        if (introText.length > 0) {
            let introContent = introText.map(para => {
                if (!para.trim()) return '';
                para = para.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                para = para.replace(/\*(.*?)\*/g, '<em>$1</em>');
                para = para.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" class="my-4 rounded-sm w-full h-auto" />');
                return '<p class="mb-4">' + para + '</p>';
            }).filter(p => p).join('\n');
            
            gridHTML += `
                <div class="content-bubble bubble-large">
                    <div class="bubble-content">
                        ${introContent}
                    </div>
                </div>
            `;
        }
        
        sections.forEach((section) => {
            // Inhalt formatieren
            let sectionContent = section.content.map(para => {
                if (!para.trim()) return '';
                // Fettdruck und Kursiv
                para = para.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                para = para.replace(/\*(.*?)\*/g, '<em>$1</em>');
                // Bilder
                para = para.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" class="my-4 rounded-sm w-full h-auto" />');
                return '<p class="mb-4">' + para + '</p>';
            }).filter(p => p).join('\n');
            
            const headingClass = section.headingLevel === 2 ? 'text-2xl' : 'text-xl';
            const bubbleSize = section.headingLevel === 2 ? 'bubble-large' : 'bubble-medium';
            
            gridHTML += `
                <div class="content-bubble ${bubbleSize}">
                    <h${section.headingLevel || 2} class="${headingClass} font-bold mb-4 text-accent">${section.heading || 'Abschnitt'}</h${section.headingLevel || 2}>
                    <div class="bubble-content">
                        ${sectionContent}
                    </div>
                </div>
            `;
        });
        
        gridHTML += '</div>';
        html = gridHTML;
    }
    
    // URLs in Links umwandeln (als Pills) - nach Absatz-Verarbeitung
    // Erkennt URLs in Text (http://, https://, www.), aber nicht in bereits existierenden Links
    // Wir müssen zuerst alle bereits existierenden Links markieren, dann URLs konvertieren, dann Markierungen entfernen
    const linkPlaceholder = '___LINK_PLACEHOLDER___';
    const linkMap = new Map();
    let linkCounter = 0;
    
    // Temporär alle existierenden Links und Bilder ersetzen
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
            
            // Datum-Zeile entfernen (Format: **DD. Monat YYYY** oder ähnlich)
            markdown = markdown.replace(/^\*\*.*?\d{1,2}\.\s+\w+\s+\d{4}.*?\*\*\s*$/gm, '');
            
            let html = parseMarkdown(markdown);
            
            // Erste Überschrift (H1) entfernen, da sie bereits als Titel extrahiert wurde
            html = html.replace(/<h1[^>]*>.*?<\/h1>\s*/i, '');
            
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

// Eintrag anzeigen
function displayEntry(index) {
    const container = document.getElementById('logbook-container');
    if (!container || !allJournalEntries[index]) return;
    
    const entry = allJournalEntries[index];
    
    const html = `
        <div class="logbook-entry">
            <div class="logbook-entry-header">
                <div class="logbook-entry-date">${entry.formattedDate}</div>
                <h2 class="logbook-entry-title">${entry.title}</h2>
            </div>
            <div class="prose prose-invert max-w-none text-gray-300">
                ${entry.html}
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Zum Anfang scrollen
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Standardmäßig die 'overview'-Seite anzeigen
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('page-overview').classList.add('active');
    // Den passenden Menüpunkt auch als "active" markieren
    dropdown.querySelector('[data-page="overview"]').classList.add('active');

    // Player initialisieren
    if (typeof populatePlaylist === 'function') {
        populatePlaylist();
        loadTrack(0); // Ersten Track laden (initialisiert auch den Marquee)
    }
    
    // Journal-Einträge laden, wenn Logbuch-Seite bereits aktiv ist
    if (document.getElementById('page-logbook').classList.contains('active')) {
        loadJournalEntries();
        journalEntriesLoaded = true;
    }
});