/**
 * PointCloudViewer - Simple WebGL2 Point Cloud Viewer
 * Self-contained without Three.js dependency for reliability
 */
import { ViewerBase } from './ViewerBase.js';

export class PointCloudViewer extends ViewerBase {
  constructor(container, options = {}, eventBus = null, scriptLoader = null, featureDetector = null) {
    super(container, options, eventBus);

    this.scriptLoader = scriptLoader;
    this.featureDetector = featureDetector;

    this.canvas = null;
    this.gl = null;
    this.program = null;
    this.animationFrameId = null;
    this.isAnimating = true;
    this.rotation = 0;
    this.rotationY = 0;
    this.rotationX = 0;
    this.autoRotation = 0;
    this.zoom = 8;
    this.pointCount = 0;

    // FPS limiting
    this.lastFrameTime = 0;
    this.targetFPS = 24;
    this.frameInterval = 1000 / this.targetFPS;

    // Mouse interaction state
    this.isDragging = false;
    this.lastMouseX = 0;
    this.lastMouseY = 0;
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
    console.log('[PointCloudViewer] No external dependencies needed');
  }

  async initialize() {
    const width = this.container.clientWidth || 600;
    const height = this.container.clientHeight || 280;

    console.log('[PointCloudViewer] Initializing:', width, 'x', height);

    // Clear container
    this.container.innerHTML = '';
    this.container.style.position = 'relative';

    // Create wrapper for flex layout (canvas + controls)
    this.wrapper = document.createElement('div');
    this.wrapper.style.cssText = `
      display: flex;
      flex-direction: column;
      width: 100%;
      height: 100%;
    `;

    // Create canvas
    this.canvas = document.createElement('canvas');
    this.canvas.width = width;
    this.canvas.height = height - 32; // Leave room for controls
    this.canvas.style.cssText = 'display: block; width: 100%; flex: 1;';

    // Get WebGL2 context
    this.gl = this.canvas.getContext('webgl2', {
      antialias: true,
      alpha: false
    });

    if (!this.gl) {
      throw new Error('WebGL2 not available');
    }

    this.wrapper.appendChild(this.canvas);
    this.container.appendChild(this.wrapper);

    // Setup shaders
    this.setupShaders();

    // Show loading indicator
    this.showLoadingIndicator();

    // Load real PLY data
    await this.loadPLYData();

    // Create control panel (under canvas)
    this.createControlPanel();

    // Setup mouse interaction
    this.setupMouseControls();

    // Resize handler
    this.resizeHandler = () => this.onResize();
    window.addEventListener('resize', this.resizeHandler);

    console.log('[PointCloudViewer] Initialized successfully');
  }

  setupMouseControls() {
    this.canvas.addEventListener('mousedown', (e) => {
      this.isDragging = true;
      this.lastMouseX = e.clientX;
      this.lastMouseY = e.clientY;
      this.canvas.style.cursor = 'grabbing';
    });

    this.canvas.addEventListener('mousemove', (e) => {
      if (!this.isDragging) return;

      const deltaX = e.clientX - this.lastMouseX;
      const deltaY = e.clientY - this.lastMouseY;

      this.rotationY += deltaX * 0.01;
      this.rotationX += deltaY * 0.01;
      this.rotationX = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, this.rotationX));

      this.lastMouseX = e.clientX;
      this.lastMouseY = e.clientY;
    });

    window.addEventListener('mouseup', () => {
      this.isDragging = false;
      this.canvas.style.cursor = 'grab';
    });

    this.canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      this.zoom += e.deltaY * 0.01;
      this.zoom = Math.max(3, Math.min(20, this.zoom));
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

    this.canvas.style.cursor = 'grab';
  }

  setupShaders() {
    const gl = this.gl;

    const vsSource = `#version 300 es
      in vec3 aPosition;
      in vec3 aColor;

      uniform mat4 uProjection;
      uniform mat4 uView;
      uniform float uRotationX;
      uniform float uRotationY;
      uniform float uPointSize;

      out vec3 vColor;

      void main() {
        float cy = cos(uRotationY);
        float sy = sin(uRotationY);
        mat3 rotY = mat3(
          cy, 0.0, sy,
          0.0, 1.0, 0.0,
          -sy, 0.0, cy
        );

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

        float dist = length(viewPos.xyz);
        gl_PointSize = uPointSize * 8.0 / dist;

        vColor = aColor;
      }
    `;

    const fsSource = `#version 300 es
      precision highp float;
      in vec3 vColor;
      out vec4 fragColor;

      void main() {
        vec2 coord = gl_PointCoord - vec2(0.5);
        float dist = length(coord);
        if (dist > 0.5) discard;

        float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
        fragColor = vec4(vColor, alpha);
      }
    `;

    const vs = this.compileShader(gl.VERTEX_SHADER, vsSource);
    const fs = this.compileShader(gl.FRAGMENT_SHADER, fsSource);

    this.program = gl.createProgram();
    gl.attachShader(this.program, vs);
    gl.attachShader(this.program, fs);
    gl.linkProgram(this.program);

    if (!gl.getProgramParameter(this.program, gl.LINK_STATUS)) {
      console.error('[PointCloudViewer] Program link error:', gl.getProgramInfoLog(this.program));
    }

    this.aPosition = gl.getAttribLocation(this.program, 'aPosition');
    this.aColor = gl.getAttribLocation(this.program, 'aColor');
    this.uProjection = gl.getUniformLocation(this.program, 'uProjection');
    this.uView = gl.getUniformLocation(this.program, 'uView');
    this.uRotationX = gl.getUniformLocation(this.program, 'uRotationX');
    this.uRotationY = gl.getUniformLocation(this.program, 'uRotationY');
    this.uPointSize = gl.getUniformLocation(this.program, 'uPointSize');
  }

  compileShader(type, source) {
    const gl = this.gl;
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.error('[PointCloudViewer] Shader error:', gl.getShaderInfoLog(shader));
      return null;
    }
    return shader;
  }

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

  showLoadingIndicator() {
    this.loadingEl = document.createElement('div');
    this.loadingEl.style.cssText = `
      position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
      color: #4ade80; font-family: 'IBM Plex Mono', monospace; font-size: 12px;
      text-align: center;
    `;
    this.loadingEl.innerHTML = 'Loading point cloud...';
    this.container.appendChild(this.loadingEl);
  }

  async loadPLYData() {
    const gl = this.gl;
    // Stanford Bunny PLY (not gzipped, much smaller than Dragon)
    const plyUrl = 'https://raw.githubusercontent.com/naucoin/VTKData/master/Data/bunny.ply';

    try {
      console.log('[PointCloudViewer] Fetching Stanford Bunny PLY:', plyUrl);
      const response = await fetch(plyUrl);

      // No decompression needed for this PLY
      const arrayBuffer = await response.arrayBuffer();

      const { positions, colors, count } = this.parsePLY(arrayBuffer);

      if (this.loadingEl) {
        this.loadingEl.remove();
      }

      this.vao = gl.createVertexArray();
      gl.bindVertexArray(this.vao);

      this.posBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, this.posBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);
      gl.enableVertexAttribArray(this.aPosition);
      gl.vertexAttribPointer(this.aPosition, 3, gl.FLOAT, false, 0, 0);

      this.colorBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, this.colorBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colors), gl.STATIC_DRAW);
      gl.enableVertexAttribArray(this.aColor);
      gl.vertexAttribPointer(this.aColor, 3, gl.FLOAT, false, 0, 0);

      gl.bindVertexArray(null);
      this.pointCount = count;

      console.log('[PointCloudViewer] Loaded', count, 'points from PLY');
      this.modelName = 'Stanford Bunny';

      // Update label after control panel is created
      setTimeout(() => {
        const label = this.controlPanel?.querySelector('.model-label');
        if (label) {
          label.textContent = `Stanford Bunny (${(count / 1000).toFixed(0)}K pts)`;
        }
      }, 100);

    } catch (error) {
      console.error('[PointCloudViewer] Failed to load PLY:', error);
      this.createFallbackPointCloud();
    }
  }

  parsePLY(arrayBuffer) {
    const textDecoder = new TextDecoder();
    const text = textDecoder.decode(arrayBuffer);

    // Parse PLY header
    const headerEndIndex = text.indexOf('end_header');
    if (headerEndIndex === -1) {
      throw new Error('Invalid PLY: no end_header');
    }

    const header = text.substring(0, headerEndIndex);
    const vertexMatch = header.match(/element vertex (\d+)/);
    const vertexCount = vertexMatch ? parseInt(vertexMatch[1]) : 0;

    // Check format
    const isBinary = header.includes('format binary');
    const isAscii = header.includes('format ascii');

    console.log('[PointCloudViewer] PLY format:', isBinary ? 'binary' : 'ascii', 'vertices:', vertexCount);

    if (isBinary) {
      return this.parseBinaryPLY(arrayBuffer, header, vertexCount);
    } else {
      return this.parseAsciiPLY(text, headerEndIndex, vertexCount);
    }
  }

  parseBinaryPLY(arrayBuffer, header, vertexCount) {
    // Find data start (after "end_header\n")
    const uint8 = new Uint8Array(arrayBuffer);
    let dataStart = 0;
    for (let i = 0; i < Math.min(2000, uint8.length - 10); i++) {
      if (uint8[i] === 101 && uint8[i+1] === 110 && uint8[i+2] === 100 &&
          uint8[i+3] === 95 && uint8[i+4] === 104) { // "end_h"
        // Find newline after end_header
        for (let j = i; j < i + 20; j++) {
          if (uint8[j] === 10) {
            dataStart = j + 1;
            break;
          }
        }
        break;
      }
    }

    const dataView = new DataView(arrayBuffer, dataStart);
    const positions = [];
    const colors = [];

    // Bounds for normalization
    let minX = Infinity, maxX = -Infinity;
    let minY = Infinity, maxY = -Infinity;
    let minZ = Infinity, maxZ = -Infinity;

    const rawPoints = [];

    // Read vertices (assuming x, y, z as float32)
    for (let i = 0; i < vertexCount; i++) {
      const offset = i * 12; // 3 floats * 4 bytes
      if (offset + 12 > dataView.byteLength) break;

      const x = dataView.getFloat32(offset, true);
      const y = dataView.getFloat32(offset + 4, true);
      const z = dataView.getFloat32(offset + 8, true);

      if (isFinite(x) && isFinite(y) && isFinite(z)) {
        rawPoints.push({ x, y, z });
        minX = Math.min(minX, x); maxX = Math.max(maxX, x);
        minY = Math.min(minY, y); maxY = Math.max(maxY, y);
        minZ = Math.min(minZ, z); maxZ = Math.max(maxZ, z);
      }
    }

    // Center and scale
    const centerX = (minX + maxX) / 2;
    const centerY = (minY + maxY) / 2;
    const centerZ = (minZ + maxZ) / 2;
    const maxDim = Math.max(maxX - minX, maxY - minY, maxZ - minZ);
    const scale = 5 / maxDim;

    for (const { x, y, z } of rawPoints) {
      positions.push(
        (x - centerX) * scale,
        (y - centerY) * scale,
        (z - centerZ) * scale
      );

      // Golden/bronze color for dragon (no RGB in file)
      const brightness = 0.4 + Math.random() * 0.2;
      colors.push(0.85 * brightness, 0.65 * brightness, 0.35 * brightness);
    }

    return { positions, colors, count: rawPoints.length };
  }

  parseAsciiPLY(text, headerEndIndex, vertexCount) {
    const dataStart = headerEndIndex + 11; // "end_header\n"
    const lines = text.substring(dataStart).trim().split('\n');

    const positions = [];
    const colors = [];

    let minX = Infinity, maxX = -Infinity;
    let minY = Infinity, maxY = -Infinity;
    let minZ = Infinity, maxZ = -Infinity;

    const rawPoints = [];

    for (let i = 0; i < Math.min(vertexCount, lines.length); i++) {
      const parts = lines[i].trim().split(/\s+/);
      if (parts.length >= 3) {
        const x = parseFloat(parts[0]);
        const y = parseFloat(parts[1]);
        const z = parseFloat(parts[2]);

        if (isFinite(x) && isFinite(y) && isFinite(z)) {
          rawPoints.push({ x, y, z });
          minX = Math.min(minX, x); maxX = Math.max(maxX, x);
          minY = Math.min(minY, y); maxY = Math.max(maxY, y);
          minZ = Math.min(minZ, z); maxZ = Math.max(maxZ, z);
        }
      }
    }

    const centerX = (minX + maxX) / 2;
    const centerY = (minY + maxY) / 2;
    const centerZ = (minZ + maxZ) / 2;
    const maxDim = Math.max(maxX - minX, maxY - minY, maxZ - minZ);
    const scale = 5 / maxDim;

    for (const { x, y, z } of rawPoints) {
      positions.push(
        (x - centerX) * scale,
        (y - centerY) * scale,
        (z - centerZ) * scale
      );

      // Golden/bronze color for dragon
      const brightness = 0.4 + Math.random() * 0.2;
      colors.push(0.85 * brightness, 0.65 * brightness, 0.35 * brightness);
    }

    return { positions, colors, count: rawPoints.length };
  }

  parsePCD(arrayBuffer) {
    const textDecoder = new TextDecoder();
    const uint8View = new Uint8Array(arrayBuffer);

    let headerEnd = 0;
    for (let i = 0; i < Math.min(1000, uint8View.length - 5); i++) {
      if (uint8View[i] === 68 && uint8View[i+1] === 65 && uint8View[i+2] === 84 && uint8View[i+3] === 65) {
        for (let j = i; j < i + 20; j++) {
          if (uint8View[j] === 10) {
            headerEnd = j + 1;
            break;
          }
        }
        break;
      }
    }

    const headerText = textDecoder.decode(uint8View.slice(0, headerEnd));
    const pointsMatch = headerText.match(/POINTS\s+(\d+)/);
    const pointCount = pointsMatch ? parseInt(pointsMatch[1]) : 0;

    console.log('[PointCloudViewer] PCD header parsed, points:', pointCount);

    const dataView = new DataView(arrayBuffer, headerEnd);
    const positions = [];
    const colors = [];

    let minX = Infinity, maxX = -Infinity;
    let minY = Infinity, maxY = -Infinity;
    let minZ = Infinity, maxZ = -Infinity;

    const rawPoints = [];

    for (let i = 0; i < pointCount; i++) {
      const offset = i * 12;
      if (offset + 12 <= dataView.byteLength) {
        const x = dataView.getFloat32(offset, true);
        const y = dataView.getFloat32(offset + 4, true);
        const z = dataView.getFloat32(offset + 8, true);

        if (isFinite(x) && isFinite(y) && isFinite(z)) {
          rawPoints.push({ x, y, z });
          minX = Math.min(minX, x); maxX = Math.max(maxX, x);
          minY = Math.min(minY, y); maxY = Math.max(maxY, y);
          minZ = Math.min(minZ, z); maxZ = Math.max(maxZ, z);
        }
      }
    }

    const centerX = (minX + maxX) / 2;
    const centerY = (minY + maxY) / 2;
    const centerZ = (minZ + maxZ) / 2;
    const maxDim = Math.max(maxX - minX, maxY - minY, maxZ - minZ);
    const scale = 5 / maxDim;

    for (const { x, y, z } of rawPoints) {
      const nx = (x - centerX) * scale;
      const ny = (z - centerZ) * scale;
      const nz = (y - centerY) * scale;

      positions.push(nx, ny, nz);

      // Multi-color gradient based on 3D position (rainbow effect)
      const normalizedX = (x - minX) / (maxX - minX);
      const normalizedY = (y - minY) / (maxY - minY);
      const normalizedZ = (z - minZ) / (maxZ - minZ);

      // Combine position into hue for rainbow coloring
      const hue = (normalizedX * 0.3 + normalizedY * 0.4 + normalizedZ * 0.3) * 0.8;
      const sat = 0.7;
      const light = 0.45 + normalizedZ * 0.2;

      const rgb = this.hslToRgb(hue, sat, light);
      colors.push(rgb.r, rgb.g, rgb.b);
    }

    return { positions, colors, count: rawPoints.length };
  }

  createFallbackPointCloud() {
    const gl = this.gl;
    const count = 10000;
    const positions = [];
    const colors = [];

    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const r = 2;

      positions.push(
        r * Math.sin(phi) * Math.cos(theta),
        r * Math.sin(phi) * Math.sin(theta),
        r * Math.cos(phi)
      );

      const hue = (theta / (Math.PI * 2));
      const rgb = this.hslToRgb(hue, 0.7, 0.5);
      colors.push(rgb.r, rgb.g, rgb.b);
    }

    this.vao = gl.createVertexArray();
    gl.bindVertexArray(this.vao);

    this.posBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.posBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(this.aPosition);
    gl.vertexAttribPointer(this.aPosition, 3, gl.FLOAT, false, 0, 0);

    this.colorBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.colorBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colors), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(this.aColor);
    gl.vertexAttribPointer(this.aColor, 3, gl.FLOAT, false, 0, 0);

    gl.bindVertexArray(null);
    this.pointCount = count;

    if (this.loadingEl) this.loadingEl.remove();
    console.log('[PointCloudViewer] Using fallback point cloud');
  }

  async render() {
    this.animate(0);
  }

  animate(currentTime) {
    if (!this.gl || !this.program) return;

    this.animationFrameId = requestAnimationFrame((t) => this.animate(t));

    // FPS limiting
    const elapsed = currentTime - this.lastFrameTime;
    if (elapsed < this.frameInterval) return;
    this.lastFrameTime = currentTime - (elapsed % this.frameInterval);

    const gl = this.gl;
    const width = this.canvas.width;
    const height = this.canvas.height;

    gl.viewport(0, 0, width, height);
    gl.clearColor(0.067, 0.067, 0.067, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.enable(gl.DEPTH_TEST);

    gl.useProgram(this.program);

    const fov = 50 * Math.PI / 180;
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

    const view = new Float32Array([
      1, 0, 0, 0,
      0, 1, 0, 0,
      0, 0, 1, 0,
      0, 0, -this.zoom, 1
    ]);

    gl.uniformMatrix4fv(this.uProjection, false, projection);
    gl.uniformMatrix4fv(this.uView, false, view);

    if (this.isAnimating && !this.isDragging) {
      this.autoRotation += 0.004;
    }

    gl.uniform1f(this.uRotationX, this.rotationX);
    gl.uniform1f(this.uRotationY, this.rotationY + this.autoRotation);
    gl.uniform1f(this.uPointSize, 1.0);

    gl.bindVertexArray(this.vao);
    gl.drawArrays(gl.POINTS, 0, this.pointCount);
    gl.bindVertexArray(null);
  }

  createControlPanel() {
    this.controlPanel = document.createElement('div');
    this.controlPanel.style.cssText = `
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      padding: 4px 8px;
      background: #111;
      border-top: 1px solid #374151;
      font-family: 'IBM Plex Mono', monospace;
    `;

    this.controlPanel.innerHTML = `
      <button data-action="toggle" style="
        width: 24px; height: 24px; background: #1f2937; border: 1px solid #374151;
        border-radius: 4px; color: ${this.isAnimating ? '#4ade80' : '#9ca3af'}; cursor: pointer; font-size: 10px;
        display: flex; align-items: center; justify-content: center;
      ">${this.isAnimating ? '⏸' : '▶'}</button>
      <div style="width: 1px; height: 16px; background: #374151;"></div>
      <span class="model-label" style="color: #9ca3af; font-size: 9px; text-transform: uppercase;">
        Stanford Bunny
      </span>
    `;

    this.controlPanel.addEventListener('click', (e) => {
      const btn = e.target.closest('button');
      if (btn && btn.dataset.action === 'toggle') {
        this.isAnimating = !this.isAnimating;
        btn.textContent = this.isAnimating ? '⏸' : '▶';
        btn.style.color = this.isAnimating ? '#4ade80' : '#9ca3af';
      }
    });

    this.wrapper.appendChild(this.controlPanel);
  }

  onResize() {
    if (!this.canvas || !this.container) return;
    this.canvas.width = this.container.clientWidth;
    this.canvas.height = (this.container.clientHeight || 280) - 32;
  }

  showFallback() {
    this.container.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: center; height: 100%;
                  background: #1f2937; color: #9ca3af;">
        WebGL2 required for Point Cloud viewer
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
      if (this.posBuffer) this.gl.deleteBuffer(this.posBuffer);
      if (this.colorBuffer) this.gl.deleteBuffer(this.colorBuffer);
      if (this.vao) this.gl.deleteVertexArray(this.vao);
      if (this.program) this.gl.deleteProgram(this.program);
    }
    this.emitEvent('viewer:disposed', { viewer: 'PointCloudViewer' });
  }
}
