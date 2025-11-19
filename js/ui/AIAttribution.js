/**
 * AIAttribution - Single Responsibility: AI attribution UI component
 * Displays information about AI tools used, with expandable details
 */
export class AIAttribution {
  constructor(container, options = {}, eventBus = null) {
    this.container = container;
    this.eventBus = eventBus;
    
    // Configuration
    this.options = {
      badge: options.badge || 'Built with Cursor AI',
      models: options.models || [
        {
          name: 'Claude Sonnet 4.5',
          provider: 'Anthropic',
          usage: 'Code generation, architecture design, documentation'
        }
      ],
      tools: options.tools || [
        {
          name: 'Cursor',
          description: 'AI-powered code editor'
        }
      ],
      workflow: options.workflow || null,
      expandable: options.expandable !== false,
      initiallyExpanded: options.initiallyExpanded === true
    };
    
    this.isExpanded = this.options.initiallyExpanded;
    this.element = null;
  }

  /**
   * Render the AI attribution component
   */
  render() {
    if (!this.container) {
      console.error('[AIAttribution] No container provided');
      return;
    }
    
    // Create main element
    this.element = document.createElement('div');
    this.element.className = 'ai-attribution';
    this.element.setAttribute('role', 'contentinfo');
    this.element.setAttribute('aria-label', 'AI Attribution Information');
    
    // Build HTML
    this.element.innerHTML = this.buildHTML();
    
    // Append to container
    this.container.appendChild(this.element);
    
    // Setup event listeners
    this.setupEventListeners();
    
    this.emitEvent('ai-attribution:rendered');
  }

  /**
   * Build HTML structure
   * @returns {string} HTML content
   */
  buildHTML() {
    // Simple one-liner, no fancy styling
    const badgeHTML = `
      <div class="ai-attribution-simple">
        <span class="ai-attribution-text">${this.options.badge}</span>
      </div>
    `;
    
    let detailsHTML = '';
    
    if (this.options.expandable) {
      detailsHTML = `
        <div 
          class="ai-attribution-details ${this.isExpanded ? 'expanded' : ''}" 
          id="ai-attribution-details"
          aria-hidden="${!this.isExpanded}"
        >
          <div class="ai-attribution-section">
            <h3 class="ai-attribution-section-title">AI Models Used</h3>
            <ul class="ai-attribution-list">
              ${this.options.models.map(model => `
                <li class="ai-attribution-list-item">
                  <strong>${model.name}</strong>
                  ${model.provider ? `<span class="ai-attribution-provider">(${model.provider})</span>` : ''}
                  ${model.usage ? `<p class="ai-attribution-usage">${model.usage}</p>` : ''}
                </li>
              `).join('')}
            </ul>
          </div>
          
          ${this.options.tools.length > 0 ? `
            <div class="ai-attribution-section">
              <h3 class="ai-attribution-section-title">Tools & Technologies</h3>
              <ul class="ai-attribution-list">
                ${this.options.tools.map(tool => `
                  <li class="ai-attribution-list-item">
                    <strong>${tool.name}</strong>
                    ${tool.description ? `<p class="ai-attribution-usage">${tool.description}</p>` : ''}
                  </li>
                `).join('')}
              </ul>
            </div>
          ` : ''}
          
          ${this.options.workflow ? `
            <div class="ai-attribution-section">
              <h3 class="ai-attribution-section-title">Workflow</h3>
              <p class="ai-attribution-workflow">${this.options.workflow}</p>
            </div>
          ` : ''}
          
          <div class="ai-attribution-note">
            <p>This project leverages AI-assisted development to enhance productivity while maintaining human oversight and creative direction.</p>
          </div>
        </div>
      `;
    }
    
    return badgeHTML + detailsHTML;
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    if (!this.options.expandable) {
      return;
    }
    
    const toggleButton = this.element.querySelector('.ai-attribution-toggle');
    
    if (toggleButton) {
      toggleButton.addEventListener('click', () => this.toggle());
    }
  }

  /**
   * Toggle expanded state
   */
  toggle() {
    this.isExpanded = !this.isExpanded;
    
    const details = this.element.querySelector('.ai-attribution-details');
    const toggle = this.element.querySelector('.ai-attribution-toggle');
    
    if (details) {
      if (this.isExpanded) {
        details.classList.add('expanded');
        details.setAttribute('aria-hidden', 'false');
      } else {
        details.classList.remove('expanded');
        details.setAttribute('aria-hidden', 'true');
      }
    }
    
    if (toggle) {
      toggle.setAttribute('aria-expanded', this.isExpanded);
    }
    
    this.emitEvent('ai-attribution:toggled', { expanded: this.isExpanded });
  }

  /**
   * Expand details
   */
  expand() {
    if (!this.isExpanded) {
      this.toggle();
    }
  }

  /**
   * Collapse details
   */
  collapse() {
    if (this.isExpanded) {
      this.toggle();
    }
  }

  /**
   * Update models list
   * @param {Array} models - New models list
   */
  updateModels(models) {
    this.options.models = models;
    this.render(); // Re-render
  }

  /**
   * Add a model to the list
   * @param {Object} model - Model to add
   */
  addModel(model) {
    this.options.models.push(model);
    this.render(); // Re-render
  }

  /**
   * Dispose and cleanup
   */
  dispose() {
    if (this.element && this.element.parentNode) {
      this.element.parentNode.removeChild(this.element);
    }
    
    this.element = null;
    this.emitEvent('ai-attribution:disposed');
  }

  /**
   * Emit event through event bus
   * @param {string} event - Event name
   * @param {*} data - Event data
   */
  emitEvent(event, data) {
    if (this.eventBus && typeof this.eventBus.emit === 'function') {
      this.eventBus.emit(event, data);
    }
  }

  /**
   * Static factory: Create with default Cursor configuration
   * @param {HTMLElement} container - Container element
   * @param {EventBus} eventBus - Event bus instance
   * @returns {AIAttribution}
   */
  static createCursorAttribution(container, eventBus = null) {
    return new AIAttribution(container, {
      badge: 'Built with Cursor using Claude Sonnet 4.5, GPT-5.1 Codex, and Cursor Composer',
      models: [],
      tools: [],
      workflow: null,
      expandable: false,
      initiallyExpanded: false
    }, eventBus);
  }
}

