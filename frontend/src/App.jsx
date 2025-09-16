import React from "react";
import "./styles.css";
import { Accordion } from "./components/Accordion";
import { SectionAnalyze } from "./components/sections/SectionAnalyze";
import { SectionMileage } from "./components/sections/SectionMileage";
import { SectionVIN } from "./components/sections/SectionVIN";

export default function App() {
  const items = [
    { id: "analyze", title: "Analyze angle", content: <SectionAnalyze /> },
    { id: "mileage", title: "Read mileage", content: <SectionMileage /> },
    { id: "vin", title: "Read VIN", content: <SectionVIN /> },
  ];

  function scrollTo(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.scrollIntoView({ behavior: "smooth", block: "start" });
    history.replaceState(null, "", `#${id}`);
  }

  return (
    <>
      <header className="header">
        <div className="header-inner">
          <h1>Car Controller</h1>
          <div className="nav">
            <button onClick={() => scrollTo("analyze")}>Analyze</button>
            <button onClick={() => scrollTo("mileage")}>Mileage</button>
            <button onClick={() => scrollTo("vin")}>VIN</button>
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
