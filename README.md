# Ryan WeChat Cover

为公众号文章制作黑白摄影拼贴封面的 Codex Skill，包含中文排版方法、近期成品参考、独立转发方图和双比例封面打包工具。

默认视觉语言是黑底留白、左侧短标题、右侧摄影拼贴、暖白文字与克制的纸张质感。具体主体随文章内容变化，也可按用户要求调整风格。

![AI 付费文章横版封面](references/examples/ai-spending-wide.png)

## 能做什么

- 从文章的核心判断提炼视觉主体，参考实际成品，而不只套用“黑白”“杂志感”等形容词。
- 先生成无字背景，再通过本地排版添加中文，保留可编辑源文件。
- 分别设计约 2.35:1 横版和 1:1 转发方图，避免方形卡片截掉文字或主体。
- 导出两种封面、上传母版、裁切参数及缩略图预览，并指导核验微信后台保存结果。

图像生成与编辑使用运行该 Skill 的助手所提供的工具。Python 脚本只打包已经完成的横图和方图，不会生成背景，也不会自动上传或发布公众号文章。

## 安装到 Codex

把仓库克隆到本机的技能目录：

```bash
git clone https://github.com/summer95950905-hue/ryan-wechat-cover.git ~/.codex/skills/ryan-wechat-cover
```

若设置了自定义 `CODEX_HOME`，使用该目录下的 `skills/ryan-wechat-cover`。目标目录已经存在时先检查原文件，不要直接覆盖本地修改。

在 Codex 中调用：

```text
用 $ryan-wechat-cover 参考之前的封面，为这篇文章设计横版标题图和转发方图。
```

也可以给出更明确的约束：

```text
用 $ryan-wechat-cover 保留现有摄影拼贴方向，缩短标题，并解决转发方图裁切不完整的问题。
```

## 封面打包工具

需要 Python 和 Pillow。建议在独立虚拟环境中安装依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/package_covers.py \
  --wide /path/to/finished-wide.png \
  --square /path/to/finished-square.png \
  --out ./output
```

横图需接近 2.35:1，方图必须已经独立取景为正方形。脚本会拒绝把横图当方图输入。默认导出：

| 文件 | 用途 |
| --- | --- |
| `cover-wide-900x383.png` / `cover-wide-1800x766.png` | 横版封面 |
| `cover-square-800x800.png` | 方形封面 |
| `cover-square-200x200.png` / `cover-square-120x120.png` | 转发缩略图检查 |
| `cover-upload-master-2680x800.png` | 左横右方的双封面上传母版 |
| `crop-fields.json` | 与母版配套的微信裁切参数 |
| `crop-check-wide.png` / `crop-check-square.png` | 按参数从母版截取的核对图 |
| `cover-preview.png` | 横图与两档方图的本地预览 |

上传母版不是最终展示封面，不能直接放进正文。后台操作与实际转发的核验方法见 [裁切说明](references/wechat-crops.md)。

## 参考与指南

- [Skill 入口](SKILL.md)
- [四次近期封面的视觉参考与取舍](references/visual-direction.md)
- [背景提示词、中文排版和方图制作](references/production.md)
- [双比例裁切与微信后台核验](references/wechat-crops.md)

示例图用于说明视觉语言。为新文章创作时，应重新选择符合内容的主体、标题与素材，不直接套用示例中的人物、文案或数字。
