"use client";

import { useState } from "react";

export default function EventForm() {
  const [form, setForm] = useState({
    event_type: "sanction",
    country: "",
    sector: "energy",
    severity: 0.5,
  });

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: name === "severity" ? Number(value) : value });
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/predict-event-impact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <div className="max-w-xl">
      <form onSubmit={handleSubmit} className="space-y-4">

        <select name="event_type" onChange={handleChange} className="w-full p-2 border">
          <option value="sanction">Sanction</option>
          <option value="war">War</option>
          <option value="tariff">Tariff</option>
          <option value="port_closure">Port Closure</option>
        </select>

        <input
          name="country"
          placeholder="Country"
          onChange={handleChange}
          className="w-full p-2 border"
        />

        <select name="sector" onChange={handleChange} className="w-full p-2 border">
          <option value="energy">Energy</option>
          <option value="technology">Technology</option>
          <option value="manufacturing">Manufacturing</option>
          <option value="trade">Trade</option>
          <option value="general">General</option>
        </select>

        <input
          type="number"
          step="0.1"
          min="0"
          max="1"
          name="severity"
          onChange={handleChange}
          className="w-full p-2 border"
        />

        <button
          type="submit"
          className="bg-black text-white px-4 py-2"
        >
          {loading ? "Running..." : "Simulate Event"}
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 border">
          <h2 className="font-semibold">Results</h2>
          <pre className="text-sm mt-2">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}