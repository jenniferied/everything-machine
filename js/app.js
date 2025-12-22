/**
 * Main Application Orchestrator
 * Coordinates all modules with dependency injection and progressive enhancement
 */

// Import core modules
import { FeatureDetector } from './core/FeatureDetector.js';
import { ScriptLoader } from './core/ScriptLoader.js';
import { EventBus } from './core/EventBus.js';

// Import viewers
import { ThreeDViewer } from './viewers/ThreeDViewer.js';
import { PointCloudViewer } from './viewers/PointCloudViewer.js';
import { VideoViewer } from './viewers/VideoViewer.js';

// Import animations
import { AnimationController } from './animations/AnimationController.js';
import { FloatingAnimation } from './animations/FloatingAnimation.js';

// Import media
import { LazyLoader } from './media/LazyLoader.js';
import { ImageGallery } from './media/ImageGallery.js';

// Import UI
import { AIAttribution } from './ui/AIAttribution.js';

// Import audio
import { MusicPlayer } from './audio/MusicPlayer.js';

// Import navigation
import { PageNavigator } from './navigation/PageNavigator.js';
import { DropdownController } from './navigation/DropdownController.js';
import { NavigationState } from './navigation/NavigationState.js';

// Import journal
import { JournalManager } from './journal/JournalManager.js';

// Import pages
import { MarkdownPageLoader } from './pages/MarkdownPageLoader.js';

/**
 * Application class
 * Follows dependency injection and SOLID principles
 */
class Application {
  constructor() {
    // Core services (Singletons)
    this.featureDetector = null;
    this.scriptLoader = null;
    this.eventBus = null;
    
    // Controllers
    this.animationController = null;
    this.lazyLoader = null;
    this.imageGallery = null;
    
    // Viewers
    this.viewers = new Map();
    
    // Animations
    this.animations = new Map();
    
    // UI Components
    this.uiComponents = new Map();
    
    // State
    this.initialized = false;
    this.capabilities = null;
  }

  /**
   * Initialize the application
   * @returns {Promise<void>}
   */
  async initialize() {
    if (this.initialized) {
      return;
    }
    
    console.log('[App] Initializing application...');
    
    // Phase 1: Initialize core services
    this.initializeCore();
    
    // Phase 2: Detect capabilities
    await this.detectCapabilities();
    
    // Phase 3: Initialize controllers
    await this.initializeControllers();
    
    // Phase 4: Setup viewers conditionally
    await this.setupViewers();
    
    // Phase 5: Setup animations
    await this.setupAnimations();
    
    // Phase 6: Setup UI components
    await this.setupUI();
    
    // Phase 7: Setup audio player
    await this.setupAudioPlayer();
    
    // Phase 8: Setup navigation
    await this.setupNavigation();
    
    // Phase 9: Setup journal
    await this.setupJournal();
    
    // Phase 10: Setup markdown pages
    await this.setupMarkdownPages();
    
    // Phase 11: Initialize media lazy loading
    await this.setupMediaLazyLoading();
    
    // Phase 12: Start the application
    this.start();
    
    this.initialized = true;
    console.log('[App] Application initialized successfully');
    
    // Log capabilities for debugging (can be disabled in production)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      this.featureDetector.logCapabilities();
      console.log('[App] Animation Controller Stats:', this.animationController.getStats());
    }
  }

  /**
   * Initialize core services
   */
  initializeCore() {
    this.featureDetector = new FeatureDetector();
    this.scriptLoader = new ScriptLoader();
    this.eventBus = new EventBus();
    
    // Enable debug mode in development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      this.eventBus.setDebugMode(true);
    }
    
    console.log('[App] Core services initialized');
  }

  /**
   * Detect device capabilities
   * @returns {Promise<void>}
   */
  async detectCapabilities() {
    this.capabilities = this.featureDetector.getCapabilities();
    
    console.log('[App] Capabilities detected:', {
      webgl: this.capabilities.webgl,
      webgl2: this.capabilities.webgl2,
      performanceTier: this.capabilities.performanceTier,
      slowNetwork: this.capabilities.slowNetwork
    });
    
    this.eventBus.emit('app:capabilities-detected', this.capabilities);
  }

  /**
   * Initialize controllers
   * @returns {Promise<void>}
   */
  async initializeControllers() {
    // Animation controller
    this.animationController = new AnimationController(
      this.featureDetector,
      this.eventBus
    );
    await this.animationController.initialize();
    
    // Lazy loader
    this.lazyLoader = new LazyLoader(
      this.featureDetector,
      this.eventBus
    );
    this.lazyLoader.initialize({
      rootMargin: '100px',
      threshold: 0.01
    });
    
    // Image gallery
    this.imageGallery = new ImageGallery(
      this.eventBus,
      this.lazyLoader
    );
    this.imageGallery.initialize();
    
    console.log('[App] Controllers initialized');
  }

  /**
   * Setup viewers based on device capabilities
   * @returns {Promise<void>}
   */
  async setupViewers() {
    console.log('[App] setupViewers called');
    
    // 3D Viewer setup
    const threeDContainer = document.getElementById('3d-viewer-container');
    console.log('[App] 3D viewer container found:', !!threeDContainer);
    
    if (threeDContainer) {
      console.log('[App] Creating ThreeDViewer...');
      const threeDViewer = new ThreeDViewer(
        threeDContainer,
        {
          autoRotate: true,
          cameraDistance: 5,
          fallbackImage: 'https://placehold.co/600x400/1f2937/4ade80?text=3D+Viewer'
        },
        this.eventBus,
        this.scriptLoader,
        this.featureDetector
      );
      
      this.viewers.set('3d-viewer', threeDViewer);
      
      // Setup viewer immediately (controls will be visible)
      console.log('[App] Calling threeDViewer.setup()...');
      threeDViewer.setup().then(() => {
        console.log('[App] ThreeDViewer setup complete');
      }).catch(err => {
        console.error('[App] ThreeDViewer setup failed:', err);
      });
    }
    
    // Point Cloud Viewer setup
    const pointCloudContainer = document.getElementById('point-cloud-viewer-container');
    if (pointCloudContainer) {
      const pointCloudViewer = new PointCloudViewer(
        pointCloudContainer,
        {
          pointCloudPath: null, // Placeholder for now
          fallbackImage: 'https://placehold.co/600x400/1f2937/4ade80?text=Point+Cloud'
        },
        this.eventBus,
        this.scriptLoader,
        this.featureDetector
      );
      
      this.viewers.set('point-cloud-viewer', pointCloudViewer);
      
      // Setup viewer immediately
      pointCloudViewer.setup();
    }
    
    // Video viewers setup
    const videoContainers = document.querySelectorAll('[data-video-viewer]');
    videoContainers.forEach((container, index) => {
      const videoSrc = container.dataset.videoSrc;
      const poster = container.dataset.poster;
      
      if (videoSrc) {
        const videoViewer = new VideoViewer(
          container,
          { videoSrc, poster },
          this.eventBus,
          this.scriptLoader,
          this.featureDetector
        );
        
        this.viewers.set(`video-viewer-${index}`, videoViewer);
        
        // Wait for viewport, then setup
        videoViewer.waitForViewport(0.1).then(() => {
          videoViewer.setup();
        });
      }
    });
    
    console.log(`[App] ${this.viewers.size} viewers configured`);
  }

  /**
   * Setup floating animations for homepage
   * @returns {Promise<void>}
   */
  async setupAnimations() {
    // Only setup animations if not on slow network and motion is not reduced
    if (this.capabilities.slowNetwork || this.capabilities.reducedMotion) {
      console.log('[App] Animations disabled (slow network or reduced motion)');
      return;
    }
    
    // Find all elements to animate
    const floatingElements = document.querySelectorAll('.floating-element, [data-floating]');
    
    if (floatingElements.length > 0) {
      const floatingAnimation = new FloatingAnimation(
        floatingElements,
        {
          duration: 3000,
          distance: 15,
          rotation: 3,
          useAnimeJs: true
        },
        this.scriptLoader
      );
      
      await floatingAnimation.initialize();
      
      // Register with animation controller
      this.animationController.register('floating-homepage', floatingAnimation);
      this.animations.set('floating', floatingAnimation);
      
      console.log(`[App] Floating animation setup for ${floatingElements.length} elements`);
    }
    
    // Add parallax effect to specific elements in overview
    const parallaxElements = document.querySelectorAll('.parallax-element, [data-parallax]');
    
    if (parallaxElements.length > 0) {
      const parallaxAnimation = FloatingAnimation.createParallax(
        parallaxElements,
        {
          duration: 4000,
          distance: 25,
          rotation: 2
        },
        this.scriptLoader
      );
      
      await parallaxAnimation.initialize();
      
      this.animationController.register('parallax-homepage', parallaxAnimation);
      this.animations.set('parallax', parallaxAnimation);
      
      console.log(`[App] Parallax animation setup for ${parallaxElements.length} elements`);
    }
  }

  /**
   * Setup UI components (AI Attribution, etc.)
   * @returns {Promise<void>}
   */
  async setupUI() {
    // AI Attribution footer
    const footerContainer = document.querySelector('footer') || document.querySelector('.ai-attribution-container');
    
    if (footerContainer) {
      const aiAttribution = AIAttribution.createCursorAttribution(
        footerContainer,
        this.eventBus
      );
      
      aiAttribution.render();
      this.uiComponents.set('ai-attribution', aiAttribution);
      
      console.log('[App] AI Attribution component rendered');
    }
  }

  /**
   * Setup audio player
   * @returns {Promise<void>}
   */
  async setupAudioPlayer() {
    // Playlist data (from scripts.js)
    const playlistData = [
      {
        artist: "Kepler",
        title: "Deine Moves",
        album: "Deine Moves (Single)",
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
        src: "assets/audio/PLATZHALTER_02.mp3",
        cover: "assets/images/10_Es_Tut_Mir_Leid_Cover.png",
        spotifyID: "YOUR_SONG_ID_2"
      },
      {
        artist: "Kepler",
        title: "Für mich",
        album: "Für mich (Single)",
        year: "2023",
        src: "assets/audio/PLATZHALTER_03.mp3",
        cover: "assets/images/10_Es_Tut_Mir_Leid_Cover.png",
        spotifyID: "YOUR_SONG_ID_3"
      }
    ];
    
    // Get DOM elements
    const elements = {
      audioPlayer: document.getElementById('audio-player'),
      playPauseButton: document.getElementById('play-pause-button'),
      prevButton: document.getElementById('prev-button'),
      nextButton: document.getElementById('next-button'),
      albumCover: document.getElementById('album-cover'),
      marqueeContent: document.getElementById('marquee-content'),
      timeDisplay: document.getElementById('time-display'),
      playlistDropdown: document.getElementById('playlist-dropdown'),
      playlistToggleBtn: document.getElementById('playlist-toggle-btn')
    };
    
    // Check if required elements exist
    if (!elements.audioPlayer) {
      console.warn('[App] Audio player element not found, skipping audio setup');
      return;
    }
    
    // Create and initialize music player
    const musicPlayer = new MusicPlayer({
      playlistData,
      elements,
      eventBus: this.eventBus
    });
    
    await musicPlayer.initialize();
    
    this.uiComponents.set('music-player', musicPlayer);
    console.log('[App] Music player initialized');
  }

  /**
   * Setup navigation system
   * @returns {Promise<void>}
   */
  async setupNavigation() {
    // Create navigation state
    const navigationState = new NavigationState('activePage');
    
    // Create page navigator
    const pageNavigator = new PageNavigator(this.eventBus, navigationState);
    pageNavigator.initialize();
    
    // Create dropdown controllers
    const mainDropdown = new DropdownController({
      dropdown: document.getElementById('dropdown-menu'),
      toggleButton: document.getElementById('contents-toggle'),
      eventBus: this.eventBus,
      name: 'main-dropdown'
    });
    mainDropdown.initialize();
    
    // Setup dropdown item click handlers
    const dropdownItems = document.querySelectorAll('#dropdown-menu .dropdown-item');
    dropdownItems.forEach(item => {
      item.addEventListener('click', () => {
        const pageId = item.dataset.page;
        if (pageId) {
          pageNavigator.showPage(pageId, item, true);
        }
      });
    });
    
    // Store in components
    this.uiComponents.set('page-navigator', pageNavigator);
    this.uiComponents.set('main-dropdown', mainDropdown);
    this.uiComponents.set('navigation-state', navigationState);
    
    console.log('[App] Navigation system initialized');
  }

  /**
   * Setup journal system
   * @returns {Promise<void>}
   */
  async setupJournal() {
    const logbookContainer = document.getElementById('logbook-container');
    const timelineContainer = document.getElementById('timeline-list');
    
    if (!logbookContainer || !timelineContainer) {
      console.warn('[App] Journal containers not found, skipping journal setup');
      return;
    }
    
    // Create journal manager with image gallery integration
    const journalManager = new JournalManager({
      logbookContainer,
      timelineContainer,
      eventBus: this.eventBus,
      imageGallery: this.imageGallery
    });
    
    await journalManager.initialize();
    
    this.uiComponents.set('journal-manager', journalManager);
    console.log('[App] Journal system initialized');
  }

  /**
   * Setup markdown pages (Forschungsrahmen, Referenzen)
   * @returns {Promise<void>}
   */
  async setupMarkdownPages() {
    const markdownPageLoader = new MarkdownPageLoader(this.eventBus);
    
    // Define pages to load
    const pages = [
      { id: 'framework', file: 'docs/FORSCHUNGSRAHMEN.md', container: 'framework-content' },
      { id: 'references', file: 'docs/referenzen.md', container: 'references-content' }
    ];
    
    // Listen for page changes to lazy-load content
    this.eventBus.on('nav:pageChanged', async (data) => {
      const page = pages.find(p => p.id === data.pageId);
      if (page) {
        const container = document.getElementById(page.container);
        if (container && !container.dataset.loaded) {
          await markdownPageLoader.loadPage(page.file, container);
          container.dataset.loaded = 'true';
        }
      }
    });
    
    this.uiComponents.set('markdown-page-loader', markdownPageLoader);
    console.log('[App] Markdown pages setup');
  }

  /**
   * Setup media lazy loading
   * @returns {Promise<void>}
   */
  async setupMediaLazyLoading() {
    // Lazy load images
    const lazyImages = document.querySelectorAll('img[data-src], img[loading="lazy"]');
    if (lazyImages.length > 0) {
      // Prepare images for lazy loading
      lazyImages.forEach(img => {
        if (!img.dataset.src && img.src) {
          img.dataset.src = img.src;
          img.removeAttribute('src');
        }
      });
      
      this.lazyLoader.observe(lazyImages);
      console.log(`[App] Lazy loading setup for ${lazyImages.length} images`);
    }
    
    // Lazy load videos
    const lazyVideos = document.querySelectorAll('video[data-src]');
    if (lazyVideos.length > 0) {
      this.lazyLoader.observe(lazyVideos);
      console.log(`[App] Lazy loading setup for ${lazyVideos.length} videos`);
    }
    
    // Auto-initialize galleries from DOM
    this.imageGallery.autoInitialize();
  }

  /**
   * Start the application (begin animations, etc.)
   */
  start() {
    // Start animation controller
    if (this.animationController && this.animations.size > 0) {
      this.animationController.startAll();
      console.log('[App] Animations started');
    }
    
    this.eventBus.emit('app:started');
  }

  /**
   * Stop the application
   */
  stop() {
    if (this.animationController) {
      this.animationController.pauseAll();
    }
    
    this.eventBus.emit('app:stopped');
    console.log('[App] Application stopped');
  }

  /**
   * Dispose and cleanup all resources
   */
  dispose() {
    // Dispose controllers
    if (this.animationController) {
      this.animationController.disposeAll();
    }
    
    if (this.lazyLoader) {
      this.lazyLoader.dispose();
    }
    
    if (this.imageGallery) {
      this.imageGallery.dispose();
    }
    
    // Dispose viewers
    this.viewers.forEach(viewer => viewer.dispose());
    this.viewers.clear();
    
    // Dispose animations
    this.animations.forEach(animation => animation.dispose());
    this.animations.clear();
    
    // Dispose UI components
    this.uiComponents.forEach(component => component.dispose());
    this.uiComponents.clear();
    
    // Clear event bus
    if (this.eventBus) {
      this.eventBus.clear();
    }
    
    this.initialized = false;
    this.eventBus.emit('app:disposed');
    console.log('[App] Application disposed');
  }

  /**
   * Get application status and statistics
   * @returns {Object}
   */
  getStatus() {
    return {
      initialized: this.initialized,
      capabilities: this.capabilities,
      viewers: this.viewers.size,
      animations: this.animations.size,
      uiComponents: this.uiComponents.size,
      animationStats: this.animationController ? this.animationController.getStats() : null,
      lazyLoaderStats: this.lazyLoader ? this.lazyLoader.getStats() : null
    };
  }
}

// Create and export global app instance
const app = new Application();

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => app.initialize());
} else {
  app.initialize();
}

// Expose app globally for debugging (optional, can be removed in production)
if (typeof window !== 'undefined') {
  window.everythingMachineApp = app;
}

export default app;

