import type { NodeStatus, PipelineNodeMeta } from "@/lib/types";
import { Check, Loader, X, iconForNode } from "./Icons";

interface AgentPipelineProps {
  nodes: PipelineNodeMeta[];
  statuses: Record<string, NodeStatus>;
  activeLabel: string;
  latestMessage: string;
  isRunning: boolean;
  errored: boolean;
  llmCalls: number;
}

export function AgentPipeline({
  nodes,
  statuses,
  activeLabel,
  latestMessage,
  isRunning,
  errored,
  llmCalls,
}: AgentPipelineProps) {
  const doneCount = nodes.filter((n) => statuses[n.id] === "done").length;

  let headerIcon = <Check style={{ color: "var(--mint)" }} />;
  let headerText = "Pipeline complete";
  if (isRunning) {
    headerIcon = <Loader className="spin" />;
    headerText = activeLabel || "Starting agents…";
  } else if (errored) {
    headerIcon = <X style={{ color: "#ff7a7a" }} />;
    headerText = "Pipeline stopped";
  }

  return (
    <div className="card pipeline reveal">
      <div className="pipeline-top">
        <div className="pipeline-title">
          {headerIcon}
          <span>{headerText}</span>
        </div>
        <div className="pipeline-counter">
          {doneCount}/{nodes.length} agents · {llmCalls} LLM calls
        </div>
      </div>

      <div className="pipeline-track">
        {nodes.map((node) => {
          const status = statuses[node.id] ?? "pending";
          const Icon = iconForNode[node.id] ?? iconForNode.request_parser;
          return (
            <div key={node.id} className={`pnode ${status}`}>
              <div className="pnode-dot">
                {status === "active" ? (
                  <Loader className="spin" />
                ) : status === "done" ? (
                  <Check />
                ) : status === "failed" ? (
                  <X />
                ) : (
                  <Icon />
                )}
              </div>
              <div className="pnode-label">{node.label}</div>
              <div className="pnode-desc">{node.description}</div>
            </div>
          );
        })}
      </div>

      {latestMessage ? (
        <div className="pipeline-log">
          <span className="tick">
            {isRunning ? (
              <Loader className="spin" width={16} height={16} />
            ) : errored ? (
              <X width={16} height={16} style={{ color: "#ff7a7a" }} />
            ) : (
              <Check width={16} height={16} />
            )}
          </span>
          <span>{latestMessage}</span>
        </div>
      ) : null}
    </div>
  );
}
