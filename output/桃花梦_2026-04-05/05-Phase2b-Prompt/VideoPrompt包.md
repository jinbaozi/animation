# 桃花梦 — VideoPrompt 包

> 项目：桃花梦 | 日期：2026-04-05 | 版本：v1.0
> 执行角色：AI美术技术总监（Phase 2b）
> 风格：国风动漫 | Seedance 2.0 / 即梦
> 镜头数：10 | 每镜 ≥4s | 分 2 个序列

---

## 序列编排

| 序列 | 涵盖镜头 | 叙事阶段 | 预估总长 |
|------|---------|---------|---------|
| SEQ-A（相遇） | S001-S005 | 初遇→转身→走近 | ~20s |
| SEQ-B（表白） | S006-S010 | 握手→告白→拥抱→留白 | ~20s |

---

## SEQ-A：十里桃林·初遇 (S001-S005)

### S001 [0:00-0:04]

**[主体锚定]** 十里桃林黄昏全景，无人物

**[场景锚定]** 桃花树错落，粉白花瓣密集飘落，地面铺满花瓣地毯，青石板小径蜿蜒，夕阳光束穿林而过

**[首帧参考]** AD image 1 = 桃林全景参考（场景资产卡-全景）

**Prompt 中文：**
```
[0:00-0:04]
  运镜：Wide establishing shot, slow crane pan left
  画面：十里桃林黄昏全景缓慢从左向右横移。数十棵盛开粉色桃花的树木错落分布，无数花瓣密集飘落入雪，地面铺满厚厚粉色花瓣层。夕阳从左后方射入金色光束照亮空气，远处暖橙色调山峦若隐若现。
  光影：暖橙色黄昏光，体积光光束穿林，丁达尔效应
```

**Prompt 英文：**
```
Wide establishing shot, slow crane pan left. Peach blossom grove at dusk, dozens of blooming pink-white peach trees scattered across the landscape. Dense petals falling like snow, thick layer of pink petals covering the ground. Golden sunset light streaming from left-rear through canopy creating volumetric light beams, Tyndall effect illuminating floating petal particles. Distant mountains in warm orange twilight haze. Chinese animation style, 8K, volumetric lighting, warm orange-pink color palette, ethereal atmosphere.

AD image 1 = scene reference (peach grove panorama)
```

---

### S002 [0:00-0:04]

**[主体锚定]** 白浅 — 素白长裙，苍白鹅蛋脸，杏核眼，黑发半束木簪

**[场景锚定]** 桃花树下，黄昏暖光，花瓣飘落

**[首帧参考]** AD image 1 = 白浅正面四视图

**Prompt 中文：**
```
[0:00-0:04]
  运镜：Extreme close-up, slow push-in to face
  主体：白浅，素白丝绸长裙，苍白鹅蛋脸，杏核眼映着花瓣，黑发半束插木簪
  动作：头微微仰起，呼吸平缓，一滴花瓣落在睫毛上，睫毛轻轻颤动
  视线：向上注视飘落的花瓣，杏核眼中映出粉色光影
  光影：侧逆光打亮面部边缘，暖粉色调
```

**Prompt 英文：**
```
Extreme close-up on 白浅's face, slow push-in. 白浅 (AD image 1), oval face, pale porcelain skin, almond-shaped eyes reflecting falling petals, long black hair half-pinned with wooden hairpin, wearing plain white silk dress. Head tilted slightly upward, calm steady breathing, a single peach petal lands on her eyelashes causing eyelashes to flutter delicately. Eyes gazing upward at falling petals, almond eyes catching pink light reflections. Side backlight illuminating facial edge contour. Warm pink-orange rim light on cheek. Chinese animation style, 8K, cinematic lighting, shallow depth of field.

AD image 1 = 白浅 character reference (front-facing 4-view)
```

---

### S003 [0:00-0:04]

**[主体锚定]** 夜华 — 黑金长袍，金色云纹，高束发冠，深邃星目

**[场景锚定]** 桃花树下，花瓣环绕，逆光剪影

**[首帧参考]** AD image 1 = 夜华正面四视图，AD image 2 = 桃林场景

**Prompt 中文：**
```
[0:00-0:04]
  运镜：Medium shot, static, backlight silhouette
  主体：夜华，黑金长袍配金色云纹刺绣，高束发冠，立于桃花树前
  动作：静立，花瓣在周身旋转飘落，微微侧头望向白浅方向
  视线：目光锁定画面右侧（白浅所在方向），眼神深沉专注
  光影：逆光剪影效果，金色边缘光勾勒身形
```

**Prompt 英文：**
```
Medium shot, static, backlight silhouette. 夜华 (AD image 1) stands before a peach blossom tree (AD image 2), wearing black and gold robe with golden cloud embroidery, high hair bun with golden crown. Standing still, petals swirling and falling around his body in a gentle vortex. Head slightly tilted, gazing toward the right side of frame (where 白浅 stands), deep focused eyes, steady and patient expression. Rim backlight creating silhouette with golden edge light outlining his tall frame. Chinese animation style, 8K, dramatic backlight, silhouette with warm golden rim, petals floating in ambient light.

AD image 1 = 夜华 character reference (front-facing 4-view)
AD image 2 = scene reference (peach grove)
```

---

### S004 [0:00-0:04]

**[主体锚定]** 白浅

**[场景锚定]** 同上，黄昏桃林

**[首帧参考]** AD image 1 = 白浅正面四视图

**Prompt 中文：**
```
[0:00-0:04]
  运镜：Single reaction shot, slow follow on turn
  主体：白浅，素白长裙
  动作：身体缓缓转身180度，裙摆随之微微飘动，杏核眼睁大，嘴唇轻启，苍白脸颊泛起微红
  视线：转身前看向画面右侧→转身后直视前方（夜华方向）
  光影：暖光从右侧面打亮面部
```

**Prompt 英文：**
```
Single reaction shot, slow follow on turn. 白浅 (AD image 1) in white silk dress slowly turns 180 degrees, dress hem swaying gently with the movement. Almond-shaped eyes widening slightly, lips parting a fraction, pale cheeks flushing faint pink. Eyes shifting from looking right to directly forward (toward 夜方向), expression of surprise melting into deep emotion. Warm golden light from right side illuminating her face. Peach petals drifting in background. Chinese animation style, 8K, warm pink-gold lighting, soft bloom highlights, shallow depth of field.

AD image 1 = 白浅 character reference
```

---

### S005 [0:00-0:04]

**[主体锚定]** 夜华与白浅

**[场景锚定]** 同上

**[首帧参考]** AD image 1 = 白浅正面四视图，AD image 2 = 夜华正面四视图

**Prompt 中文：**
```
[0:00-0:04]
  运镜：Over-the-shoulder from behind 白浅, slow push-in, rack focus
  主体：夜华（背景）+ 白浅肩部（前景虚化）
  动作：夜华缓步走近，伸手轻轻拂去白浅发间花瓣。手指动作极其轻柔，花瓣从指尖滑落
  视线：夜华目光锁定白浅双眼，瞳孔中有白浅的倒影。白浅回望夜华，目光温柔
  光影：暖光从侧面打在两人脸上
```

**Prompt 英文：**
```
Over-the-shoulder shot from behind 白浅's shoulder (foreground, soft focus). 夜华 (AD image 2, background) stepping slowly closer to foreground, reaching out to gently brush a petal from 白浅's hair. Right hand rising slowly, fingers moving with extreme delicacy, petal slipping off fingertips and fluttering down. 夜华's eyes locked steadily on 白浅's eyes, pupils reflecting her image, eyebrows slightly raised in tenderness. Warm side light illuminating 夜华's face. Soft warm glow on 白浅's shoulder edge. Pale pink peach petals floating between them. Chinese animation style, 8K, cinematic lighting, rack focus from foreground to background, shallow depth of field.

AD image 1 = 白浅 character reference (foreground shoulder)
AD image 2 = 夜华 character reference (background, full body)
```

---

## SEQ-B：十里桃林·表白 (S006-S010)

### S006 [0:00-0:04]

**[主体锚定]** 夜华的手与白浅的手

**[场景锚定]** 黄昏桃林背景虚化

**[首帧参考]** AD image 1 = 白浅手部参考，AD image 2 = 夜华手部参考

**Prompt 中文：**
```
[0:00-0:04]
  运镜：Extreme close-up on hands, slow push-in
  主体：夜华的手覆上白浅的手背，黑金袖口与苍白手指对比
  动作：夜华手指轻轻收紧包裹住白浅的手背，白浅的手指微微颤抖
  视线：不适用（手部特写）
  光影：暖光从上方照亮双手，肤色对比明显
```

**Prompt 英文：**
```
Extreme close-up on hands, slow push-in. 夜华's hand (AD image 2 cuff visible, black gold sleeve) gently covering 白浅's hand back (AD image 1, pale slender fingers). 夜华's fingers slowly tightening around her hand, 白浅's fingers trembling slightly with delicate micro-tremors. Warm light from above illuminating both hands, stark contrast between warm wheat-toned skin and pale porcelain skin. Blurred peach blossom background. Chinese animation style, 8K, cinematic warm lighting, shallow depth of field, detailed skin texture rendering.

AD image 1 = 白浅 character reference
AD image 2 = 夜华 character reference
```

---

### S007 [0:00-0:04]

**[主体锚定]** 夜华胸口与白浅的手

**[场景锚定]** 黄昏桃林

**[首帧参考]** AD image 1 = 夜华正面四视图，AD image 2 = 白浅正面四视图

**Prompt 中文：**
```
[0:00-0:04]
  运镜：Close-up on chest, slow push-in
  主体：夜华，白浅的手按在黑金衣料胸口上
  动作：白浅的手被轻轻按在夜华心口，夜华另一只手覆在她手背上。夜华胸口衣料随心跳微微起伏
  视线：白浅低头看手上的心跳→缓缓抬眼望向夜华双眼
  光影：暖光从右下方照亮胸口区域
```

**Prompt 英文：**
```
Close-up on chest, slow push-in. 白浅's hand (AD image 2, pale and delicate) pressed against 夜华's chest (AD image 1, black gold robe fabric). 夜华's other hand covering hers from above, fingers gently resting on her knuckles. Black fabric of his robe rising and falling subtly with heartbeat rhythm. 白浅's eyes looking down at his hand and chest, then slowly lifting to meet 夜华's eyes, almond eyes softening with emotion. Warm light from lower right illuminating their hands on his chest. Chinese animation style, 8K, cinematic lighting, warm golden tones, shallow depth of field.

AD image 1 = 夜华 character reference
AD image 2 = 白浅 character reference
```

---

### S008 [0:00-0:04]

**[主体锚定]** 白浅面部

**[场景锚定]** 黄昏桃林

**[首帧参考]** AD image 1 = 白浅面部特写

**Prompt 中文：**
```
[0:00-0:04]
  运镜：Close-up, slow push-in from low angle
  主体：白浅，素白长裙上缘可见
  动作：睫毛上噙着泪珠，杏核眼中反射暖光，嘴唇微微抿起浮出浅笑，下巴微微抬起
  视线：直视画面右侧上方（夜华双眼方向），目光温柔而坚定
  光影：暖光从右下方打亮面部，眼眶中泪珠反光闪烁
```

**Prompt 英文：**
```
Close-up, slow push-in from low angle. 白浅's face (AD image 1), oval face, pale skin, almond-shaped eyes with a single tear shimmering on lower eyelash catching warm light reflections. Lips pressed together forming a faint smile, chin tilting slightly upward. Eyes gazing directly upward-right (toward 夜华's face direction), warm and steady expression, emotion visible through micro-trembling of the lips and slight widening of the eyes. Warm golden light from lower right illuminating her face, tear drop catching light. Soft peach-pink background blur. Chinese animation style, 8K, cinematic warm lighting, shallow depth of field, detailed emotional rendering.

AD image 1 = 白浅 character reference (face close-up)
```

---

### S009 [0:00-0:04]

**[主体锚定]** 夜华与白浅相拥

**[场景锚定]** 黄昏桃林，花瓣密集飘落

**[首帧参考]** AD image 1 = 夜华正面四视图，AD image 2 = 白浅正面四视图

**Prompt 中文：**
```
[0:00-0:04]
  运镜：Medium shot, slow 180-degree orbit, then pull-back
  主体：夜华与白浅紧紧相拥，夜华手臂环住白浅腰部，白浅手臂环住夜华腰部
  动作：白浅闭眼靠在夜华胸口，表情安宁。夜华下巴轻抵白浅头顶。密集花瓣如雪般从天空飘落
  视线：白浅闭眼，夜华目光越过白浅头顶望向远处
  光影：柔和暮光从后方照射，金色轮廓光勾勒两人边缘
```

**Prompt 英文：**
```
Medium shot, slow 180-degree orbit around the couple, then gentle pull-back. 夜华 (AD image 1) embracing 白浅 (AD image 2) tightly. 夜华's arms wrapped securely around 白浅's waist, 白浅's arms encircling his torso. White's eyes closed in peaceful contentment, face resting against his chest in black gold fabric. 夜华's chin gently resting on top of her head, eyes looking past her toward the distant horizon over her shoulder. Dense peach petals falling like heavy snow around them. Soft twilight backlight creating golden rim light around both figures. Chinese animation style, 8K, cinematic golden-hour lighting, volumetric atmosphere, romantic warm tones, shallow depth of field.

AD image 1 = 夜华 character reference
AD image 2 = 白浅 character reference
```

---

### S010 [0:00-0:04]

**[主体锚定]** 十里桃林远景，两人在花海中化为小点

**[场景锚定]** 黄昏渐变为暮色深蓝

**[首帧参考]** AD image 1 = 桃林全景

**Prompt 中文：**
```
[0:00-0:04]
  运镜：Wide shot, slow pull-back with crane up
  画面：十里桃林全景，相拥的两人身影在地面花瓣海中越来越小。暮光从暖橙渐变为深蓝，无数花瓣继续飘落。画面缓慢升空，桃林全貌显现
  视线：不适用（远景空镜）
  光影：天空从暖橙→深蓝渐变，余晖最后的金光
```

**Prompt 英文：**
```
Wide establishing shot, slow pull-back with crane upward movement. Peach blossom grove panorama at transitioning twilight. Two embracing figures becoming smaller and smaller dots amid pink petal sea on the ground. Sky color transitioning from warm orange to deep blue twilight, final golden afterglow rays catching the tops of peach tree canopies. Thousands of petals continuing to fall in slow motion. Scene slowly ascending to reveal full grove layout. Chinese animation style, 8K, cinematic lighting, color gradient from warm orange to deep blue, volumetric atmosphere, ethereal and eternal mood.

AD image 1 = scene reference (peach grove panorama)
```

---

## 负面提示词（统一，所有镜头添加）

```
deformed hands, extra fingers, extra limbs, bad anatomy, distorted face, mutated, disfigured,
blurry, watermark, text overlay, logo, signature, inconsistent clothing, morphing features,
floating objects without source, multiple views, 2koma, 4koma, 古风写实, 影视质感, 电影级
```

---

## 版本历史

| 版本 | 日期 | 修改内容 |
|------|------|---------|
| v1.0 | 2026-04-05 | Phase 2b 首次执行，按 v2.0 新规则（≥4s/镜，AD Reference，四要素） |
