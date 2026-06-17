import { Markdown } from "./Markdown";

export function FinalPlan({ content }: { content: string }) {
  return (
    <div className="card final-wrap reveal">
      <div className="final-inner">
        <Markdown content={content} />
      </div>
    </div>
  );
}
