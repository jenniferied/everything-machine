/**
 * GaussianSplatViewer - Viewer for 3D Gaussian Splats
 * Uses the antimatter15/splat WebGL viewer approach
 *
 * Open Source Examples:
 * - https://huggingface.co/datasets/Voxel51/gaussian_splatting
 * - https://antimatter15.com/splat/
 */
import { ViewerBase } from './ViewerBase.js';

export class GaussianSplatViewer extends ViewerBase {
  constructor(container, options = {}, eventBus = null, scriptLoader = null, featureDetector = null) {
    super(container, options, eventBus);

    this.scriptLoader = scriptLoader;
    this.featureDetector = featureDetector;

    // Viewer state
    this.canvas = null;
    this.gl = null;
    this.animationFrameId = null;
    this.isAnimating = true;
    this.rotation = 0;
    this.rotationY = 0;  // Horizontal rotation (user controlled)
    this.rotationX = 0;  // Vertical rotation (user controlled)
    this.autoRotation = 0; // Auto-rotation component
    this.zoom = 5;       // Camera distance

    // Mouse interaction state
    this.isDragging = false;
    this.lastMouseX = 0;
    this.lastMouseY = 0;

    // Demo splat data
    this.splatData = null;
  }

  async checkSupport() {
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl2');
      return !!gl;
    } catch (e) {
      return false;
    }
  }

  async loadDependencies() {
    // No external dependencies needed for demo
    console.log('[GaussianSplatViewer] Dependencies ready');
  }

  async initialize() {
    const width = this.container.clientWidth || 600;
    const height = this.container.clientHeight || 280;

    // Create canvas
    this.canvas = document.createElement('canvas');
    this.canvas.width = width;
    this.canvas.height = height;
    this.canvas.style.cssText = 'display: block; width: 100%; height: 100%;';

    // Get WebGL2 context
    this.gl = this.canvas.getContext('webgl2', {
      antialias: true,
      alpha: false,
      preserveDrawingBuffer: true
    });

    if (!this.gl) {
      throw new Error('WebGL2 not supported');
    }

    // Clear container and add canvas
    this.container.innerHTML = '';
    this.container.style.position = 'relative';
    this.container.appendChild(this.canvas);

    // Create control panel
    this.createControlPanel();

    // Setup mouse interaction
    this.setupMouseControls();

    // Handle resize
    this.resizeHandler = () => this.onResize();
    window.addEventListener('resize', this.resizeHandler);

    console.log('[GaussianSplatViewer] Initialized');
  }

  setupMouseControls() {
    // Mouse down - start dragging
    this.canvas.addEventListener('mousedown', (e) => {
      this.isDragging = true;
      this.lastMouseX = e.clientX;
      this.lastMouseY = e.clientY;
      this.canvas.style.cursor = 'grabbing';
    });

    // Mouse move - rotate
    this.canvas.addEventListener('mousemove', (e) => {
      if (!this.isDragging) return;

      const deltaX = e.clientX - this.lastMouseX;
      const deltaY = e.clientY - this.lastMouseY;

      this.rotationY += deltaX * 0.01;
      this.rotationX += deltaY * 0.01;

      // Clamp vertical rotation
      this.rotationX = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, this.rotationX));

      this.lastMouseX = e.clientX;
      this.lastMouseY = e.clientY;
    });

    // Mouse up - stop dragging
    window.addEventListener('mouseup', () => {
      this.isDragging = false;
      this.canvas.style.cursor = 'grab';
    });

    // Mouse wheel - zoom
    this.canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      this.zoom += e.deltaY * 0.01;
      this.zoom = Math.max(2, Math.min(15, this.zoom));
    }, { passive: false });

    // Touch support
    this.canvas.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        this.isDragging = true;
        this.lastMouseX = e.touches[0].clientX;
        this.lastMouseY = e.touches[0].clientY;
      }
    });

    this.canvas.addEventListener('touchmove', (e) => {
      if (!this.isDragging || e.touches.length !== 1) return;
      e.preventDefault();

      const deltaX = e.touches[0].clientX - this.lastMouseX;
      const deltaY = e.touches[0].clientY - this.lastMouseY;

      this.rotationY += deltaX * 0.01;
      this.rotationX += deltaY * 0.01;
      this.rotationX = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, this.rotationX));

      this.lastMouseX = e.touches[0].clientX;
      this.lastMouseY = e.touches[0].clientY;
    }, { passive: false });

    this.canvas.addEventListener('touchend', () => {
      this.isDragging = false;
    });

    // Set initial cursor
    this.canvas.style.cursor = 'grab';
  }

  async render() {
    // Create demo gaussian splat visualization
    this.createDemoSplats();
    this.animate();
  }

  /**
   * Create a demo visualization representing gaussian splats
   * Real gaussian splats would load .ply or .splat files
   */
  createDemoSplats() {
    const gl = this.gl;

    // Vertex shader - renders splats as points with gaussian falloff
    const vsSource = `#version 300 es
      in vec3 aPosition;
      in vec3 aColor;
      in float aSize;

      uniform mat4 uProjection;
      uniform mat4 uView;
      uniform float uRotationX;
      uniform float uRotationY;

      out vec3 vColor;
      out float vSize;

      void main() {
        // Rotation around Y axis (horizontal drag)
        float cy = cos(uRotationY);
        float sy = sin(uRotationY);
        mat3 rotY = mat3(
          cy, 0.0, sy,
          0.0, 1.0, 0.0,
          -sy, 0.0, cy
        );

        // Rotation around X axis (vertical drag)
        float cx = cos(uRotationX);
        float sx = sin(uRotationX);
        mat3 rotX = mat3(
          1.0, 0.0, 0.0,
          0.0, cx, -sx,
          0.0, sx, cx
        );

        vec3 rotatedPos = rotY * rotX * aPosition;
        vec4 viewPos = uView * vec4(rotatedPos, 1.0);
        gl_Position = uProjection * viewPos;

        // Size attenuation
        float dist = length(viewPos.xyz);
        gl_PointSize = aSize * 300.0 / dist;

        vColor = aColor;
        vSize = aSize;
      }
    `;

    // Fragment shader - gaussian splat appearance
    const fsSource = `#version 300 es
      precision highp float;

      in vec3 vColor;
      in float vSize;
      out vec4 fragColor;

      void main() {
        vec2 center = gl_PointCoord - vec2(0.5);
        float dist = length(center) * 2.0;

        // Gaussian falloff
        float alpha = exp(-dist * dist * 4.0);

        if (alpha < 0.01) discard;

        // Soft glow effect
        vec3 color = vColor * (1.0 + alpha * 0.5);
        fragColor = vec4(color, alpha * 0.8);
      }
    `;

    // Compile shaders
    const vs = this.compileShader(gl.VERTEX_SHADER, vsSource);
    const fs = this.compileShader(gl.FRAGMENT_SHADER, fsSource);

    // Create program
    this.program = gl.createProgram();
    gl.attachShader(this.program, vs);
    gl.attachShader(this.program, fs);
    gl.linkProgram(this.program);

    if (!gl.getProgramParameter(this.program, gl.LINK_STATUS)) {
      console.error('[GaussianSplatViewer] Program link error:', gl.getProgramInfoLog(this.program));
      return;
    }

    // Generate splat data - create a stylized bust/head shape
    // Resembles a 3D scanned sculpture
    const splatCount = 8000;
    const positions = [];
    const colors = [];
    const sizes = [];

    for (let i = 0; i < splatCount; i++) {
      let x, y, z, accepted = false;

      // Use rejection sampling to create a bust-like shape
      while (!accepted) {
        // Random point in bounding box
        x = (Math.random() - 0.5) * 3;
        y = (Math.random() - 0.5) * 4;
        z = (Math.random() - 0.5) * 3;

        // Head shape (ellipsoid, higher up)
        const headY = y - 0.8;
        const headDist = (x * x) / 0.64 + (headY * headY) / 1.0 + (z * z) / 0.64;

        // Neck (cylinder, middle)
        const neckY = y + 0.3;
        const neckDist = (x * x + z * z) / 0.16;
        const inNeck = neckDist < 1 && neckY > -0.5 && neckY < 0.5;

        // Shoulders (ellipsoid, lower)
        const shoulderY = y + 1.2;
        const shoulderDist = (x * x) / 1.44 + (shoulderY * shoulderY) / 0.25 + (z * z) / 0.36;

        // Accept if near surface of any component
        const headSurface = Math.abs(headDist - 1) < 0.15 && headY < 0.8;
        const neckSurface = inNeck;
        const shoulderSurface = Math.abs(shoulderDist - 1) < 0.2 && shoulderY > 0;

        if (headSurface || neckSurface || shoulderSurface) {
          accepted = true;

          // Add slight surface noise
          const noise = (Math.random() - 0.5) * 0.08;
          x += noise;
          z += noise;
        }
      }

      positions.push(x, y, z);

      // Skin-like color with subtle variation (marble/bronze statue look)
      const baseHue = 30; // Orange/bronze
      const hueVar = (Math.random() - 0.5) * 20;
      const hue = (baseHue + hueVar) / 360;
      const sat = 0.3 + Math.random() * 0.2;
      const light = 0.5 + y * 0.1 + Math.random() * 0.1;

      // Convert HSL to RGB
      const rgb = this.hslToRgb(hue, sat, Math.max(0.3, Math.min(0.8, light)));
      colors.push(rgb.r, rgb.g, rgb.b);

      // Varying splat sizes for organic feel
      const sizeBase = 0.025;
      const sizeVar = Math.random() * 0.02;
      sizes.push(sizeBase + sizeVar);
    }

    // Create buffers
    this.positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);

    this.colorBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.colorBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colors), gl.STATIC_DRAW);

    this.sizeBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.sizeBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(sizes), gl.STATIC_DRAW);

    this.splatCount = splatCount;

    // Get attribute/uniform locations
    this.aPosition = gl.getAttribLocation(this.program, 'aPosition');
    this.aColor = gl.getAttribLocation(this.program, 'aColor');
    this.aSize = gl.getAttribLocation(this.program, 'aSize');
    this.uProjection = gl.getUniformLocation(this.program, 'uProjection');
    this.uView = gl.getUniformLocation(this.program, 'uView');
    this.uRotationX = gl.getUniformLocation(this.program, 'uRotationX');
    this.uRotationY = gl.getUniformLocation(this.program, 'uRotationY');

    console.log('[GaussianSplatViewer] Demo splats created:', splatCount);
  }

  compileShader(type, source) {
    const gl = this.gl;
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.error('[GaussianSplatViewer] Shader compile error:', gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  }

  /**
   * Convert HSL to RGB
   */
  hslToRgb(h, s, l) {
    let r, g, b;
    if (s === 0) {
      r = g = b = l;
    } else {
      const hue2rgb = (p, q, t) => {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1/6) return p + (q - p) * 6 * t;
        if (t < 1/2) return q;
        if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
        return p;
      };
      const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      const p = 2 * l - q;
      r = hue2rgb(p, q, h + 1/3);
      g = hue2rgb(p, q, h);
      b = hue2rgb(p, q, h - 1/3);
    }
    return { r, g, b };
  }

  animate() {
    if (!this.gl || !this.program) return;

    this.animationFrameId = requestAnimationFrame(() => this.animate());

    const gl = this.gl;
    const width = this.canvas.width;
    const height = this.canvas.height;

    // Clear
    gl.viewport(0, 0, width, height);
    gl.clearColor(0.067, 0.067, 0.067, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // Enable blending for transparent splats
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.enable(gl.DEPTH_TEST);
    gl.depthMask(false);

    gl.useProgram(this.program);

    // Projection matrix (perspective)
    const fov = 60 * Math.PI / 180;
    const aspect = width / height;
    const near = 0.1;
    const far = 100;
    const f = 1.0 / Math.tan(fov / 2);
    const projection = new Float32Array([
      f / aspect, 0, 0, 0,
      0, f, 0, 0,
      0, 0, (far + near) / (near - far), -1,
      0, 0, (2 * far * near) / (near - far), 0
    ]);

    // View matrix (camera looking at origin, distance controlled by zoom)
    const view = new Float32Array([
      1, 0, 0, 0,
      0, 1, 0, 0,
      0, 0, 1, 0,
      0, 0, -this.zoom, 1
    ]);

    gl.uniformMatrix4fv(this.uProjection, false, projection);
    gl.uniformMatrix4fv(this.uView, false, view);

    // Update auto-rotation when not dragging
    if (this.isAnimating && !this.isDragging) {
      this.autoRotation += 0.004;
    }

    // Combine auto-rotation with user rotation
    gl.uniform1f(this.uRotationX, this.rotationX);
    gl.uniform1f(this.uRotationY, this.rotationY + this.autoRotation);

    // Bind attributes
    gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);
    gl.enableVertexAttribArray(this.aPosition);
    gl.vertexAttribPointer(this.aPosition, 3, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ARRAY_BUFFER, this.colorBuffer);
    gl.enableVertexAttribArray(this.aColor);
    gl.vertexAttribPointer(this.aColor, 3, gl.FLOAT, false, 0, 0);

    gl.bindBuffer(gl.ARRAY_BUFFER, this.sizeBuffer);
    gl.enableVertexAttribArray(this.aSize);
    gl.vertexAttribPointer(this.aSize, 1, gl.FLOAT, false, 0, 0);

    // Draw
    gl.drawArrays(gl.POINTS, 0, this.splatCount);

    gl.depthMask(true);
  }

  createControlPanel() {
    this.controlPanel = document.createElement('div');
    this.controlPanel.style.cssText = `
      position: absolute;
      bottom: 10px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      background: rgba(17, 17, 17, 0.95);
      border: 1px solid #4ade80;
      border-radius: 8px;
      z-index: 10;
      font-family: 'IBM Plex Mono', monospace;
    `;

    const animBtn = this.isAnimating ? '⏸' : '▶';
    this.controlPanel.innerHTML = `
      <button data-action="toggle" style="
        width: 32px; height: 32px; background: #1f2937; border: 1px solid #374151;
        border-radius: 6px; color: #4ade80; cursor: pointer; font-size: 14px;
      ">${animBtn}</button>
      <span style="color: #9ca3af; font-size: 11px; text-transform: uppercase;">
        3DGS Bust (8K splats)
      </span>
      <a href="https://huggingface.co/datasets/Voxel51/gaussian_splatting" target="_blank"
         style="color: #4ade80; font-size: 11px; opacity: 0.7;">[Examples]</a>
    `;

    this.controlPanel.addEventListener('click', (e) => {
      const btn = e.target.closest('button');
      if (btn) {
        this.isAnimating = !this.isAnimating;
        btn.textContent = this.isAnimating ? '⏸' : '▶';
      }
    });

    this.container.appendChild(this.controlPanel);
  }

  onResize() {
    if (!this.canvas || !this.container) return;
    this.canvas.width = this.container.clientWidth;
    this.canvas.height = this.container.clientHeight || 280;
  }

  showFallback() {
    this.container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: center; height: 100%;
                  background: #1f2937; color: #9ca3af; text-align: center; padding: 20px;">
        <div>
          <p style="margin-bottom: 10px;">WebGL2 required for Gaussian Splats</p>
          <a href="https://antimatter15.com/splat/" target="_blank" style="color: #4ade80;">
            View examples online →
          </a>
        </div>
      </div>
    `;
  }

  dispose() {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
    if (this.resizeHandler) {
      window.removeEventListener('resize', this.resizeHandler);
    }
    if (this.gl) {
      if (this.positionBuffer) this.gl.deleteBuffer(this.positionBuffer);
      if (this.colorBuffer) this.gl.deleteBuffer(this.colorBuffer);
      if (this.sizeBuffer) this.gl.deleteBuffer(this.sizeBuffer);
      if (this.program) this.gl.deleteProgram(this.program);
    }
    this.emitEvent('viewer:disposed', { viewer: 'GaussianSplatViewer' });
  }
}
