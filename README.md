# 结构

```
flareflow_stress_test/
├── api/            # 更新脚本/接口
├── api_cases/      # 接口测试用例集合
├── api_clients/    # 请求封装逻辑，如HTTP客户端
├── locust_tasks/   # locust请求封装逻辑
├── log/            # 日志输出目录
├── reports/        # locust压测报告输出目录
├── stressCases/    # locust压测脚本(入口文件)
├── utils/      # 工具函数、通用工具类
```

# 接口测试执行

```
├── api_cases/  # 接口测试用例集合
│ ├── 1_2_8     # 版本
│ │  └── case   # 用例
```

示例:  pytest api_cases/1_2_8/test_shortPlay_unlockEpisodeByWatchAd.py -v

# locust 压测执行

- 执行:  locust -f stressCases/saveWatchHistory.py
    - 输入用户数和孵化率启动压测
- 无UI模式执行:
    - locust -f testcases/top.py --headless -u 10 -r 10 -t 10s --csv=output/report --html=report.html
      --host  https://api-stress.ffff.team
    - locust -f testcases/top.py --users 1 --spawn-rate 1 --run-time 10s --headless --host  https://api-stress.ffff.team

# 更新接口

说明:

- 匹配前端代码, 获取真实在用的接口, 脚本: get_api_from_arron.py, 产物: matched_urls.txt
- 下载yapi最新的接口信息, 脚本:download_from_yapi.py, 产物: swaggerApi.json
- 处理接口信息, 去掉以及废弃接口, 保留最终接口信息, 脚本: update_swagger.py, 产物: swagger_updated.json
- 生成封装函数, 脚本: update_code.py,
    - 接口测试产物: api_clients
    - locust压测产物: locust_tasks

```shell
# 设置前端路径
SRC="$HOME/code/flareflow_stress_test/api"
# 设置后端路径
DST="$HOME/code/aaron"
# 在项目api目录下执行
python3 "$DST/download_from_yapi.py"
cp "$SRC/get_api_from_arron.py" "$DST/"
python3 "$DST/get_api_from_arron.py"
cp "$DST/matched_urls.txt" "$SRC/"
python3 "$SRC/update_swagger.py"
```
