import { useState } from "react";
export function Accordion({ items, initialOpenId }) {
  const [openId, setOpenId] = useState(initialOpenId ?? items[0]?.id ?? null);
  const toggle = (id) => setOpenId((prev) => (prev === id ? null : id));

  return (
    <div className="accordion">
      {items.map((it) => {
        const open = openId === it.id;
        return (
          <div className="ac-item" key={it.id} id={it.id}>
            <button
              className="ac-head"
              aria-expanded={open}
              onClick={() => toggle(it.id)}
            >
              <span>{it.title}</span>
              <span className={open ? "badge-open" : "badge-close"}>
                {open ? "open" : "closed"}
              </span>
            </button>
            {open && <div className="ac-body">{it.content}</div>}
          </div>
        );
      })}
    </div>
  );
}
