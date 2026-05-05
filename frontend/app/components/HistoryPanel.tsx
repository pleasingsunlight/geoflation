"use client";

import { useEffect, useState } from "react";

export default function HistoryPanel() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/prediction-history`)
      .then((res) => res.json())
      .then(setData);
  }, []);

  if (!data.length) return <p>No history yet</p>;

  return (
    <div className="mt-6">
      <h2 className="font-semibold mb-2">Prediction History</h2>

      <div className="space-y-2">
        {data.map((item, i) => (
          <div key={i} className="border p-3 rounded text-sm">
            <p><strong>{item.event_type}</strong> in {item.country}</p>
            <p>Sector: {item.sector}</p>
            <p>Oil: {item.oil}, Gas: {item.gas}</p>
            <p>Delay: {item.delay} weeks</p>
            <p>Risk: {item.risk}</p>
          </div>
        ))}
      </div>
    </div>
  );
}