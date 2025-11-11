// scripts/markdown.js
window.simpleMarkdownToHtml = function(md){
  if(!md) return '';
  md = md.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
  md = md.replace(/```([\s\S]*?)```/g, function(m){ return '<pre><code>'+m.slice(3,-3).replaceAll('&lt;','&lt;') +'</code></pre>' });
  md = md.replace(/`([^`]+)`/g,'<code>$1</code>');
  md = md.replace(/!\[([^\]]*)\]\(([^)]+)\)/g,'<img alt="$1" src="$2">');
  md = md.replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');
  md = md.replace(/^###### (.*$)/gim,'<h6>$1</h6>');
  md = md.replace(/^##### (.*$)/gim,'<h5>$1</h5>');
  md = md.replace(/^#### (.*$)/gim,'<h4>$1</h4>');
  md = md.replace(/^### (.*$)/gim,'<h3>$1</h3>');
  md = md.replace(/^## (.*$)/gim,'<h2>$1</h2>');
  md = md.replace(/^# (.*$)/gim,'<h1>$1</h1>');
  md = md.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
  md = md.replace(/\*([^*]+)\*/g,'<em>$1</em>');
  md = md.replace(/(^|\n)[ \t]*\* (.+)/g, function(_,prefix,line){ return prefix + '<li>'+line+'</li>'; });
  md = md.replace(/(<li>[\s\S]*?<\/li>)/g, function(m){ return '<ul>'+m.replaceAll('\n','')+'</ul>'; });
  md = md.split(/\n{2,}/).map(p=>{
    if(p.match(/^\s*<(h|ul|pre|img|blockquote|ol|h[1-6])/)) return p;
    return '<p>'+p.replace(/\n/g,' ').trim()+'</p>';
  }).join('');
  return md;
}
