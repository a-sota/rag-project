# Manual Evaluation Log1

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


# Manual Evaluation Log2

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

#　Manual Evaluation Log3

## Purpose
- 原因・理由系Q&Aを追加したあとに、言い換え・抽象化質問でも答えられるか確認する
- retrieval と generation のどちらが弱いかを観察する
- 今後さらに追加すべき質問タイプを見つける

## Evaluation Criteria
- retrieval_ok:
  - yes = 正しい文書が top-1 または top-k 内にある
  - no = 正しい文書が取得できていない
- generation_ok:
  - yes = 回答が参照文書に忠実で、質問にも正しく答えている
  - no = 間違っている、ずれている、余計な補完がある
- failure_type:
  - no_issue
  - retrieval_fail
  - generation_fail
  - data_missing

---

## 1
- type: paraphrase
- question: 検索で外すと回答はどうなる？
- expected: retrievalが失敗すると、誤った文脈に基づく誤答や、質問に答えられない回答が出やすくなる。
- retrieved_top1: retrievalが失敗すると、誤った文脈に基づく誤答や、質問に答えられない回答が出やすくなる。
- retrieval_ok: yes
- generated_answer: retrievalが失敗すると、誤った文脈に基づく誤答や、質問に答えられない回答が出やすくなる。
- generation_ok: yes
- failure_type: no_issue
- note: 原因系の言い換え質問に自然に対応できている。

## 2
- type: paraphrase
- question: 文脈が足りないと何がまずい？
- expected: 文脈不足だと回答に必要な情報が足りず、LLMが不完全な回答や曖昧な回答をしやすくなる。
- retrieved_top1: 文脈不足だと回答に必要な情報が足りず、LLMが不完全な回答や曖昧な回答をしやすくなるためである。
- retrieval_ok: yes
- generated_answer: 脈が足りないと回答に必要な情報が足りず、LLMが不完全な回答や曖昧な回答をしやすくなるため、回答品質が下がることがまずいです。
- generation_ok: yes
- failure_type: no_issue
- note: 生成文に軽い言い換えはあるが、内容は期待答えに忠実。

## 3
- type: paraphrase
- question: top_kを増やしすぎると、なんで危ないの？
- expected: top_kを増やしすぎるとノイズ文書が増え、LLMが誤った情報に引っ張られやすくなるためである。
- retrieved_top1: top_kを増やしすぎるとノイズ文書が増え、LLMが誤った情報に引っ張られやすくなるためである。
- retrieval_ok: yes
- generated_answer: top_kを増やしすぎるとノイズ文書が増え、LLMが誤った情報に引っ張られやすくなるため危ないです。
- generation_ok: yes
- failure_type: no_issue
- note: Day 5 の学びがデータとして機能している。

## 4
- type: paraphrase
- question: 無理に答えさせない方がいいのはなぜ？
- expected: 分からない場合は分からないと答えさせるのは、retrieval失敗やデータ不足のときに無理に補完して誤答するのを防ぐためである。
- retrieved_top1: 参照文書にない情報を無理に補完させないためであり、誤答を減らすためである。
- retrieval_ok: yes
- generated_answer: 無理に答えさせない方がいいのは、参照文書にない情報を無理に補完させないためであり、誤答を減らすためです。また、retrieval失敗やデータ不足のときに無理に補完して誤答するのを防ぐためでもあります。
- generation_ok: yes
- failure_type: no_issue
- note: retrieved_top1 は期待答えの一部だが、generation が不足分を自然に補っている。

## 5
- type: paraphrase
- question: RAGが変な答えを出すのはどんなとき？
- expected: RAGで間違った答えが出る主な原因は、retrievalの失敗、文脈不足、ノイズ混入、hallucinationなどである。
- retrieved_top1: RAGは検索した文書をもとに回答を生成する手法である。
- retrieval_ok: no
- generated_answer: RAGが変な答えを出すのは、retrievalの失敗、文脈不足、ノイズ混入、hallucinationなどが原因のときです。
- generation_ok: yes
- failure_type: retrieval_fail
- note: top1 はRAGの定義で意図した文書ではないが、生成回答は期待内容に近い。top-k内の別文書参照かモデルの一般化が効いている可能性があり、faithfulness はやや要確認。

## 6
- type: paraphrase
- question: 質問もベクトル化するのは何のため？
- expected: 質問もembeddingするのは、文書ベクトルと同じ空間で意味の近さを比較するためである。
- retrieved_top1: 質問もembeddingするのは、文書ベクトルと同じ空間で意味の近さを比較するためである。
- retrieval_ok: yes
- generated_answer: 質問もベクトル化するのは、文書ベクトルと同じ空間で意味の近さを比較し、意味の近い文書を検索できるようにするためです。
- generation_ok: yes
- failure_type: no_issue
- note: 理由系の paraphrase に安定して対応できている。

## 7
- type: abstract
- question: 同じembeddingモデルを使わないと何が困る？
- expected: 文書と質問を同じembeddingモデルで変換するのは、同じ意味空間で扱うためである。
- retrieved_top1: 文書と質問を同じembeddingモデルで変換するのは、同じ意味空間で扱うためである。
- retrieval_ok: yes
- generated_answer: 参照文書からは分かりません。
- generation_ok: no
- failure_type: generation_fail
- note: retrieval は成功しているが、「何が困るか」という抽象的な聞き方に対して generation が展開できていない。

## 8
- type: abstract
- question: 検索対象が増えたときにFAISSを使う理由は？
- expected: FAISSのようなベクトル検索ライブラリを使うのは、大量の検索対象から近い文書を高速に探すためである。
- retrieved_top1: FAISSのようなベクトル検索ライブラリを使うのは、大量の検索対象から近い文書を高速に探すためである。
- retrieval_ok: yes
- generated_answer: FAISSのようなベクトル検索ライブラリを使うのは、大量の検索対象から近い文書を高速に探すためである。
- generation_ok: yes
- failure_type: no_issue
- note: abstract質問でも安定して正答。

## 9
- type: paraphrase
- question: 言い換えを増やすと検索が良くなるのはなぜ？
- expected: 言い換え表現をデータに追加すると、多様な質問表現に対応しやすくなり、retrievalが改善する。
- retrieved_top1: 言い換え表現をデータに追加すると、多様な質問表現に対応しやすくなり、retrievalが改善する。
- retrieval_ok: yes
- generated_answer: 言い換え表現をデータに追加すると、多様な質問表現に対応しやすくなり、retrievalが改善するためです。
- generation_ok: yes
- failure_type: no_issue
- note: Day 4 の改善経験と整合的な出力。

## 10
- type: abstract
- question: 定義問題でtop_kの差が出にくいのはなぜ？
- expected: 定義系の質問では、正しい文書が上位に来やすく、追加文書の影響が小さいため、top_kの差が出にくい。
- retrieved_top1: 定義系の質問では、正しい文書が上位に来やすく、追加文書の影響が小さいため、top_kの差が出にくい。
- retrieval_ok: yes
- generated_answer: 定義系の質問では、正しい文書が上位に来やすく、追加文書の影響が小さいため、top_kの差が出にくいからです。
- generation_ok: yes
- failure_type: no_issue
- note: Day 5 で観察した傾向をそのまま説明できている。

## 11
- type: abstract
- question: 答えがデータにない質問で、件数を増やすと危ないのはなぜ？
- expected: data missingの質問でtop_k=5が危険なのは、半関連のノイズ文書が増え、もっともらしい誤答を生成しやすくなるためである。
- retrieved_top1: data missingの質問でtop_k=5が危険なのは、半関連のノイズ文書が増え、もっともらしい誤答を生成しやすくなるためである。
- retrieval_ok: yes
- generated_answer: 答えがデータにない質問で件数（top_k）を増やすと危ないのは、半関連のノイズ文書が増え、LLMがそれらの誤った情報に引っ張られてもっともらしい誤答を生成しやすくなるためです。
- generation_ok: yes
- failure_type: no_issue
- note: data missing に関する理解がかなり良い。

## 12
- type: abstract
- question: 検索と生成を分けて見るべきなのはなぜ？
- expected: retrievalとgenerationを分けて評価するのは、どこで失敗しているかを切り分け、改善箇所を特定するためである。
- retrieved_top1: FAISSのようなベクトル検索ライブラリを使うのは、大量の検索対象から近い文書を高速に探すためである。
- retrieval_ok: no
- generated_answer: 検索と生成を分けて見るべきなのは、どこで失敗しているかを切り分け、改善箇所を特定するためである。
- generation_ok: yes
- failure_type: retrieval_fail
- note: top1 はズレているが、生成回答は期待答えに近い。top-k 内の別文書利用か補完の可能性があり、faithfulness はやや注意。

## 13
- type: paraphrase
- question: 一度にいろいろ直すと何が困る？
- expected: 改善は一箇所ずつ行うべきなのは、どの変更が効果を出したのか分からなくなるのを防ぐためである。
- retrieved_top1: 改善は一箇所ずつ行うべきなのは、どの変更が効果を出したのか分からなくなるのを防ぐためである。
- retrieval_ok: yes
- generated_answer: 改善は一箇所ずつ行うべきなのは、どの変更が効果を出したのか分からなくなるのを防ぐためである、ということから、一度にいろいろ直すと、どの変更が効果的だったのか分からなくなり困る。
- generation_ok: yes
- failure_type: no_issue
- note: 評価設計の原則に対応できている。

## 14
- type: implementation
- question: 検索結果をそのままLLMに投げず、まとめ直すのはなぜ？
- expected: build_contextの役割は、検索結果の複数文書をLLMが読める1つのcontext文字列にまとめることである。
- retrieved_top1: FAISSのようなベクトル検索ライブラリを使うのは、大量の検索対象から近い文書を高速に探すためである。
- retrieval_ok: no
- generated_answer: 参照文書からは分かりません。
- generation_ok: no
- failure_type: retrieval_fail
- note: implementation系の抽象化質問では retrieval が弱く、generation も停止した。build_context に関する言い換え追加が必要。

## 15
- type: implementation
- question: scoreを返しておくと何がうれしい？
- expected: scoreも一緒に返しているのは、文書の関連度を確認し、検索精度の確認やデバッグ、順位判断に使うためである。
- retrieved_top1: scoreも一緒に返しているのは、文書の関連度を確認し、検索精度の確認やデバッグ、順位判断に使うためである。
- retrieval_ok: yes
- generated_answer: scoreを返しておくとうれしいのは、文書の関連度を確認でき、検索精度の確認やデバッグ、順位判断に使えるためです。
- generation_ok: yes
- failure_type: no_issue
- note: implementation系でも具体的な役割を問う質問には強い。

---

## Day 6 Findings
### 改善した点
- 原因・理由系Q&Aを追加したことで、定義系だけでなく説明系・言い換え系の質問にもかなり対応できるようになった。
- 特に retrieval失敗、文脈不足、top_k増加の危険性、data missing などの説明に強くなった。
- paraphrase質問に対する retrieval は全体としてかなり改善している。

### まだ弱い点
- abstractな聞き方や implementation寄りの質問では、retrieval がまだ不安定な場合がある。
- 「何が困るか」「なぜまとめ直すのか」のように、少し抽象化された実装質問は弱い。
- 包括的な失敗原因をまとめて問う質問では、top1 が意図した文書からずれることがある。

### retrievalの失敗
- 「RAGが変な答えを出すのはどんなとき？」では top1 がRAGの定義文になっていた。
- 「検索と生成を分けて見るべきなのはなぜ？」では top1 が FAISS の説明になっていた。
- 「検索結果をそのままLLMに投げず、まとめ直すのはなぜ？」でも top1 が build_context ではなく FAISS 側に寄っていた。

### generationの失敗
- 「同じembeddingモデルを使わないと何が困る？」では retrievalは成功していたが、generation が「分かりません」と停止していた。
- implementation系では、retrieval が近くても generation が質問の意図に十分対応できない場合がある。

### data_missing
- 今回の15問では明確な data_missing は少なかったが、包括的で抽象度の高い質問では、データ不足に近い不安定さが見られた。
- 特に build_context の抽象化質問は、現状のデータではカバーが不十分だった。

### 次の改善方針
- implementation系・評価系の言い換え質問をさらに追加する。
- 「何が困るか」「なぜ必要か」など、抽象度の高い問いに対応するQ&Aを増やす。
- retrieval_fail と generation_fail が分かれた質問を重点的に再設計する。