"use client";

import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function Charts() {
  const [data, setData] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log("Fetching commodity trends...");

        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/commodity-trends`
        );

        const json = await res.json();
        console.log("API Response:", json);

        const merged: any = {};

        json.trends.forEach((series: any) => {
          series.data.forEach((point: any) => {
            if (!merged[point.date]) {
              merged[point.date] = { date: point.date };
            }
            merged[point.date][series.commodity] = point.price;
          });
        });

        const finalData = Object.values(merged);
        console.log("Transformed Data:", finalData);

        setData(finalData);
      } catch (err) {
        console.error("Error fetching trends:", err);
      }
    };

    fetchData();
  }, []);

  if (!data.length) {
    return <p>Loading commodity trends...</p>;
  }

  return (
    <div className="w-full h-[400px]">
      <h2 className="font-semibold mb-2">Commodity Trends</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="oil" />
          <Line type="monotone" dataKey="gas" />
          <Line type="monotone" dataKey="wheat" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}