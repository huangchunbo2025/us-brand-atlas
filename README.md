# 美国品牌地图 · US Brand Atlas

一个可离线使用的交互式美国品牌地图。收录 **261 个品牌**，覆盖美国本土 **48 州**，点击品牌即可查看中文简介、创立或源起年份、历史渊源和官网链接。

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/huangchunbo2025/us-brand-atlas)

## 在线体验

**https://us-brand-atlas.onrender.com**

由 Render Static Site 托管，推送到 `main` 分支后自动部署。

## 功能

- 地图点击、拖动、缩放与州内品牌列表。
- 中英文品牌搜索，精确名称优先；支持与州、行业筛选叠加。
- 地图与全部品牌目录两种视图。
- 桌面资料侧栏和手机资料面板，支持键盘操作。
- 单个 HTML 文件，无运行时依赖，无外部字体、脚本或图片请求。

## 本地使用

直接下载并打开 [`public/index.html`](public/index.html) 即可。无需安装依赖、启动服务器或配置密钥。

如果需要通过 HTTP 访问，在仓库根目录执行：

```sh
python3 -m http.server 8000 --directory public
```

访问 `http://localhost:8000`。

## 在 Render 免费部署

本项目使用 Render **Static Site（静态站点）**，不需要付费 Web Service、数据库或后台进程。免费额度及超额规则以 [Render 官方定价](https://render.com/pricing) 为准。

点击上方 **Deploy to Render**，登录 Render 并按 Blueprint 创建站点。仓库已提供 `render.yaml`：

| 配置 | 值 |
| --- | --- |
| 类型 | Static Site |
| 仓库 | `https://github.com/huangchunbo2025/us-brand-atlas` |
| 分支 | `main` |
| Build Command | 留空，使用已提交的 HTML |
| Publish Directory | `public` |
| 自动部署 | 每次提交到 `main` |

Render 完成部署后会提供 HTTPS 的 `*.onrender.com` 地址。不需要环境变量。

## 修改与重新生成

源文件与生成的 HTML 一起保存在仓库中，方便复用与维护。

```text
data/brands.txt       品牌数据，每行以 | 分隔的八个字段
data/us-map.json      US Atlas 预投影州界数据
src/template.html    页面结构、样式与交互逻辑
tools/build.py       仅使用 Python 标准库的生成工具
public/index.html    可独立打开的成品，Render 发布目录
tests/check.cjs      DOM 层面的交互检查
render.yaml          Render 静态站点 Blueprint
```

品牌数据字段为：`英文名|中文名|州代码|源起年份|创立地点或历史渊源|行业|简介|官网域名或资料路径`。

修改源文件后重新生成，并将成品一并提交：

```sh
python3 tools/build.py
git add data src tools public
git commit -m "Update brand atlas"
git push
```

构建过程无需联网。维护资料时应核对品牌官方历史，尤其注意创立年份、品牌启用年份和企业合并年份的区别。

## 验证

开发检查需要 Node.js 22+，运行时不需要 Node.js。

```sh
npm ci
npm test
```

检查涵盖品牌卡片、链接、搜索、空结果、组合筛选、州列表、缩放边界、上一个/下一个、说明弹窗及手机资料面板。使用 LinkeDOM 检查 DOM 和事件逻辑，**不等同于真实浏览器的视觉或兼容性测试**。

## 数据口径与来源

- 灵感来自用户提供的 “United States of Brands” 图片，图片署名为 International Relations Illustrated。仓库未包含该原图。
- 仅整理原图中可辨识的品牌，并补充部分品牌；不是对原图全部商标的逐一复刻。
- 地图州位置表示历史或总部关联，不统一代表创立地或现总部。资料卡单列历史渊源；部分关联沿用原图。
- 简介为公开历史资料的简要整理，官网链接用于进一步核对，不保证经营状态等信息实时更新。欢迎提交有来源的更正。
- 州界来自 [US Atlas](https://github.com/topojson/us-atlas)，基于美国人口普查局边界数据，使用 ISC 许可，原始许可见 [`licenses/us-atlas-ISC.txt`](licenses/us-atlas-ISC.txt)。

## 许可

项目代码及本项目撰写的说明采用 [MIT License](LICENSE)。第三方地图数据保留其原有 ISC 许可。

品牌名称仅用于识别和说明，不是官方商标图稿。品牌名称、商标及其他第三方权利属于各自权利人；MIT 许可不授予这些第三方权利，不代表品牌授权或背书。
