<!-- sync-version: 2026-06-21 -->
<!-- autoqa:document:human-e2e -->
# 人工端到端測試指南

[English](HUMAN-E2E.md) | [简体中文](HUMAN-E2E_CN.md) | [繁體中文（香港）](HUMAN-E2E_HK.md)

<!-- sync-key: purpose -->
這份清單用來檢查視覺是否正確、是否易用、資訊是否清晰，以及真實業務流程是否完整。Agent 負責準備環境和執行指令式檢查；人負責記錄產品實際使用時是否合理。

<!-- autoqa:section:instructions -->
<!-- sync-key: instructions -->
## 使用說明

1. 按次序執行，除非某項清楚註明可以獨立測試。
2. 每項記錄「通過」「失敗」或「受阻」，不要靜靜跳過。
3. 附上要求的螢幕截圖或簡短說明。
4. 出現 P0 或 P1 時立即停止，把檢查 ID 交給 agent。
5. P2/P3 要記錄；只有之後的項目互相獨立而且安全時才繼續。

<!-- autoqa:section:environment -->
<!-- sync-key: environment -->
## 測試環境

- Build 或版本：
- URL 或應用程式：
- 瀏覽器/裝置：
- 測試帳戶及角色：
- 起始測試資料：
- 重設方法：

<!-- autoqa:section:checks -->
<!-- sync-key: checks -->
## 檢查項目

### HUMAN-001：<用一般語言描述業務流程或視覺問題>

- 前置條件：
- 步驟：
  1.
- 預期結果：
- 請特別留意：
- 需要附上的證據：
- 失敗等級：`P0 | P1 | P2 | P3`
- 結果：`待測試 | 通過 | 失敗 | 受阻`
- 備註：

<!-- autoqa:section:defects -->
<!-- sync-key: defects -->
## 發現的問題

| 問題 ID | 檢查 ID | 實際發生甚麼 | 應該發生甚麼 | 等級 | 證據 | 狀態 |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

<!-- autoqa:section:sign-off -->
<!-- sync-key: sign-off -->
## 人工確認

- 是否完成全部檢查：
- 尚未關閉的 P0/P1：
- 今次發佈接受的 P2/P3：
- 未測試的裝置、角色或業務流程：
- 決定：`批准 | 不批准 | 記錄剩餘風險後批准`
- 姓名/日期：
