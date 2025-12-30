export function validateWorkflow(nodes, edges) {
  const errors = [];

  const incoming = {};
  const outgoing = {};

  nodes.forEach((n) => {
    incoming[n.id] = 0;
    outgoing[n.id] = 0;
  });

  edges.forEach((e) => {
    incoming[e.target]++;
    outgoing[e.source]++;
  });

  const startNodes = nodes.filter(
    (n) => n.type === "userQuery" && incoming[n.id] === 0
  );

  if (startNodes.length !== 1) {
    errors.push("Workflow must have exactly one User Query start node.");
  }

  const endNodes = nodes.filter(
    (n) => n.type === "output" && outgoing[n.id] === 0
  );

  if (endNodes.length !== 1) {
    errors.push("Workflow must have exactly one Output end node.");
  }

  const hasLLM = nodes.some((n) => n.type === "llmEngine");
  if (!hasLLM) {
    errors.push("Workflow must include an LLM Engine node.");
  }

  return errors;
}
