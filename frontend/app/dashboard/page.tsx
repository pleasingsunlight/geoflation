import Charts from "../components/Charts";
import TradeGraph from "../components/TradeGraph";

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-semibold">Dashboard</h1>

      <Charts />
      <TradeGraph />
    </div>
  );
}