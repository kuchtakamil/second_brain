# Second Brain Framework with Markdown, LLMs & Automated Ingestion

## Executive Summary

This framework describes a personal knowledge management system that automatically captures, processes, and connects information using markdown files as the foundation, LLMs for intelligent processing, and automation pipelines for seamless content ingestion.

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SECOND BRAIN SYSTEM                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │   CAPTURE    │───▶│   PROCESS    │───▶│    STORE     │                   │
│  │    LAYER     │    │    LAYER     │    │    LAYER     │                   │
│  └──────────────┘    └──────────────┘    └──────────────┘                   │
│         │                   │                   │                            │
│         │                   ▼                   │                            │
│         │           ┌──────────────┐            │                            │
│         │           │  LLM ENGINE  │            │                            │
│         │           └──────────────┘            │                            │
│         │                   │                   │                            │
│         ▼                   ▼                   ▼                            │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │                    RETRIEVAL & SYNTHESIS                     │            │
│  └─────────────────────────────────────────────────────────────┘            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Directory Structure

```
second-brain/
├── 00-inbox/                    # Unprocessed captures
│   ├── web-clips/
│   ├── voice-notes/
│   ├── screenshots/
│   └── quick-notes/
│
├── 01-sources/                  # Reference materials
│   ├── articles/
│   ├── books/
│   ├── papers/
│   ├── podcasts/
│   └── videos/
│
├── 02-notes/                    # Processed knowledge
│   ├── permanent/               # Evergreen notes
│   ├── literature/              # Source summaries
│   ├── fleeting/                # Quick thoughts
│   └── meeting/                 # Meeting notes
│
├── 03-projects/                 # Active projects
│   ├── active/
│   ├── archived/
│   └── someday/
│
├── 04-areas/                    # Life areas
│   ├── health/
│   ├── career/
│   ├── relationships/
│   └── finances/
│
├── 05-resources/                # Topic collections
│   ├── programming/
│   ├── business/
│   └── creativity/
│
├── 06-archive/                  # Inactive content
│
├── .system/                     # System files
│   ├── embeddings/              # Vector store
│   ├── graphs/                  # Knowledge graphs
│   ├── logs/                    # Processing logs
│   ├── templates/               # Note templates
│   └── config/                  # Configuration
│
└── index.md                     # Entry point
```

---

## 3. Markdown Schema & Templates

### 3.1 Universal Frontmatter Schema

```yaml
---
# Identity
id: uuid-v4
title: "Note Title"
aliases: ["alternate name", "abbreviation"]
type: permanent | literature | fleeting | meeting | project | source

# Temporal
created: 2024-01-15T10:30:00Z
modified: 2024-01-15T14:22:00Z
reviewed: 2024-01-10

# Classification
status: seedling | growing | evergreen | archived
certainty: speculation | hypothesis | established | verified
importance: 1-5

# Taxonomy
tags: [tag1, tag2, tag3]
domains: [domain1, domain2]

# Relationships
parent: "[[Parent Note]]"
related: ["[[Note 1]]", "[[Note 2]]"]
source: "[[Source Reference]]"

# AI Metadata
embedding_version: 2
last_indexed: 2024-01-15T10:35:00Z
auto_tags: [ai-generated-tag1, ai-generated-tag2]
summary_hash: sha256-hash

# Source Tracking (for ingested content)
source_url: "https://..."
source_type: article | video | podcast | book | paper
capture_method: manual | browser-extension | api | email
---
```

### 3.2 Note Templates

#### Permanent Note Template

```markdown
---
type: permanent
status: seedling
---

# {{title}}
stablish YAML template in 06-System/templates/.
## Core Idea
<!-- One atomic concept, clearly stated -->

## Explanation
<!-- Develop the idea in your own words -->

## Evidence
<!-- Supporting facts, examples, quotes -->

## Connections
<!-- How this relates to other knowledge -->
- Supports: [[]]
- Contradicts: [[]]
- Extends: [[]]
- Applied in: [[]]

## Questions
<!-- Open questions this raises -->

## Source Context
<!-- Where this idea originated -->
Derived from: [[]]

---
*Last reviewed: {{date}}*
```

#### Literature Note Template

```markdown
---
type: literature
source_type: {{book|article|paper|video}}
---

# {{title}}

## Metadata
- **Author**: 
- **Published**: 
- **Read/Watched**: {{date}}
- **Rating**: ⭐⭐⭐⭐⭐

## Summary
<!-- 3-5 sentence overview -->

## Key Takeaways
1. 
2. 
3. 

## Highlights & Annotations
### Chapter/Section
> Quote or highlight

My thoughts: ...

## Extracted Concepts
<!-- Concepts worth developing into permanent notes -->
- [ ] [[Concept 1]] - brief description
- [ ] [[Concept 2]] - brief description

## Action Items
- [ ] 

## Related
- [[Similar Book]]
- [[Related Topic]]
```

#### Meeting Note Template

```markdown
---
type: meeting
---

# {{Meeting Title}} - {{date}}

## Attendees
- 

## Agenda
1. 

## Notes

## Decisions Made
- 

## Action Items
- [ ] @{{person}} - Task - Due: {{date}}

## Follow-up
- Next meeting: 
- Topics to revisit: 

## Linked Notes
- [[Related Project]]
```

---

## 4. Automated Ingestion System

### 4.1 Ingestion Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    INGESTION SOURCES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ Browser │ │  Email  │ │  RSS    │ │  API    │ │  File   │   │
│  │Extension│ │ Forward │ │  Feeds  │ │ Webhooks│ │ Watcher │   │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘   │
│       │           │           │           │           │         │
│       └───────────┴───────────┴─────┬─────┴───────────┘         │
│                                     │                            │
│                                     ▼                            │
│                          ┌──────────────────┐                    │
│                          │  INTAKE QUEUE    │                    │
│                          │   (Redis/RMQ)    │                    │
│                          └────────┬─────────┘                    │
│                                   │                              │
│                                   ▼                              │
│                          ┌──────────────────┐                    │
│                          │   PROCESSOR      │                    │
│                          │    WORKERS       │                    │
│                          └────────┬─────────┘                    │
│                                   │                              │
│       ┌───────────────────────────┼───────────────────────────┐  │
│       ▼               ▼           ▼           ▼               ▼  │
│  ┌─────────┐    ┌─────────┐ ┌─────────┐ ┌─────────┐    ┌─────────┐
│  │ Extract │    │  Clean  │ │Summarize│ │  Tag &  │    │ Embed & │
│  │ Content │───▶│ & Parse │─▶│  (LLM) │─▶│Classify │───▶│  Store │
│  └─────────┘    └─────────┘ └─────────┘ └─────────┘    └─────────┘
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Source Connectors

```python
# ingestion/connectors/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class IngestedContent:
    """Standardized format for all ingested content"""
    source_id: str
    source_type: str
    source_url: Optional[str]
    title: str
    content: str
    content_html: Optional[str]
    author: Optional[str]
    published_date: Optional[datetime]
    captured_date: datetime
    metadata: Dict[str, Any]
    attachments: list[str]
    raw_data: Any

class BaseConnector(ABC):
    """Base class for all content connectors"""
    
    @abstractmethod
    async def fetch(self, source: str) -> IngestedContent:
        """Fetch content from source"""
        pass
    
    @abstractmethod
    async def watch(self, callback) -> None:
        """Watch for new content (if supported)"""
        pass
    
    @abstractmethod
    def supports_watch(self) -> bool:
        """Whether this connector supports watching"""
        pass
```

```python
# ingestion/connectors/web.py
import trafilatura
from playwright.async_api import async_playwright
from readability import Document
import httpx

class WebConnector(BaseConnector):
    """Connector for web articles and pages"""
    
    async def fetch(self, url: str) -> IngestedContent:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            html = response.text
        
        # Extract main content
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            include_images=True,
            output_format='markdown'
        )
        
        # Fallback to readability
        if not extracted:
            doc = Document(html)
            extracted = doc.summary()
        
        # Extract metadata
        metadata = trafilatura.extract_metadata(html)
        
        return IngestedContent(
            source_id=self._generate_id(url),
            source_type="web_article",
            source_url=url,
            title=metadata.title if metadata else "",
            content=extracted,
            content_html=html,
            author=metadata.author if metadata else None,
            published_date=self._parse_date(metadata.date) if metadata else None,
            captured_date=datetime.utcnow(),
            metadata={
                "sitename": metadata.sitename if metadata else None,
                "description": metadata.description if metadata else None,
            },
            attachments=[],
            raw_data=response
        )
    
    async def fetch_with_js(self, url: str) -> IngestedContent:
        """Fetch JavaScript-rendered pages"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle")
            html = await page.content()
            await browser.close()
        
        # Continue with extraction...
        return await self._process_html(url, html)
```

```python
# ingestion/connectors/email.py
import imaplib
import email
from email.header import decode_header

class EmailConnector(BaseConnector):
    """Connector for email-forwarded content"""
    
    def __init__(self, config: dict):
        self.server = config["imap_server"]
        self.email = config["email"]
        self.password = config["password"]
        self.folder = config.get("folder", "SecondBrain")
    
    async def watch(self, callback) -> None:
        """Watch inbox for new emails to specific folder"""
        mail = imaplib.IMAP4_SSL(self.server)
        mail.login(self.email, self.password)
        mail.select(self.folder)
        
        while True:
            # Check for new emails
            _, messages = mail.search(None, "UNSEEN")
            
            for msg_num in messages[0].split():
                _, msg_data = mail.fetch(msg_num, "(RFC822)")
                email_body = msg_data[0][1]
                msg = email.message_from_bytes(email_body)
                
                content = self._parse_email(msg)
                await callback(content)
                
                # Mark as processed
                mail.store(msg_num, "+FLAGS", "\\Seen")
            
            await asyncio.sleep(60)  # Check every minute
    
    def _parse_email(self, msg) -> IngestedContent:
        subject = decode_header(msg["Subject"])[0][0]
        
        # Extract body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()
        
        # Detect if this is a forwarded article
        urls = self._extract_urls(body)
        
        return IngestedContent(
            source_id=msg["Message-ID"],
            source_type="email",
            source_url=urls[0] if urls else None,
            title=subject,
            content=body,
            # ... other fields
        )
```

```python
# ingestion/connectors/rss.py
import feedparser
from datetime import datetime

class RSSConnector(BaseConnector):
    """Connector for RSS/Atom feeds"""
    
    def __init__(self, feeds: list[dict]):
        self.feeds = feeds  # [{"url": "...", "tags": [...], "priority": 1}]
        self.seen_ids = set()  # Persist this
    
    async def watch(self, callback) -> None:
        while True:
            for feed_config in self.feeds:
                feed = feedparser.parse(feed_config["url"])
                
                for entry in feed.entries:
                    if entry.id not in self.seen_ids:
                        content = await self._fetch_full_content(entry)
                        content.metadata["feed_tags"] = feed_config.get("tags", [])
                        content.metadata["priority"] = feed_config.get("priority", 3)
                        
                        await callback(content)
                        self.seen_ids.add(entry.id)
            
            await asyncio.sleep(900)  # Check every 15 minutes
```

```python
# ingestion/connectors/readwise.py
import httpx

class ReadwiseConnector(BaseConnector):
    """Connector for Readwise highlights"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://readwise.io/api/v2"
        self.last_fetch = None
    
    async def fetch_highlights(self) -> list[IngestedContent]:
        headers = {"Authorization": f"Token {self.api_key}"}
        
        params = {}
        if self.last_fetch:
            params["updated__gt"] = self.last_fetch.isoformat()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/highlights/",
                headers=headers,
                params=params
            )
            data = response.json()
        
        contents = []
        for highlight in data["results"]:
            contents.append(IngestedContent(
                source_id=f"readwise-{highlight['id']}",
                source_type="highlight",
                title=highlight["book"]["title"],
                content=highlight["text"],
                metadata={
                    "book_id": highlight["book"]["id"],
                    "author": highlight["book"]["author"],
                    "note": highlight.get("note"),
                    "location": highlight.get("location"),
                    "highlighted_at": highlight["highlighted_at"],
                },
                # ... other fields
            ))
        
        self.last_fetch = datetime.utcnow()
        return contents
```

### 4.3 Content Processor

```python
# ingestion/processor.py
from dataclasses import dataclass
from typing import Optional
import hashlib

@dataclass
class ProcessedNote:
    """Processed and ready-to-store note"""
    filepath: str
    content: str
    frontmatter: dict
    embeddings: list[float]
    links_to_create: list[str]
    suggested_connections: list[tuple[str, float]]  # (note_id, similarity)

class ContentProcessor:
    """Main processor for ingested content"""
    
    def __init__(self, llm_client, embedding_model, knowledge_base):
        self.llm = llm_client
        self.embedder = embedding_model
        self.kb = knowledge_base
        self.templates = TemplateManager()
    
    async def process(self, content: IngestedContent) -> ProcessedNote:
        # Step 1: Clean and normalize content
        cleaned = await self._clean_content(content)
        
        # Step 2: Generate summary and extract key points
        analysis = await self._analyze_content(cleaned)
        
        # Step 3: Auto-tag and classify
        classification = await self._classify_content(cleaned, analysis)
        
        # Step 4: Generate embeddings
        embeddings = await self._generate_embeddings(cleaned, analysis)
        
        # Step 5: Find related notes
        connections = await self._find_connections(embeddings)
        
        # Step 6: Generate markdown
        markdown = await self._generate_markdown(
            content, cleaned, analysis, classification, connections
        )
        
        # Step 7: Determine file path
        filepath = self._determine_filepath(content, classification)
        
        return ProcessedNote(
            filepath=filepath,
            content=markdown,
            frontmatter=self._build_frontmatter(content, analysis, classification),
            embeddings=embeddings,
            links_to_create=analysis.get("concepts_to_link", []),
            suggested_connections=connections
        )
    
    async def _analyze_content(self, content: str) -> dict:
        """Use LLM to analyze content"""
        prompt = """Analyze the following content and extract:

1. **Summary**: A 2-3 sentence summary
2. **Key Points**: 3-5 main takeaways as bullet points
3. **Concepts**: Important concepts that should become separate notes
4. **Questions**: Questions this content raises
5. **Action Items**: Any actionable items mentioned
6. **Quotes**: Notable quotes worth preserving

Content:
---
{content}
---

Respond in JSON format."""

        response = await self.llm.complete(
            prompt.format(content=content[:8000]),  # Truncate if needed
            response_format={"type": "json_object"}
        )
        
        return json.loads(response)
    
    async def _classify_content(self, content: str, analysis: dict) -> dict:
        """Classify content into categories and generate tags"""
        
        # Get existing tags for consistency
        existing_tags = await self.kb.get_all_tags()
        existing_domains = await self.kb.get_all_domains()
        
        prompt = """Classify this content:

Content Summary: {summary}
Key Points: {key_points}

Existing tags in the system (prefer these): {existing_tags}
Existing domains: {existing_domains}

Provide:
1. Primary domain (1)
2. Secondary domains (0-2)
3. Tags (3-7, mix of existing and new if needed)
4. Content type: article | book | paper | video | podcast | tweet | note
5. Importance (1-5)
6. Suggested location in folder structure

Respond in JSON."""

        response = await self.llm.complete(
            prompt.format(
                summary=analysis["summary"],
                key_points=analysis["key_points"],
                existing_tags=existing_tags[:50],
                existing_domains=existing_domains
            ),
            response_format={"type": "json_object"}
        )
        
        return json.loads(response)
    
    async def _find_connections(
        self, 
        embeddings: list[float]
    ) -> list[tuple[str, float]]:
        """Find related notes using vector similarity"""
        
        similar = await self.kb.vector_search(
            embeddings,
            top_k=20,
            threshold=0.7
        )
        
        return [(note_id, score) for note_id, score in similar]
    
    async def _generate_markdown(
        self,
        original: IngestedContent,
        cleaned: str,
        analysis: dict,
        classification: dict,
        connections: list[tuple[str, float]]
    ) -> str:
        """Generate final markdown content"""
        
        # Get template based on content type
        template = self.templates.get(classification["content_type"])
        
        # Build connections section
        connection_links = []
        for note_id, score in connections[:5]:
            note = await self.kb.get_note(note_id)
            connection_links.append(f"- [[{note.title}]] (relevance: {score:.0%})")
        
        # Render template
        return template.render(
            title=original.title,
            source_url=original.source_url,
            author=original.author,
            published_date=original.published_date,
            summary=analysis["summary"],
            key_points=analysis["key_points"],
            content=cleaned,
            quotes=analysis.get("quotes", []),
            concepts=analysis.get("concepts", []),
            questions=analysis.get("questions", []),
            action_items=analysis.get("action_items", []),
            connections=connection_links,
            captured_date=original.captured_date,
        )
```

### 4.4 Browser Extension

```javascript
// browser-extension/content.js
class SecondBrainClipper {
  constructor() {
    this.apiEndpoint = 'http://localhost:8080/api/ingest';
    this.init();
  }

  init() {
    // Add keyboard shortcut
    document.addEventListener('keydown', (e) => {
      if (e.altKey && e.shiftKey && e.key === 'S') {
        this.clipPage();
      }
    });

    // Listen for selection clips
    document.addEventListener('mouseup', (e) => {
      const selection = window.getSelection().toString().trim();
      if (selection.length > 50) {
        this.showClipButton(e, selection);
      }
    });
  }

  async clipPage() {
    const pageData = {
      url: window.location.href,
      title: document.title,
      content: this.extractContent(),
      selection: window.getSelection().toString(),
      metadata: this.extractMetadata(),
      timestamp: new Date().toISOString()
    };

    try {
      const response = await fetch(this.apiEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pageData)
      });

      if (response.ok) {
        this.showNotification('✓ Clipped to Second Brain');
      }
    } catch (error) {
      this.showNotification('✗ Failed to clip', 'error');
    }
  }

  extractContent() {
    // Use Readability-like extraction
    const article = document.querySelector('article') || 
                   document.querySelector('[role="main"]') ||
                   document.querySelector('.post-content') ||
                   document.body;
    
    return article.innerText;
  }

  extractMetadata() {
    return {
      author: this.getMetaContent('author') || 
              this.getMetaContent('twitter:creator'),
      description: this.getMetaContent('description') ||
                  this.getMetaContent('og:description'),
      image: this.getMetaContent('og:image'),
      publishedDate: this.getMetaContent('article:published_time'),
      siteName: this.getMetaContent('og:site_name')
    };
  }

  getMetaContent(name) {
    const meta = document.querySelector(
      `meta[name="${name}"], meta[property="${name}"]`
    );
    return meta?.content;
  }

  showClipButton(event, selection) {
    const button = document.createElement('div');
    button.className = 'second-brain-clip-button';
    button.innerHTML = '📎 Clip';
    button.style.cssText = `
      position: fixed;
      top: ${event.clientY - 40}px;
      left: ${event.clientX}px;
      background: #4A90D9;
      color: white;
      padding: 8px 12px;
      border-radius: 4px;
      cursor: pointer;
      z-index: 10000;
      font-size: 14px;
    `;

    button.addEventListener('click', () => {
      this.clipSelection(selection);
      button.remove();
    });

    document.body.appendChild(button);
    setTimeout(() => button.remove(), 5000);
  }

  async clipSelection(selection) {
    const data = {
      url: window.location.href,
      title: document.title,
      selection: selection,
      context: this.getSelectionContext(),
      timestamp: new Date().toISOString(),
      type: 'highlight'
    };

    await fetch(this.apiEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }
}

new SecondBrainClipper();
```

---

## 5. LLM Integration Layer

### 5.1 LLM Service Architecture

```python
# llm/service.py
from abc import ABC, abstractmethod
from typing import AsyncIterator
import openai
import anthropic
from ollama import AsyncClient as OllamaClient

class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        pass
    
    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
        self.embedding_model = "text-embedding-3-small"
    
    async def complete(self, prompt: str, **kwargs) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    
    async def embed(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding

class OllamaProvider(LLMProvider):
    """Local LLM provider for privacy-sensitive processing"""
    
    def __init__(self, model: str = "llama3:8b", host: str = "http://localhost:11434"):
        self.client = OllamaClient(host=host)
        self.model = model
        self.embedding_model = "nomic-embed-text"
    
    async def complete(self, prompt: str, **kwargs) -> str:
        response = await self.client.generate(
            model=self.model,
            prompt=prompt,
            **kwargs
        )
        return response['response']
    
    async def embed(self, text: str) -> list[float]:
        response = await self.client.embeddings(
            model=self.embedding_model,
            prompt=text
        )
        return response['embedding']

class LLMService:
    """Unified LLM service with fallback and routing"""
    
    def __init__(self, config: dict):
        self.providers = {}
        self.default_provider = config.get("default", "openai")
        
        if config.get("openai"):
            self.providers["openai"] = OpenAIProvider(**config["openai"])
        if config.get("anthropic"):
            self.providers["anthropic"] = AnthropicProvider(**config["anthropic"])
        if config.get("ollama"):
            self.providers["ollama"] = OllamaProvider(**config["ollama"])
    
    async def complete(
        self, 
        prompt: str, 
        provider: str = None,
        task_type: str = "general"
    ) -> str:
        """Route to appropriate provider based on task"""
        
        # Route sensitive tasks to local model
        if task_type in ["personal", "private", "journal"]:
            provider = "ollama"
        
        provider = provider or self.default_provider
        
        try:
            return await self.providers[provider].complete(prompt)
        except Exception as e:
            # Fallback logic
            for fallback in self.providers:
                if fallback != provider:
                    try:
                        return await self.providers[fallback].complete(prompt)
                    except:
                        continue
            raise e
```

### 5.2 Prompt Templates

```python
# llm/prompts.py

PROMPTS = {
    "summarize": """Summarize the following content in {length} format.
Focus on: key arguments, main conclusions, and actionable insights.

Content:
{content}

Summary:""",

    "extract_concepts": """Extract the key concepts from this text that would be worth 
developing into standalone notes. For each concept:
1. Name the concept clearly
2. Provide a one-sentence definition
3. Note its relationship to other concepts

Text:
{content}

Concepts (JSON array):""",

    "generate_connections": """Given this note and the list of existing notes, 
identify meaningful connections.

Current note:
Title: {title}
Content: {content}

Existing notes:
{existing_notes}

For each connection, explain:
1. The linked note title
2. Type of connection (supports, contradicts, extends, example-of, etc.)
3. Brief explanation of the relationship

Connections (JSON array):""",

    "ask_questions": """Based on this content, generate thoughtful questions that:
1. Test understanding of key concepts
2. Explore implications and applications
3. Identify gaps or areas for further research

Content:
{content}

Questions:""",

    "expand_note": """Expand on this note by:
1. Adding more context and explanation
2. Providing examples
3. Connecting to broader themes
4. Suggesting related topics to explore

Current note:
{content}

Expanded version:""",

    "daily_review": """Based on these notes from today, provide:
1. A summary of themes and topics covered
2. Connections between today's notes and existing knowledge
3. Suggestions for follow-up and consolidation
4. Questions to reflect on

Today's notes:
{notes}

Daily review:"""
}
```

### 5.3 Intelligent Query System

```python
# llm/query.py
import re
from typing import Optional

class IntelligentQuery:
    """Natural language query interface for the knowledge base"""
    
    def __init__(self, llm: LLMService, kb: KnowledgeBase):
        self.llm = llm
        self.kb = kb
    
    async def query(self, question: str) -> str:
        """Answer questions using knowledge base context"""
        
        # Step 1: Understand query intent
        intent = await self._classify_intent(question)
        
        # Step 2: Retrieve relevant context
        context = await self._retrieve_context(question, intent)
        
        # Step 3: Generate answer
        answer = await self._generate_answer(question, context, intent)
        
        # Step 4: Add source citations
        answer_with_sources = self._add_citations(answer, context)
        
        return answer_with_sources
    
    async def _classify_intent(self, question: str) -> dict:
        prompt = """Classify this question's intent:

Question: {question}

Categories:
- factual: Looking for specific information
- synthesis: Combining multiple pieces of knowledge
- exploration: Discovering related topics
- comparison: Comparing concepts
- application: How to apply knowledge
- reflection: Personal reflection/journaling

Also identify:
- Key concepts to search for
- Time constraints (if any)
- Specific sources to prioritize

JSON response:"""

        response = await self.llm.complete(
            prompt.format(question=question),
            response_format={"type": "json_object"}
        )
        return json.loads(response)
    
    async def _retrieve_context(self, question: str, intent: dict) -> list[dict]:
        """Multi-strategy retrieval"""
        results = []
        
        # Vector similarity search
        query_embedding = await self.llm.embed(question)
        vector_results = await self.kb.vector_search(query_embedding, top_k=10)
        results.extend(vector_results)
        
        # Keyword search for specific concepts
        for concept in intent.get("concepts", []):
            keyword_results = await self.kb.keyword_search(concept)
            results.extend(keyword_results)
        
        # Graph traversal for connected notes
        if intent["type"] == "synthesis":
            for note in vector_results[:3]:
                connected = await self.kb.get_connected_notes(note.id, depth=2)
                results.extend(connected)
        
        # Deduplicate and rank
        unique_results = self._deduplicate_and_rank(results, intent)
        
        return unique_results[:15]
    
    async def _generate_answer(
        self, 
        question: str, 
        context: list[dict], 
        intent: dict
    ) -> str:
        context_text = "\n\n---\n\n".join([
            f"**{note['title']}**\n{note['content'][:1000]}"
            for note in context
        ])
        
        prompt = f"""Answer this question using ONLY the provided context from my notes.
If the answer isn't in the context, say so.

Question: {question}

Context from my notes:
{context_text}

Instructions:
- Be specific and cite which notes support your answer
- If synthesizing, explain how pieces connect
- Highlight any contradictions or gaps
- Suggest follow-up questions if relevant

Answer:"""

        return await self.llm.complete(prompt)
    
    async def synthesize_topic(self, topic: str) -> str:
        """Generate a comprehensive synthesis of a topic"""
        
        # Get all related notes
        related_notes = await self.kb.search(topic, limit=50)
        
        # Cluster into subtopics
        clusters = await self._cluster_notes(related_notes)
        
        # Generate synthesis for each cluster
        syntheses = []
        for cluster_name, notes in clusters.items():
            synthesis = await self._synthesize_cluster(cluster_name, notes)
            syntheses.append(synthesis)
        
        # Combine into final document
        final = await self._combine_syntheses(topic, syntheses)
        
        return final
```

---

## 6. Storage & Retrieval Layer

### 6.1 Knowledge Base Implementation

```python
# storage/knowledge_base.py
import os
import sqlite3
from pathlib import Path
import yaml
import chromadb
from chromadb.config import Settings
import networkx as nx

class KnowledgeBase:
    """Core storage and retrieval system"""
    
    def __init__(self, base_path: str, config: dict):
        self.base_path = Path(base_path)
        self.config = config
        
        # Initialize components
        self._init_sqlite()
        self._init_vector_store()
        self._init_graph()
        self._init_file_watcher()
    
    def _init_sqlite(self):
        """SQLite for metadata and full-text search"""
        db_path = self.base_path / ".system" / "metadata.db"
        self.db = sqlite3.connect(str(db_path))
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                filepath TEXT UNIQUE,
                title TEXT,
                content TEXT,
                frontmatter TEXT,
                created_at TIMESTAMP,
                modified_at TIMESTAMP,
                indexed_at TIMESTAMP
            )
        """)
        self.db.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts USING fts5(
                title, content, tags,
                content='notes',
                content_rowid='rowid'
            )
        """)
    
    def _init_vector_store(self):
        """ChromaDB for vector similarity search"""
        chroma_path = self.base_path / ".system" / "embeddings"
        self.chroma = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(chroma_path),
            anonymized_telemetry=False
        ))
        self.collection = self.chroma.get_or_create_collection(
            name="notes",
            metadata={"hnsw:space": "cosine"}
        )
    
    def _init_graph(self):
        """NetworkX for relationship graph"""
        graph_path = self.base_path / ".system" / "graphs" / "knowledge.graphml"
        if graph_path.exists():
            self.graph = nx.read_graphml(str(graph_path))
        else:
            self.graph = nx.DiGraph()
    
    async def index_note(self, filepath: str) -> None:
        """Index a single note"""
        path = self.base_path / filepath
        content = path.read_text()
        
        # Parse frontmatter
        frontmatter, body = self._parse_markdown(content)
        
        # Generate embedding
        embedding = await self.embedder.embed(
            f"{frontmatter.get('title', '')}\n{body}"
        )
        
        # Store in SQLite
        self.db.execute("""
            INSERT OR REPLACE INTO notes 
            (id, filepath, title, content, frontmatter, modified_at, indexed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            frontmatter.get('id', filepath),
            filepath,
            frontmatter.get('title', ''),
            body,
            yaml.dump(frontmatter),
            os.path.getmtime(path),
            datetime.utcnow()
        ))
        
        # Store in vector DB
        self.collection.upsert(
            ids=[frontmatter.get('id', filepath)],
            embeddings=[embedding],
            documents=[body[:5000]],
            metadatas=[{
                "title": frontmatter.get('title', ''),
                "filepath": filepath,
                "tags": ",".join(frontmatter.get('tags', [])),
            }]
        )
        
        # Update graph
        self._update_graph(filepath, frontmatter, body)
    
    def _update_graph(self, filepath: str, frontmatter: dict, body: str):
        """Update knowledge graph with note relationships"""
        note_id = frontmatter.get('id', filepath)
        
        # Add/update node
        self.graph.add_node(
            note_id,
            title=frontmatter.get('title', ''),
            type=frontmatter.get('type', 'note'),
            tags=frontmatter.get('tags', [])
        )
        
        # Extract wikilinks
        wikilinks = re.findall(r'\[\[(.*?)(?:\|.*?)?\]\]', body)
        
        # Add edges for each link
        for link in wikilinks:
            target_id = self._resolve_link(link)
            if target_id:
                self.graph.add_edge(
                    note_id, 
                    target_id,
                    type="links_to"
                )
        
        # Add explicit relationships from frontmatter
        for related in frontmatter.get('related', []):
            target_id = self._resolve_link(related)
            if target_id:
                self.graph.add_edge(note_id, target_id, type="related")
        
        if frontmatter.get('parent'):
            parent_id = self._resolve_link(frontmatter['parent'])
            if parent_id:
                self.graph.add_edge(note_id, parent_id, type="child_of")
    
    async def vector_search(
        self, 
        query_embedding: list[float], 
        top_k: int = 10,
        threshold: float = 0.0,
        filters: dict = None
    ) -> list[dict]:
        """Search by vector similarity"""
        where_clause = None
        if filters:
            where_clause = self._build_where_clause(filters)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause,
            include=["documents", "metadatas", "distances"]
        )
        
        return [
            {
                "id": id,
                "content": doc,
                "metadata": meta,
                "score": 1 - dist  # Convert distance to similarity
            }
            for id, doc, meta, dist in zip(
                results['ids'][0],
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )
            if 1 - dist >= threshold
        ]
    
    async def get_connected_notes(
        self, 
        note_id: str, 
        depth: int = 1,
        relationship_types: list[str] = None
    ) -> list[dict]:
        """Get notes connected in the knowledge graph"""
        if note_id not in self.graph:
            return []
        
        # BFS to find connected nodes
        connected = set()
        queue = [(note_id, 0)]
        
        while queue:
            current, current_depth = queue.pop(0)
            if current_depth >= depth:
                continue
            
            for neighbor in self.graph.neighbors(current):
                edge_data = self.graph.edges[current, neighbor]
                
                if relationship_types and edge_data.get('type') not in relationship_types:
                    continue
                
                if neighbor not in connected:
                    connected.add(neighbor)
                    queue.append((neighbor, current_depth + 1))
        
        # Fetch full note data
        notes = []
        for nid in connected:
            note = await self.get_note(nid)
            if note:
                notes.append(note)
        
        return notes
    
    async def find_orphans(self) -> list[str]:
        """Find notes with no incoming or outgoing links"""
        orphans = []
        for node in self.graph.nodes():
            if self.graph.degree(node) == 0:
                orphans.append(node)
        return orphans
    
    async def find_clusters(self) -> list[set]:
        """Find clusters of related notes"""
        return list(nx.weakly_connected_components(self.graph))
    
    async def suggest_links(self, note_id: str) -> list[dict]:
        """Suggest potential links for a note"""
        note = await self.get_note(note_id)
        if not note:
            return []
        
        # Get embedding
        embedding = await self.embedder.embed(note['content'])
        
        # Find similar notes
        similar = await self.vector_search(embedding, top_k=20)
        
        # Filter out already linked notes
        current_links = set(self.graph.neighbors(note_id))
        suggestions = [
            s for s in similar 
            if s['id'] != note_id and s['id'] not in current_links
        ]
        
        return suggestions[:10]
```

### 6.2 File Watcher for Auto-Sync

```python
# storage/watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import asyncio

class NoteWatcher(FileSystemEventHandler):
    """Watch for changes to markdown files"""
    
    def __init__(self, kb: KnowledgeBase, debounce_ms: int = 1000):
        self.kb = kb
        self.debounce_ms = debounce_ms
        self.pending_changes = {}
        self._loop = asyncio.get_event_loop()
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            self._schedule_index(event.src_path)
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            self._schedule_index(event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            filepath = self._to_relative(event.src_path)
            self._loop.create_task(self.kb.remove_note(filepath))
    
    def _schedule_index(self, path: str):
        """Debounce rapid changes"""
        if path in self.pending_changes:
            self.pending_changes[path].cancel()
        
        async def do_index():
            await asyncio.sleep(self.debounce_ms / 1000)
            filepath = self._to_relative(path)
            await self.kb.index_note(filepath)
            del self.pending_changes[path]
        
        self.pending_changes[path] = self._loop.create_task(do_index())

def start_watcher(base_path: str, kb: KnowledgeBase):
    event_handler = NoteWatcher(kb)
    observer = Observer()
    observer.schedule(event_handler, base_path, recursive=True)
    observer.start()
    return observer
```

---

## 7. Daily Workflows & Automation

### 7.1 Daily Review System

```python
# workflows/daily.py
from datetime import datetime, timedelta

class DailyWorkflow:
    """Automated daily review and maintenance"""
    
    def __init__(self, kb: KnowledgeBase, llm: LLMService):
        self.kb = kb
        self.llm = llm
    
    async def morning_review(self) -> str:
        """Generate morning review"""
        
        # Get yesterday's notes
        yesterday = datetime.now() - timedelta(days=1)
        recent_notes = await self.kb.get_notes_since(yesterday)
        
        # Get due reviews (spaced repetition)
        due_reviews = await self.kb.get_notes_due_for_review()
        
        # Get stale notes
        stale_notes = await self.kb.get_notes_older_than(
            days=30, 
            status="seedling"
        )
        
        # Generate AI summary
        prompt = f"""Create a morning review based on:

Recent Notes ({len(recent_notes)}):
{self._format_notes(recent_notes[:10])}

Due for Review ({len(due_reviews)}):
{self._format_notes(due_reviews[:5])}

Stale Notes Needing Attention ({len(stale_notes)}):
{self._format_notes(stale_notes[:5])}

Please provide:
1. Summary of yesterday's learning themes
2. Connections to explore today
3. Prioritized review list
4. One note to develop further

Morning Review:"""

        review = await self.llm.complete(prompt)
        
        # Create daily note
        await self._create_daily_note(review, recent_notes, due_reviews)
        
        return review
    
    async def evening_reflection(self) -> str:
        """Generate evening reflection prompts"""
        
        # Get today's notes
        today = datetime.now().replace(hour=0, minute=0, second=0)
        todays_notes = await self.kb.get_notes_since(today)
        
        # Get today's highlights/captures
        todays_captures = await self.kb.get_captures_since(today)
        
        prompt = f"""Based on today's activity, generate reflection prompts:

Notes Created/Modified Today:
{self._format_notes(todays_notes)}

Content Captured Today:
{self._format_captures(todays_captures)}

Generate:
1. What patterns do you notice in today's learning?
2. What connections can be made between today's topics?
3. What questions remain unanswered?
4. What should be consolidated into permanent notes?

Reflection:"""

        return await self.llm.complete(prompt)
    
    async def weekly_synthesis(self) -> str:
        """Generate weekly knowledge synthesis"""
        
        week_ago = datetime.now() - timedelta(days=7)
        
        # Get all notes from the week
        weekly_notes = await self.kb.get_notes_since(week_ago)
        
        # Cluster by topic
        clusters = await self._cluster_notes_by_topic(weekly_notes)
        
        # Generate synthesis
        prompt = f"""Create a weekly knowledge synthesis:

This Week's Topics and Notes:
{self._format_clusters(clusters)}

Statistics:
- Total notes: {len(weekly_notes)}
- New permanent notes: {self._count_by_type(weekly_notes, 'permanent')}
- Sources processed: {self._count_by_type(weekly_notes, 'literature')}

Generate:
1. Main themes of the week
2. Key insights gained
3. Knowledge gaps identified
4. Connections made between topics
5. Action items for next week
6. Concepts to develop further

Weekly Synthesis:"""

        synthesis = await self.llm.complete(prompt)
        
        # Create weekly note
        await self._create_weekly_note(synthesis)
        
        return synthesis

### 7.2 Spaced Repetition Integration

```python
# workflows/spaced_repetition.py
from datetime import datetime, timedelta
from enum import Enum

class ReviewRating(Enum):
    AGAIN = 0  # Forgot
    HARD = 1   # Difficult recall
    GOOD = 2   # Correct with effort
    EASY = 3   # Instant recall

class SpacedRepetition:
    """SM-2 based spaced repetition for note review"""
    
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
    
    async def get_due_cards(self, limit: int = 20) -> list[dict]:
        """Get notes due for review"""
        return await self.kb.query(
            """
            SELECT * FROM note_reviews 
            WHERE next_review <= ? 
            ORDER BY next_review ASC 
            LIMIT ?
            """,
            [datetime.now(), limit]
        )
    
    async def review_note(self, note_id: str, rating: ReviewRating) -> dict:
        """Process a review and calculate next interval"""
        
        review = await self.kb.get_review_data(note_id)
        
        if review is None:
            # First review
            review = {
                "note_id": note_id,
                "easiness": 2.5,
                "interval": 1,
                "repetitions": 0
            }
        
        # SM-2 algorithm
        if rating == ReviewRating.AGAIN:
            review["repetitions"] = 0
            review["interval"] = 1
        else:
            if review["repetitions"] == 0:
                review["interval"] = 1
            elif review["repetitions"] == 1:
                review["interval"] = 6
            else:
                review["interval"] = round(review["interval"] * review["easiness"])
            
            review["repetitions"] += 1
        
        # Update easiness factor
        rating_value = rating.value
        review["easiness"] = max(
            1.3,
            review["easiness"] + (0.1 - (3 - rating_value) * (0.08 + (3 - rating_value) * 0.02))
        )
        
        # Calculate next review date
        review["next_review"] = datetime.now() + timedelta(days=review["interval"])
        
        await self.kb.save_review_data(review)
        
        return review
    
    async def generate_review_questions(self, note_id: str) -> list[str]:
        """Generate questions for a note using LLM"""
        
        note = await self.kb.get_note(note_id)
        
        prompt = f"""Generate 3 review questions for this note. 
Questions should test:
1. Core concept understanding
2. Connections to other ideas
3. Practical application

Note:
Title: {note['title']}
Content: {note['content'][:2000]}

Generate questions that would help reinforce memory of key concepts.

Questions:"""

        response = await self.llm.complete(prompt)
        questions = response.strip().split('\n')
        return [q.strip() for q in questions if q.strip()]
```

### 7.3 Automated Maintenance

```python
# workflows/maintenance.py

class MaintenanceWorkflow:
    """Automated knowledge base maintenance"""
    
    async def run_daily_maintenance(self):
        """Run daily maintenance tasks"""
        
        # 1. Find and report orphan notes
        orphans = await self.kb.find_orphans()
        if orphans:
            await self._create_report("orphan_notes", orphans)
        
        # 2. Find duplicate or similar notes
        duplicates = await self._find_potential_duplicates()
        if duplicates:
            await self._create_report("potential_duplicates", duplicates)
        
        # 3. Update stale tags
        await self._consolidate_tags()
        
        # 4. Re-index modified notes
        await self._reindex_modified()
        
        # 5. Backup
        await self._create_backup()
    
    async def _find_potential_duplicates(self) -> list[tuple]:
        """Find notes with high similarity that might be duplicates"""
        
        all_notes = await self.kb.get_all_notes()
        potential_duplicates = []
        
        for i, note in enumerate(all_notes):
            # Get similar notes
            similar = await self.kb.vector_search(
                note['embedding'],
                top_k=5,
                threshold=0.9
            )
            
            for match in similar:
                if match['id'] != note['id']:
                    potential_duplicates.append((
                        note['id'],
                        match['id'],
                        match['score']
                    ))
        
        # Deduplicate pairs
        seen = set()
        unique_pairs = []
        for a, b, score in potential_duplicates:
            pair = tuple(sorted([a, b]))
            if pair not in seen:
                seen.add(pair)
                unique_pairs.append((a, b, score))
        
        return unique_pairs
    
    async def _consolidate_tags(self):
        """Use LLM to suggest tag consolidation"""
        
        all_tags = await self.kb.get_all_tags()
        
        prompt = f"""Review these tags and suggest consolidation:

Current tags ({len(all_tags)}):
{', '.join(all_tags)}

Identify:
1. Duplicate or similar tags to merge
2. Tags that should be split
3. Missing high-level category tags
4. Suggested tag hierarchy

Consolidation suggestions (JSON):"""

        suggestions = await self.llm.complete(
            prompt,
            response_format={"type": "json_object"}
        )
        
        return json.loads(suggestions)
    
    async def suggest_note_improvements(self, note_id: str) -> dict:
        """Analyze a note and suggest improvements"""
        
        note = await self.kb.get_note(note_id)
        connections = await self.kb.get_connected_notes(note_id)
        similar = await self.kb.vector_search(note['embedding'], top_k=10)
        
        prompt = f"""Analyze this note and suggest improvements:

Note:
{note['content']}

Current connections: {len(connections)}
Similar notes found: {len(similar)}

Evaluate and suggest:
1. Clarity: Is the main idea clear?
2. Atomicity: Should this be split into multiple notes?
3. Completeness: What information is missing?
4. Connections: What links should be added?
5. Development: How could this be expanded?
6. Status: Should the status (seedling/growing/evergreen) change?

Analysis (JSON):"""

        analysis = await self.llm.complete(
            prompt,
            response_format={"type": "json_object"}
        )
        
        return json.loads(analysis)
```

---

## 8. API & Interface Layer

### 8.1 REST API

```python
# api/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Second Brain API")

# Initialize services
kb = KnowledgeBase(config["base_path"], config)
llm = LLMService(config["llm"])
processor = ContentProcessor(llm, kb)

class IngestRequest(BaseModel):
    url: Optional[str] = None
    content: Optional[str] = None
    title: Optional[str] = None
    type: str = "web"
    metadata: dict = {}

class QueryRequest(BaseModel):
    question: str
    filters: Optional[dict] = None
    include_sources: bool = True

class NoteCreate(BaseModel):
    title: str
    content: str
    type: str = "fleeting"
    tags: list[str] = []
    parent: Optional[str] = None

@app.post("/api/ingest")
async def ingest_content(request: IngestRequest, background_tasks: BackgroundTasks):
    """Ingest new content into the second brain"""
    
    # Add to processing queue
    task_id = str(uuid.uuid4())
    background_tasks.add_task(process_ingestion, task_id, request)
    
    return {"task_id": task_id, "status": "queued"}

@app.get("/api/ingest/{task_id}")
async def get_ingestion_status(task_id: str):
    """Check status of ingestion task"""
    status = await get_task_status(task_id)
    return status

@app.post("/api/query")
async def query_knowledge(request: QueryRequest):
    """Query the knowledge base"""
    
    query_engine = IntelligentQuery(llm, kb)
    
    answer = await query_engine.query(request.question)
    
    return {
        "answer": answer,
        "sources": answer.sources if request.include_sources else []
    }

@app.get("/api/search")
async def search(
    q: str,
    type: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 20
):
    """Search notes"""
    
    filters = {}
    if type:
        filters["type"] = type
    if tags:
        filters["tags"] = tags.split(",")
    
    results = await kb.search(q, filters=filters, limit=limit)
    
    return {"results": results}

@app.post("/api/notes")
async def create_note(note: NoteCreate):
    """Create a new note"""
    
    # Generate ID
    note_id = str(uuid.uuid4())
    
    # Build frontmatter
    frontmatter = {
        "id": note_id,
        "title": note.title,
        "type": note.type,
        "tags": note.tags,
        "created": datetime.utcnow().isoformat(),
        "status": "seedling"
    }
    
    if note.parent:
        frontmatter["parent"] = note.parent
    
    # Generate markdown
    content = f"""---
{yaml.dump(frontmatter)}---

# {note.title}

{note.content}
"""
    
    # Determine path
    filepath = f"02-notes/{note.type}/{note_id}.md"
    
    # Save and index
    await kb.save_note(filepath, content)
    await kb.index_note(filepath)
    
    return {"id": note_id, "filepath": filepath}

@app.get("/api/notes/{note_id}")
async def get_note(note_id: str):
    """Get a specific note"""
    note = await kb.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.get("/api/notes/{note_id}/connections")
async def get_connections(note_id: str, depth: int = 1):
    """Get connected notes"""
    connections = await kb.get_connected_notes(note_id, depth=depth)
    return {"connections": connections}

@app.post("/api/notes/{note_id}/suggest-links")
async def suggest_links(note_id: str):
    """Get AI-suggested links for a note"""
    suggestions = await kb.suggest_links(note_id)
    return {"suggestions": suggestions}

@app.get("/api/graph")
async def get_knowledge_graph(
    center: Optional[str] = None,
    depth: int = 2
):
    """Get knowledge graph data for visualization"""
    
    if center:
        subgraph = await kb.get_subgraph(center, depth)
    else:
        subgraph = await kb.get_graph_overview()
    
    return {
        "nodes": [
            {"id": n, **kb.graph.nodes[n]} 
            for n in subgraph.nodes()
        ],
        "edges": [
            {"source": u, "target": v, **d}
            for u, v, d in subgraph.edges(data=True)
        ]
    }

@app.post("/api/daily/review")
async def trigger_daily_review():
    """Trigger daily review generation"""
    workflow = DailyWorkflow(kb, llm)
    review = await workflow.morning_review()
    return {"review": review}

@app.get("/api/stats")
async def get_statistics():
    """Get knowledge base statistics"""
    return {
        "total_notes": await kb.count_notes(),
        "by_type": await kb.count_by_type(),
        "by_status": await kb.count_by_status(),
        "total_connections": kb.graph.number_of_edges(),
        "orphan_notes": len(await kb.find_orphans()),
        "tags_used": len(await kb.get_all_tags()),
        "last_indexed": await kb.get_last_index_time()
    }
```

### 8.2 CLI Interface

```python
# cli/main.py
import click
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

console = Console()

@click.group()
def cli():
    """Second Brain CLI"""
    pass

@cli.command()
@click.argument('url')
@click.option('--tags', '-t', multiple=True, help='Tags to add')
def clip(url, tags):
    """Clip a web page"""
    with console.status("Clipping..."):
        result = api.ingest(url=url, tags=list(tags))
    console.print(f"✓ Clipped: {result['filepath']}")

@cli.command()
@click.argument('query')
@click.option('--limit', '-l', default=10)
def search(query, limit):
    """Search notes"""
    results = api.search(query, limit=limit)
    
    table = Table(title=f"Search Results: {query}")
    table.add_column("Title")
    table.add_column("Type")
    table.add_column("Score")
    
    for r in results:
        table.add_row(r['title'], r['type'], f"{r['score']:.0%}")
    
    console.print(table)

@cli.command()
@click.argument('question')
def ask(question):
    """Ask a question"""
    with console.status("Thinking..."):
        answer = api.query(question)
    
    console.print(Markdown(answer['answer']))
    
    if answer.get('sources'):
        console.print("\n[dim]Sources:[/dim]")
        for source in answer['sources']:
            console.print(f"  • {source}")

@cli.command()
@click.option('--type', '-t', default='fleeting')
def new(type):
    """Create a new note"""
    import tempfile
    import subprocess
    import os
    
    # Create temp file with template
    template = get_template(type)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(template)
        temp_path = f.name
    
    # Open in editor
    editor = os.environ.get('EDITOR', 'vim')
    subprocess.call([editor, temp_path])
    
    # Read edited content
    with open(temp_path) as f:
        content = f.read()
    
    # Save to knowledge base
    result = api.create_note(content=content, type=type)
    console.print(f"✓ Created: {result['filepath']}")
    
    os.unlink(temp_path)

@cli.command()
def daily():
    """Run daily review"""
    with console.status("Generating daily review..."):
        review = api.daily_review()
    
    console.print(Markdown(review))

@cli.command()
def review():
    """Start spaced repetition review session"""
    cards = api.get_due_reviews()
    
    if not cards:
        console.print("No cards due for review!")
        return
    
    console.print(f"[bold]{len(cards)} cards due for review[/bold]\n")
    
    for card in cards:
        console.print(Markdown(f"# {card['title']}\n\n{card['content']}"))
        
        console.print("\n[dim]Rate your recall:[/dim]")
        console.print("  [1] Again  [2] Hard  [3] Good  [4] Easy  [q] Quit")
        
        rating = click.getchar()
        
        if rating == 'q':
            break
        
        rating_map = {'1': 0, '2': 1, '3': 2, '4': 3}
        if rating in rating_map:
            result = api.review_card(card['id'], rating_map[rating])
            console.print(f"Next review: {result['next_review']}\n")

@cli.command()
def status():
    """Show knowledge base status"""
    stats = api.get_stats()
    
    console.print("\n[bold]📚 Second Brain Status[/bold]\n")
    console.print(f"Total Notes: {stats['total_notes']}")
    console.print(f"Connections: {stats['total_connections']}")
    console.print(f"Orphan Notes: {stats['orphan_notes']}")
    
    table = Table(title="By Type")
    table.add_column("Type")
    table.add_column("Count")
    for t, c in stats['by_type'].items():
        table.add_row(t, str(c))
    console.print(table)

if __name__ == '__main__':
    cli()
```

---

## 9. Configuration

### 9.1 Main Configuration File

```yaml
# config/config.yaml

# Base paths
base_path: ~/second-brain
backup_path: ~/second-brain-backups

# LLM Configuration
llm:
  default: openai
  
  openai:
    api_key: ${OPENAI_API_KEY}
    model: gpt-4-turbo
    embedding_model: text-embedding-3-small
    
  ollama:
    host: http://localhost:11434
    model: llama3:8b
    embedding_model: nomic-embed-text

# Ingestion sources
ingestion:
  web:
    enabled: true
    js_rendering: false
    
  email:
    enabled: true
    imap_server: imap.gmail.com
    folder: SecondBrain
    
  rss:
    enabled: true
    feeds:
      - url: https://example.com/feed.xml
        tags: [tech, news]
        priority: 2
        
  readwise:
    enabled: true
    api_key: ${READWISE_API_KEY}
    sync_interval: 3600

# Processing
processing:
  auto_tag: true
  auto_summarize: true
  auto_link: true
  min_content_length: 100
  
# Storage
storage:
  vector_db: chromadb
  embedding_dim: 1536
  
# Workflows
workflows:
  daily_review:
    enabled: true
    time: "08:00"
    
  weekly_synthesis:
    enabled: true
    day: sunday
    time: "18:00"
    
  maintenance:
    enabled: true
    time: "03:00"
    
# Spaced repetition
spaced_repetition:
  enabled: true
  new_cards_per_day: 10
  review_order: due_date

# API
api:
  host: 0.0.0.0
  port: 8080
  cors_origins:
    - http://localhost:3000
```

---

## 10. Deployment

### 10.1 Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ${BRAIN_PATH:-./data}:/app/second-brain
      - ./config:/app/config
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - READWISE_API_KEY=${READWISE_API_KEY}
    depends_on:
      - redis
      - ollama
    restart: unless-stopped

  worker:
    build: .
    command: python -m celery -A tasks worker
    volumes:
      - ${BRAIN_PATH:-./data}:/app/second-brain
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - redis
    restart: unless-stopped

  scheduler:
    build: .
    command: python -m celery -A tasks beat
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]

volumes:
  redis_data:
  ollama_data:
```

### 10.2 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 11. Extension Points

### 11.1 Plugin System

```python
# plugins/base.py
from abc import ABC, abstractmethod

class Plugin(ABC):
    """Base class for Second Brain plugins"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        pass
    
    @abstractmethod
    async def initialize(self, kb: KnowledgeBase, llm: LLMService):
        """Called when plugin is loaded"""
        pass
    
    @abstractmethod
    async def shutdown(self):
        """Called when plugin is unloaded"""
        pass

class IngestionPlugin(Plugin):
    """Plugin for custom ingestion sources"""
    
    @abstractmethod
    async def ingest(self, source: str) -> IngestedContent:
        pass

class ProcessingPlugin(Plugin):
    """Plugin for custom processing steps"""
    
    @abstractmethod
    async def process(self, content: IngestedContent) -> IngestedContent:
        pass

class ExportPlugin(Plugin):
    """Plugin for exporting to external systems"""
    
    @abstractmethod
    async def export(self, notes: list[dict]) -> None:
        pass
```

### 11.2 Example Custom Plugin: Twitter/X Integration

```python
# plugins/twitter.py

class TwitterPlugin(IngestionPlugin):
    """Ingest Twitter bookmarks and threads"""
    
    name = "twitter"
    version = "1.0.0"
    
    async def initialize(self, kb, llm):
        self.kb = kb
        self.llm = llm
        self.client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER"))
    
    async def ingest_bookmarks(self) -> list[IngestedContent]:
        """Fetch and process Twitter bookmarks"""
        bookmarks = self.client.get_bookmarks(
            expansions=["author_id", "referenced_tweets.id"],
            tweet_fields=["created_at", "text", "context_annotations"]
        )
        
        contents = []
        for tweet in bookmarks.data:
            # Check if it's a thread
            if self._is_thread(tweet):
                content = await self._fetch_thread(tweet)
            else:
                content = self._process_single_tweet(tweet)
            
            contents.append(content)
        
        return contents
    
    async def _fetch_thread(self, tweet) -> IngestedContent:
        """Fetch entire thread and combine"""
        # Implementation...
        pass
```

---

## 12. Usage Examples

### Basic Workflow

```bash
# 1. Clip a web article
brain clip "https://example.com/article" -t programming -t architecture

# 2. Search your notes
brain search "microservices patterns"

# 3. Ask a question
brain ask "What are the tradeoffs between monoliths and microservices?"

# 4. Create a new note
brain new --type permanent

# 5. Run daily review
brain daily

# 6. Start review session
brain review

# 7. Check status
brain status
```

### API Usage

```python
import requests

# Ingest content
response = requests.post("http://localhost:8080/api/ingest", json={
    "url": "https://example.com/article",
    "tags": ["programming", "architecture"]
})

# Query knowledge base
response = requests.post("http://localhost:8080/api/query", json={
    "question": "What are the best practices for API design?"
})
print(response.json()["answer"])

# Get knowledge graph
response = requests.get("http://localhost:8080/api/graph?center=api-design&depth=2")
graph_data = response.json()
```

---

## Summary

This framework provides:

1. **Structured Storage**: Markdown files with rich frontmatter organized in PARA-inspired folders
2. **Automated Ingestion**: Browser extension, email forwarding, RSS, API webhooks
3. **LLM Processing**: Auto-summarization, tagging, connection discovery
4. **Vector Search**: Semantic search across all content
5. **Knowledge Graph**: Relationship tracking and visualization
6. **Daily Workflows**: Automated reviews, spaced repetition, maintenance
7. **Multiple Interfaces**: REST API, CLI, browser extension
8. **Extensibility**: Plugin system for custom sources and processing

The system is designed to be self-hosted, privacy-respecting (with local LLM options), and to grow with your knowledge over time.
