import os
import cloudpss
import matplotlib.pyplot as plt
import json
import time

# 用户信息
TOKEN = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTQxMywidXNlcm5hbWUiOiJ4aWFvanMyMCIsInNjb3BlcyI6WyJtb2RlbDo5ODM2NyIsImZ1bmN0aW9uOjk4MzY3IiwiYXBwbGljYXRpb246MzI4MzEiXSwicm9sZXMiOlsieGlhb2pzMjAiXSwidHlwZSI6ImFwcGx5IiwiZXhwIjoxODAzNzE2NTMwLCJub3RlIjoic2RrX3hpYW9vIiwiaWF0IjoxNzcyNjEyNTMwfQ.Pds8At5AEb0EFeLyEo8wYN8xBuugbywZLIvoGklJBSDxCcAdmBJK5mZ-cQ7jhzyNF33sSQzv_1JO68aV9zUOew"
RID = "model/xiaojs20/low_freq_copy"

def run():
    # 1. 设置 Token 和 API 地址
    cloudpss.setToken(TOKEN)
    os.environ['CLOUDPSS_API_URL'] = 'https://cloudpss.net/'

    print(f"Fetching model: {RID}...")
    model = cloudpss.Model.fetch(RID)
    
    print(f"Model Name: {model.name}")
    print(f"Available Configs: {[c['name'] for c in model.configs]}")
    print(f"Available Jobs: {[j['name'] for j in model.jobs]}")

    # 探索参数修改
    # 打印第一个 config 的参数结构，方便用户查看如何修改
    if model.configs:
        config = model.configs[0]
        print("\n--- Model Configuration Parameters (First 5 keys) ---")
        # 参数通常在 config['args']['parameters'] 中
        # 我们这里尝试打印一些关键结构
        params = config.get('args', {}).get('parameters', {})
        for i, (k, v) in enumerate(params.items()):
            if i >= 10: break
            print(f"Parameter ID: {k}, Value: {v}")
        
    # 保存参数结构到文件供参考
    with open('report/model_config.json', 'w', encoding='utf-8') as f:
        json.dump(model.configs[0], f, indent=4, ensure_ascii=False)

    # 2. 运行仿真 (假设第一个 job 是电磁暂态或潮流)
    # 这里的 rid 是 low_freq_copy，看名字可能是低频相关的电磁暂态仿真
    # 我们尝试运行第一个 Job
    job = model.jobs[0]
    config = model.configs[0]
    
    # 示例如何修改参数 (如果知道具体的 key)
    # config['args']['parameters']['some_id'] = new_value
    
    print(f"\nStarting job: {job['name']}...")
    runner = model.run(job, config)
    
    while not runner.status():
        logs = runner.result.getLogs()
        for log in logs:
            print(f"[Log] {log}")
        time.sleep(1)
    
    print("Job finished.")

    # 3. 处理结果
    # 潮流计算结果处理 (如果是潮流)
    try:
        buses = runner.result.getBuses()
        if buses:
            print("\nPower Flow Results (Buses):")
            print(json.dumps(buses, indent=2)[:500] + "...")
            with open('report/buses.json', 'w') as f:
                json.dump(buses, f, indent=2)
    except:
        pass

    # 电磁暂态结果处理 (绘制曲线)
    plots = runner.result.getPlots()
    if plots:
        print(f"\nFound {len(plots)} plot groups. Generating figures...")
        for i in range(len(plots)):
            group_name = plots[i].get('title', f'Plot_{i}')
            channels = runner.result.getPlotChannelNames(i)
            
            plt.figure(figsize=(10, 6))
            for channel_name in channels:
                data = runner.result.getPlotChannelData(i, channel_name)
                # data 通常是 [x_values, y_values] 或者仅仅是 y_values
                # 根据 SDK 文档，返回的是通道的数据
                plt.plot(data, label=channel_name)
            
            plt.title(f"Result: {group_name}")
            plt.xlabel("Step")
            plt.ylabel("Value")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            
            fig_path = f"figures/plot_{i}.png"
            plt.savefig(fig_path)
            print(f"Saved: {fig_path}")
            plt.close()

if __name__ == "__main__":
    run()
