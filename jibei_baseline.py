import os
import cloudpss
import matplotlib.pyplot as plt
import json
import time

TOKEN = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTQxMywidXNlcm5hbWUiOiJ4aWFvanMyMCIsInNjb3BlcyI6WyJtb2RlbDo5ODM2NyIsImZ1bmN0aW9uOjk4MzY3IiwiYXBwbGljYXRpb246MzI4MzEiXSwicm9sZXMiOlsieGlhb2pzMjAiXSwidHlwZSI6ImFwcGx5IiwiZXhwIjoxODAzNzE2NTMwLCJub3RlIjoic2RrX3hpYW9vIiwiaWF0IjoxNzcyNjEyNTMwfQ.Pds8At5AEb0EFeLyEo8wYN8xBuugbywZLIvoGklJBSDxCcAdmBJK5mZ-cQ7jhzyNF33sSQzv_1JO68aV9zUOew"
RID = "model/xiaojs20/low_freq_copy"

def run_baseline():
    cloudpss.setToken(TOKEN)
    os.environ['CLOUDPSS_API_URL'] = 'https://cloudpss.net/'

    model = cloudpss.Model.fetch(RID)
    
    # 找到冀北方案
    config = next(c for c in model.configs if c['name'] == '方案-冀北')
    job = model.jobs[0] # 电磁暂态仿真方案 1

    # 设置较短时间以确保快速完成
    job['args']['end_time'] = 0.5
    
    print(f"Starting baseline simulation with {config['name']}...")
    runner = model.run(job, config)
    
    while not runner.status():
        time.sleep(2)
    
    print("Baseline simulation finished.")
    plots = runner.result.getPlots()
    if plots:
        for i in range(len(plots)):
            group_name = plots[i].get('title', f'Plot_{i}')
            channels = runner.result.getPlotChannelNames(i)
            plt.figure(figsize=(10, 6))
            for channel_name in channels:
                data = runner.result.getPlotChannelData(i, channel_name)
                plt.plot(data, label=channel_name)
            plt.title(f"Baseline: {group_name}")
            plt.xlabel("Step")
            plt.ylabel("Value")
            plt.legend()
            plt.grid(True)
            plt.savefig(f"figures/jibei_baseline_{i}.png")
            plt.close()
            print(f"Saved: figures/jibei_baseline_{i}.png")

if __name__ == "__main__":
    run_baseline()
