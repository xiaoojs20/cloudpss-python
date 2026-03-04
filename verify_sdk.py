import os
import cloudpss
import time

TOKEN = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTQxMywidXNlcm5hbWUiOiJ4aWFvanMyMCIsInNjb3BlcyI6WyJtb2RlbDo5ODM2NyIsImZ1bmN0aW9uOjk4MzY3IiwiYXBwbGljYXRpb246MzI4MzEiXSwicm9sZXMiOlsieGlhb2pzMjAiXSwidHlwZSI6ImFwcGx5IiwiZXhwIjoxODAzNzE2NTMwLCJub3RlIjoic2RrX3hpYW9vIiwiaWF0IjoxNzcyNjEyNTMwfQ.Pds8At5AEb0EFeLyEo8wYN8xBuugbywZLIvoGklJBSDxCcAdmBJK5mZ-cQ7jhzyNF33sSQzv_1JO68aV9zUOew"
RID = "model/CloudPSS/IEEE3"

cloudpss.setToken(TOKEN)
os.environ['CLOUDPSS_API_URL'] = 'https://cloudpss.net/'

print(f"Fetching public model: {RID}...")
model = cloudpss.Model.fetch(RID)
print(f"Model: {model.name}")

# Try the first job (usually Power Flow in this case)
job = model.jobs[0]
config = model.configs[0]

print(f"Starting job {job['name']}...")
runner = model.run(job, config)

start_time = time.time()
while not runner.status() and (time.time() - start_time) < 60:
    logs = runner.result.getLogs()
    for log in logs:
        print(f"[Sample Log] {log}")
    time.sleep(2)

if runner.status():
    print("Sample run SUCCESS.")
    try:
        buses = runner.result.getBuses()
        print(f"Buses count: {len(buses)}")
    except:
        print("No bus results (standard for EMT or failed PF).")
else:
    print("Sample run hanging or failed.")
