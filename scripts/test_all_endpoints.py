\
import requests, time, random, string, sys, json
BASE = "http://127.0.0.1:8000"

def pr(title, data):
    print(f"\n=== {title} ===")
    print(json.dumps(data, indent=2, default=str))

def reg_login(email, password, role="student"):
    r = requests.post(f"{BASE}/auth/register", json={
        "name": "User "+email.split("@")[0],
        "email": email,
        "password": password,
        "role": role,
        "branch": "CSE",
        "year": 3,
        "achievements": "None",
        "linkedin": "",
        "github": ""
    })
    pr("register", r.json())
    # Pull code from server logs in real life; for demo, skip verification

    # Login
    r = requests.post(f"{BASE}/auth/login", json={"email": email, "password": password})
    pr("login", r.json())
    return r.json()["access_token"]

def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def smoke():
    # users
    suffix = ''.join(random.choices(string.ascii_lowercase+string.digits, k=4))
    campus_domain = "@college.edu"
    admin_email = f"admin{suffix}{campus_domain}"
    fac_email = f"faculty{suffix}{campus_domain}"
    stu_email = f"student{suffix}{campus_domain}"
    alu_email = f"alumni{suffix}{campus_domain}"
    admin = reg_login(admin_email, "Passw0rd!", "admin")
    faculty = reg_login(fac_email, "Passw0rd!", "faculty")
    student = reg_login(stu_email, "Passw0rd!", "student")
    alumni = reg_login(alu_email, "Passw0rd!", "alumni")

    # notices
    r = requests.post(f"{BASE}/notices/", json={"title": "Exam", "content":"Exam on Friday", "audience":"all"}, headers=auth_header(faculty)); pr("notice create", r.json())
    r = requests.get(f"{BASE}/notices/"); pr("notices list", r.json())

    # clubs
    r = requests.post(f"{BASE}/clubs/", json={"name": f"Coding-{suffix}", "description":"We code"}, headers=auth_header(student)); club = r.json(); pr("club create", club)
    cid = club["id"]
    r = requests.post(f"{BASE}/clubs/{cid}/join", headers=auth_header(student)); pr("club join request", r.json())
    # owner approves (student is owner because created; simulate approve self-req)
    r = requests.get(f"{BASE}/clubs/"); pr("clubs list", r.json())

    # forum
    r = requests.post(f"{BASE}/forum/questions", json={"title":"How to sort?", "body":"Help with sorting", "tags":["algo","python"]}, headers=auth_header(student)); q = r.json(); pr("question", q)
    qid = q["id"]
    r = requests.post(f"{BASE}/forum/questions/{qid}/answers", json={"body":"Use Timsort"}, headers=auth_header(faculty)); ans = r.json(); pr("answer", ans)
    r = requests.post(f"{BASE}/forum/questions/{qid}/upvote", headers=auth_header(alumni)); pr("q upvote", r.json())
    r = requests.post(f"{BASE}/forum/answers/{ans['id']}/upvote", headers=auth_header(student)); pr("a upvote", r.json())

    # projects
    r = requests.post(f"{BASE}/projects/", json={"title":"App", "description":"Cool app", "github":"", "demo_url":""}, headers=auth_header(student)); proj = r.json(); pr("project", proj)
    r = requests.post(f"{BASE}/projects/{proj['id']}/collaborators", json={"message":"join pls"}, headers=auth_header(alumni)); pr("collab req", r.json())

    # events
    import datetime as dt
    now = dt.datetime.utcnow()
    r = requests.post(f"{BASE}/events/", json={"title":"Hack Day","description":"24h","category":"technical","starts_at":now.isoformat(),"ends_at":(now+dt.timedelta(hours=4)).isoformat(),"location":"Auditorium"}, headers=auth_header(admin)); ev = r.json(); pr("event", ev)
    r = requests.post(f"{BASE}/events/{ev['id']}/rsvp", json={"status":"going"}, headers=auth_header(student)); pr("rsvp", r.json())

    # placements
    r = requests.post(f"{BASE}/placements/", json={"company":"ACME","role":"SDE","description":"Internship","deadline":(now+dt.timedelta(days=10)).isoformat()}, headers=auth_header(faculty)); pr("placement", r.json())
    r = requests.post(f"{BASE}/placements/experiences", json={"company":"Globex","content":"Great process"}, headers=auth_header(alumni)); pr("alumni exp", r.json())

    # marketplace
    r = requests.post(f"{BASE}/marketplace/listings", json={"title":"Calc","description":"Fx-991ES","price":499.0,"category":"calculator"}, headers=auth_header(student)); lst = r.json(); pr("listing", lst)
    r = requests.post(f"{BASE}/marketplace/listings/{lst['id']}/message", json={"receiver_id": lst["owner_id"], "content":"Is it available?"}, headers=auth_header(alumni)); pr("message", r.json())

    # alumni mentorship
    r = requests.post(f"{BASE}/alumni/mentorships", json={"mentee_id": lst["owner_id"], "topic":"Career"}, headers=auth_header(alumni)); ms = r.json(); pr("mentorship", ms)

    # lost & found
    r = requests.post(f"{BASE}/lostfound/", json={"type":"lost","title":"ID Card","description":"Blue lanyard","contact":"99999"}, headers=auth_header(student)); pr("lost", r.json())

    # utilities
    r = requests.post(f"{BASE}/utilities/gpa", json={"courses":[{"credits":4,"grade":"A"},{"credits":3,"grade":"B+"}]}); pr("gpa", r.json())
    r = requests.post(f"{BASE}/utilities/timetable", json={"subjects":["DBMS","OS","DS","CN","SE","ENG"]}); pr("timetable", r.json())

    # hackathons
    r = requests.post(f"{BASE}/hackathons/", json={"name":f"H-{suffix}","description":"fun","starts_at":now.isoformat(),"ends_at":(now+dt.timedelta(days=1)).isoformat()}, headers=auth_header(admin)); h = r.json(); pr("hackathon", h)
    r = requests.post(f"{BASE}/hackathons/{h['id']}/teams", json={"name":"Alpha"}, headers=auth_header(student)); team = r.json(); pr("team", team)
    r = requests.post(f"{BASE}/hackathons/{h['id']}/leaderboard", json={"team_id":team["id"], "score": 95.5}, headers=auth_header(admin)); pr("leaderboard add", r.json())
    r = requests.get(f"{BASE}/hackathons/{h['id']}/leaderboard"); pr("leaderboard", r.json())

    # moderation
    r = requests.post(f"{BASE}/moderation/reports", json={"target_type":"question","target_id":qid,"reason":"spam"}, headers=auth_header(student)); rep = r.json(); pr("report", rep)
    r = requests.get(f"{BASE}/moderation/reports", headers=auth_header(admin)); pr("reports list", r.json())

if __name__ == "__main__":
    try:
        smoke()
        print("\\nAll smoke calls executed.")
    except Exception as e:
        print("Failure:", e)
        sys.exit(1)
