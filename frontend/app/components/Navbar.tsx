"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="w-full bg-black text-white p-4 flex justify-between">
      <h1 className="font-bold text-lg">Geoflation</h1>
      <div className="space-x-4">
        <Link href="/">Home</Link>
        <Link href="/dashboard">Dashboard</Link>
        <Link href="/simulator">Simulator</Link>
      </div>
    </nav>
  );
}