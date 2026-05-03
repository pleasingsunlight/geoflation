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
    fetch("http://127.0.0.1:8000/commodity-trends")
      .then((res) => res.json())
      .then((res) => {
        // Transform data for Recharts
        const merged: any = {};

        res.trends.forEach((series: any) => {
          series.data.forEach((point: any) => {
            if (!merged[point.date]) {
              merged[point.date] = { date: point.date };
            }
            merged[point.date][series.commodity] = point.price;
          });
        });

        setData(Object.values(merged));
      });
  }, []);

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