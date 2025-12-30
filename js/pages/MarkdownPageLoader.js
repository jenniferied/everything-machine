/**
 * MarkdownPageLoader
 * Single responsibility: Load and render markdown files to page containers
 * Simpler than JournalManager - for static content pages
 */

export class MarkdownPageLoader {
  constructor(eventBus) {
    this.eventBus = eventBus;
    this.loadedPages = new Map();
  }

  /**
   * Load a markdown file and render to container
   * @param {string} filePath - Path to markdown file
   * @param {HTMLElement} container - Container element
   * @returns {Promise<void>}
   */
  async loadPage(filePath, container) {
    if (!container) {
      console.warn('[MarkdownPageLoader] Container not found');
      return;
    }

    // Check cache
    if (this.loadedPages.has(filePath)) {
      container.innerHTML = this.loadedPages.get(filePath);
      return;
    }

    try {
      const response = await fetch(filePath);
      if (!response.ok) {
        throw new Error(`Failed to load ${filePath}: ${response.status}`);
      }

      const markdown = await response.text();
      const html = this.parseMarkdown(markdown);
      
      // Cache the result
      this.loadedPages.set(filePath, html);
      
      // Render
      container.innerHTML = html;
      
      // Make external links open in new tab
      this.processLinks(container);
      
      this.eventBus?.emit('markdown-page:loaded', { filePath });
      
    } catch (error) {
      console.error('[MarkdownPageLoader] Error loading page:', error);
      container.innerHTML = `<p class="text-red-400">Fehler beim Laden: ${error.message}</p>`;
    }
  }

  /**
   * Parse markdown to HTML
   * Simpler than JournalManager - for documentation-style content
   * @param {string} markdown - Raw markdown
   * @returns {string} HTML
   */
  parseMarkdown(markdown) {
    let html = markdown;

    // Tables (simple support)
    html = this.parseTables(html);

    // Code blocks
    html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
      return `<pre class="bg-gray-800 p-4 rounded-sm overflow-x-auto my-4"><code class="text-sm text-gray-300">${this.escapeHtml(code.trim())}</code></pre>`;
    });

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code class="bg-gray-700 px-1 py-0.5 rounded text-green-300 text-sm">$1</code>');

    // Horizontal rules
    html = html.replace(/^---$/gm, '<hr class="border-gray-700 my-8">');

    // Bold and italic (order matters)
    html = html.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong><em>$1</em></strong>');
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Blockquotes
    html = html.replace(/^>\s*(.+)$/gm, '<blockquote class="border-l-4 border-green-400 pl-4 my-4 text-gray-300 italic">$1</blockquote>');

    // Lists (unordered)
    html = this.parseUnorderedLists(html);

    // Lists (ordered)
    html = this.parseOrderedLists(html);

    // Checkboxes
    html = html.replace(/- \[x\]/gi, '<span class="text-green-400">✓</span>');
    html = html.replace(/- \[ \]/g, '<span class="text-gray-500">☐</span>');

    // Images
    html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, 
      '<figure class="my-6"><img src="$2" alt="$1" class="rounded-sm max-w-full h-auto" /><figcaption class="text-sm text-gray-500 mt-2">$1</figcaption></figure>');

    // Links - markdown style [text](url)
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, text, url) => {
      const href = url.startsWith('http') ? url : url;
      return `<a href="${href}" class="text-green-400 hover:text-green-300 underline">${text}</a>`;
    });

    // Emoji shortcuts
    html = html.replace(/:\+1:/g, '👍');
    html = html.replace(/:target:/g, '🎯');
    html = html.replace(/❌/g, '<span class="text-red-400">❌</span>');
    html = html.replace(/✅/g, '<span class="text-green-400">✅</span>');
    html = html.replace(/⚡/g, '<span class="text-yellow-400">⚡</span>');

    // Headings (after other processing to avoid conflicts)
    html = html.replace(/^######\s+(.+)$/gm, '<h6 class="text-sm font-bold mt-6 mb-2 text-gray-400">$1</h6>');
    html = html.replace(/^#####\s+(.+)$/gm, '<h5 class="text-base font-bold mt-6 mb-2 text-gray-300">$1</h5>');
    html = html.replace(/^####\s+(.+)$/gm, '<h4 class="text-lg font-bold mt-6 mb-3 text-gray-200">$1</h4>');
    html = html.replace(/^###\s+(.+)$/gm, '<h3 class="text-xl font-bold mt-8 mb-4 text-green-400">$1</h3>');
    html = html.replace(/^##\s+(.+)$/gm, '<h2 class="text-2xl font-bold mt-10 mb-4 text-white border-b border-gray-700 pb-2">$1</h2>');
    html = html.replace(/^#\s+(.+)$/gm, '<h1 class="text-3xl font-bold mt-8 mb-6 text-white">$1</h1>');

    // Paragraphs
    html = this.wrapParagraphs(html);

    return html;
  }

  /**
   * Parse simple markdown tables
   * @param {string} text - Text with tables
   * @returns {string} Text with HTML tables
   */
  parseTables(text) {
    const lines = text.split('\n');
    const result = [];
    let inTable = false;
    let tableLines = [];

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      
      // Check if this is a table row (starts and ends with |)
      if (line.startsWith('|') && line.endsWith('|')) {
        if (!inTable) {
          inTable = true;
          tableLines = [];
        }
        tableLines.push(line);
      } else {
        if (inTable) {
          // End of table - process it
          result.push(this.buildTable(tableLines));
          inTable = false;
          tableLines = [];
        }
        result.push(lines[i]);
      }
    }

    // Handle table at end of file
    if (inTable && tableLines.length > 0) {
      result.push(this.buildTable(tableLines));
    }

    return result.join('\n');
  }

  /**
   * Build HTML table from table lines
   * @param {Array} lines - Table lines
   * @returns {string} HTML table
   */
  buildTable(lines) {
    if (lines.length < 2) return lines.join('\n');

    let html = '<div class="overflow-x-auto my-6"><table class="w-full text-sm">';
    
    // Header row
    const headerCells = lines[0].split('|').filter(c => c.trim());
    html += '<thead class="bg-gray-800"><tr>';
    headerCells.forEach(cell => {
      html += `<th class="px-4 py-2 text-left text-green-400 font-bold border-b border-gray-700">${cell.trim()}</th>`;
    });
    html += '</tr></thead>';

    // Body rows (skip separator row which is index 1)
    html += '<tbody>';
    for (let i = 2; i < lines.length; i++) {
      const cells = lines[i].split('|').filter(c => c.trim());
      html += '<tr class="border-b border-gray-800 hover:bg-gray-800/50">';
      cells.forEach(cell => {
        html += `<td class="px-4 py-2 text-gray-300">${cell.trim()}</td>`;
      });
      html += '</tr>';
    }
    html += '</tbody></table></div>';

    return html;
  }

  /**
   * Parse unordered lists
   * @param {string} text - Text with lists
   * @returns {string} Text with HTML lists
   */
  parseUnorderedLists(text) {
    const lines = text.split('\n');
    const result = [];
    let inList = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();
      
      // Check for list item (- or *)
      if (/^[-*]\s+/.test(trimmed)) {
        if (!inList) {
          result.push('<ul class="list-disc list-inside space-y-2 my-4 ml-4">');
          inList = true;
        }
        const content = trimmed.replace(/^[-*]\s+/, '');
        result.push(`<li class="text-gray-300">${content}</li>`);
      } else {
        if (inList && trimmed !== '') {
          result.push('</ul>');
          inList = false;
        }
        result.push(line);
      }
    }

    if (inList) {
      result.push('</ul>');
    }

    return result.join('\n');
  }

  /**
   * Parse ordered lists
   * @param {string} text - Text with lists
   * @returns {string} Text with HTML lists
   */
  parseOrderedLists(text) {
    const lines = text.split('\n');
    const result = [];
    let inList = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();
      
      // Check for numbered list item
      if (/^\d+\.\s+/.test(trimmed)) {
        if (!inList) {
          result.push('<ol class="list-decimal list-inside space-y-2 my-4 ml-4">');
          inList = true;
        }
        const content = trimmed.replace(/^\d+\.\s+/, '');
        result.push(`<li class="text-gray-300">${content}</li>`);
      } else {
        if (inList && trimmed !== '') {
          result.push('</ol>');
          inList = false;
        }
        result.push(line);
      }
    }

    if (inList) {
      result.push('</ol>');
    }

    return result.join('\n');
  }

  /**
   * Wrap remaining text in paragraphs
   * @param {string} html - Partially processed HTML
   * @returns {string} HTML with paragraphs
   */
  wrapParagraphs(html) {
    const lines = html.split('\n');
    const result = [];
    let paragraph = [];

    const isBlockElement = (line) => {
      const trimmed = line.trim();
      return trimmed.startsWith('<h') ||
             trimmed.startsWith('<ul') ||
             trimmed.startsWith('<ol') ||
             trimmed.startsWith('<li') ||
             trimmed.startsWith('</ul') ||
             trimmed.startsWith('</ol') ||
             trimmed.startsWith('<pre') ||
             trimmed.startsWith('</pre') ||
             trimmed.startsWith('<table') ||
             trimmed.startsWith('<div') ||
             trimmed.startsWith('</div') ||
             trimmed.startsWith('<blockquote') ||
             trimmed.startsWith('<hr') ||
             trimmed.startsWith('<figure') ||
             trimmed === '';
    };

    for (const line of lines) {
      if (isBlockElement(line)) {
        if (paragraph.length > 0) {
          result.push(`<p class="mb-4 text-gray-300">${paragraph.join(' ')}</p>`);
          paragraph = [];
        }
        if (line.trim()) {
          result.push(line);
        }
      } else {
        paragraph.push(line.trim());
      }
    }

    if (paragraph.length > 0) {
      result.push(`<p class="mb-4 text-gray-300">${paragraph.join(' ')}</p>`);
    }

    return result.join('\n');
  }

  /**
   * Process links to open external ones in new tab
   * @param {HTMLElement} container - Container with links
   */
  processLinks(container) {
    const links = container.querySelectorAll('a');
    links.forEach(link => {
      const href = link.getAttribute('href');
      if (href && (href.startsWith('http') || href.startsWith('//'))) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
      }
    });
  }

  /**
   * Escape HTML entities
   * @param {string} text - Text to escape
   * @returns {string} Escaped text
   */
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Dispose
   */
  dispose() {
    this.loadedPages.clear();
  }
}
