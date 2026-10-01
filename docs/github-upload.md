# 本机一键同步到 GitHub

项目根目录中的 `scripts/upload-github.local.sh` 是被 Git 忽略的本机脚本。它不会进入公开仓库。目标固定为 `Archwindos/lean4interactions`，接受该仓库的 HTTPS 地址（带或不带 `.git`）以及 `git@github.com:Archwindos/lean4interactions.git` / `ssh://git@github.com/Archwindos/lean4interactions.git`。已有 origin 指向其他仓库时会退出。

首次使用 HTTPS 上传时，在这台服务器的真实终端中运行 `--setup-auth`，按隐藏提示输入有效 GitHub PAT。验证成功后，之后普通上传可直接复用本机凭据。从任意工作目录调用：

```bash
bash /mnt/data2/wyh/lean4project/scripts/upload-github.local.sh --setup-auth
bash /mnt/data2/wyh/lean4project/scripts/upload-github.local.sh --check-only
bash /mnt/data2/wyh/lean4project/scripts/upload-github.local.sh --message 'Update public proof archive'
```

`--check-only` 检查工作树与现有暂存区，不暂存、提交或推送。`--dry-run` 做同样检查并说明正常执行步骤，也不修改仓库或访问远端。多行提交消息可先写入项目内的文本文件，再用 `--message-file 路径`；文本按原样传给 Git，不作为 shell 代码执行。

正常执行先审查工作树，再暂存允许发布的变更，审查准确暂存内容并显示变更统计。有变更才提交，然后实时显示 `git push --progress`，最后查询远端分支 SHA 与本地提交比较。私有池、本机脚本、临时测试仓库和旧非活动输入均由 ignore 与出版审查排除；强制加入的私有文件仍会被暂存区审查拒绝。

`--setup-auth` 只设置认证，不做出版审查、不暂存、不提交、不实际推送。它使用 Git 的现有代理配置，在最多 90 秒的 `push --dry-run` 中验证新凭据；失败时删除临时凭据，保留原凭据与 helper 设置。成功后使用标准 Git credential-store，将令牌以明文保存于 `.git/local-auth/github-credentials`，文件权限为 `600`、目录权限为 `700`。这些文件位于私有 `.git` 内，不会上传；仅修改本仓库的 Git 配置。非交互运行不能设置认证，令牌不从参数或聊天文件读取。令牌失效后，在本机终端再次执行同一 `--setup-auth` 命令。

普通上传使用本机 Git credential helper、SSH agent 或终端隐藏输入。脚本清除继承的 VSCode askpass 与 IPC 环境，并为网络 Git 调用禁用 `core.askPass`，避免失效 socket 接管认证；保留凭据 helper，非交互缺凭据时立即失败。不要把令牌发到聊天、写入脚本、放进远端 URL 或提交到仓库。创建 fine-grained PAT 时仅选择此仓库并授予 Contents 读写权限；只有修改 GitHub Actions 工作流时才按需授予工作流权限。旧已撤销的令牌不能复用。官方说明见 [管理个人访问令牌](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)。

历史诊断中，GitHub 应用连接曾在 GitData `create_blob` 返回 `403 Resource not accessible by integration`；这是当时的连接权限问题，记录见 `reader/evidence/root-github-write-check.json`。当前本机上传入口使用上述 Git 凭据设置。

普通上传的每个网络操作默认最多 600 秒，可用 `--timeout 30` 调整为 1–600 秒；`--setup-auth` 验证上限始终为 90 秒。HTTP 低速阈值已关闭，网络操作由总超时限制。审查失败、身份验证失败、403、超时、非 fast-forward 和 SHA 不一致均返回非零退出码并说明原因。推送失败时本地提交保留；先修复凭据或连接、或 fetch 后核对并合并远端历史，再重试。脚本不 force push、不 reset、不自动无限重试、不修改全局 Git 配置。

验证记录见 `reader/evidence/upload-script-checks.json`：使用 `.tmp/vnext-upload-tests/` 中隔离仓库和本地 bare remote，验证同步、无变更、忽略规则、审查拒绝、非 fast-forward、超时、实时进度、同仓库地址别名以及特殊消息文本。这些测试没有向 GitHub 实际推送，也没有暂存或提交当前项目。
