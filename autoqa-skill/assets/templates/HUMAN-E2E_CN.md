<!-- sync-version: 2026-06-21 -->
<!-- autoqa:document:human-e2e -->
# 人工端到端测试指南

[English](HUMAN-E2E.md) | [简体中文](HUMAN-E2E_CN.md) | [繁體中文（香港）](HUMAN-E2E_HK.md)

<!-- sync-key: purpose -->
这份清单用于检查视觉正确性、易用性、信息是否清楚，以及真实业务旅程是否完整。Agent 负责准备环境和执行命令类检查；人类负责记录产品实际使用起来是否合理。

<!-- autoqa:section:instructions -->
<!-- sync-key: instructions -->
## 使用说明

1. 按顺序执行，除非某项明确说明可以独立测试。
2. 每项记录“通过”“失败”或“受阻”，不要默默跳过。
3. 附上要求的截图或简短说明。
4. 出现 P0 或 P1 时立即停止，把检查 ID 发给 agent。
5. P2/P3 应记录；只有后续项目相互独立且安全时才继续。

<!-- autoqa:section:environment -->
<!-- sync-key: environment -->
## 测试环境

- 构建版本：
- URL 或应用：
- 浏览器/设备：
- 测试账号及角色：
- 初始测试数据：
- 重置方法：

<!-- autoqa:section:checks -->
<!-- sync-key: checks -->
## 检查项目

### HUMAN-001：<使用普通语言描述业务旅程或视觉问题>

- 前置条件：
- 步骤：
  1.
- 预期结果：
- 请特别观察：
- 需要附上的证据：
- 失败等级：`P0 | P1 | P2 | P3`
- 结果：`待测试 | 通过 | 失败 | 受阻`
- 备注：

<!-- autoqa:section:defects -->
<!-- sync-key: defects -->
## 发现的问题

| 问题 ID | 检查 ID | 实际发生了什么 | 应当发生什么 | 等级 | 证据 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

<!-- autoqa:section:sign-off -->
<!-- sync-key: sign-off -->
## 人工确认

- 是否完成全部检查：
- 尚未关闭的 P0/P1：
- 本次发布接受的 P2/P3：
- 未测试的设备、角色或业务旅程：
- 决定：`批准 | 不批准 | 记录剩余风险后批准`
- 姓名/日期：
