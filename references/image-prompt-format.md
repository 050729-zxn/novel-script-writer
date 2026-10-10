# 文生图提示词(封面 / 人物立绘 / 场景插图)

把小说里的人物、场景、封面需求,转成绘图 AI 能**无歧义读懂**的提示词。核心理念与视频镜头提示词一致:**提示词是给 AI 的指令,不是文学描写**——每块写清、名词具体、单一主体,AI 才能一次生成对。

## 一、AI 完全理解的三条铁律

1. **分层写、顺序固定**:主体 → 特征 → 动作/表情 → 环境 → 光线/氛围 → 镜头/构图 → 风格/媒介 → 画质。每层一个逗号短语,别把不同层搅在一起。
2. **具体名词替代抽象形容词**:「悲伤」写「眼角带泪、嘴角下压」;「绝美」写「银白长发、琥珀色眼睛、下颌线条利落」。AI 认具体名词,不认「意境」「气质」。
3. **一条提示词 = 一个主体 + 一个清晰动作**:多人、多动作就拆成多张图;别塞「她既在笑又在哭」这类矛盾指令。

## 二、通用分层模板

```
[主体] 谁 + 年龄/身份/种族
[特征] 外貌、发型、服装饰品(具体颜色/材质)
[动作/表情] 正在做什么、什么表情、朝向
[环境] 地点、时间、天气、前后景
[光线/氛围] 光的方向、色温、氛围词
[镜头/构图] 特写/半身/全身、角度、景深
[风格/媒介] 写实/国风水墨/赛博朋克/油画/厚涂…
[画质] 高清、细节、质量词(工具相关)
```

## 三、主流工具适配

| 工具 | 语言 | 格式 | 关键参数 |
|---|---|---|---|
| 即梦 / Seedream(字节) | 中文 | 自然语言逗号分隔 | 比例、风格词、画质词 |
| 可灵 / Kling(快手) | 中文 | 自然语言逗号分隔 | 风格词 |
| Midjourney | 英文 | 自然语言逗号堆叠 | `--ar 3:4` 画幅、`--style raw` 少美化、`--no` 排除、`--v 6` |
| Stable Diffusion / ComfyUI | 英文 | 正面 tag + 负面 tag 分离 | 权重 `(词:1.2)`、LoRA 触发词必带、负面词 |

### Stable Diffusion 通用负面词(直接套)

```
(worst quality, low quality:1.4), (bad anatomy, bad hands, extra fingers, mutated hands:1.2),
(deformed, disfigured:1.3), blurry, cropped, out of frame, lowres, text, watermark, signature, jpeg artifacts
```

## 四、从小说内容生成的工作流

1. **先问清缺项**:画什么(人物立绘 / 场景概念图 / 封面)、主体是谁、什么画风、用途尺寸(竖版封面 3:4 / 横版 16:9 / 方图 1:1)。
2. **从正文/设定提炼具体特征**:外貌、服饰、气质线索,把抽象情绪转成可见细节。
3. **写一条中文底稿**:按分层模板逐层填。
4. **按目标工具转写**:即梦/可灵直接用中文;Midjourney 翻英文+参数;SD 拆正面/负面 tag。
5. **交付**:给「中文通用版 + 目标工具成品提示词(含参数/负面词)」,方便直接复制。

## 五、完整示例对照

同一个「雪夜红衣女剑客拔剑回头」,四版:

**中文通用版**

> 二十岁女剑客,黑色长发高束,红衣黑披风,半回身拔剑出鞘三寸,眼神戒备;雪夜古街客栈门前,红色灯笼;暖光从左侧打来,雪地反光;半身、微仰视、浅景深;国风水墨厚涂写实;高清细节。

**即梦 / 可灵(中文,直接可用)**

> 一位二十岁的红衣女剑客,黑色高马尾,红衣黑披风,手按剑柄拔剑出鞘,半侧身,眼神警惕,雪夜古街,客栈门前红灯笼,暖光从左侧照来,雪地反光,半身构图,微仰视角,浅景深,国风水墨写实厚涂,高清细节,比例 3:4

**Midjourney(英文)**

> a young female swordswoman in her twenties, high black ponytail, red hanfu with black cloak, hand drawing a sword three inches from its scabbard, half-turned body, wary gaze, snowy night old street, inn doorway with warm red lanterns, warm lantern light from the left, snow reflecting light, waist-up shot, slight low angle, shallow depth of field, Chinese ink-wash realism, thick paint style, highly detailed --ar 3:4 --style raw --v 6

**Stable Diffusion(正面 + 负面)**

正面:

> (masterpiece, best quality, highly detailed:1.2), 1girl, 20 years old, black high ponytail, red hanfu, black cloak, drawing sword, half-turned body, wary eyes, snowy night, old street, inn, red lantern, warm light from left, snow reflection, waist-up, low angle, shallow depth of field, chinese ink painting style, thick paint

负面:

> (worst quality, low quality:1.4), (bad anatomy, bad hands, extra fingers:1.2), (deformed, disfigured:1.3), blurry, cropped, out of frame, lowres, text, watermark, signature, jpeg artifacts
