### Git协作方案

#### 分支命名规范

- **开发分支**: `dev_1.0`
- **个人分支**: `dev_1.0_<username>`，例如 `dev_1.0_hxy`

#### 工作流程

1. **从开发分支创建个人分支**
    ```bash
    git checkout dev_1.0
    git pull origin dev_1.0
    git checkout -b dev_1.0_hxy
    ```

2. **在个人分支上进行开发和自测**
    - 进行代码开发和自测，确保功能完整且无明显Bug。

3. **从主分支合并最新代码到个人分支**
    ```bash
    git checkout dev_1.0
    git pull origin dev_1.0
    git checkout dev_1.0_hxy
    git merge dev_1.0
    ```

4. **解决合并冲突（如果有）**
    - 如果在合并过程中出现冲突，手动解决冲突并提交。
    ```bash
    git add .
    git commit -m "Resolved merge conflicts"
    ```

5. **推送个人分支到远程仓库**
    ```bash
    git push origin dev_1.0_hxy
    ```

6. **创建合并请求（Merge Request, MR）**
    - 在代码托管平台（如GitHub、GitLab）上创建一个合并请求，将 `dev_1.0_hxy` 分支合并到 `dev_1.0` 分支。
    - 在合并请求中描述所做的更改和测试情况。
    - 提交MR链接 https://gitlab.shorttv.live/shorttv/tools/mobile-ui-automation-tests/-/merge_requests/new

7. **代码审查和合并**
    - 团队成员或代码审查员对合并请求进行审查。
    - 审查通过后，将合并请求合并到 `dev_1.0` 分支。
    ```

### 示例命令

```bash
# Step 1: 从开发分支创建个人分支
git checkout dev_1.0
git pull origin dev_1.0
git checkout -b dev_1.0_hxy

# Step 2: 在个人分支上进行开发和自测
# (进行代码开发和自测)

# Step 3: 从主分支合并最新代码到个人分支
git checkout dev_1.0
git pull origin dev_1.0
git checkout dev_1.0_hxy
git merge dev_1.0

# Step 4: 解决合并冲突（如果有）
# (手动解决冲突并提交)
git add .
git commit -m "Resolved merge conflicts"

# Step 5: 推送个人分支到远程仓库
git push origin dev_1.0_hxy

# Step 6: 创建合并请求（MR）
# (在代码托管平台上创建合并请求)

# Step 7: 代码审查和合并
# (团队成员审查并合并代码)

# Step 8: 删除个人分支（可选）
git branch -d dev_1.0_hxy
git push origin --delete dev_1.0_hxy
```

这个方案可以帮助团队成员在开发过程中保持代码的同步和一致性，同时通过代码审查确保代码质量。