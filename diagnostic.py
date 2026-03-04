import os
import cloudpss
import time

TOKEN = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTQxMywidXNlcm5hbWUiOiJ4aWFvanMyMCIsInNjb3BlcyI6WyJtb2RlbDo5ODM2NyIsImZ1bmN0aW9uOjk4MzY3IiwiYXBwbGljYXRpb246MzI4MzEiXSwicm9sZXMiOlsieGlhb2pzMjAiXSwidHlwZSI6ImFwcGx5IiwiZXhwIjoxODAzNzE2NTMwLCJub3RlIjoic2RrX3hpYW9vIiwiaWF0IjoxNzcyNjEyNTMwfQ.Pds8At5AEb0EFeLyEo8wYN8xBuugbywZLIvoGklJBSDxCcAdmBJK5mZ-cQ7jhzyNF33sSQzv_1JO68aV9zUOew"
RID = "model/xiaojs20/low_freq_copy"

cloudpss.setToken(TOKEN)
os.environ['CLOUDPSS_API_URL'] = 'https://cloudpss.net/'

model = cloudpss.Model.fetch(RID)
print(f"Model: {model.name}")
# Some SDKs allow fetching recent runners or jobs. 
# Let's try to just list the jobs and see if we can see current status if possible, 
# although SDK usually doesn't have a direct 'list active jobs' unless through user account.

# If the previous job is truly stuck, it might be due to server load.
# Let's try a very short run (if we can modify end time)
job = model.jobs[0]
config = model.configs[0]

print("Trying a shorter run (0.1s) to test connectivity and responsiveness...")
job['args']['end_time'] = 0.1 

runner = model.run(job, config)
max_wait = 30
start_time = time.time()
while not runner.status() and (time.time() - start_time) < max_wait:
    logs = runner.result.getLogs()
    for log in logs:
        print(f"[Diag Log] {log}")
    time.sleep(2)

if runner.status():
    print("Diagnostic run SUCCESSful.")
    plots = runner.result.getPlots()
    print(f"Plots found: {len(plots)}")
else:
    print("Diagnostic run timed out or failed. Check connection.")
