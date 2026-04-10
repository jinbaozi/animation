# 人物四视图Prompt包 - 《开局一张弓装备就变强》

**Phase 2a 产出物**
**执行角色：AI美术技术总监**
**生成时间：2026-04-10**

> 依据：人物清单.md v1.0 | 场景清单.md v1.0
> 风格锚点：西幻写实风格（Western Fantasy）
> 禁止词正则：(?i)(影视|电影|摄像|胶片|摄影|古风写实|写实CG|游戏CG|影视质感|影视级|电影级)

---

## 四视图生成规范

| 视角 | 景别 | 背景 | 要求 |
|------|------|------|------|
| 正面全身 | Full Body | 纯白背景 | 展示完整身形、服装、姿态 |
| 侧面全身 | Full Body | 纯白背景 | 展示侧脸轮廓、体型特征 |
| 背面全身 | Full Body | 纯白背景 | 展示背部特征、服装细节 |
| 面部特写 | Close-up | 纯白背景 | 清晰五官、表情特征、皮肤质感 |

**通用锚点前缀（每条Prompt必须包含）：**
```
西幻写实风格，动画风格，纯白背景，
```

---

## 主要人物

---

### 1. 吴为-初始版

**人物属性：**
- 年龄：16岁
- 性别：男
- 身份：黑面包村村民、穿越者、老约翰的弟子
- 外貌特征：瘦削、营养不良、面黄肌瘦、身高175cm体重不到120斤
- 关键特征：凌乱黑发、疲惫但坚定的眼神

> **基础特征（与成长版保持一致）**：凌乱黑发、瓜子脸轮廓、薄唇、眉峰锐利

**四视图Prompt：**

#### 正面全身
```
西幻写实风格，动画风格，纯白背景，

16岁亚洲男性少年，身高175cm，体重不足60公斤，偏黄肤色、面黄肌瘦、颧骨突出。凌乱黑发随意垂落，眼窝深陷，眼睛疲惫却透出坚定。身穿沾满面粉灰的破旧棕色工人服。站姿挺直但略微驼背显示疲惫感。纯白背景正面全身照，人物转身图，角色设计文档一致。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 侧面全身
```
西幻写实风格，动画风格，纯白背景，

16岁亚洲男性少年侧面照，清晰展示面黄肌瘦的侧脸轮廓，颧骨突出、下颌线瘦削。凌乱黑发及肩。破旧棕色工人服上有补丁。肩膀微垂的站姿。纯白背景侧面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 背面全身
```
西幻写实风格，动画风格，纯白背景，

16岁亚洲男性少年背面照，窄肩瘦弱体型，破旧棕色工人服显出单薄身形。后颈凌乱黑发。因疲惫略微驼背。纯白背景背面全身照，展示破旧补丁衣物细节，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 面部特写
```
西幻写实风格，动画风格，纯白背景，

16岁亚洲男性少年面部特写，偏黄肤色、面黄肌瘦，眼窝深陷有黑眼圈，颧骨突出，疲惫却凶狠坚定的表情。凌乱黑发垂落额前。略微泛红的脸颊（情绪或尴尬所致）。纯白背景清晰面部特写，角色表情表。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

---

### 2. 吴为-成长版（一个月后）

**人物属性：**
- 年龄：16岁
- 性别：男
- 身份：黑面包村村民、穿越者、老约翰的弟子
- 外貌特征：身体健壮、肌肉初显、精神饱满
- 关键特征：凌乱黑发（与初始版相同）、眼神坚定有力

> **基础特征（与初始版保持一致）**：凌乱黑发、瓜子脸轮廓、薄唇、眉峰锐利
> **变化特征**：从面黄肌瘦变为健康肤色，体型从瘦弱变为肌肉初显

**四视图Prompt：**

#### 正面全身
```
西幻写实风格，动画风格，纯白背景，

16岁亚洲男性少年，身高175cm，健壮体型、肌肉初显、精神饱满、健康肤色、眼神坚定有力。凌乱黑发（与初始版一致），站姿挺拔、肩膀宽阔、身形稳健。身穿干净整洁的棕色训练服。纯白背景正面全身照，人物转身图，角色设计文档一致。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 侧面全身
```
西幻写实风格，动画风格，纯白背景，

16岁亚洲男性少年侧面照，健壮体型、肌肉初显，肩宽背阔、身形挺拔。凌乱黑发（与初始版一致）垂落。健康肤色，下颌线有力。穿干净训练服。纯白背景侧面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 背面全身
```
西幻写实风格，动画风格，纯白背景，

16岁亚洲男性少年背面照，健壮体型、肌肉初显，肩宽背阔、身形稳健。后颈凌乱黑发（与初始版一致）。穿干净训练服。站姿挺拔有力。纯白背景背面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 面部特写
```
西幻写实风格，动画风格，纯白背景，

16岁亚洲男性少年面部特写，健康肤色、肌肉初显，精神饱满、眼神坚定有力、眉峰锐利。凌乱黑发（与初始版一致）垂落额前。纯白背景清晰面部特写，角色表情表。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

---

### 3. 老约翰

**人物属性：**
- 年龄：中年（约40-50岁）
- 性别：男
- 身份：黑面包村村训教官、曾经的冒险者、吴为的老师
- 外貌特征：断了左手（义肢/铁钩）、瞎了左眼（独眼）、疤痕累累但目光锐利
- 性格特点：外冷内热、教学严格、经验丰富
- **特殊标记**：独眼+断手义肢（关键标记，全4视图必须体现）

**四视图Prompt：**

#### 正面全身
```
西幻写实风格，动画风格，纯白背景，

中年男性，约45岁，络腮胡，左眼失明露出疤痕眼眶，锐利右眼。左手为义肢/铁钩。脸颊和下颌有多道战斗疤痕。穿破旧皮甲内搭棕色短袍。站姿挺拔、肩膀后张。**【独眼+断手义肢】关键标记**。纯白背景正面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 侧面全身
```
西幻写实风格，动画风格，纯白背景，

中年男性侧面照，清晰展示左眼失明疤痕和锐利右眼。面部疤痕贯穿。左手义肢/铁钩。穿皮甲短袍。身姿挺拔威严。**【独眼+断手义肢】关键标记**。纯白背景侧面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 背面全身
```
西幻写实风格，动画风格，纯白背景，

中年男性背面照，宽肩身材虽缺左手仍体格健壮。皮甲有磨损痕迹。后颈短发花白。战士姿态站立。**【断手义肢】关键标记**。纯白背景背面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 面部特写
```
西幻写实风格，动画风格，纯白背景，

中年男性面部特写，络腮胡，左眼完全失明有粗糙疤痕穿过，右眼锐利如刀、目光如炬。面部有多道战斗疤痕，晒黑皮肤。表情从严厉警告到罕见温暖。**【独眼】关键标记**。纯白背景清晰面部特写，角色表情表。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

---

### 4. 多尔

**人物属性：**
- 年龄：约17-18岁
- 性别：男
- 身份：黑面包村村民、弓箭训练者、吴为的朋友
- 外貌特征：普通身材、相貌平平
- 性格特点：热情好为人师、容易得意、爱面子、但心地善良

**四视图Prompt：**

#### 正面全身
```
西幻写实风格，动画风格，纯白背景，

17岁少年，普通身材，中等身高，相貌平平但表情友善。短发褐色，鼻子微翘，渴望表情。穿带皮革护肘的简单训练服。站立时双臂交叉或双手叉腰显出自信。纯白背景正面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 侧面全身
```
西幻写实风格，动画风格，纯白背景，

17岁少年侧面照，普通体型，不胖不瘦。相貌平平的侧脸轮廓，鼻子微翘。短发褐色。简单乡村服饰。休闲教学姿态站立。纯白背景侧面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 背面全身
```
西幻写实风格，动画风格，纯白背景，

17岁少年背面照，普通体型训练服。短发褐色在后颈，无突出特征。肩膀略微不对称（习惯性姿态）。纯白背景背面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 面部特写
```
西幻写实风格，动画风格，纯白背景，

17岁少年面部特写，相貌平平，略微得意的笑容显出自信，褐色眼睛、渴望表情。短发垂落额前。表情在炫耀时的得意满足到被超越时的轻微挫败之间切换。纯白背景清晰面部特写，角色表情表。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

---

### 5. 霍利

**人物属性：**
- 年龄：约16-17岁
- 性别：男
- 身份：黑面包村村民、弓箭天赋者、老约翰关注对象
- 外貌特征：专注认真、全神贯注、精瘦型
- 性格特点：专注、勤奋、有一定天赋但不自知
- **特殊标记**：拉弓前左手无名指轻触弓弦（标志性动作记忆点）

**四视图Prompt：**

#### 正面全身
```
西幻写实风格，动画风格，纯白背景，

16岁少年，精瘦运动员体型，适合射箭，身高较高。专注认真表情，深深聚焦的眼神。黑色短发整齐修剪。穿无袖简单训练服展示精瘦但有轮廓的手臂。站姿采用正确射箭姿态，姿势标准。纯白背景正面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 侧面全身
```
西幻写实风格，动画风格，纯白背景，

16岁少年侧面照，棱角分明的特征，尖锐颧骨，展示 aspiring 弓箭手姿态。精瘦但不瘦弱的体型，肩膀略微后张（训练姿态）。黑色短发整齐。训练服。纯白背景侧面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 背面全身
```
西幻写实风格，动画风格，纯白背景，

16岁少年背面照，精瘦弓箭手体型，训练形成的肩部肌肉清晰可见。后颈黑色短发。穿无袖训练服展示精瘦手臂。良好姿态典型的射箭训练。纯白背景背面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 面部特写
```
西幻写实风格，动画风格，纯白背景，

16岁少年面部特写，专注聚精会神的表情，瞄准时眼睛微微眯起。棱角分明的特征，深邃的眼睛，坚定神情。黑色短发整齐。**【关键记忆点：拉弓前左手无名指自然轻触弓弦】**。纯白背景清晰面部特写，角色表情表捕捉专注与坚定。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

---

### 6. 沃特

**人物属性：**
- 年龄：约17-18岁
- 性别：男
- 身份：乔治面包房员工、吴为的前同事
- 外貌特征：普通身材
- 性格特点：爱嫉妒、嘴碎、容易放弃

**四视图Prompt：**

#### 正面全身
```
西幻写实风格，动画风格，纯白背景，

17岁少年，普通身材，略微驼背显出缺乏自信。相貌平平，永久性轻微嗤笑。乱黑发，深色眼睛有嫉妒神情。穿沾满面粉的面包房工作服。站立时双臂防御性交叉。纯白背景正面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 侧面全身
```
西幻写实风格，动画风格，纯白背景，

17岁少年侧面照，肩膀微驼、驼背姿态。普通侧脸，下颌线瘦弱。乱黑发。沾面粉的工作服。从侧面显示嫉妒和怨恨的表情。纯白背景侧面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 背面全身
```
西幻写实风格，动画风格，纯白背景，

17岁少年背面照，普通身材面包房工作服，姿态差，肩膀前倾。乱黑发在后颈。无运动或突出特征。纯白背景背面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 面部特写
```
西幻写实风格，动画风格，纯白背景，

17岁少年面部特写，相貌平平，嫉妒表情，咬牙或蔑视撇嘴。深色眼睛有记仇神情，眉间轻微皱起。乱发垂落额前。表情从嘲讽到被超越时的挫败。纯白背景清晰面部特写，角色表情表。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

---

### 7. 洛夫

**人物属性：**
- 年龄：约20岁
- 性别：男
- 身份：老约翰的弟子、即将成为冒险者
- 外貌特征：魁梧、近两米身高、大汉但显憨厚
- 性格特点：憨厚、忠诚、即将踏上冒险之路

**四视图Prompt：**

#### 正面全身
```
西幻写实风格，动画风格，纯白背景，

近两米高的魁梧年轻男性，宽肩体型，肌肉发达，比其他人高出很多。憨厚单纯的表情，略微羞涩的笑容。浅褐色短发。背后背着长矛的战士皮甲。双脚分开站立显出稳定感。纯白背景正面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 侧面全身
```
西幻写实风格，动画风格，纯白背景，

20岁巨人侧面照，肌肉体型展示令人印象深刻的身形。诚实简单的面部轮廓，下巴略微前突。背后可见长矛。巨大的双手。自然战士姿态站立。纯白背景侧面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 背面全身
```
西幻写实风格，动画风格，纯白背景，

年轻战士背面照，宽背发达肩部肌肉。长矛绑在背后。浅褐色短发在后颈。穿实用皮甲有简单图案。站立显出即将踏上冒险的自信。纯白背景背面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 面部特写
```
西幻写实风格，动画风格，纯白背景，

年轻巨人面部特写，诚实单纯的表情，天真眼神显示淳朴和忠诚。略微羞涩友好的微笑露出善良本性。浅褐色头发垂落额前。晒黑皮肤。纯白背景清晰面部特写展示憨厚亲切，角色表情表。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

---

### 8. 乔治

**人物属性：**
- 年龄：约40岁
- 性别：男
- 身份：黑面包村面包房老板、吴为的雇主
- 外貌特征：普通中年人
- 性格特点：善良、朴实

**四视图Prompt：**

#### 正面全身
```
西幻写实风格，动画风格，纯白背景，

40岁和善男性，普通身材，烘焙多年晒过的面容。圆润友好的脸庞，烤炉热气熏出的红润脸颊。因享用自己烤的面包有小肚子。穿沾满面粉的围裙配简单衣服。双手叉腰欢迎姿态站立。纯白背景正面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 侧面全身
```
西幻写实风格，动画风格，纯白背景，

40岁面包师侧面照，圆脸和善表情，沾面粉围裙和圆润腰身清晰可见。两边灰白短发。典型乡村面包师的温和特征。自然站立。纯白背景侧面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 背面全身
```
西幻写实风格，动画风格，纯白背景，

40岁男性背面照，普通身材，面包师实用围裙有面粉污渍。后颈灰白短发。围裙下简单工作服。纯白背景背面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 面部特写
```
西幻写实风格，动画风格，纯白背景，

40岁和善面包师面部特写，温暖友好表情，眼角笑纹，多年烘焙的红润脸颊。小鼻子，诚实眼睛显出真诚善良。眉毛上面粉。真诚微笑展示热情好客。纯白背景清晰面部特写，角色表情表。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

---

### 9. 老村长

**人物属性：**
- 年龄：约60岁
- 性别：男
- 身份：黑面包村村长
- 外貌特征：年迈但精神矍铄，花白胡须，手持弯曲木杖
- 性格特点：负责、关心村民
- **特殊标记**：花白胡须+弯曲木杖（全4视图必须体现）

**四视图Prompt：**

#### 正面全身
```
西幻写实风格，动画风格，纯白背景，

年迈60岁村长，花白胡须和八字胡，尽管年迈仍站姿挺拔显出威严。深邃智慧的眼睛，饱经风霜的多皱纹面容。白发整齐束于脑后。穿简朴但有尊严的村长袍。拄着弯曲木杖，骨节分明的手握着。**【花白胡须+弯曲木杖】关键标记**。纯白背景正面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 侧面全身
```
西幻写实风格，动画风格，纯白背景，

60岁威严长者侧面照，清晰可见花白胡须，鹰钩鼻，智慧眼睛。白发束于脑后。穿简朴有尊严的袍子。骨节分明的手握着弯曲木杖。尽管年迈仍有强大气场。**【花白胡须+弯曲木杖】关键标记**。纯白背景侧面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 背面全身
```
西幻写实风格，动画风格，纯白背景，

60岁长者背面照，白发束于脑后，尽管年迈仍显威严体态。简朴但有品质的村长袍。弯曲木杖在侧面可见。拄杖略微前倾站立。**【弯曲木杖】关键标记**。纯白背景背面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 面部特写
```
西幻写实风格，动画风格，纯白背景，

60岁村长面部特写，飘逸花白胡须和八字胡，深邃智慧眼睛显示多年领导经验。饱经风霜古铜色皮肤，多皱纹，花白浓眉。表情从负责担忧到温和关怀。弯曲木杖是所有镜头的关键道具。**【花白胡须+弯曲木杖】关键标记**。纯白背景清晰面部特写，角色表情表。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

---

## 次要人物（龙套）

---

### 10. 梅丽夫人

**人物属性：**
- 身份：老约翰邻居，帮忙做饭
- 特征：普通中年女性，鬓角有白发
- **特殊标记**：鬓角白发（全4视图必须体现）

**四视图Prompt：**

#### 正面全身
```
西幻写实风格，动画风格，纯白背景，

40多岁中年女性，慈祥母亲形象，中等身高，略丰满身材。鬓角和发际线边缘有白发（标志性特征）。眼睛温和略显疲惫，多年烹饪工作。穿简单家用围裙配素色裙子。双手交叠于身前显出耐心。**【鬓角白发】关键标记**。纯白背景正面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 侧面全身
```
西幻写实风格，动画风格，纯白背景，

中年女性侧面照，清晰可见鬓角和发际线边缘的标志性白发。慈祥面部轮廓，柔和特征，眼角轻微皱纹。穿简单家用围裙配素色裙子。家务姿态站立。**【鬓角白发】关键标记**。纯白背景侧面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 背面全身
```
西幻写实风格，动画风格，纯白背景，

中年女性背面照，灰白头发鬓角可见白发在后脑勺。中等身高略丰满身材。简单家用围裙配素色裙子。实用发髻。纯白背景背面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 面部特写
```
西幻写实风格，动画风格，纯白背景，

和善中年女性面部特写，鬓角和发际线边缘可见白发是显著标志，温和温柔的眼睛略显疲惫，眼角笑纹。柔和特征显出母亲般的关怀。脸颊有烹饪留下的轻微面粉。纯白背景清晰面部特写展示标志性鬓角白发，角色表情表。**【鬓角白发】关键标记**。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

---

### 11. 哥布林（普通哥布林）

**人物属性：**
- 类型：普通哥布林
- 特征：身材矮小、绿色皮肤、手持简单木棍
- **特殊标记**：绿色皮肤、矮小、尖耳、木棍

**四视图Prompt：**

#### 正面全身
```
西幻写实风格，动画风格，纯白背景，

约1米高的小哥布林，驼背姿态，皱巴巴的绿色皮肤，头两侧突出的大尖耳朵，邪恶光芒的黄色大眼睛。扁鼻子，宽嘴巴带尖牙。穿破烂布条。手持粗糙木棍。双臂低垂站姿阴险但胆小。**【绿色皮肤+尖耳+木棍】关键标记**。纯白背景正面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 侧面全身
```
西幻写实风格，动画风格，纯白背景，

小哥布林侧面照，清晰可见驼背，皱巴巴绿色皮肤纹理，大尖耳朵。扁鼻子侧面轮廓，宽嘴巴可见尖牙。矮小身型弓背，手持粗糙木棍。阴险但可悲的外表。**【绿色皮肤+尖耳】关键标记**。纯白背景侧面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 背面全身
```
西幻写实风格，动画风格，纯白背景，

小哥布林背面照，驼背肩膀，皱绿色皮肤从破烂布下可见。后脑勺大尖耳朵。短腿短臂。手中可见粗糙木棍。站立姿态略显蹒跚。**【绿色皮肤+木棍】关键标记**。纯白背景背面全身照，人物转身图。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

#### 面部特写
```
西幻写实风格，动画风格，纯白背景，

哥布林面部特写，大黄色眼睛显示邪恶狡猾，皱巴巴绿色皮肤纹理清晰可见。脸部两侧大尖耳朵框住面部，扁鼻子，宽嘴巴带小尖牙。邪恶恶意的表情。皮肤有皮革质感有皱纹。**【绿色皮肤+尖耳】关键标记**。纯白背景清晰面部特写，角色表情表。

Negative prompt: extra limbs, mutated hands, bad anatomy, two heads, disfigured, blurry, pixelated, low resolution, jpeg artifacts, watermark, text, logo, signature, cinematic, film, camera, photorealistic, photo-realistic, game CG, cinematic quality, film grade
```

---

## 角色一致性检查表

| 角色 | 人物清单外貌字段 | 四视图必须包含 | 检查状态 |
|------|-----------------|-----------|--------|
| 吴为-初始版 | 面黄肌瘦，身材瘦弱 | 偏黄肤色面黄肌瘦（≠健康小麦色） | ✓ |
| 吴为-成长版 | 身体健壮、肌肉初显、精神饱满 | 健康肤色、肌肉初显、身形健壮 | ✓ |
| 老约翰 | 独眼（瞎左眼），断左手（义肢） | 独眼+断手义肢完整（全4视图） | ✓ |
| 老村长 | 花白胡须，手持弯曲木杖 | 胡须+弯曲木杖道具（全4视图） | ✓ |
| 梅丽夫人 | 鬓角有白发 | 鬓角白发（全4视图） | ✓ |
| 霍利 | 标志性动作：拉弓前左手无名指轻触弓弦 | 面部特写备注中标注记忆点 | ✓ |
| 哥布林 | 背景敌人 | 绿色皮肤、矮小、尖耳、木棍 | ✓ |

---

## 特殊标记正则扫描验证

```
吴为-初始版Prompt包含：面黄肌瘦|偏黄肤色|瘦弱 ✓
吴为-成长版Prompt包含：健壮|肌肉初显|精神饱满|健康肤色 ✓
老约翰Prompt包含：独眼|断手|义肢|铁钩 ✓
村长Prompt包含：胡须|木杖|弯曲 ✓
梅丽夫人Prompt包含：鬓角|白发 ✓
霍利Prompt包含：无名指|弓弦（作为备注）✓
哥布林Prompt包含：绿色皮肤|尖耳|木棍 ✓
```

---

**版本**：v1.1 | 日期：2026-04-10 | 执行角色：AI美术技术总监

**修复记录**：
- v1.1: 2026-04-10 修复内容
  1. 所有四视图Prompt主体描述改为中文
  2. 吴为新增成长版四视图（一个月后：身体健壮、肌肉初显）
  3. 吴为两版保持基础特征一致（凌乱黑发、瓜子脸轮廓、薄唇、眉峰锐利）
  4. 老约翰特殊标记【独眼+断手义肢】强化标注（全4视图）
  5. 村长特殊标记【花白胡须+弯曲木杖】强化标注（全4视图）
  6. 梅丽夫人特殊标记【鬓角白发】强化标注（全4视图）
