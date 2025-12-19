# Git運用ルール（GitHub Flow）

## ブランチ構成

- main
  - 常に安定して動作するブランチ
  - 公開・デプロイ可能な状態を維持する
  - 直接 commit / push は行わない

- feature/*
  - 新機能追加・改善・リファクタリング用
  - main から作成し、完了後に main へマージする

---

## ブランチ命名規則

### 基本ルール
- 小文字のみ使用する
- 単語区切りはハイフン（-）
- 何をするブランチかが一目で分かる名前にする

### 命名形式
- feature/<概要>

### 命名例

- feature/password-reset
- feature/https-nginx
- feature/task-validation

---

## 開発フロー（GitHub Flow）

1. main を最新化する
   git checkout main
   git pull

2. ブランチを作成する
   git checkout -b feature/xxx

3. ブランチ上で実装・コミットする
   git add .
   git commit -m "Add new feature"

4. GitHub に push する
   git push -u origin feature/xxx

5. Pull Request を作成し、動作確認を行う

6. 問題なければ main にマージする

7. マージ後、不要なブランチを削除する
   git branch -d feature/xxx
   git push origin --delete feature/xxx

---

## 運用ルール

- main は常に人に見せられる状態を保つ
- 1ブランチ = 1機能 / 1修正
- 実装途中のコードは main に入れない
- 機能追加・修正は必ずブランチを切って行う

---

## コミットメッセージ指針

- 英語で簡潔に記述する
- 変更内容が分かる動詞から始める

例:
- Add password reset email feature
- Refactor project structure
- Fix validation error on task creation

---

## 補足

本ルールは GitHub Flow に準拠し、  
個人開発においても実務を意識した開発フローを再現することを目的とする
