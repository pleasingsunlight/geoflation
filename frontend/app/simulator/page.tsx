import EventForm from "../components/EventForm";

export default function Simulator() {
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">
        Event Simulator
      </h1>

      <EventForm />
    </div>
  );
}