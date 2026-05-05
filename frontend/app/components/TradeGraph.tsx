"use client";

import { useEffect, useState } from "react";

export default function TradeGraph() {
  const [network, setNetwork] = useState<any>(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/trade-network`)
      .then((res) => res.json())
      .then(setNetwork);
  }, []);

  if (!network) return <p>Loading trade network...</p>;

  return (
    <div className="mt-6">
      <h2 className="font-semibold mb-2">Trade Network</h2>

      <div className="border p-4">
        <h3 className="font-medium">Nodes</h3>
        <ul className="text-sm">
          {network.nodes.map((n: any) => (
            <li key={n.id}>
              {n.name} ({n.type})
            </li>
          ))}
        </ul>

        <h3 className="font-medium mt-4">Edges</h3>
        <ul className="text-sm">
          {network.edges.map((e: any, i: number) => (
            <li key={i}>
              {e.source} → {e.target} ({e.weight})
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}