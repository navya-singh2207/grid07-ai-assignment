"use client";

import { FormEvent, useState } from "react";
import { runPredictor } from "./api";

type PredictorItem = {
  college_id: number;
  college_name: string;
  location: string;
  estimated_cutoff: number;
};

export default function PredictorClient() {
  const [exam, setExam] = useState("JEE");
  const [rank, setRank] = useState("");
  const [items, setItems] = useState<PredictorItem[]>([]);
  const [error, setError] = useState("");

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const res = await runPredictor(exam, Number(rank));
      setItems(res.suggestions || []);
    } catch {
      setError("Could not run predictor.");
      setItems([]);
    }
  };

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h1>College Predictor</h1>
      <form className="card" onSubmit={submit} style={{ display: "grid", gap: 10, maxWidth: 500 }}>
        <label>
          Exam
          <select className="select" value={exam} onChange={(e) => setExam(e.target.value)}>
            <option value="JEE">JEE</option>
          </select>
        </label>
        <label>
          Rank
          <input
            className="input"
            type="number"
            value={rank}
            onChange={(e) => setRank(e.target.value)}
            min={1}
            required
          />
        </label>
        <button className="btn" type="submit">
          Predict Colleges
        </button>
      </form>

      {error ? <div className="card">{error}</div> : null}

      {items.length > 0 ? (
        <div className="card">
          <h3>Suggested Colleges</h3>
          <ul>
            {items.map((item) => (
              <li key={item.college_id}>
                {item.college_name} ({item.location}) - estimated cutoff rank {item.estimated_cutoff}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
