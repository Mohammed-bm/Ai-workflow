export function exportWorkflow(nodes, edges) {
  return {
    nodes: nodes.map((node) => ({
      id: node.id,
      type: node.type,
      config: node.data || {},
    })),
    edges: edges.map((edge) => ({
      from: edge.source,
      to: edge.target,
    })),
  };
}
