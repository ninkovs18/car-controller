import { useState, useEffect } from "react";
import "./styles.css";
import { Accordion } from "./components/Accordion";
import { SectionAnalyze } from "./components/sections/SectionAnalyze";
import { SectionMileage } from "./components/sections/SectionMileage";
import { SectionVIN } from "./components/sections/SectionVIN";
import { AuthButton } from "./components/AuthButton";

export default function App() {
  const [openId, setOpenId] = useState(null);

  const items = [
    { id: "analyze", title: "Analyze angle", content: <SectionAnalyze /> },
    { id: "mileage", title: "Read mileage", content: <SectionMileage /> },
    { id: "vin", title: "Read VIN", content: <SectionVIN /> },
  ];

  useEffect(() => {
    const hash = window.location.hash.replace("#", "");
    if (hash && items.some((item) => item.id === hash)) {
      setOpenId(hash);
    } else if (items[0]) {
      setOpenId(items[0].id);
    }
  }, []);

  function toggleAndScroll(id) {
    setOpenId(id); // <--- Menja stanje
    const el = document.getElementById(id);
    if (!el) return;
    el.scrollIntoView({ behavior: "smooth", block: "start" });
    history.replaceState(null, "", `#${id}`);
  }
  return (
    <>
      <header className="header">
        <div className="header-inner">
          <h1>Vehicle Controller</h1>
          <div className="nav">
            <button onClick={() => toggleAndScroll("analyze")}>Analyze</button>
            <button onClick={() => toggleAndScroll("mileage")}>Mileage</button>
            <button onClick={() => toggleAndScroll("vin")}>VIN</button>
            <AuthButton />
          </div>
        </div>
      </header>

      <main className="container">
        <div className="stack">
          <Accordion items={items} openId={openId} setOpenId={setOpenId} />
        </div>
      </main>
    </>
  );
}
