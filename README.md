# College Discovery Platform (Track B MVP)

Production-style MVP inspired by Careers360 and Collegedunia.

## Implemented Features (4)

1. **College Listing + Search**
   - Search by college name
   - Filters: location and max fees
   - Pagination with fast card-based UI
2. **College Detail Page**
   - Overview (fees, location, rating, placement)
   - Sections: courses, placements, reviews
3. **Compare Colleges (High Priority)**
   - Select 2-3 colleges from listing
   - Decision table for fees, placement %, rating, location
4. **Simple Predictor Tool**
   - Input exam + rank
   - Rule-based suggestion list from rank cutoff data in DB

## Tech Stack

- **Frontend**: Next.js 14 (App Router), TypeScript
- **Backend**: FastAPI + SQLAlchemy
- **Database**: SQLite locally, `DATABASE_URL` compatible with Postgres on Render

## Project Structure

- `frontend/`: Next.js app (`/`, `/colleges/[id]`, `/compare`, `/predictor`)
- `backend/`: FastAPI service and DB models/seed

## Local Run

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
cp .env.example .env.local
# Set NEXT_PUBLIC_API_URL to backend URL
npm install
npm run dev
```

## API Endpoints

- `GET /api/colleges` (search, filters, pagination)
- `GET /api/colleges/{id}`
- `POST /api/compare`
- `POST /api/predictor`

## Deployment

### Frontend (Vercel)

1. Import `frontend` as the root directory in Vercel.
2. Set env var:
   - `NEXT_PUBLIC_API_URL=<your-render-backend-url>`
3. Deploy.

### Backend (Render)

1. Create a new Web Service from this repo and set root directory to `backend`.
2. Build command:
   - `pip install -r requirements.txt`
3. Start command:
   - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set env var:
   - `DATABASE_URL` (Render Postgres URL or keep SQLite default for demo)
5. Deploy and use generated Render URL in frontend env vars.

