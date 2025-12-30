# Literature Review Setup

## Firecrawl MCP Configuration (Optional)

Firecrawl enables web crawling of AR-specific venues that aren't indexed in traditional academic databases.

### Target Venues

| Venue | URL | Purpose |
|-------|-----|---------|
| Research Catalogue | https://researchcatalogue.net | AR expositions |
| JAR | https://jar-online.net | AR journal |
| PARSE | https://parsejournal.com | AR journal |
| VIS | https://visjournal.nu | Nordic AR journal |

### Option A: Configure Firecrawl MCP

1. Get API key from [firecrawl.dev](https://firecrawl.dev) (free tier available)

2. Add to Claude Code MCP settings (`~/.claude/settings.json` or VS Code settings):

```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@anthropic/firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

3. Restart Claude Code to load the MCP

4. Available tools after configuration:
   - `firecrawl_scrape` - Scrape single URL
   - `firecrawl_map` - Map site structure
   - `firecrawl_crawl` - Crawl entire site

### Option B: Manual Fallback (No Firecrawl)

If Firecrawl is not configured, use these alternatives:

1. **WebFetch MCP** - Fetch specific URLs manually
2. **Manual browsing** - Visit venues and note relevant papers
3. **Semantic Scholar** - Search for AR papers that are indexed

### Cost Estimate

- **Free tier:** 500 credits/month (sufficient for initial exploration)
- **Paid tier:** $5-20 if more extensive crawling needed

## Other Requirements

### Already Configured MCPs

These should already be available:
- `mcp__papers__search_semantic_scholar` - Academic paper search
- `mcp__science__search_papers` - OpenAlex search
- `mcp__zotero__search_library` - Personal library

### Python Dependencies (for bibliometric analysis)

```bash
pip install pandas matplotlib seaborn
```

## Verification

To verify setup is complete:

1. Check folder structure exists:
   ```
   literature-review/
   ├── CLAUDE.md
   ├── Skill.md
   ├── SETUP.md
   ├── checkpoint.md
   ├── todo.md
   ├── reviews.log
   ├── data/exports/
   ├── drafts/
   └── scripts/
   ```

2. Test MCP availability by running a search

3. Verify `../submission/` exists with bibliography.bib
