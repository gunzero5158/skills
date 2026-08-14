# 好/坏推文对比范例

品牌均为架空（BridgeAPI），用于锚定「克制」与「推销味」的分界线。起草前通读一遍，写完自查时对照。

## 对比 1：独立发帖——先讲问题 vs 开头报菜名

**❌ 坏（推销味）：**

```
🚀BridgeAPIなら主要AIモデルが1つのAPIキーで使える！円建て請求書払い対応！今なら公式価格から5%OFF〜！詳しくはこちら→ https://bridgeapi.example.com #BridgeAPI #AI #LLM #お得 #キャンペーン #API #生成AI
```

问题：开头就是品牌名+感叹号轰炸；全是卖点没有洞察；「今なら」制造虚假紧迫感；hashtag 堆砌到 7 个且混入 #お得 这种垃圾 tag。

**✅ 好（有用+克制）：**

```
複数のLLMを検証していると、意外と時間を食うのがモデルの性能比較ではなく、各社のAPIキー管理と請求書の突き合わせだったりします。検証を始める前に「請求をどう一本化するか」を決めておくと、後がだいぶ楽になります。BridgeAPIはその一本化の選択肢の一つです。

Hashtags: #BridgeAPI #LLM #生成AI
```

好在哪：先给一个从业者会点头的真实观察；品牌只在结尾以「选择之一」的姿态出现；观点本身独立成立，就算删掉最后一句也是条好推文。

## 对比 2：回帖——蹭流量 vs 有增量

场景：对方发帖抱怨「AIのAPI料金、モデルごとに請求書がバラバラで経理に怒られた」。

**❌ 坏：**

```
その悩み、BridgeAPIが解決します！1つのAPIキーで主要モデルが使えて請求も一本化。ぜひお試しください→ https://bridgeapi.example.com
```

问题：把别人的抱怨当广告位，公开处刑级别的回复；带链接的陌生回帖几乎必被反感。

**✅ 好：**

```
わかります。うちも最初は経理側でモデル別にコストコードを切って管理していました。件数が増えるとゲートウェイ型のサービスで請求を束ねる方が現実的になってきますね。
```

好在哪：先共情+分享自己的真实做法；只提「ゲートウェイ型」这个品类而不报品牌名、不留链接；对方有兴趣自然会点进主页——回帖的目的是建立存在感，不是当场成交。

## 对比 3：多语言——机翻 vs 本地化

日文原帖讲「請求書の突き合わせ」的痛点（见对比 1 好例）。

**❌ 坏（逐句机翻）：**

```
When verifying multiple LLMs, what unexpectedly eats time is not model performance comparison but each company's API key management and invoice matching...
```

问题：日文的「経理に怒られる」语境直译后在英文圈没有共鸣点，句式也是日式英语。

**✅ 好（同一意图，独立成文）：**

```
The hidden cost of a multi-LLM stack isn't the per-token pricing — it's juggling five API keys and reconciling five invoices at month-end. Decide how you'll consolidate billing before the eval starts, not after. That's half of why we built BridgeAPI.

Hashtags: #BridgeAPI #LLMOps #AIInfrastructure
```

好在哪：换成英文圈熟悉的「hidden cost」「month-end reconciliation」表达；hashtag 也换成英文生态的（#LLMOps 而不是硬译日文 tag）。
