import React from "react";
import 'aframe';
import { ForceGraph2D } from "react-force-graph";


const data = {
    nodes: [
        { id: "Alice", val: 5 },
        { id: "Bob", val: 1 },
        { id: "Charlie", val: 5 },
        { id: "Dana", val: 1 }
    ],
    links: [
        { source: "Alice", target: "Bob", label: "baking" },
        { source: "Alice", target: "Charlie", label: "poetry" },
        { source: "Bob", target: "Dana", label: "climbing" },
        { source: "Bob", target: "Charlie", label: "climbing" },
    ]
}

const data2 = {
    nodes: [
      { id: "Alice", type: "person" },
      { id: "Bob", type: "person" },
      { id: "Charlie", type: "person" },
      { id: "baking", type: "interest" },
      { id: "poetry", type: "interest" },
      { id: "climbing", type: "interest" }
    ],
    links: [
      { source: "Alice", target: "baking" },
      { source: "Alice", target: "poetry" },
      { source: "Bob", target: "baking" },
      { source: "Bob", target: "climbing" },
      { source: "Charlie", target: "poetry" }
    ]
  };

  const data3 = {
    nodes: [
        { id: "Alice", type: "person" },
        { id: "Bob", type: "person" },
        { id: "Charlie", type: "person" },
        { id: "Dana", type: "person" },
        { id: "baking", type: "interest", val: 10 },
        { id: "poetry", type: "interest", val: 10 },
        { id: "climbing", type: "interest", val: 10  }
    ],
    links: [
        { source: "Alice", target: "Bob", label: "baking" },
        { source: "Alice", target: "Charlie", label: "poetry" },
        { source: "Bob", target: "Dana", label: "climbing" },
        { source: "Bob", target: "Charlie", label: "climbing" },
        { source: "Alice", target: "baking" },
        { source: "Alice", target: "poetry" },
        { source: "Bob", target: "baking" },
        { source: "Bob", target: "climbing" },
        { source: "Charlie", target: "poetry" }
    ]
}


export default function GraphView(props) {
    const { onNodeClick, graphData, isLoading } = props;
  console.log('isLoading', isLoading)

    return (
      isLoading ? (
        "Loading..."
      ) : (
        <ForceGraph2D
        onNodeClick={onNodeClick}

        graphData={graphData}
        nodeCanvasObject={(node, ctx, globalScale) => {

            const radius = 6 * (node.val || 1);
            ctx.beginPath();
            ctx.arc(node.x, node.y, radius, 0, 2 * Math.PI, false);
            ctx.fillStyle = node.color || 'orange';
            ctx.fill();
            ctx.strokeStyle = 'gray';
            ctx.stroke();

            const label = node.id; // or any other property
            const fontSize = 12 / globalScale;
            ctx.font = `${fontSize}px Sans-Serif`;
            ctx.fillStyle = 'black';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(label, node.x, node.y);
            
          }}
          nodePointerAreaPaint={(node, color, ctx) => {
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(node.x, node.y, 5, 0, 2 * Math.PI, false);
            ctx.fill();
          }}
          nodeLabel="id"
          linkLabel="label"
          nodeRelSize={6}
          nodeAutoColorBy="id"
    
    />
      )

    );
}