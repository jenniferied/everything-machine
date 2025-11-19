/**
 * PlayerUI
 * Single responsibility: UI updates and marquee animation
 * Listens to playback events and updates the DOM accordingly
 */
import { formatTime } from './timeFormatter.js';

export class PlayerUI {
  /**
   * @param {Object} elements - DOM elements for the player UI
   * @param {EventBus} eventBus - Event bus for communication
   */
  constructor(elements, eventBus) {
    if (!eventBus) {
      throw new Error('[PlayerUI] EventBus instance required');
    }

    this.elements = {
      playPauseButton: elements.playPauseButton,
      prevButton: elements.prevButton,
      nextButton: elements.nextButton,
      albumCover: elements.albumCover,
      marqueeContent: elements.marqueeContent,
      timeDisplay: elements.timeDisplay,
      playlistDropdown: elements.playlistDropdown,
      playlistToggleBtn: elements.playlistToggleBtn
    };
    
    this.eventBus = eventBus;
    this.currentTrackIndex = 0;
    
    // Bind event handlers
    this.handleTrackChanged = this.handleTrackChanged.bind(this);
    this.handlePlay = this.handlePlay.bind(this);
    this.handlePause = this.handlePause.bind(this);
    this.handleTimeUpdate = this.handleTimeUpdate.bind(this);
    this.handleLoadedMetadata = this.handleLoadedMetadata.bind(this);
    this.handleDurationChange = this.handleDurationChange.bind(this);
  }

  /**
   * Initialize the UI controller
   */
  initialize() {
    // Listen to playback events
    this.eventBus.on('playback:trackChanged', this.handleTrackChanged);
    this.eventBus.on('playback:play', this.handlePlay);
    this.eventBus.on('playback:pause', this.handlePause);
    this.eventBus.on('playback:timeupdate', this.handleTimeUpdate);
    this.eventBus.on('playback:loadedmetadata', this.handleLoadedMetadata);
    this.eventBus.on('playback:durationchange', this.handleDurationChange);
    
    console.log('[PlayerUI] Initialized');
  }

  /**
   * Handle track changed event
   * @param {Object} data - Event data with trackIndex and track
   */
  handleTrackChanged(data) {
    const { trackIndex, track } = data;
    this.currentTrackIndex = trackIndex;
    
    // Update marquee
    this.updateMarquee(track);
    
    // Update album cover
    this.updateAlbumCover(track);
    
    // Reset time display
    if (this.elements.timeDisplay) {
      this.elements.timeDisplay.textContent = '0:00/0:00';
    }
    
    // Update active state in playlist
    this.updatePlaylistActiveState(trackIndex);
  }

  /**
   * Handle play event
   */
  handlePlay() {
    if (this.elements.playPauseButton) {
      this.elements.playPauseButton.classList.add('playing');
    }
    this.changeMarqueeSpeed(7); // Fast when playing
  }

  /**
   * Handle pause event
   */
  handlePause() {
    if (this.elements.playPauseButton) {
      this.elements.playPauseButton.classList.remove('playing');
    }
    this.changeMarqueeSpeed(40); // Slow when paused
  }

  /**
   * Handle time update event
   * @param {Object} data - Event data with currentTime and duration
   */
  handleTimeUpdate(data) {
    if (!this.elements.timeDisplay) return;
    
    const { currentTime, duration } = data;
    const currentTimeFormatted = formatTime(currentTime);
    const durationFormatted = formatTime(duration);
    
    this.elements.timeDisplay.textContent = `${currentTimeFormatted}/${durationFormatted}`;
  }

  /**
   * Handle loaded metadata event
   */
  handleLoadedMetadata(data) {
    this.updateTimeDisplay(0, data.duration);
  }

  /**
   * Handle duration change event
   */
  handleDurationChange(data) {
    // Update time display with new duration
    if (this.elements.timeDisplay) {
      const currentTimeFormatted = formatTime(0);
      const durationFormatted = formatTime(data.duration);
      this.elements.timeDisplay.textContent = `${currentTimeFormatted}/${durationFormatted}`;
    }
  }

  /**
   * Update time display
   * @param {number} currentTime - Current time in seconds
   * @param {number} duration - Duration in seconds
   */
  updateTimeDisplay(currentTime, duration) {
    if (!this.elements.timeDisplay) return;
    
    const currentTimeFormatted = formatTime(currentTime);
    const durationFormatted = formatTime(duration);
    
    this.elements.timeDisplay.textContent = `${currentTimeFormatted}/${durationFormatted}`;
  }

  /**
   * Update marquee text with track info
   * @param {Object} track - Track object
   */
  updateMarquee(track) {
    if (!this.elements.marqueeContent) return;
    
    const newText = `${track.artist} - ${track.title} (${track.album}, ${track.year})`;
    const newLink = `https://open.spotify.com/track/${track.spotifyID || ''}`;
    
    // Marquee with two copies for seamless loop
    this.elements.marqueeContent.innerHTML = `
      <a href="${newLink}" target="_blank" rel="noopener noreferrer" title="${track.artist} auf Spotify öffnen" style="pointer-events: auto;">${newText}</a>
      <span class="mx-4">|</span>
      <a href="${newLink}" target="_blank" rel="noopener noreferrer" title="${track.artist} auf Spotify öffnen" style="pointer-events: auto;">${newText}</a>
    `;
  }

  /**
   * Update album cover
   * @param {Object} track - Track object
   */
  updateAlbumCover(track) {
    if (!this.elements.albumCover) return;
    
    if (track.cover) {
      this.elements.albumCover.src = track.cover;
      this.elements.albumCover.alt = `${track.album} Cover`;
      this.elements.albumCover.style.display = 'block';
      this.elements.albumCover.style.cursor = 'pointer';
      
      // Spotify link
      const spotifyLink = `https://open.spotify.com/track/${track.spotifyID || ''}`;
      this.elements.albumCover.onclick = (e) => {
        e.preventDefault();
        if (track.spotifyID && track.spotifyID !== 'YOUR_SONG_ID_2' && track.spotifyID !== 'YOUR_SONG_ID_3') {
          window.open(spotifyLink, '_blank', 'noopener,noreferrer');
        }
      };
      
      // Fallback on error
      this.elements.albumCover.onerror = function() {
        this.style.display = 'none';
      };
    } else {
      this.elements.albumCover.style.display = 'none';
    }
  }

  /**
   * Update active state in playlist dropdown
   * @param {number} activeIndex - Index of active track
   */
  updatePlaylistActiveState(activeIndex) {
    if (!this.elements.playlistDropdown) return;
    
    const playlistItems = this.elements.playlistDropdown.querySelectorAll('.playlist-item');
    playlistItems.forEach((item, index) => {
      if (index === activeIndex) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });
  }

  /**
   * Change marquee animation speed
   * @param {number} newDuration - New animation duration in seconds
   */
  changeMarqueeSpeed(newDuration) {
    const marqueeContent = this.elements.marqueeContent;
    if (!marqueeContent) return;
    
    // Step 1: Read current position
    const computedStyle = window.getComputedStyle(marqueeContent);
    const transform = computedStyle.transform;
    
    let currentTranslateX = 0;
    if (transform && transform !== 'none') {
      const matrix = transform.match(/matrix\(([^)]+)\)/);
      if (matrix) {
        const values = matrix[1].split(',');
        currentTranslateX = parseFloat(values[4]) || 0;
      }
    }
    
    // Step 2: Calculate progress
    const totalWidth = marqueeContent.scrollWidth;
    const oneCopyWidth = totalWidth / 2;
    const maxTranslate = -oneCopyWidth;
    
    let progress = 0;
    if (Math.abs(maxTranslate) > 0) {
      progress = (Math.abs(currentTranslateX) / Math.abs(maxTranslate)) % 1;
    }
    
    // Step 3: Calculate negative delay for seamless transition
    const newDelay = -(progress * newDuration);
    
    // Step 4: Set position manually BEFORE removing animation
    marqueeContent.style.transform = `translateX(${currentTranslateX}px)`;
    
    // Step 5: Remove animation
    marqueeContent.style.animation = 'none';
    
    // Step 6: Wait frames, then restart with new duration
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        // Step 7: Start animation with new duration and negative delay
        marqueeContent.style.animation = `marquee ${newDuration}s linear ${newDelay}s infinite`;
        
        // Step 8: Check position and remove manual transform
        let checkCount = 0;
        const maxChecks = 20;
        
        const checkPosition = () => {
          checkCount++;
          const newTransform = window.getComputedStyle(marqueeContent).transform;
          let newTranslateX = 0;
          if (newTransform && newTransform !== 'none') {
            const matrix = newTransform.match(/matrix\(([^)]+)\)/);
            if (matrix) {
              const values = matrix[1].split(',');
              newTranslateX = parseFloat(values[4]) || 0;
            }
          }
          
          const expectedTranslateX = -(progress * oneCopyWidth);
          const diff = Math.abs(newTranslateX - expectedTranslateX);
          
          if (diff < 0.5 || checkCount >= maxChecks) {
            if (diff < 0.5) {
              marqueeContent.style.transform = '';
            } else {
              setTimeout(() => {
                marqueeContent.style.transform = '';
              }, 200);
            }
          } else {
            requestAnimationFrame(checkPosition);
          }
        };
        
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            requestAnimationFrame(checkPosition);
          });
        });
      });
    });
  }

  /**
   * Dispose and clean up
   */
  dispose() {
    // Remove event listeners
    this.eventBus.off('playback:trackChanged', this.handleTrackChanged);
    this.eventBus.off('playback:play', this.handlePlay);
    this.eventBus.off('playback:pause', this.handlePause);
    this.eventBus.off('playback:timeupdate', this.handleTimeUpdate);
    this.eventBus.off('playback:loadedmetadata', this.handleLoadedMetadata);
    this.eventBus.off('playback:durationchange', this.handleDurationChange);
    
    console.log('[PlayerUI] Disposed');
  }
}

