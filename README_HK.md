<!-- sync-version: 2026-06-21 -->
# Coding Agent AutoQA

[English](README.md) | [简体中文](README_CN.md) | [繁體中文（香港）](README_HK.md)

<!-- sync-key: promise -->
AutoQA 是一個為 coding agent 軟件開發而設、以證據為本的 QA skill，尤其適合沒有技術背景的產品負責人。它配合 [coding_agent_constitution](https://github.com/CUHK-Business-School-AI-Hub/coding_agent_constitution) 使用：constitution 把產品意圖、架構和合約沉澱成長期文件；AutoQA 再把這些文件轉成測試、可執行業務流程、最新證據，以及方便人執行的發佈檢查清單。

AutoQA 不會取代測試框架、code reviewer 或人的判斷。它防止 coding agent 把預設 QA harness、一個 happy-path 測試或漂亮的 coverage 數字當成充分證明。

<!-- sync-key: mindset -->
## QA Mindset

核心功能開發可以探索多種合理實現；QA 的自由度較低，因為它的職責是挑戰實現，而不是欣賞實現。

工具可以改變，但以下證明責任不能改變：

- 從業務行為和合約出發，而不是從 agent 剛好寫出的程式碼出發。
- 聲稱模組已覆蓋之前，先列出所有公開入口和出口。
- 適用時測試拒絕、邊界、狀態、權限和依賴失敗。
- 證明關鍵測試真的能發現一個故意改錯的實現。
- 執行每一條已命名業務流程變體，並保留最新指令證據。
- 由人判斷視覺質素、易用性、資訊清晰度和完整真實流程。
- 安全、私隱、資料損失、核心流程或重大業務結果錯誤必須立即停止。

QA 不是悲觀，而是有紀律地把「agent 看起來很有信心」換成「這是證據、這是缺口、這是需要人作出的決定」。

| 不可妥協 | 可以按項目調整 |
| --- | --- |
| 需求到測試可追蹤 | pytest、Vitest、JUnit 或其他框架 |
| 入口出口及業務邊界覆蓋 | 測試檔案的組織和命名 |
| 最新的可執行證據 | 指令如何組合 |
| 人負責視覺和易用性判斷 | 瀏覽器、裝置及清單格式 |
| 發佈時沒有未解決的 P0/P1 | P2/P3 如何排期 |

<!-- sync-key: partnership -->
## 如何與 Constitution 配合

```text
產品想法
   |
   v
constitution-skill
   SPEC -> 用戶目標、業務流程、驗收準則
   ARCH -> 模組及職責邊界
   CONTRACTS -> 輸入、輸出、錯誤、schema、event
   RULES -> repository 專屬安全和測試規則
   TASKS -> 細小而清楚的實現工作
   |
   v
autoqa-skill
   QA plan -> 必須證明甚麼、為甚麼
   file gates -> 每個程式檔案修改後的快速回饋
   module cases -> 面向業務的黑盒邊界測試
   integration flows -> 用 script 跑完整流程
   human E2E -> 視覺、易用性及發佈判斷
   |
   v
有證據支持的發佈決定
```

沒有 constitution 文件時 AutoQA 仍可運作，但必須把推斷出的需求標成假設。兩者結合更強，因為 QA agent 可以根據長期產品事實獨立設計測試，而不是從實現程式碼倒推原本意圖。

<!-- sync-key: gates -->
## 為甚麼需要這些「門」

門是停止條件，不是儀式。每一道門都在仍然容易定位和修正的時候攔截一類不同錯誤。

### 門 0：QA 規劃

實現之前，agent 先整理需求、風險、模組、入口、出口、業務流程變體、環境、指令和人工檢查。這樣測試不會被現有實現帶偏。

### 門 1：檔案冒煙

每修改一個可執行程式檔案，agent 立即執行最窄的語法、類型、import、compile、啟動或業務冒煙檢查。被動 schema 或 type 檔案由 validator 或 consumer 覆蓋，不強行製造無意義測試。

原因：一個剛寫壞的檔案，比五個之後的檔案都依賴它時更容易診斷。

### 門 2：模組黑盒

把每個架構模組當成黑盒，覆蓋所有公開入口和出口，以及適用的正常、拒絕、邊界、狀態、權限、依賴、冪等、並發和復原行為。

原因：一次 request 能穿到一次 response，只能證明連接存在，不能證明業務正確。

### 門 3：功能整合

透過 HTTP、CLI、event、檔案、job 或其他 script 介面，執行每一條已命名的正常、替代和失敗流程。內部組件盡量保持真實；外部系統只在有文件的合約邊界替換。

原因：每個模組單獨正確，接起來仍可能錯誤。

### 門 4：人工 E2E

Agent 準備一般語言清單和測試環境；人按真實流程操作，判斷版面、文案、回饋、鍵盤/觸控、responsive layout、資訊清晰度和整體是否合理。

原因：agent 可以讀取像素和 DOM 狀態，但不能代目標用戶作出視覺和體驗批准。

### 發佈門

只有自動化證據仍然最新、人工檢查已完成、而且沒有未解決的 P0/P1 時，AutoQA 才接受「可以發佈」的聲明。P2/P3 會繼續作為剩餘風險展示。

<!-- sync-key: quick-start -->
## 非技術負責人的快速開始

### 1. 安裝或提供 skill

把 `autoqa-skill/` 放入 coding harness 支援的 skill 目錄，或直接把該資料夾路徑交給 agent。常用安裝方法如下：

```bash
# Codex 個人 skill
mkdir -p ~/.codex/skills
cp -R autoqa-skill ~/.codex/skills/autoqa-skill

# Cursor 項目級 skill
mkdir -p .cursor/skills
cp -R autoqa-skill .cursor/skills/autoqa-skill

# Claude Code 項目級 skill
mkdir -p .claude/skills
cp -R autoqa-skill .claude/skills/autoqa-skill
```

安裝後重新啟動或開一個新的 agent session。如果 harness 找不到 skill，請以它目前的文件為準，因為安裝慣例可能會演進。

### 2. 同時使用 constitution 和 AutoQA

可以這樣開始：

```text
使用 constitution-skill 定義這個產品，並把下一個功能拆成一項有邊界的工作。
然後在實現前使用 autoqa-skill 建立 QA 計劃；寫程式期間執行檔案門和模組門；
功能完成後準備人工 E2E 清單。所有需要我決定的事情請用非技術語言解釋。
```

### 3. 主動索取真正證據

常用提示包括：

```text
告訴我還有哪些業務需求沒有對應測試。
```

```text
把這個模組當成黑盒審核。列出每個入口、出口、適用邊界，以及證明它的測試。
```

```text
執行 AutoQA 自動化門，告訴我甚麼通過、甚麼失敗、還有甚麼未測試。
```

```text
用香港繁體中文準備人工 E2E 指南。如果我發現 P0 或 P1，請立即叫我停止。
```

### 4. 完成人應該做的部分

打開 `docs/QA/HUMAN-E2E.md`，逐項操作。你不需要檢查程式碼或 log。記錄實際發生的事情，附上要求的證據；失敗時把檢查 ID 交回 agent。

遇到陌生詞，可以按需要閱讀 [QA 新手百科](autoqa-skill/references/rookie-qa-pedia_HK.md)。

<!-- sync-key: artifacts -->
## AutoQA 會向項目加入甚麼

| 檔案 | 讀者 | 用途 |
| --- | --- | --- |
| `docs/QA/QA-PLAN.md` | 人和 agent | 範圍、風險、來源、環境和退出條件 |
| `docs/QA/QA-MATRIX.md` | 人和 reviewer | 從需求到測試和證據的可讀映射 |
| `docs/QA/qa-manifest.json` | Agent 和 validator | 可機械檢查的邊界、案例、流程、指令、人工檢查和缺陷 |
| `docs/QA/HUMAN-E2E.md` | 非技術人士 | 編號後的視覺和易用性清單 |
| `.autoqa/evidence/latest.json` | 本地 validator | 最新指令結果及指令指紋，通常不提交 |

確定性檢查指令：

```bash
python3 autoqa-skill/scripts/check_qa.py --root /path/to/project --phase plan
python3 autoqa-skill/scripts/check_qa.py --root /path/to/project --phase automated --run
python3 autoqa-skill/scripts/check_qa.py --root /path/to/project --phase release
```

指令執行器使用參數陣列，不使用隱藏邏輯的 shell 字串。指令改變或證據超過時間限制後，原有證據會失效。

<!-- sync-key: defects -->
## QA 失敗時怎樣做

| 等級 | 常見例子 | 下一步 |
| --- | --- | --- |
| P0 | 資料損失、私隱/安全洩漏、不受控的不可逆行為 | 立即停止；不要在該環境繼續 |
| P1 | 應用程式無法啟動、核心流程受阻、重大結果錯誤、嚴重無障礙障礙 | 停止受影響測試；修正並重測後再繼續 |
| P2 | 非核心行為錯誤或容易誤解，但有安全替代方法 | 保留證據；繼續互相獨立的安全檢查；之後集中提交 |
| P3 | 視覺、文案、間距或低影響細節問題 | 記錄並完成清單 |

等級取決於影響，不取決於修正看起來是否容易。阻斷問題修正後，agent 必須說明要重跑哪些自動化測試、重做哪些已通過的人工檢查。

<!-- sync-key: best-practices -->
## 不斷演進的最佳實踐

AutoQA 初始版本刻意保留一個空的最佳實踐 registry。規劃測試前，agent 先檢查 registry；沒有目前適用的 practice pack 時，再查找最新官方文件、標準和第一手資料，而不是只依賴記憶。

新 practice pack 依次經歷 `Candidate`、`Active` 和 `Superseded`。每個 pack 記錄範圍、不適用情況、來源、覆核日期、驗證案例和限制。尚未證實的想法放在 `TODO_BEST_PRACTICE_EVOLUTION.md`，不能被暗中當成業界事實。

<!-- sync-key: languages -->
## 語言

`SKILL.md`、scripts、schema 欄位、ID 和 agent 技術參考以英文為規範源。README、QA 新手百科和人工 E2E 模板同時維護英文、簡體中文和香港繁體中文。`check_translations.py` 檢查這些關鍵文件的版本和章節是否同步。

<!-- sync-key: influences -->
## 參考項目與授權

AutoQA 的「先證據後聲明」、red-green 測試和防止 mock 偷懶的機制受到 MIT 項目 [obra/superpowers](https://github.com/obra/superpowers) 啟發；更廣泛的測試詞彙亦參考了 MIT 項目 [wshobson/agents](https://github.com/wshobson/agents) 和 [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills)。

本 repository 採用 [MIT License](LICENSE)。
