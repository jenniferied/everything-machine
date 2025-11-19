/**
 * ThreeDViewer - Concrete implementation of ViewerBase
 * Implements Three.js 3D model viewer with WebGL detection
 */
import { ViewerBase } from './ViewerBase.js';

export class ThreeDViewer extends ViewerBase {
  constructor(container, options = {}, eventBus = null, scriptLoader = null, featureDetector = null) {
    super(container, options, eventBus);
    
    this.scriptLoader = scriptLoader;
    this.featureDetector = featureDetector;
    
    // Three.js objects
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.model = null;
    this.animationFrameId = null;
    this.controls = null;
    
    // Configuration
    this.modelPath = options.modelPath || null;
    this.autoRotate = options.autoRotate !== false;
    this.cameraDistance = options.cameraDistance || 5;
  }

  /**
   * Check if WebGL is supported
   * @returns {Promise<boolean>}
   */
  async checkSupport() {
    if (this.featureDetector) {
      const caps = this.featureDetector.getCapabilities();
      return caps.webgl && !caps.reducedMotion;
    }
    
    // Fallback check
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      return !!gl;
    } catch (e) {
      return false;
    }
  }

  /**
   * Load Three.js library dynamically
   * @returns {Promise<void>}
   */
  async loadDependencies() {
    if (!this.scriptLoader) {
      throw new Error('ScriptLoader required for ThreeDViewer');
    }

    // Load Three.js from CDN
    const threeUrl = 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js';
    await this.scriptLoader.loadScript(threeUrl);
    
    // Check if THREE is available globally
    if (typeof THREE === 'undefined') {
      throw new Error('Three.js failed to load');
    }
  }

  /**
   * Initialize Three.js scene, camera, and renderer
   * @returns {Promise<void>}
   */
  async initialize() {
    if (!window.THREE) {
      throw new Error('THREE is not available');
    }

    const width = this.container.clientWidth;
    const height = this.container.clientHeight || 400;

    // Create scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x111111);

    // Create camera
    this.camera = new THREE.PerspectiveCamera(
      75,
      width / height,
      0.1,
      1000
    );
    this.camera.position.z = this.cameraDistance;

    // Create renderer
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true
    });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    
    // Clear container and add renderer
    this.container.innerHTML = '';
    this.container.appendChild(this.renderer.domElement);

    // Add lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    this.scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 5, 5);
    this.scene.add(directionalLight);

    // Handle window resize
    this.resizeHandler = () => this.onWindowResize();
    window.addEventListener('resize', this.resizeHandler);
  }

  /**
   * Render the 3D content
   * @returns {Promise<void>}
   */
  async render() {
    // Create placeholder geometry if no model path provided
    if (!this.modelPath) {
      this.createPlaceholderModel();
    } else {
      await this.loadModel(this.modelPath);
    }

    // Start animation loop
    this.animate();
  }

  /**
   * Create a placeholder 3D model (cube)
   */
  createPlaceholderModel() {
    const geometry = new THREE.BoxGeometry(2, 2, 2);
    const material = new THREE.MeshPhongMaterial({
      color: 0x4ade80,
      emissive: 0x2a7a4a,
      shininess: 100,
      wireframe: false
    });
    
    this.model = new THREE.Mesh(geometry, material);
    this.scene.add(this.model);
    
    // Add wireframe overlay
    const wireframeGeometry = new THREE.EdgesGeometry(geometry);
    const wireframeMaterial = new THREE.LineBasicMaterial({ color: 0x86efac });
    const wireframe = new THREE.LineSegments(wireframeGeometry, wireframeMaterial);
    this.model.add(wireframe);
  }

  /**
   * Load a 3D model (GLTF/GLB format)
   * @param {string} path - Path to model file
   * @returns {Promise<void>}
   */
  async loadModel(path) {
    // This would require GLTFLoader
    // For now, fallback to placeholder
    console.log(`[ThreeDViewer] Model loading not yet implemented: ${path}`);
    this.createPlaceholderModel();
  }

  /**
   * Animation loop
   */
  animate() {
    this.animationFrameId = requestAnimationFrame(() => this.animate());

    // Rotate model
    if (this.model && this.autoRotate) {
      this.model.rotation.y += 0.005;
      this.model.rotation.x += 0.002;
    }

    this.renderer.render(this.scene, this.camera);
  }

  /**
   * Handle window resize
   */
  onWindowResize() {
    const width = this.container.clientWidth;
    const height = this.container.clientHeight || 400;

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height);
  }

  /**
   * Show static fallback image
   */
  showFallback() {
    this.fallbackShown = true;
    
    const fallbackPath = this.options.fallbackImage || 'https://placehold.co/600x400/1f2937/4ade80?text=3D+Model';
    
    this.container.innerHTML = `
      <div class="viewer-fallback">
        <img src="${fallbackPath}" alt="3D Model Preview" class="viewer-fallback-image" />
        <p class="viewer-fallback-text">3D Viewer not supported on this device</p>
      </div>
    `;
  }

  /**
   * Cleanup resources
   */
  dispose() {
    // Stop animation loop
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }

    // Remove event listeners
    if (this.resizeHandler) {
      window.removeEventListener('resize', this.resizeHandler);
    }

    // Dispose Three.js objects
    if (this.renderer) {
      this.renderer.dispose();
      if (this.renderer.domElement && this.renderer.domElement.parentNode) {
        this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
      }
    }

    if (this.model) {
      if (this.model.geometry) this.model.geometry.dispose();
      if (this.model.material) {
        if (Array.isArray(this.model.material)) {
          this.model.material.forEach(mat => mat.dispose());
        } else {
          this.model.material.dispose();
        }
      }
    }

    // Clear references
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.model = null;

    this.emitEvent('viewer:disposed', { viewer: this.constructor.name });
  }
}

