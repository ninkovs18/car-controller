import "./styles.css";
import { Accordion } from "./components/Accordion";
import { SectionAnalyze } from "./components/sections/SectionAnalyze";
import { SectionMileage } from "./components/sections/SectionMileage";
import { SectionVIN } from "./components/sections/SectionVIN";
import { AuthButton } from "./components/AuthButton";

export default function App() {
  const items = [
    { id: "analyze", title: "Analyze angle", content: <SectionAnalyze /> },
    { id: "mileage", title: "Read mileage", content: <SectionMileage /> },
    { id: "vin", title: "Read VIN", content: <SectionVIN /> },
  ];

  return (
    <>
      <header className="header">
        <div className="header-inner">
          <h1>Vehicle Controller</h1>
          <div className="nav">
            <AuthButton />
          </div>
        </div>
      </header>

      <main className="container">
        <div className="stack">
          <Accordion items={items} initialOpenId="analyze" />
        </div>
      </main>
    </>
  );
}
