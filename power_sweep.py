import os
import cloudpss
import matplotlib.pyplot as plt
import json
import time

TOKEN = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTQxMywidXNlcm5hbWUiOiJ4aWFvanMyMCIsInNjb3BlcyI6WyJtb2RlbDo5ODM2NyIsImZ1bmN0aW9uOjk4MzY3IiwiYXBwbGljYXRpb246MzI4MzEiXSwicm9sZXMiOlsieGlhb2pzMjAiXSwidHlwZSI6ImFwcGx5IiwiZXhwIjoxODAzNzE2NTMwLCJub3RlIjoic2RrX3hpYW9vIiwiaWF0IjoxNzcyNjEyNTMwfQ.Pds8At5AEb0EFeLyEo8wYN8xBuugbywZLIvoGklJBSDxCcAdmBJK5mZ-cQ7jhzyNF33sSQzv_1JO68aV9zUOew"
RID = "model/xiaojs20/low_freq_copy"

def run_sweep():
    cloudpss.setToken(TOKEN)
    os.environ['CLOUDPSS_API_URL'] = 'https://cloudpss.net/'

    model = cloudpss.Model.fetch(RID)
    config_orig = next(c for c in model.configs if c['name'] == '方案-冀北')
    job_orig = model.jobs[0]
    
    # 容量
    CAP_P_WT2WF = 100.0
    CAP_P_WF_Other = 900.0
    
    results = []
    
    for i in range(11):
        ratio = i * 0.1
        p_wt2wf = CAP_P_WT2WF * ratio
        p_wf_other = CAP_P_WF_Other * ratio
        
        print(f"--- Run {i}: Ratio {ratio:.1f}, P_WT2WF={p_wt2wf}, P_WF_Other={p_wf_other} ---")
        
        # 深度拷贝或每次重新获取
        config = json.loads(json.dumps(config_orig))
        job = json.loads(json.dumps(job_orig))
        
        config['args']['P_WT2WF'] = p_wt2wf
        config['args']['P_WF_Other'] = p_wf_other
        job['args']['end_time'] = 0.2 # 扫描用极短时间
        
        runner = model.run(job, config)
        
        # Poll for status with timeout
        start_wait = time.time()
        success = False
        while (time.time() - start_wait) < 45: # Max 45s per run
            try:
                # runner.status() seems to hang if things are slow, 
                # but it's the only way to wait for completion.
                if runner.status():
                    success = True
                    break
            except Exception as e:
                print(f"Polling error: {e}")
            time.sleep(5)
        
        if success:
            print(f"Run {i} finished.")
            try:
                # 记录数据用于汇总图
                plots = runner.result.getPlots()
                if plots:
                    channel_names = runner.result.getPlotChannelNames(0)
                    if channel_names:
                        data = runner.result.getPlotChannelData(0, channel_names[0])
                        results.append((ratio, data[-1]))
                    
                    # 保存该比例下的图像
                    for p_idx in range(len(plots)):
                        plt.figure()
                        chs = runner.result.getPlotChannelNames(p_idx)
                        for ch in chs:
                            d = runner.result.getPlotChannelData(p_idx, ch)
                            plt.plot(d, label=ch)
                        plt.title(f"Sweep Ratio {ratio:.1f}")
                        plt.savefig(f"figures/sweep_{i}_plot_{p_idx}.png")
                        plt.close()
            except Exception as e:
                print(f"Result fetching error in Run {i}: {e}")
        else:
            print(f"Run {i} timed out or failed to reach completion.")

    # 绘制总结图
    if results:
        ratios, values = zip(*results)
        plt.figure(figsize=(10, 6))
        plt.plot(ratios, values, 'o-', markerfacecolor='red')
        plt.title("Wind Power Sweep Sensitivity")
        plt.xlabel("Power Ratio (0.0 - 1.0)")
        plt.ylabel("Key Metric Value")
        plt.grid(True)
        plt.savefig("figures/sweep_sensitivity.png")
        plt.close()
        print("Saved sensitivity summary: figures/sweep_sensitivity.png")

if __name__ == "__main__":
    run_sweep()
