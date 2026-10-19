# 一练

每周四练的上下肢分化训练计划，做成一个手机上看的网页。没有账号，没有后端，一个 HTML 文件加 42 张动作图。

线上：https://yilian-app.pages.dev

## 它是什么

我自己在用的健身计划。练过一段时间 PPL 六练之后发现一周去不了六次，改成上下肢四练，每个部位一周还是两次。计划本身不新鲜，网页解决的是在健身房里掏手机看计划这件事：

- 四天分 tab，每个动作一张卡片，右边大字是组数 × 次数
- 每个动作有起始和结束两帧真人照片，自动切换，点一下暂停
- 三个短标签写最要紧的要点，想看完整做法点「详细」
- 右边圆圈勾选完成，进度条跟着走，记录存在手机浏览器里
- 底部固定一个组间休息计时器，60 秒 / 90 秒 / 3 分钟，到点响一声并震动
- 「说明」页有排班、强度、减量周信号、引体向上过渡

加到 iPhone 主屏幕可以当独立 App 用，跟系统深浅色。

## 计划

上肢 A（推为主）/ 下肢 A（蹲为主）/ 上肢 B（拉为主）/ 下肢 B（后链为主），练二休一、练二休二。引体向上用高位下拉替代，上肢 B 末尾加离心引体过渡。每练 5 到 6 周减量一周：组数砍半，重量不变。

想换动作或者改组次数，改 `public/index.html` 里的 `EX` 和 `DAYS` 两个对象就行，图片放 `public/img/` 下按 `<名字>_0.jpg` / `<名字>_1.jpg` 命名。

## 部署

纯静态，任何静态托管都行。我用 Cloudflare Pages：

```sh
npx wrangler login
npx wrangler pages project create yilian-app --production-branch main --force   # 只有建项目这一次要 --force，否则新版 wrangler 会把它转成 Worker
npm run deploy
```

本地看效果：`npm run dev`，然后开 http://localhost:3000 。

## 图片来源

动作照片来自 [free-exercise-db](https://github.com/yuhonas/free-exercise-db)（Unlicense，公有领域），每个动作取起始和结束两帧，缩到 640 像素宽。

## 许可

MIT。

---

## English

A four-day upper/lower split workout plan as a single-page mobile web app. No account, no backend: one HTML file and 42 exercise photos.

Live: https://yilian-app.pages.dev (Chinese UI)

Each exercise card shows two photos (start and end position) that alternate automatically, sets × reps in large type, three short form cues, and a check-off circle. A rest timer (60 s / 90 s / 3 min) is pinned to the bottom. Progress is stored in the browser only. Works as a home-screen PWA on iOS.

Edit the `EX` and `DAYS` objects in `public/index.html` to change exercises or volume. Photos are from [free-exercise-db](https://github.com/yuhonas/free-exercise-db) (Unlicense). MIT licensed.
