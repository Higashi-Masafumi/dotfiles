# Global Rules

## 実装手順
- ユーザーから曖昧な指示が来た場合はなんらかのユーザーに対して必要な項目について全て質問を行い、それによって決定された要件を特定のマークダウンファイルに出力して要件として残すようにする

## All Languages

- early returnとearly continueを徹底する。ネストを深くしない
- 不要な後方互換性の担保をしない（未使用の `_var` リネーム、re-export、`// removed` コメント等）
- 不要なフォールバックやエラーハンドリングを追加しない。内部コードやフレームワークの保証を信頼する
- 一度しか使わない処理のためにヘルパー関数やユーティリティ、抽象化を作らない
- 仮定の将来要件のための設計をしない。現在のタスクに必要な最小限の複雑さで実装する
- 固定値はクラス変数やモジュールレベル定数として定義する。関数内にハードコードしない
- 再定義不要な関数の切り出しはしない。同じ処理を2箇所以上で使う場合のみ関数化する
- 既に同じ責務を持つようなメソッドや包含するメソッドが存在する場合は新たにメソッドを増やさずに再利用するようにする（つまりできるだけ既存の実装で利用できる部分はできるだけ再利用することを心がけて重複実装を減らすようにしてください）
- 実装後には必ずデッドコードが存在しないかをチェックする、新しい実装や修正によりデッドコードは常に生まれる危険性があるので注意すること
- 非自明なインデックスアクセスについてはどのような変数にアクセスしているのか、なぜそのインデックスなのかをコメントすること

## Python

- バックエンドはDDD（Domain-Driven Design）+ Clean Architecture / Onion Architectureで実装する。これは必須
- 型定義はPydanticの`BaseModel`を使用する。Value Objectは`frozen=True`
- ドメイン層は外側の層に依存しない。依存の方向は常に内向き
- Repository/Gatewayはドメイン層にabstractインターフェースを定義し、infrastructureに実装を置く
- Use Caseはビジネスロジックを含まない。ドメイン層に委譲する
- ドメインエラーは具体的なサブクラスとして定義する。汎用的な`ValueError`や`Exception`を使わない
- FastAPIの`Depends`でDIを行い、具象をabstractインターフェースに接続する

## Pythonエージェントチーム (Agent Teams)

このプロジェクトはAgent Teams(`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)を有効にしている。Python実装を伴うタスクでは、以下の3つのsubagent定義をteammateとして使い分ける。

- **ddd-onion-architect**: 新機能の実装・既存コードのDDD/Onion Architectureへのリファクタリングを担当
- **python-reviewer**: 実装後のコードスタイル・DDD原則遵守をレビューし、その場で修正
- **test-coverage-checker**: テストの網羅性(APIバージョン差分、境界値・異常系の入力)をレビューし、不足するテストを追加

### チームの立ち上げ方
リードのセッションで自然文で依頼する。例:

```
ddd-onion-architect agent typeでteammateを立ち上げて〇〇機能を実装させて。
実装が固まったら、python-reviewer agent typeのteammateにレビュー・修正させ、
test-coverage-checker agent typeのteammateにテストの網羅性を確認・追加させて。
```

### 依存関係の目安
- 実装(ddd-onion-architect)が完了してから、レビュー(python-reviewer)とテスト網羅性チェック(test-coverage-checker)に着手させる。実装が固まる前に走らせると手戻りが大きい
- python-reviewerとtest-coverage-checkerは実装完了後であれば並列実行可能
