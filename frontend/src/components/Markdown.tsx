import type { ReactNode } from "react";

/**
 * A small, dependency-free Markdown renderer tuned for the LLM travel plan
 * output (headings, bold, links, bullet and numbered lists, paragraphs, rules).
 */

function renderInline(text: string, keyPrefix: string): ReactNode[] {
  const nodes: ReactNode[] = [];
  // Tokenize bold (**...**) and links [text](url); everything else is plain.
  const regex = /(\*\*([^*]+)\*\*)|(\[([^\]]+)\]\((https?:\/\/[^)\s]+)\))/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;
  let i = 0;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      nodes.push(text.slice(lastIndex, match.index));
    }
    if (match[2] !== undefined) {
      nodes.push(<strong key={`${keyPrefix}-b-${i}`}>{match[2]}</strong>);
    } else if (match[4] !== undefined && match[5] !== undefined) {
      nodes.push(
        <a key={`${keyPrefix}-a-${i}`} href={match[5]} target="_blank" rel="noreferrer">
          {match[4]}
        </a>,
      );
    }
    lastIndex = regex.lastIndex;
    i += 1;
  }
  if (lastIndex < text.length) nodes.push(text.slice(lastIndex));
  return nodes;
}

export function Markdown({ content }: { content: string }) {
  const lines = content.replace(/\r\n/g, "\n").split("\n");
  const blocks: ReactNode[] = [];

  let listBuffer: string[] = [];
  let listType: "ul" | "ol" | null = null;
  let key = 0;

  const flushList = () => {
    if (listBuffer.length === 0 || !listType) return;
    const items = listBuffer.map((item, idx) => (
      <li key={`li-${key}-${idx}`}>{renderInline(item, `li-${key}-${idx}`)}</li>
    ));
    blocks.push(
      listType === "ul" ? (
        <ul key={`list-${key}`}>{items}</ul>
      ) : (
        <ol key={`list-${key}`}>{items}</ol>
      ),
    );
    key += 1;
    listBuffer = [];
    listType = null;
  };

  for (const raw of lines) {
    const line = raw.trimEnd();
    const trimmed = line.trim();

    if (trimmed === "") {
      flushList();
      continue;
    }

    if (/^(-{3,}|\*{3,}|_{3,})$/.test(trimmed)) {
      flushList();
      blocks.push(<hr key={`hr-${key++}`} />);
      continue;
    }

    const heading = trimmed.match(/^(#{1,6})\s+(.*)$/);
    if (heading) {
      flushList();
      const level = Math.min(heading[1].length, 3);
      const text = heading[2].replace(/[*#]+$/, "").trim();
      const inner = renderInline(text, `h-${key}`);
      if (level === 1) blocks.push(<h1 key={`h-${key++}`}>{inner}</h1>);
      else if (level === 2) blocks.push(<h2 key={`h-${key++}`}>{inner}</h2>);
      else blocks.push(<h3 key={`h-${key++}`}>{inner}</h3>);
      continue;
    }

    const ordered = trimmed.match(/^\d+[.)]\s+(.*)$/);
    if (ordered) {
      if (listType === "ul") flushList();
      listType = "ol";
      listBuffer.push(ordered[1]);
      continue;
    }

    const bullet = trimmed.match(/^[-*•]\s+(.*)$/);
    if (bullet) {
      if (listType === "ol") flushList();
      listType = "ul";
      listBuffer.push(bullet[1]);
      continue;
    }

    flushList();
    blocks.push(<p key={`p-${key++}`}>{renderInline(trimmed, `p-${key}`)}</p>);
  }

  flushList();

  return <div className="md">{blocks}</div>;
}
