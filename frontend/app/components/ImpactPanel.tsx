type Props = {
  data: any;
};

export default function ImpactPanel({ data }: Props) {
  if (!data) return null;

  return (
    <div className="mt-6 space-y-4">

      {/* Risk */}
      <p className={`text-lg font-bold ${
        data.risk_severity === "High"
        ? "text-red-500"
        : data.risk_severity === "Medium"
        ? "text-yellow-500"
        : "text-green-500"
      }`}>
        {data.risk_severity}
      </p>

      {/* Shipping Delay */}
      <div className="p-4 border rounded">
        <h2 className="font-semibold">Shipping Delay</h2>
        <p>{data.shipping_delay_weeks} weeks</p>
      </div>

      {/* Price Impacts */}
      <div className="p-4 border rounded">
        <h2 className="font-semibold">Price Impacts</h2>
        <ul className="mt-2 space-y-1">
          {Object.entries(data.price_impacts).map(([key, value]) => (
            <li key={key}>
              {key}: {value as string}
            </li>
          ))}
        </ul>
      </div>
      
      {/* Impacted Countries */}
      <div className="p-4 border rounded">
        <h2 className="font-semibold">Impacted Countries</h2>

        <ul className="mt-2">
          {Object.entries(
            data.impacted_countries || {}
          ).map(([country, impact]) => (
            <li key={country}>
              {country}: {String(impact)}
            </li>
          ))}
        </ul>
      </div>

      {/* Industries */}
      <div className="p-4 border rounded">
        <h2 className="font-semibold">Affected Industries</h2>
        <ul className="mt-2">
          {data.affected_industries.map((ind: string) => (
            <li key={ind}>{ind}</li>
          ))}
        </ul>
      </div>

      <div className="p-4 border rounded">
        <h2 className="font-semibold">Analysis</h2>
        <p className="mt-2 text-sm">{data.explanation}</p>
      </div>

    </div>
  );
}