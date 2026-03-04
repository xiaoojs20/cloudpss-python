import os
import cloudpss
import json

TOKEN = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTQxMywidXNlcm5hbWUiOiJ4aWFvanMyMCIsInNjb3BlcyI6WyJtb2RlbDo5ODM2NyIsImZ1bmN0aW9uOjk4MzY3IiwiYXBwbGljYXRpb246MzI4MzEiXSwicm9sZXMiOlsieGlhb2pzMjAiXSwidHlwZSI6ImFwcGx5IiwiZXhwIjoxODAzNzE2NTMwLCJub3RlIjoic2RrX3hpYW9vIiwiaWF0IjoxNzcyNjEyNTMwfQ.Pds8At5AEb0EFeLyEo8wYN8xBuugbywZLIvoGklJBSDxCcAdmBJK5mZ-cQ7jhzyNF33sSQzv_1JO68aV9zUOew"
RID = "model/xiaojs20/low_freq_copy"

def extract():
    cloudpss.setToken(TOKEN)
    os.environ['CLOUDPSS_API_URL'] = 'https://cloudpss.net/'
    
    model = cloudpss.Model.fetch(RID)
    
    # 查找“方案-冀北”
    jibei_config = None
    for config in model.configs:
        if config['name'] == '方案-冀北':
            jibei_config = config
            break
    
    if not jibei_config:
        print("未找到 方案-冀北")
        return

    params = jibei_config.get('args', {})
    
    with open('jibei_parameters.md', 'w', encoding='utf-8') as f:
        f.write("# 方案-冀北 参数列表\n\n")
        f.write("| 参数 ID | 当前值 | 说明 |\n")
        f.write("| --- | --- | --- |\n")
        for k, v in params.items():
            # 过滤掉非基础类型的参数或空的键
            if k == "" or isinstance(v, dict): continue
            f.write(f"| {k} | {v} | - |\n")
    
    # 同时保存一份 json 供后续脚本加载
    with open('jibei_config.json', 'w', encoding='utf-8') as f:
        json.dump(jibei_config, f, indent=4, ensure_ascii=False)
        
    print("已生成 jibei_parameters.md 和 jibei_config.json")

if __name__ == "__main__":
    extract()
