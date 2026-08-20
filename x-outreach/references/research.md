# 调查方法：查清 X 账号主是谁

目标：确定真实姓名（含正确汉字）、当前身份职位、公司与业务、近期关注点、约束与风险。全程约 3~6 次检索调用，不要只靠单一来源下结论。

## 渠道与顺序

**1. 社交媒体垂直搜索（首选，X 官网直接抓会 402/403）**

若环境装有 anysearch skill（或同类支持 X 垂直搜索的工具），用它的 social_media 域。CLI 一般位于 anysearch skill 目录的 `scripts/anysearch_cli.py`，路径不确定时先调用该 skill 获取用法：

```bash
# 第一步：查身份——x_people 用账号 ID 搜。结果里的推文作者栏会带当前显示名/粉丝数/认证状态，
# 提及该账号的推文常包含真名（「〇〇さん(@handle)」句式）
python3 <cli> search "<handle>" --domain social_media --sub_domain social_media.social_media \
  --sdp type=x_people,keyword=<handle>,region= --max_results 5

# 第二步：查近况——x_latest 找最近推文（钩子素材）。注意结果混有旧推，逐条看发帖日期
python3 <cli> search "<真名或handle>" --domain social_media --sub_domain social_media.social_media \
  --sdp type=x_latest,keyword=<handle>,region= --max_results 8

# 需要时：linkedin_people 查职业履历
python3 <cli> search "<真名>" --domain social_media --sub_domain social_media.social_media \
  --sdp "type=linkedin_people,keyword=<真名>,region=" --max_results 5
```

没有垂直搜索工具时，退而求其次：WebSearch `"<handle>" twitter OR x.com`——搜索结果标题常直接带「显示名 (@handle) / X」。

**2. WebSearch 交叉核实**：用「真名 + 会社 OR 代表 OR プロフィール」搜公司官网、note、Wantedly、新闻稿、书籍页。公司官网的会社概要页是职位与实体的最权威来源。

**3. WebFetch 深挖**：note 主页（近期文章=优质钩子）、公司官网会社概要页。X 镜像站（nitter、sotwe 等）大多也被拦，不要浪费太多次尝试。

## 核实清单（缺一不可）

- [ ] **姓名汉字**：账号 ID 的罗马字对应多种姓氏写法（如 saito→斉藤/斎藤/齊藤/齋藤，watanabe→渡辺/渡邊/渡部）。必须找到本人官网/公司页/出版物上的汉字写法。称呼写错一票否决
- [ ] **当前职位**：显示名和 bio 会频繁改；搜到的推文可能是多年前的。以最近 1 年内的信源为准，注意「已离职/已卖掉公司/已调岗」的可能
- [ ] **身份类型**：公务员？上市公司员工？经营者？——直接决定 SKILL.md 第 2 步的约束判定
- [ ] **公司实体**：正式社名、所在地、主营业务（写問題段要贴合业务）
- [ ] **近期关注点**：最近 1~3 个月的推文/文章主题，从中选钩子

## 风险扫描

顺手留意（不用专门深挖，但看到必须报告用户）：

- 争议、指控、炎上历史——报告用户定夺，不要擅自放弃也不要装没看见
- 与竞品的合作或站台关系
- bio/官网明写「営業お断り」

## 常见坑（实战教训）

- x_latest 的结果并不严格按时间排序，且 keyword 命中的多是**提及**该账号的推文而非本人的推文，看清作者栏的 @handle
- 旧推文里的头衔（如「〇〇株式会社代表」）可能已过时，镜像站的存档标题同理
- 公务员运营的项目可能挂着地方政府事业名义，别误判成民间机构——身份类型判错会让整封信的方案违规
