# Workflow Module: archive

Archive 只处理已持久化的 Compact/Full 记录。Inline 没有变更目录，不强制生成知识或归档文档；如出现 durable knowledge，应先 `Inline -> Compact` 或直接 Full。

## Process

1. 读取当前记录源的实际执行、review、风险和 knowledge candidates。
2. 只读 `knowledge/index.md`，定位需要新增或合并的目标知识文件。
3. 提取可复用知识、Harness gap 和 Loop 改进，不强制伪造条目。
4. 展示候选，等待用户确认写入哪些内容。
5. 更新稳定 K-ID、Tags、Scope、Applies-To、Risk、Last-Verified、File。
6. 将变更移入 `changes/archives/`；Complex 子项目先确保 `log.summary.md` 可供下游读取。
7. 运行验证并使用 `docs(archive): ...` 提交。
