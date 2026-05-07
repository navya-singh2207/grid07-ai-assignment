"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { CollegeCard, fetchColleges } from "./api";

const PAGE_SIZE = 6;

function getSavedCompareIds() {
  if (typeof window === "undefined") return [];
  const raw = localStorage.getItem("compare_college_ids");
  return raw ? (JSON.parse(raw) as number[]) : [];
}

export default function CollegeListClient() {
  const [items, setItems] = useState<CollegeCard[]>([]);
  const [totalPages, setTotalPages] = useState(1);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [location, setLocation] = useState("");
  const [maxFees, setMaxFees] = useState("");
  const [selectedIds, setSelectedIds] = useState<number[]>([]);

  const locationOptions = useMemo(
    () => ["Delhi", "Mumbai", "Bengaluru", "Vellore", "Tiruchirappalli"],
    []
  );

  useEffect(() => {
    setSelectedIds(getSavedCompareIds());
  }, []);

  useEffect(() => {
    fetchColleges({
      page,
      page_size: PAGE_SIZE,
      search,
      location,
      max_fees: maxFees || undefined,
    })
      .then((res) => {
        setItems(res.items);
        setTotalPages(res.total_pages);
      })
      .catch(() => {
        setItems([]);
      });
  }, [page, search, location, maxFees]);

  const toggleCompare = (id: number) => {
    let next = [...selectedIds];
    if (next.includes(id)) {
      next = next.filter((x) => x !== id);
    } else if (next.length < 3) {
      next.push(id);
    }
    setSelectedIds(next);
    localStorage.setItem("compare_college_ids", JSON.stringify(next));
  };

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h1>College Discovery Platform</h1>

      <div className="card" style={{ display: "grid", gridTemplateColumns: "2fr 1fr 1fr", gap: 10 }}>
        <input
          className="input"
          placeholder="Search by college name"
          value={search}
          onChange={(e) => {
            setPage(1);
            setSearch(e.target.value);
          }}
        />
        <select
          className="select"
          value={location}
          onChange={(e) => {
            setPage(1);
            setLocation(e.target.value);
          }}
        >
          <option value="">All locations</option>
          {locationOptions.map((loc) => (
            <option value={loc} key={loc}>
              {loc}
            </option>
          ))}
        </select>
        <input
          className="input"
          type="number"
          placeholder="Max fees"
          value={maxFees}
          onChange={(e) => {
            setPage(1);
            setMaxFees(e.target.value);
          }}
        />
      </div>

      <div className="grid">
        {items.map((college) => (
          <div className="card" key={college.id}>
            <h3 style={{ marginTop: 0 }}>{college.name}</h3>
            <p>Location: {college.location}</p>
            <p>Fees: INR {college.fees.toLocaleString()}</p>
            <p>Rating: {college.rating.toFixed(1)}</p>
            <div style={{ display: "flex", gap: 8 }}>
              <Link href={`/colleges/${college.id}`} className="btn">
                View details
              </Link>
              <button className="btn" onClick={() => toggleCompare(college.id)}>
                {selectedIds.includes(college.id) ? "Selected" : "Compare"}
              </button>
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <button className="btn" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
          Previous
        </button>
        <span>
          Page {page} of {totalPages}
        </span>
        <button className="btn" disabled={page >= totalPages} onClick={() => setPage((p) => p + 1)}>
          Next
        </button>
        <Link href="/compare" className="btn">
          Compare selected ({selectedIds.length})
        </Link>
      </div>
    </div>
  );
}
