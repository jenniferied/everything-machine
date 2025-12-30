/**
 * ReflectionComponent
 * Single responsibility: Render reflection sections as structured widgets
 * Creates HTML for autoethnographic reflection following Ellis et al. (2011) and Schön (1983)
 */
export class ReflectionComponent {
  /**
   * Fixed questions for the reflection widget (hardcoded)
   * These follow the autoethnographic methodology
   */
  static QUESTIONS = {
    context: {
      tool: 'Tool/Workflow',
      intention: 'Intention'
    },
    process: {
      input: 'Input',
      iterations: 'Iterationen',
      output: 'Output'
    },
    insights: {
      surprise: 'Überraschungen',
      errorFeature: 'Fehler als Feature',
      myRole: 'Meine Rolle vs. KI'
    },
    development: {
      workflowChange: 'Workflow-Änderung',
      openQuestions: 'Offene Fragen',
      nextSteps: 'Nächste Schritte'
    }
  };

  /**
   * Section titles (German)
   */
  static SECTIONS = {
    context: 'Kontext',
    process: 'Prozess',
    insights: 'Erkenntnisse',
    development: 'Weiterentwicklung'
  };

  /**
   * Parse reflection section from markdown
   * @param {string} markdown - Full markdown text
   * @returns {Object} Object with hasReflection, reflectionData, and markdownWithoutReflection
   */
  static parseReflection(markdown) {
    // Find ## Reflexion section
    const reflectionMatch = markdown.match(/^## Reflexion\s*$/m);

    if (!reflectionMatch) {
      return {
        hasReflection: false,
        reflectionData: null,
        markdownWithoutReflection: markdown
      };
    }

    const reflectionStart = reflectionMatch.index;
    const beforeReflection = markdown.substring(0, reflectionStart);
    const reflectionSection = markdown.substring(reflectionStart);

    // Parse the reflection content
    const reflectionData = this.parseReflectionContent(reflectionSection);

    return {
      hasReflection: true,
      reflectionData,
      markdownWithoutReflection: beforeReflection.trim()
    };
  }

  /**
   * Parse reflection content into structured data
   * @param {string} reflectionMarkdown - Markdown starting with ## Reflexion
   * @returns {Object} Structured reflection data
   */
  static parseReflectionContent(reflectionMarkdown) {
    const data = {
      context: { tool: '', intention: '' },
      process: { input: '', iterations: '', output: '' },
      insights: { surprise: '', errorFeature: '', myRole: '' },
      development: { workflowChange: '', openQuestions: '', nextSteps: '' },
      keywords: []
    };

    // Extract keywords (hashtags) - can be after **Keywords:** or standalone
    const keywordMatches = reflectionMarkdown.match(/#([\w-]+)/g);
    if (keywordMatches) {
      data.keywords = keywordMatches.map(k => k.substring(1));
    }

    // Parse sections
    const lines = reflectionMarkdown.split('\n');
    let currentMainSection = null;
    let currentField = null;
    let currentContent = [];

    for (const line of lines) {
      const trimmed = line.trim();

      // Skip ## Reflexion header, intro text, and Keywords line
      if (trimmed.startsWith('## Reflexion') ||
          trimmed.startsWith('*Dieser Abschnitt') ||
          trimmed.startsWith('**Keywords:**') ||
          trimmed.startsWith('*Referenzen:')) {
        continue;
      }

      // Detect main sections (### Kontext, ### Prozess, etc.)
      const sectionMatch = trimmed.match(/^### (Kontext|Prozess|Erkenntnisse|Weiterentwicklung)\s*$/);
      if (sectionMatch) {
        // Save previous field content
        if (currentField && currentContent.length > 0) {
          this.setFieldValue(data, currentMainSection, currentField, currentContent.join(' '));
        }

        currentMainSection = this.getSectionKey(sectionMatch[1]);
        currentField = null;
        currentContent = [];
        continue;
      }

      // Detect field labels (- **Tool/Workflow:** ...)
      const fieldMatch = trimmed.match(/^-\s*\*\*([^:]+):\*\*\s*(.*)$/);
      if (fieldMatch) {
        // Save previous field content
        if (currentField && currentContent.length > 0) {
          this.setFieldValue(data, currentMainSection, currentField, currentContent.join(' '));
        }

        const fieldName = fieldMatch[1].trim();
        currentField = this.getFieldKey(fieldName);
        currentContent = fieldMatch[2].trim() ? [fieldMatch[2].trim()] : [];
        continue;
      }

      // Detect sub-items (indented with -)
      const subItemMatch = trimmed.match(/^\s*-\s+(.+)$/);
      if (subItemMatch && currentField) {
        currentContent.push(subItemMatch[1].trim());
        continue;
      }

      // Regular continuation line
      if (trimmed && currentField) {
        currentContent.push(trimmed);
      }
    }

    // Save last field content
    if (currentField && currentContent.length > 0) {
      this.setFieldValue(data, currentMainSection, currentField, currentContent.join(' '));
    }

    return data;
  }

  /**
   * Get section key from German name
   */
  static getSectionKey(germanName) {
    const mapping = {
      'Kontext': 'context',
      'Prozess': 'process',
      'Erkenntnisse': 'insights',
      'Weiterentwicklung': 'development'
    };
    return mapping[germanName] || null;
  }

  /**
   * Get field key from label
   */
  static getFieldKey(label) {
    const mapping = {
      'Tool/Workflow': 'tool',
      'Intention': 'intention',
      'Input': 'input',
      'Iterationen': 'iterations',
      'Output': 'output',
      'Überraschungen': 'surprise',
      'Fehler als Feature': 'errorFeature',
      'Meine Rolle vs. KI': 'myRole',
      'Workflow-Änderung': 'workflowChange',
      'Offene Fragen': 'openQuestions',
      'Nächste Schritte': 'nextSteps'
    };
    return mapping[label] || null;
  }

  /**
   * Set field value in data object
   */
  static setFieldValue(data, section, field, value) {
    if (section && field && data[section]) {
      data[section][field] = value;
    }
  }

  /**
   * Create reflection widget HTML
   * @param {Object} reflectionData - Parsed reflection data
   * @returns {string} HTML string
   */
  static createWidget(reflectionData) {
    if (!reflectionData) return '';

    const id = `reflection-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const infoId = `reflection-info-${id}`;

    // Build keywords HTML
    const keywordsHTML = reflectionData.keywords.length > 0
      ? `<div class="reflection-keywords">
          ${reflectionData.keywords.map(k => `<span class="reflection-keyword">#${k}</span>`).join('')}
        </div>`
      : '';

    // Build sections HTML
    const sectionsHTML = Object.entries(this.SECTIONS).map(([sectionKey, sectionTitle]) => {
      const sectionData = reflectionData[sectionKey];
      const questions = this.QUESTIONS[sectionKey];

      const fieldsHTML = Object.entries(questions).map(([fieldKey, fieldLabel]) => {
        const value = sectionData[fieldKey] || '';
        if (!value) return '';

        return `
          <div class="reflection-field">
            <div class="reflection-question">${fieldLabel}</div>
            <div class="reflection-answer">${this.formatAnswer(value)}</div>
          </div>
        `;
      }).filter(Boolean).join('');

      if (!fieldsHTML) return '';

      return `
        <div class="reflection-section">
          <div class="reflection-section-title">${sectionTitle}</div>
          ${fieldsHTML}
        </div>
      `;
    }).filter(Boolean).join('');

    // Info box content about the autoethnographic methodology
    const infoBoxHTML = `
      <div class="reflection-info-box" id="${infoId}">
        <div class="reflection-info-content">
          <h4>Über diesen Reflexionsprozess</h4>

          <p><strong>Autoethnografie</strong> ist eine qualitative Forschungsmethode, die persönliche Erfahrungen systematisch dokumentiert und analysiert. Sie verbindet das Subjektive mit dem Kulturellen und macht implizites Wissen explizit (Ellis, Adams & Bochner, 2011).</p>

          <p><strong>Reflection-in-Action</strong> nach Donald Schön (1983) beschreibt, wie Praktiker*innen während des Arbeitens reflektieren – ein kontinuierlicher Dialog zwischen Handeln und Nachdenken.</p>

          <h4>Mein Workflow</h4>
          <ol>
            <li><strong>Dokumentieren:</strong> Ich schreibe den Journal-Eintrag während oder direkt nach der kreativen Arbeit.</li>
            <li><strong>Reflektieren mit KI:</strong> Nach dem Schreiben führe ich eine Konversation mit der KI (Claude). Sie liest den Artikel, stellt Rückfragen und hilft mir, die strukturierten Reflexionsfragen zu beantworten.</li>
            <li><strong>Verdichten:</strong> Die KI fasst unsere Konversation in diesem standardisierten Format zusammen – mit den immer gleichen Fragen, um Vergleichbarkeit über alle Einträge hinweg zu gewährleisten.</li>
          </ol>

          <p>Dieser Prozess selbst ist Teil meiner Artistic Research: Die KI wird zum Sparringspartner für die Selbstreflexion, nicht zum Autor. Die Antworten entstehen im Dialog – die KI strukturiert und verdichtet, aber die Erkenntnisse kommen aus meiner Erfahrung.</p>

          <div class="reflection-info-sources">
            <strong>Quellen:</strong><br>
            Ellis, C., Adams, T. E., & Bochner, A. P. (2011). Autoethnography: An Overview. <em>Historical Social Research</em>, 36(4), 273–290.<br>
            Schön, D. A. (1983). <em>The Reflective Practitioner: How Professionals Think in Action</em>. Basic Books.
          </div>
        </div>
      </div>
    `;

    return `
      <div class="reflection-widget" id="${id}">
        <div class="reflection-header">
          <div class="reflection-icon">◈</div>
          <div class="reflection-title">Reflexion</div>
          <div class="reflection-subtitle">Autoethnografische Dokumentation</div>
          <button class="reflection-info-toggle" onclick="toggleReflectionInfo('${infoId}')" title="Was ist das?">
            <span class="reflection-info-icon">?</span>
          </button>
        </div>
        ${infoBoxHTML}
        ${keywordsHTML}
        <div class="reflection-content">
          ${sectionsHTML}
        </div>
        <div class="reflection-footer">
          <span class="reflection-reference">Ellis et al. (2011) · Schön (1983)</span>
        </div>
      </div>
    `;
  }

  /**
   * Format answer text (handle lists, links, etc.)
   */
  static formatAnswer(text) {
    if (!text) return '';

    // Convert markdown bold
    let formatted = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

    // Convert markdown italic
    formatted = formatted.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Convert markdown links
    formatted = formatted.replace(/\[([^\]]+)\]\(([^)]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener noreferrer" class="reflection-link">$1</a>');

    // Highlight hashtags
    formatted = formatted.replace(/#(\w+)/g, '<span class="reflection-keyword-inline">#$1</span>');

    return formatted;
  }
}

/**
 * Global function for toggling reflection info box
 * Called from onclick in HTML
 * @param {string} id - Info box ID
 */
window.toggleReflectionInfo = function(id) {
  const infoBox = document.getElementById(id);
  const button = infoBox ? infoBox.previousElementSibling?.querySelector('.reflection-info-toggle') : null;

  if (infoBox) {
    infoBox.classList.toggle('show');
    if (button) {
      button.classList.toggle('active');
    }
  }
};
