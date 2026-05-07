"use client";

import { useEffect, useState } from "react";
import { compareColleges } from "./api";

type CompareItem = {
  id: number;
  name: string;
  fees: number;
  placement_percent: number;
  rating: number;
  location: string;
};

export default function CompareClient() {
  const [items, setItems] = useState<CompareItem[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const raw = localStorage.getItem("compare_college_ids");
    const ids = raw ? (JSON.parse(raw) as number[]) : [];
    if (ids.length < 2) {
      setError("Select at least 2 colleges from listing page.");
      return;
    }
    compareColleges(ids)
      .then((res) => setItems(res.items))
      .catch(() => setError("Could not load comparison."));
  }, []);

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h1>Compare Colleges</h1>
      {error ? <div className="card">{error}</div> : null}
      {items.length > 0 ? (
        <div className="card">
          <table className="table">
            <thead>
              <tr>
                <th>College</th>
                <th>Fees</th>
                <th>Placement %</th>
                <th>Rating</th>
                <th>Location</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td>{item.name}</td>
                  <td>INR {item.fees.toLocaleString()}</td>
                  <td>{item.placement_percent}%</td>
                  <td>{item.rating.toFixed(1)}</td>
                  <td>{item.location}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </div>
  );
}
