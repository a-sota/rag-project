# Manual Evaluation Log

## Date
- 2026-04-09

## Evaluation Criteria
- retrieval_ok:
  - yes = 正しい文書が top-1 または top-k 内にある
  - no = 正しい文書が取得できていない
- generation_ok:
  - yes = 回答が参照文書に忠実で、質問にも正しく答えている
  - no = 間違っている、ずれている、余計なことを言っている
- failure_type:
  - no_issue
  - retrieval_fail
  - generation_fail
  - data_missing

---

## 1
- type: exact
- question: RAGとは何か？
- expected: RAGは検索した文書をもとに回答を生成する手法である。
- retrieved_top1: RAGとは、検索した文書をもとに回答を生成する手法である。
- retrieval_ok: yes
- generated_answer: RAGとは、検索した文書をもとに回答を生成する手法である。
- generation_ok: yes
- failure_type: no_issue
- note: exact質問で安定して正解。

## 2
- type: exact
- question: embeddingとは何か？
- expected: embeddingはテキストを意味を保ったままベクトルに変換する技術である。
- retrieved_top1: embeddingはテキストを意味を保ったままベクトルに変換する技術である。
- retrieval_ok: yes
- generated_answer: embeddingはテキストを意味を保ったままベクトルに変換する技術である。
- generation_ok: yes
- failure_type: no_issue
- note: exact質問で安定して正解。

## 3
- type: exact
- question: retrievalとは何か？
- expected: retrievalは質問に関連する文書を検索して取得する処理である。
- retrieved_top1: retrievalは質問に関連する文書を検索して取得する処理である。
- retrieval_ok: yes
- generated_answer: retrievalは質問に関連する文書を検索して取得する処理である。
- generation_ok: yes
- failure_type: no_issue
- note: exact質問で安定して正解。

## 4
- type: paraphrase
- question: RAGって何？
- expected: RAGは検索した文書をもとに回答を生成する手法である。
- retrieved_top1: RAGは検索した文書をもとに回答を生成する手法である。
- retrieval_ok: yes
- generated_answer: RAGは検索した文書をもとに回答を生成する手法である。
- generation_ok: yes
- failure_type: no_issue
- note: 「RAGって何？」という砕けた表現でも正しく取得できた。

## 5
- type: paraphrase
- question: embeddingってどういう意味？
- expected: embeddingはテキストを意味を保ったままベクトルに変換する技術である。
- retrieved_top1: embeddingはテキストを意味を保ったままベクトルに変換する技術である。
- retrieval_ok: yes
- generated_answer: embeddingはテキストを意味を保ったままベクトルに変換する技術である。
- generation_ok: yes
- failure_type: no_issue
- note: 「どういう意味？」という言い換えにも対応できた。

## 6
- type: paraphrase
- question: 関連する文書を探してくる処理って何？
- expected: retrievalは質問に関連する文書を検索して取得する処理である。
- retrieved_top1: retrievalは質問に関連する文書を検索して取得する処理である。
- retrieval_ok: yes
- generated_answer: 関連する文書を探してくる処理は「retrieval」である。
- generation_ok: yes
- failure_type: no_issue
- note: retrieval を自然な言い換えで聞いても正しく答えられた。

## 7
- type: paraphrase
- question: RAGで嘘っぽい回答が出る現象は何？
- expected: hallucinationは生成AIが事実と異なる内容をもっともらしく出力してしまう現象である。
- retrieved_top1: RAGは検索した文書をもとに回答を生成する手法である。
- retrieval_ok: no
- generated_answer: 参照文書からは分かりません。
- generation_ok: yes
- failure_type: retrieval_fail
- note: hallucination を問う質問に対して RAG の定義文書を取得した。生成側は参照文書にないことを補完せず「分かりません」と返しており健全。

---

## Findings
### retrievalの失敗
- 概念的な言い換え（例: 「嘘っぽい回答」→ hallucination）には弱い。
- exact質問と簡単なparaphraseには強いが、抽象的な言い換えでは誤検索が起こる。

### generationの失敗
- 現時点では大きな失敗は見られない。
- 参照文書にない場合は「分かりません」と返せており、hallucination抑制は機能している。

### データ不足
- hallucination に対応する言い換え表現がデータに不足している可能性がある。
- hard質問に対しては、説明用データの粒度や表現バリエーションが不足しているかもしれない。

### 気づいたこと
- exact質問と簡単な言い換えにはかなり強い。
- generation より retrieval の改善余地が大きい。
- prompt の「参照文書に答えがない場合は分かりませんと答える」という指示は有効に働いている。