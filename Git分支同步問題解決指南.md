# Git 分支同步問題解決指南

## 📋 問題概述

當您發現本機檔案與 GitHub 遠端儲存庫不同步時，通常是因為以下原因：

1. **分支命名不一致**：本機使用 `master`，遠端使用 `main`
2. **多個遠端儲存庫**：同時存在 `origin` 和 `upstream`
3. **檔案結構差異**：不同分支中檔案路徑不一致
4. **提交歷史分歧**：不同分支有不同的提交記錄

---

## 🔍 問題診斷步驟

### 1. 檢查目前狀態
```bash
# 檢查目前所在分支
git branch

# 檢查所有分支（包含遠端）
git branch -a

# 檢查遠端儲存庫設定
git remote -v

# 檢查工作區狀態
git status
```

### 2. 檢查分支差異
```bash
# 檢查本機與遠端的提交差異
git log --oneline -10

# 檢查特定遠端分支的提交
git log --oneline -5 origin/main
git log --oneline -5 origin/master
```

### 3. 確認檔案差異
```bash
# 檢查檔案結構
ls -la

# 比較不同分支的檔案
git diff origin/main origin/master --name-only
```

---

## 🛠️ 解決方案

### 方案 A：統一到 main 分支（推薦）

#### 步驟 1：清理重複的遠端儲存庫
```bash
# 檢查遠端設定
git remote -v

# 如果有重複的遠端（如 upstream 指向同一個儲存庫），移除它
git remote remove upstream
```

#### 步驟 2：獲取最新的遠端資訊
```bash
# 獲取所有遠端分支的最新資訊
git fetch origin
```

#### 步驟 3：統一分支內容
```bash
# 將本機 master 的內容推送到遠端 main 分支
git push origin master:main

# 重新命名本機分支為 main
git branch -m master main

# 設定本機 main 分支追蹤遠端 main 分支
git branch --set-upstream-to=origin/main main
```

#### 步驟 4：處理檔案差異
如果發現檔案在不同位置：

```bash
# 方法 1：從其他分支複製檔案（PowerShell）
copy "source_path\filename" "destination_path\"

# 方法 2：使用 git 檢出特定檔案
git checkout origin/main -- path/to/file

# 添加並提交變更
git add .
git commit -m "同步遺失的檔案"
```

#### 步驟 5：最終同步
```bash
# 推送到遠端
git push origin main

# 確認狀態
git status
```

### 方案 B：保持 master 分支

如果您偏好使用 master 分支：

```bash
# 將遠端 main 分支的內容合併到本機 master
git merge origin/main

# 推送到遠端 master
git push origin master

# 在 GitHub 上將 master 設為預設分支
```

---

## 🔄 日常同步工作流程

### 每日開始工作前
```bash
# 1. 檢查狀態
git status

# 2. 獲取遠端更新
git fetch origin

# 3. 拉取並合併遠端變更
git pull origin main  # 或 master
```

### 工作完成後
```bash
# 1. 檢查變更
git status

# 2. 添加變更
git add .

# 3. 提交變更
git commit -m "描述您的變更"

# 4. 推送到遠端
git push origin main  # 或 master
```

### 推送前的安全檢查
```bash
# 檢查是否有未推送的提交
git log --oneline origin/main..HEAD

# 檢查是否有遠端更新
git fetch origin
git status
```

---

## 🚨 緊急修復指令

### 強制同步到遠端狀態（謹慎使用）
```bash
# 警告：這會丟失本機未提交的變更
git fetch origin
git reset --hard origin/main
```

### 處理合併衝突
```bash
# 如果拉取時出現衝突
git pull origin main

# 手動解決衝突後
git add .
git commit -m "解決合併衝突"
git push origin main
```

### 恢復意外刪除的檔案
```bash
# 從特定分支恢復檔案
git checkout origin/main -- path/to/file

# 從特定提交恢復檔案
git checkout <commit-hash> -- path/to/file
```

---

## 📚 最佳實踐建議

### 1. 分支命名統一
- 新專案建議使用 `main` 作為主分支
- 團隊內部統一分支命名規範

### 2. 定期同步
- 每天開始工作前執行 `git pull`
- 完成功能後及時 `git push`
- 不要積累太多本機變更

### 3. 提交訊息規範
```bash
# 好的提交訊息範例
git commit -m "新增友誼相關的英語學習內容"
git commit -m "修復 A1 學習者檔案格式問題"
git commit -m "更新 YouTube 影片轉錄格式"
```

### 4. 分支保護
- 在 GitHub 上設定分支保護規則
- 要求 pull request 審核
- 啟用狀態檢查

### 5. 備份重要變更
```bash
# 建立功能分支進行重要變更
git checkout -b feature/new-content
# 完成後合併回主分支
git checkout main
git merge feature/new-content
```

---

## 🔧 常用檢查指令參考

```bash
# 檢查分支關係
git branch -vv

# 檢查遠端分支
git branch -r

# 檢查提交圖表
git log --oneline --graph --all

# 檢查特定檔案的變更歷史
git log --follow -- filename

# 檢查目前分支與遠端的差異
git diff origin/main

# 檢查工作區和暫存區的差異
git diff
git diff --cached
```

---

## 📞 故障排除

### 問題：推送被拒絕
```bash
error: failed to push some refs to 'origin'
hint: Updates were rejected because the remote contains work that you do not have locally
```

**解決方案：**
```bash
git fetch origin
git pull origin main
# 解決任何衝突後
git push origin main
```

### 問題：檔案意外消失
```bash
# 檢查檔案是否在其他分支
git ls-files
git show origin/main:path/to/file

# 從其他分支恢復
git checkout origin/main -- path/to/file
```

### 問題：分支追蹤錯誤
```bash
# 重新設定分支追蹤
git branch --set-upstream-to=origin/main main
```

---

## 📝 本次解決案例記錄

### 遇到的問題
1. 本機使用 `master` 分支，GitHub 有 `main` 和 `master` 兩個分支
2. 存在重複的 `upstream` 遠端儲存庫
3. 檔案 `A1 learners.md`、`10 Years Together.md`、`Day to Night.md` 在遠端存在但本機缺失
4. 檔案結構不一致：遠端在 `white/youtube_data/`，本機在 `youtube_data/`

### 採用的解決步驟
1. ✅ 清理重複的遠端儲存庫：`git remote remove upstream`
2. ✅ 統一分支內容：`git push origin master:main`
3. ✅ 重新命名本機分支：`git branch -m master main`
4. ✅ 設定分支追蹤：`git branch --set-upstream-to=origin/main main`
5. ✅ 複製遺失檔案到正確位置
6. ✅ 提交並推送所有變更

### 最終結果
- 所有檔案已同步
- 分支追蹤關係正確
- 工作區乾淨，無衝突

---

*建立日期：2025年7月15日*  
*最後更新：2025年7月15日*

> **注意**：執行任何可能丟失資料的指令（如 `git reset --hard`）前，請務必先備份重要檔案。
