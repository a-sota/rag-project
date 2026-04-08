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

### hallucinationまわりのQ＆Aを３つ増やして再試行
- question: RAGで嘘っぽい回答が出る現象は何？
- expected: hallucinationは生成AIが事実と異なる内容をもっともらしく出力してしまう現象である。
- retrieved_top1: hallucinationは生成AIが事実と異なる内容をもっともらしく出力してしまう現象である。
- retrieval_ok: yes
- generated_answer: hallucinationは生成AIが事実と異なる内容をもっともらしく出力してしまう現象である。
- generation_ok: yes
- failure_type: no_issue

- hallucination の言い換え表現を追加することで retrieval が改善した。
- generation には変更を加えていないため、今回の改善の主因は retrieval 側のデータ拡張である。
- 一方で top2, top3 には RAG という語に引っ張られた関連文書も残っており、順位付けにはまだ改善余地がある。


## Day 5: top_k Comparison

### Purpose
- top_k = 1, 3, 5 を比較し、retrieval と generation の挙動の違いを観察する。
- 現時点のデータ規模で最も安定する top_k を決める。

### Evaluation Points
- retrieval_quality: 正しい文書が top1 に来ているか、ノイズが多すぎないか
- generation_quality: 回答が正確か、余計な情報に引っ張られていないか
- note: 気づいたこと

---

## Question 1
- question: RAGの良いところは？
- expected: 最新知識や独自知識を追加学習なしで参照でき、回答の根拠も示しやすいこと。

### top_k = 1
- retrieved_top1: RAGの利点は、最新知識や独自知識を追加学習なしで参照できることと、回答の根拠を示しやすいことである。
- generation_answer: RAGの良いところは、最新知識や独自知識を追加学習なしで参照できることと、回答の根拠を示しやすいことである。
- retrieval_quality: good
- generation_quality: good
- note: 上位1件で十分に必要な情報が取れており、回答も自然。

### top_k = 3
- retrieved_top1: RAGの利点は最新知識や独自知識を追加学習なしで参照でき、回答の根拠も示しやすいことである。
- generation_answer: RAGの良いところは、最新知識や独自知識を追加学習なしで参照でき、回答の根拠も示しやすいことである。
- retrieval_quality: good
- generation_quality: good
- note: top_k=1 とほぼ同等で安定。

### top_k = 5
- retrieved_top1: RAGの利点は最新知識や独自知識を追加学習なしで参照でき、回答の根拠も示しやすいことである。
- generation_answer: RAGの良いところは、最新知識や独自知識を追加学習なしで参照できることや、回答の根拠を示しやすいことである。
- retrieval_quality: good
- generation_quality: good
- note: わずかに言い回しが増えたが、悪化は見られない。

---

## Question 2
- question: 文書を探してくる処理って何？
- expected: retrievalは質問に関連する文書を検索して取得する処理である。

### top_k = 1
- retrieved_top1: retrievalは質問に関連する文書を検索して取得する処理である。
- generation_answer: retrievalは質問に関連する文書を検索して取得する処理である。
- retrieval_quality: good
- generation_quality: good
- note: 最もシンプルで素直な出力。

### top_k = 3
- retrieved_top1: retrievalは質問に関連する文書を検索して取得する処理である。
- generation_answer: retrievalは質問に関連する文書を検索して取得する処理である。
- retrieval_quality: good
- generation_quality: good
- note: top_k=1 と同程度に安定。

### top_k = 5
- retrieved_top1: retrievalは質問に関連する文書を検索して取得する処理である。
- generation_answer: 参照文書からは、文書を探してくる処理は「retrieval」と説明されています。  
具体的には、retrievalは質問に関連する文書を検索して取得する処理です（文書1）。
- retrieval_quality: good
- generation_quality: okay
- note: 正答ではあるが、文書参照の説明が増えて少し冗長になった。

---

## Question 3
- question: なぜ質問もembeddingする必要があるの？
- expected: 質問もembeddingすることで文書ベクトルと同じ空間で比較でき、意味の近い文書を検索できるようにするため。

### top_k = 1
- retrieved_top1: 質問もembeddingすることで文書ベクトルと同じ空間で比較でき、意味の近い文書を検索できる。
- generation_answer: 質問もembeddingすることで文書ベクトルと同じ空間で比較でき、意味の近い文書を検索できるためです。
- retrieval_quality: good
- generation_quality: good
- note: 必要十分な回答。

### top_k = 3
- retrieved_top1: 質問もembeddingすることで文書ベクトルと同じ空間で比較でき、意味の近い文書を検索できる。
- generation_answer: 質問もembeddingすることで文書ベクトルと同じ空間で比較でき、意味の近い文書を検索できるためです。
- retrieval_quality: good
- generation_quality: good
- note: top_k=1 と差はほぼ見られない。

### top_k = 5
- retrieved_top1: 質問もembeddingすることで文書ベクトルと同じ空間で比較でき、意味の近い文書を検索できる。
- generation_answer: 質問もembeddingすることで文書ベクトルと同じ空間で比較でき、意味の近い文書を検索できるためです。
- retrieval_quality: good
- generation_quality: good
- note: top_k増加による悪影響は見られない。

---

## Question 4
- question: RAGで間違った答えが出るのは何が原因？
- expected: retrievalの失敗、文脈不足、またはhallucinationが原因になりうる。
- note_expected: 今のデータでは完全一致する文書がない可能性があるため、data_missing になってもよい。

### top_k = 1
- retrieved_top1: RAGは検索した文書をもとに回答を生成する手法である。
- generation_answer: 参照文書からは分かりません。
- retrieval_quality: poor
- generation_quality: good
- note: データ不足のため retrieval は不十分だが、generation は無理に答えず健全に停止できている。

### top_k = 3
- retrieved_top1: RAGは検索した文書をもとに回答を生成する手法である。
- generation_answer: 参照文書からは分かりません。
- retrieval_quality: poor
- generation_quality: good
- note: top_k=1 と同様に、安全に「分かりません」と返せている。

### top_k = 5
- retrieved_top1: RAGは検索した文書をもとに回答を生成する手法である。
- generation_answer: hallucinationは生成AIが事実と異なる内容をもっともらしく出力してしまう現象であり、これがRAGで間違った答えが出る原因である。
- retrieval_quality: poor
- generation_quality: poor
- note: 半関連の hallucination 文書に引っ張られて、もっともらしいが不十分な誤答を生成した。

---

## Question 5
- question: chunkサイズってなんで大事？
- expected: chunkサイズが大きすぎるとノイズが増え、小さすぎると文脈が不足するため重要である。

### top_k = 1
- retrieved_top1: chunkサイズが大きすぎるとノイズが増え、小さすぎると文脈が不足するため重要である。
- generation_answer: chunkサイズが大事なのは、大きすぎるとノイズが増え、小さすぎると文脈が不足してしまうためです。
- retrieval_quality: good
- generation_quality: good
- note: 十分に正答できている。

### top_k = 3
- retrieved_top1: chunkサイズが大きすぎるとノイズが増え、小さすぎると文脈が不足するため重要である。
- generation_answer: chunkサイズが大事なのは、chunkサイズが大きすぎるとノイズが増え、小さすぎると文脈が不足するためです。
- retrieval_quality: good
- generation_quality: good
- note: top_k=1 とほぼ同等に安定。

### top_k = 5
- retrieved_top1: chunkサイズが大きすぎるとノイズが増え、小さすぎると文脈が不足するため重要である。
- generation_answer: chunkサイズが大きすぎるとノイズが増え、小さすぎると文脈が不足するため重要である。
- retrieval_quality: good
- generation_quality: good
- note: 大きな悪化は見られない。

---

## Day 5 Findings

### top_k = 1
- 強み: ノイズが少なく、必要な文書が明確な質問では安定して正答できた。
- 弱み: データに答えがない質問では「分かりません」になりやすく、補足情報は得にくい。

### top_k = 3
- 強み: top_k=1 と同程度に安定しつつ、今後データが増えた場合にも対応しやすいバランスの良い設定だった。
- 弱み: 今回の小規模データでは top_k=1 に対する明確な優位性はまだ小さい。

### top_k = 5
- 強み: 定義が明確な質問では正答を維持でき、場合によっては少し丁寧な説明ができた。
- 弱み: データに直接答えがない質問では、半関連の文書に引っ張られて誤答を生成しやすい。Question 4 でその傾向が見られた。

### Best Setting
- best_top_k: 3
- reason: top_k=1 でも十分強いが、今後の拡張性とバランスを考えると top_k=3 が最も妥当だった。top_k=5 は data_missing の質問で誤答リスクが高い。

### Overall Notes
- 定義が明確で対応文書がある質問では、top_k=1,3,5 の差は小さかった。
- 一方で、答えがデータに存在しない質問では top_k=5 にすると generation が半関連文書から無理に答えを作る傾向が見られた。
- 現時点では top_k の微調整よりも、原因・理由系Q&Aの追加や言い換え表現の拡張のほうが改善効果は大きいと考えられる。