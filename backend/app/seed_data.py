from .models import College, RankCutoff


COLLEGES = [
    {
        "name": "Indian Institute of Technology Delhi",
        "location": "Delhi",
        "fees": 240000,
        "rating": 4.8,
        "placement_percent": 93.0,
        "courses_csv": "Computer Science,Mechanical Engineering,Electrical Engineering",
        "overview": "Premier institute with strong academics and research ecosystem.",
        "placements_info": "Top recruiters include global tech and consulting firms.",
        "reviews_info": "Students praise faculty depth and peer quality.",
    },
    {
        "name": "Indian Institute of Technology Bombay",
        "location": "Mumbai",
        "fees": 238000,
        "rating": 4.9,
        "placement_percent": 95.0,
        "courses_csv": "Computer Science,Chemical Engineering,Civil Engineering",
        "overview": "Known for strong innovation culture and startup ecosystem.",
        "placements_info": "Excellent median packages across circuit branches.",
        "reviews_info": "Campus life and alumni network receive strong reviews.",
    },
    {
        "name": "National Institute of Technology Trichy",
        "location": "Tiruchirappalli",
        "fees": 165000,
        "rating": 4.5,
        "placement_percent": 88.0,
        "courses_csv": "Computer Science,Electronics,Production Engineering",
        "overview": "Top NIT with balanced academics and student activities.",
        "placements_info": "High placement in CS and ECE with stable growth.",
        "reviews_info": "Students value infrastructure and technical clubs.",
    },
    {
        "name": "Vellore Institute of Technology",
        "location": "Vellore",
        "fees": 195000,
        "rating": 4.3,
        "placement_percent": 82.0,
        "courses_csv": "Computer Science,Information Technology,Biotechnology",
        "overview": "Large private university with broad course options.",
        "placements_info": "Mass and product recruiters both visit campus.",
        "reviews_info": "Reviews mention modern labs and diverse student body.",
    },
    {
        "name": "Delhi Technological University",
        "location": "Delhi",
        "fees": 190000,
        "rating": 4.4,
        "placement_percent": 84.0,
        "courses_csv": "Computer Engineering,Software Engineering,Mathematics and Computing",
        "overview": "Strong state university with improving industry connect.",
        "placements_info": "Competitive packages in software-related branches.",
        "reviews_info": "Good city access and active coding culture.",
    },
    {
        "name": "PES University",
        "location": "Bengaluru",
        "fees": 360000,
        "rating": 4.1,
        "placement_percent": 80.0,
        "courses_csv": "Computer Science,Electronics,Data Science",
        "overview": "Private university focused on employability and projects.",
        "placements_info": "Strong Bengaluru recruiter footprint.",
        "reviews_info": "Students highlight practical curriculum and pace.",
    },
]


def seed(db):
    if db.query(College).count() > 0:
        return

    created = []
    for college_payload in COLLEGES:
        college = College(**college_payload)
        db.add(college)
        created.append(college)

    db.commit()
    for college in created:
        db.refresh(college)

    cutoff_rows = [
        ("JEE", created[0].id, 2500),
        ("JEE", created[1].id, 1800),
        ("JEE", created[2].id, 12000),
        ("JEE", created[4].id, 18000),
        ("JEE", created[3].id, 35000),
        ("JEE", created[5].id, 42000),
    ]
    for exam, college_id, max_rank in cutoff_rows:
        db.add(RankCutoff(exam=exam, college_id=college_id, max_rank=max_rank))
    db.commit()
