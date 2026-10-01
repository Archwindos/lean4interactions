# 本机一键同步到 GitHub

项目根目录中的 `scripts/upload-github.local.sh` 是被 Git 忽略的本机脚本。它不会进入公开仓库。目标固定为 `Archwindos/lean4interactions`，接受该仓库的 HTTPS 地址（带或不带 `.git`）以及 `git@github.com:Archwindos/lean4interactions.git` / `ssh://git@github.com/Archwindos/lean4interactions.git`。已有 origin 指向其他仓库时会退出。

从任意工作目录调用：

```bash
bash /mnt/data2/wyh/lean4project/scripts/upload-github.local.sh --check-only
bash /mnt/data2/wyh/lean4project/scripts/upload-github.local.sh --message 'Update public proof archive'
```

`--check-only` 检查工作树与现有暂存区，不暂存、提交或推送。`--dry-run` 做同样检查并说明正常执行步骤，也不修改仓库或访问远端。多行提交消息可先写入项目内的文本文件，再用 `--message-file 路径`；文本按原样传给 Git，不作为 shell 代码执行。

正常执行先审查工作树，再暂存允许发布的变更，审查准确暂存内容并显示变更统计。有变更才提交，然后实时显示 `git push --progress`，最后查询远端分支 SHA 与本地提交比较。私有池、本机脚本、临时测试仓库和旧非活动输入均由 ignore 与出版审查排除；强制加入的私有文件仍会被暂存区审查拒绝。

凭据使用本机已有的 Git credential helper、SSH agent 或终端输入。HTTPS 身份验证需要令牌时，在本机 Git 的密码提示中输入，输入内容不回显；不要把令牌发到聊天、写入脚本、放进远端 URL 或提交到仓库。若自行创建 fine-grained PAT，选择仅此仓库，授予 Contents 读写权限；只有确实改动 GitHub Actions 工作流时才按需授予工作流权限。旧已撤销的令牌不能复用。脚本不会读取或保存令牌；仅清除指向不存在或不可执行程序的 askpass 环境变量，保留可用 helper。

本轮已连接的 GitHub 应用能读取仓库，返回的账号仓库权限包含 push/admin，但实际 GitData `create_blob` 返回 `403 Resource not accessible by integration`。账号权限与应用安装权限是两项独立条件，读仓库成功不能证明该连接能写入。诊断记录见 `reader/evidence/root-github-write-check.json`；尚未通过该连接发布。遇到同样错误，应在本机核查应用对本仓库的 Contents 写权限、组织批准及凭据授权，再使用有写权限的本机 Git 凭据或修复连接。GitHub Apps 只能批准应用所请求的权限，重新选择仓库不保证该连接具备写权限。官方说明见 [管理个人访问令牌](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)及[审查已安装 GitHub Apps](https://docs.github.com/en/apps/using-github-apps/reviewing-and-modifying-installed-github-apps)。不要用已撤销令牌重试。

每个网络操作默认最多 90 秒，可用 `--timeout 30` 调整为 1–600 秒。HTTP 长时间低速也会退出。审查失败、身份验证失败、403、超时、非 fast-forward 和 SHA 不一致均返回非零退出码并说明原因。推送失败时本地提交保留；先修复凭据或连接、或 fetch 后核对并合并远端历史，再重试。脚本不 force push、不 reset、不自动无限重试、不修改全局 Git 配置。

验证记录见 `reader/evidence/upload-script-checks.json`：使用 `.tmp/vnext-upload-tests/` 中隔离仓库和本地 bare remote，验证同步、无变更、忽略规则、审查拒绝、非 fast-forward、超时、实时进度、同仓库地址别名以及特殊消息文本。这些测试没有向 GitHub 实际推送，也没有暂存或提交当前项目。
