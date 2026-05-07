import { fetchCollegeDetail } from "../../../components/api";

export default async function CollegeDetailPage({ params }: { params: { id: string } }) {
  const college = await fetchCollegeDetail(params.id);

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h1>{college.name}</h1>
      <div className="card">
        <p>
          <strong>Location:</strong> {college.location}
        </p>
        <p>
          <strong>Fees:</strong> INR {college.fees.toLocaleString()}
        </p>
        <p>
          <strong>Rating:</strong> {college.rating.toFixed(1)}
        </p>
        <p>
          <strong>Placement:</strong> {college.placement_percent}%
        </p>
      </div>

      <div className="card">
        <h2>Courses</h2>
        <ul>
          {college.courses.map((course: string) => (
            <li key={course}>{course}</li>
          ))}
        </ul>
      </div>

      <div className="card">
        <h2>Placements</h2>
        <p>{college.placements_info}</p>
      </div>

      <div className="card">
        <h2>Reviews</h2>
        <p>{college.reviews_info}</p>
      </div>
    </div>
  );
}
