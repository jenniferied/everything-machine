{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 // scripts/markdown.js\
window.simpleMarkdownToHtml = function(md)\{\
  if(!md) return '';\
  // escape HTML early for safety\
  md = md.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');\
  // code blocks (```lang ... ```)\
  md = md.replace(/```([\\s\\S]*?)```/g, function(m)\{ return '<pre><code>'+m.slice(3,-3).replaceAll('&lt;','&lt;') +'</code></pre>' \});\
  // inline code\
  md = md.replace(/`([^`]+)`/g,'<code>$1</code>');\
  // images ![alt](url)\
  md = md.replace(/!\\[([^\\]]*)\\]\\(([^)]+)\\)/g,'<img alt="$1" src="$2">');\
  // links [text](url)\
  md = md.replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g,'<a href="$2" target="_blank" rel="noopener">$1</a>');\
  // headings\
  md = md.replace(/^###### (.*$)/gim,'<h6>$1</h6>');\
  md = md.replace(/^##### (.*$)/gim,'<h5>$1</h5>');\
  md = md.replace(/^#### (.*$)/gim,'<h4>$1</h4>');\
  md = md.replace(/^### (.*$)/gim,'<h3>$1</h3>');\
  md = md.replace(/^## (.*$)/gim,'<h2>$1</h2>');\
  md = md.replace(/^# (.*$)/gim,'<h1>$1</h1>');\
  // bold & italic\
  md = md.replace(/\\*\\*([^*]+)\\*\\*/g,'<strong>$1</strong>');\
  md = md.replace(/\\*([^*]+)\\*/g,'<em>$1</em>');\
  // unordered lists\
  md = md.replace(/(^|\\n)[ \\t]*\\* (.+)/g, function(_,prefix,line)\{ return prefix + '<li>'+line+'</li>'\});\
  // wrap list items into <ul>\
  md = md.replace(/(<li>[\\s\\S]*?<\\/li>)/g, function(m)\{ return '<ul>'+m.replaceAll('\\\\n','')+'</ul>' \});\
  // paragraphs (double newline)\
  md = md.split(/\\n\{2,\}/).map(p=>\{\
    if(p.match(/^\\s*<(h|ul|pre|img|blockquote|ol|h[1-6])/)) return p;\
    return '<p>'+p.replace(/\\n/g,' ').trim()+'</p>';\
  \}).join('');\
  return md;\
\}\
}