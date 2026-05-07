const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type CollegeCard = {
  id: number;
  name: string;
  location: string;
  fees: number;
  rating: number;
};

export type PaginatedCollegeResponse = {
  items: CollegeCard[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
};

export async function fetchColleges(params: Record<string, string | number | undefined>) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== "") {
      query.set(key, String(value));
    }
  });
  const res = await fetch(`${API_BASE}/api/colleges?${query.toString()}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error("Failed to fetch colleges");
  }
  return (await res.json()) as PaginatedCollegeResponse;
}

export async function fetchCollegeDetail(id: string | number) {
  const res = await fetch(`${API_BASE}/api/colleges/${id}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error("Failed to fetch college detail");
  }
  return res.json();
}

export async function compareColleges(ids: number[]) {
  const res = await fetch(`${API_BASE}/api/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ college_ids: ids }),
  });
  if (!res.ok) {
    throw new Error("Failed to compare colleges");
  }
  return res.json();
}

export async function runPredictor(exam: string, rank: number) {
  const res = await fetch(`${API_BASE}/api/predictor`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ exam, rank }),
  });
  if (!res.ok) {
    throw new Error("Failed to run predictor");
  }
  return res.json();
}
