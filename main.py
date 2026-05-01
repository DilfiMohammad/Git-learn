from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
import os

app = FastAPI()

# ✅ Serve HTML directly (no Jinja issues)
@app.get("/")
def home():
    return FileResponse(os.path.join("templates", "index.html"))

# ✅ API route
@app.get("/jobs")
def get_jobs(query: str, location: str = ""):
    url = f"https://remotive.com/api/remote-jobs?search={query}"
    
    response = requests.get(url)
    data = response.json()

    jobs = []

    for job in data["jobs"]:
        job_location = job["candidate_required_location"]

        # ✅ Filter by location if provided
        if location.lower() in job_location.lower():
            jobs.append({
                "title": job["title"],
                "company": job["company_name"],
                "location": job_location,
                "url": job["url"]
            })

    return {"results": jobs[:10]}