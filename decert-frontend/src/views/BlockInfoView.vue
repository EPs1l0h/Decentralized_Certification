<template>
  <div class="block-info-view">
    <div class="network-graph" ref="networkGraph"></div>
    <div class="global-info">
      <div class="info-item">
        <span class="label">Total Nodes:</span>
        <span class="value">{{ totalNodes }}</span>
      </div>
      <div class="info-item">
        <span class="label">Total Edges:</span>
        <span class="value">{{ totalEdges }}</span>
      </div>
    </div>
    <div class="node-info" v-if="selectedNode" ref="nodeInfo">
      <h3>{{ selectedNode.id }}</h3>
      <p>Type: {{ selectedNode.type }}</p>
      <p>DID: {{ selectedNode.did }}</p>
      <p>Transactions: {{ selectedNode.transactions }}</p>
      <p>Balance: {{ selectedNode.balance }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import * as d3 from "d3";

const networkGraph = ref<HTMLElement | null>(null);
const nodeInfo = ref<HTMLElement | null>(null);
const totalNodes = ref(0);
const totalEdges = ref(0);
const selectedNode = ref(null);

onMounted(() => {
  // 模拟区块链网络数据
  const data = {
    nodes: [
      {
        id: "node1",
        type: "miner",
        did: "did:example:123",
        transactions: 100,
        balance: 1000,
      },
      {
        id: "node2",
        type: "wallet",
        did: "did:example:456",
        transactions: 50,
        balance: 500,
      },
      {
        id: "node3",
        type: "contract",
        did: "did:example:789",
        transactions: 200,
        balance: 2000,
      },
      {
        id: "node4",
        type: "miner",
        did: "did:example:abc",
        transactions: 80,
        balance: 800,
      },
      {
        id: "node5",
        type: "wallet",
        did: "did:example:def",
        transactions: 30,
        balance: 300,
      },
      {
        id: "node6",
        type: "contract",
        did: "did:example:ghi",
        transactions: 150,
        balance: 1500,
      },
      {
        id: "node7",
        type: "miner",
        did: "did:example:jkl",
        transactions: 120,
        balance: 1200,
      },
    ],
    edges: [
      { source: "node1", target: "node2", type: "transfer", amount: 100 },
      { source: "node1", target: "node3", type: "call", gasUsed: 0.01 },
      { source: "node2", target: "node3", type: "call", gasUsed: 0.02 },
      { source: "node4", target: "node5", type: "transfer", amount: 200 },
      { source: "node4", target: "node6", type: "call", gasUsed: 0.015 },
      { source: "node5", target: "node6", type: "call", gasUsed: 0.025 },
      { source: "node7", target: "node1", type: "transfer", amount: 300 },
      { source: "node7", target: "node4", type: "transfer", amount: 150 },
    ],
  };

  // 更新全局统计信息
  totalNodes.value = data.nodes.length;
  totalEdges.value = data.edges.length;

  // 创建力导向图
  const forceGraph = d3
    .forceSimulation(data.nodes)
    .force(
      "link",
      d3
        .forceLink(data.edges)
        .id((d: any) => d.id)
        .distance((d: any) => {
          return 100; // 根据需要调整节点之间的距离
        })
    )
    .force("charge", d3.forceManyBody().strength(-800)) // 调整节点之间的斥力
    .force("center", d3.forceCenter(400, 300));

  // 创建 SVG 画布
  const svg = d3
    .select(networkGraph.value)
    .append("svg")
    .attr("width", 800)
    .attr("height", 600);

  // 定义箭头标记
  svg
    .append("defs")
    .append("marker")
    .attr("id", "arrow")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 20)
    .attr("refY", 0)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M0,-5L10,0L0,5")
    .attr("fill", (d: any) => {
      if (d && d.type) {
        switch (d.type) {
          case "transfer":
            return "#8E5EA2";
          case "call":
            return "#3CBA9F";
          default:
            return "#F5A623";
        }
      }
      return "#F5A623"; // Default color if d or d.type is undefined
    });

  // 绘制边
  const edges = svg
    .append("g")
    .selectAll("line")
    .data(data.edges)
    .join("line")
    .attr("stroke", (d) => {
      switch (d.type) {
        case "transfer":
          return "#8E5EA2";
        case "call":
          return "#3CBA9F";
        default:
          return "#F5A623";
      }
    })
    .attr("stroke-width", (d) => {
      switch (d.type) {
        case "transfer":
          return 2;
        case "call":
          return 1;
        default:
          return 1.5;
      }
    })
    .attr("marker-end", "url(#arrow)");

  // 绘制节点
  const nodes = svg
    .append("g")
    .selectAll("circle")
    .data(data.nodes)
    .join("circle")
    .attr("r", (d) => {
      switch (d.type) {
        case "miner":
          return 25;
        case "wallet":
          return 20;
        case "contract":
          return 30;
        default:
          return 22;
      }
    })
    .attr("fill", (d) => {
      switch (d.type) {
        case "miner":
          return "#4C4C4C";
        case "wallet":
          return "#69b3a2";
        case "contract":
          return "#F8B195";
        default:
          return "#4d4d4d";
      }
    })
    .attr("stroke", "white")
    .attr("stroke-width", 2)
    .call(drag(forceGraph));

  // 节点文字
  const nodeLabels = svg
    .append("g")
    .selectAll("text")
    .data(data.nodes)
    .join("text")
    .attr("dx", 0)
    .attr("dy", 40)
    .text((d) => d.id)
    .attr("fill", "black")
    .attr("font-family", "Arial")
    .attr("font-size", 12)
    .attr("text-anchor", "middle");

  // 节点悬停事件
  nodes
    .on("mouseover", (event, d) => {
      d3.select(event.target).attr("r", (d) => {
        switch (d.type) {
          case "miner":
            return 30;
          case "wallet":
            return 25;
          case "contract":
            return 35;
          default:
            return 27;
        }
      });
      selectedNode.value = d;
      updateNodeInfoPosition();
    })
    .on("mouseout", (event, d) => {
      d3.select(event.target).attr("r", (d) => {
        switch (d.type) {
          case "miner":
            return 25;
          case "wallet":
            return 20;
          case "contract":
            return 30;
          default:
            return 22;
        }
      });
      selectedNode.value = null;
    });

  // 边悬停事件
  edges
    .on("mouseover", (event, d) => {
      d3.select(event.target).attr("stroke-width", 3);
      nodes.attr("opacity", (n) =>
        n === d.source || n === d.target ? 1 : 0.2
      );
      nodeLabels.attr("opacity", (n) =>
        n === d.source || n === d.target ? 1 : 0.2
      );
      edges.attr("opacity", (e) => (e === d ? 1 : 0.2));
    })
    .on("mouseout", (event, d) => {
      d3.select(event.target).attr("stroke-width", (d) => {
        switch (d.type) {
          case "transfer":
            return 2;
          case "call":
            return 1;
          default:
            return 1.5;
        }
      });
      nodes.attr("opacity", 1);
      nodeLabels.attr("opacity", 1);
      edges.attr("opacity", 1);
    });

  // 启动力导向图
  forceGraph.on("tick", () => {
    edges
      .attr("x1", (d) => (d.source as any).x)
      .attr("y1", (d) => (d.source as any).y)
      .attr("x2", (d) => (d.target as any).x)
      .attr("y2", (d) => (d.target as any).y);
    nodes.attr("cx", (d) => (d as any).x).attr("cy", (d) => (d as any).y);
    nodeLabels.attr("x", (d) => (d as any).x).attr("y", (d) => (d as any).y);
  });
});

// 更新节点信息框的位置
function updateNodeInfoPosition() {
  const infoBox = nodeInfo.value;
  if (!infoBox) return;

  const svg = networkGraph.value;
  if (!svg) return;

  const rect = svg.getBoundingClientRect();
  infoBox.style.left = `${rect.right + 10}px`;
  infoBox.style.top = `${rect.top + 10}px`;
}

// 拖拽交互
function drag(simulation: d3.Simulation<any, undefined>) {
  function dragstarted(event: any) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }
  function dragged(event: any) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }
  function dragended(event: any) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }
  return d3
    .drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);
}
</script>

<style scoped>
.block-info-view {
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  background: linear-gradient(45deg, #f7f7f7, #e0e0e0);
}

.network-graph {
  flex: 1;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.global-info {
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
}

.info-item {
  margin-right: 20px;
  padding: 10px 20px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.label {
  font-weight: bold;
  color: #333;
}

.value {
  font-size: 24px;
  color: #69b3a2;
}

.node-info {
  position: absolute;
  padding: 10px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #ccc;
  border-radius: 4px;
  pointer-events: none;
  opacity: 0.9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 200px;
}
.node-info h3 {
  margin: 0 0 5px;
  font-size: 16px;
  color: #333;
}
.node-info p {
  margin: 0;
  font-size: 14px;
  color: #666;
}
</style>
