/**
 * EntryRenderer
 * Single responsibility: Render journal entries
 * Displays single entry with grid layout and animations
 */
import { TypingAnimation } from './TypingAnimation.js';
import { GridLayoutOptimizer } from './GridLayoutOptimizer.js';

export class EntryRenderer {
  /**
   * @param {HTMLElement} container - Container element for entries
   * @param {GridLayoutOptimizer} layoutOptimizer - Layout optimizer instance
   * @param {ImageGallery} imageGallery - Image gallery instance (optional)
   */
  constructor(container, layoutOptimizer, imageGallery = null) {
    if (!container) {
      throw new Error('[EntryRenderer] Container element required');
    }
    if (!layoutOptimizer) {
      throw new Error('[EntryRenderer] GridLayoutOptimizer required');
    }

    this.container = container;
    this.layoutOptimizer = layoutOptimizer;
    this.imageGallery = imageGallery;
    this.currentAnimation = null;
  }

  /**
   * Render an entry
   * @param {Object} entry - Entry object with html property
   */
  render(entry) {
    // Stop any existing animation
    if (this.currentAnimation) {
      this.currentAnimation.stop();
      this.currentAnimation = null;
    }
    
    // Insert HTML
    let html = entry.html;
    
    // Ensure content-grid wrapper exists
    if (!html.includes('content-grid')) {
      html = `<div class="content-grid">${html}</div>`;
    }
    
    this.container.innerHTML = html;
    
    // Get grid element
    const gridElement = this.container.querySelector('.content-grid');
    if (!gridElement) {
      console.warn('[EntryRenderer] No content-grid found');
      return;
    }
    
    // Setup image load listeners for layout optimization
    this.setupMediaLoadListeners(gridElement);
    
    // Initial layout optimization
    setTimeout(() => {
      this.layoutOptimizer.optimize(gridElement);
    }, 0);
    
    // Setup typing animation for title
    this.setupTypingAnimation(gridElement);
    
    // Initialize image lightbox/gallery
    this.initializeImageLightbox(gridElement);
    
    console.log('[EntryRenderer] Entry rendered');
  }

  /**
   * Initialize image lightbox for entry images
   * @param {HTMLElement} gridElement - Grid element
   */
  initializeImageLightbox(gridElement) {
    if (!this.imageGallery) {
      console.warn('[EntryRenderer] No ImageGallery instance available');
      return;
    }
    
    // Find all bubbles
    const bubbles = gridElement.querySelectorAll('.content-bubble');
    
    bubbles.forEach((bubble, bubbleIndex) => {
      // Find all images in this bubble
      const images = bubble.querySelectorAll('img');
      
      if (images.length === 0) return;
      
      // Register gallery for this bubble
      const galleryId = `journal-bubble-${bubbleIndex}`;
      this.imageGallery.registerGallery(galleryId, images);
    });
  }

  /**
   * Setup media load listeners to trigger layout optimization
   * @param {HTMLElement} gridElement - Grid element
   */
  setupMediaLoadListeners(gridElement) {
    const mediaElements = gridElement.querySelectorAll('img, video');
    
    const requestOptimize = () => {
      window.requestAnimationFrame(() => {
        this.layoutOptimizer.optimize(gridElement);
      });
    };
    
    mediaElements.forEach(element => {
      if (element.complete || element.readyState >= 2) {
        requestOptimize();
      } else {
        element.addEventListener('load', requestOptimize, { once: true });
        element.addEventListener('error', requestOptimize, { once: true });
      }
    });
  }

  /**
   * Setup typing animation for title
   * @param {HTMLElement} gridElement - Grid element
   */
  setupTypingAnimation(gridElement) {
    const titleElement = this.container.querySelector('.journal-title');
    if (!titleElement) return;
    
    const text = titleElement.dataset.fullText || titleElement.textContent.trim();
    const titleBubble = titleElement.closest('.content-bubble');
    
    if (!titleBubble) return;
    
    // Set typing animation active flag
    this.layoutOptimizer.setTypingAnimationActive(true);
    
    // Track last height for optimization
    let lastTitleBubbleHeight = titleBubble.offsetHeight;
    let layoutUpdateScheduled = false;
    
    // Create typing animation
    this.currentAnimation = new TypingAnimation(titleElement, text, {
      speed: 55,
      speedVariation: 45,
      onProgress: () => {
        // Schedule layout update on character add
        if (layoutUpdateScheduled) return;
        layoutUpdateScheduled = true;
        
        requestAnimationFrame(() => {
          const currentHeight = titleBubble.offsetHeight;
          const heightDiff = Math.abs(currentHeight - lastTitleBubbleHeight);
          
          if (heightDiff > 1) {
            lastTitleBubbleHeight = currentHeight;
            this.layoutOptimizer.optimize(gridElement);
          }
          
          layoutUpdateScheduled = false;
        });
      },
      onComplete: () => {
        // Final layout update
        requestAnimationFrame(() => {
          this.layoutOptimizer.optimize(gridElement);
        });
        
        // Reset typing flag
        setTimeout(() => {
          this.layoutOptimizer.setTypingAnimationActive(false);
        }, 300);
      }
    });
    
    // Start animation after delay
    setTimeout(() => {
      this.currentAnimation.start();
    }, 300);
  }

  /**
   * Clear the container
   */
  clear() {
    if (this.currentAnimation) {
      this.currentAnimation.stop();
      this.currentAnimation = null;
    }
    this.container.innerHTML = '';
  }

  /**
   * Dispose and clean up
   */
  dispose() {
    this.clear();
  }
}

