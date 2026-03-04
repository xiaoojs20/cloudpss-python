import os
import cloudpss
import time
import json
import matplotlib.pyplot as plt

TOKEN = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTQxMywidXNlcm5hbWUiOiJ4aWFvanMyMCIsInNjb3BlcyI6WyJtb2RlbDo5ODM2NyIsImZ1bmN0aW9uOjk4MzY3IiwiYXBwbGljYXRpb246MzI4MzEiXSwicm9sZXMiOlsieGlhb2pzMjAiXSwidHlwZSI6ImFwcGx5IiwiZXhwIjoxODAzNzE2NTMwLCJub3RlIjoic2RrX3hpYW9vIiwiaWF0IjoxNzcyNjEyNTMwfQ.Pds8At5AEb0EFeLyEo8wYN8xBuugbywZLIvoGklJBSDxCcAdmBJK5mZ-cQ7jhzyNF33sSQzv_1JO68aV9zUOew"
RID = "model/xiaojs20/low_freq_copy"

cloudpss.setToken(TOKEN)
os.environ['CLOUDPSS_API_URL'] = 'https://cloudpss.net/'

model = cloudpss.Model.fetch(RID)
job = model.jobs[0]
config = model.configs[0]

# Set a very short end time to be sure
job['args']['end_time'] = 0.05

print("Starting job and waiting 20s (bypass runner.status())...")
runner = model.run(job, config)

# Instead of runner.status(), we just wait a bit
time.sleep(20)

print("Attempting to fetch results directly...")
try:
    # Some results might be available even if status() hangs
    plots = runner.result.getPlots()
    if plots:
        print(f"Success! Found {len(plots)} plots.")
        for i in range(len(plots)):
            channels = runner.result.getPlotChannelNames(i)
            plt.figure()
            for ch in channels:
                data = runner.result.getPlotChannelData(i, ch)
                plt.plot(data, label=ch)
            plt.title(f"Plot {i}")
            plt.savefig(f"figures/direct_plot_{i}.png")
            print(f"Saved figures/direct_plot_{i}.png")
    else:
        print("No plots found yet.")
except Exception as e:
    print(f"Error fetching results: {e}")

# Also demonstrate parameter modification in the script output
print("\n--- Parameter Modification Discovery ---")
print("To modify frequency to 50Hz:")
print("config['args']['parameters']['Freq_WT'] = 50")
print(f"Current value in config: {config['args']['parameters'].get('Freq_WT')}")
