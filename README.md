# **Bilibili等级svg解析器**

将硬编码到js代码中的等级svg转换成svg图片

## **运行要求**

- Python 3

## **使用方式**

### 直接下载
如果你不想手动提取请点击 [assets](https://github.com/ManTouQAQ/BiliLevelSVGParser/tree/master/assets) 文件夹

里面有LV0~6包括6级闪电标的SVG图片, 可以直接下载使用 (侵权必删)

### 手动提取

先找到网页B站的这个资源 `https://s1.hdslb.com/bfs/static/laputa-home/client/assets/index.<这里是hash值>.js`

打开网页B站后按 `F12`, 点击 `源代码/来源` 后跟着找到上面连接的文件位置

在这个文件中按 `Ctrl + F` 搜索 `"level-bg"`

你会发现搜索到了几个结果, 观察这个结果:

```javascript
function vm(e, t) {
    return c(),
    u("svg", Am, fm)
}
var Cm = Q(dm, [["render", vm]]);
const mm = {}  <------------------------------------------------ 这里 (1)
  , gm = {
    t: "1641783191890",
    class: "icon",
    viewBox: "0 0 1901 1024",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    "p-id": "2545",
    width: "200",
    height: "200"
}
  , wm = l("path", {
    d: "M146.285714 169.984h1609.142857v707.364571H146.285714z",
    fill: "#FFFFFF",
    "p-id": "2546"
}, null, -1)
  , bm = l("path", {
    class: "level-bg",  <--------------------------------------- 这里是搜索到的位置 (2)
    d: "这里太长了 省略了",
    fill: "#C0C0C0",
    "p-id": "2547"
}, null, -1)
  , km = [wm, bm];
function ym(e, t) {  <------------------------------------------ 这里 (3)
    return c(),
    u("svg", gm, km)
}
var Lm = Q(mm, [["render", ym]]);
```

你会发现有个 `const` 关键字 (在箭头1)

从 `const` 开始 (包括 const) 一直到下面的 `function` 关键字 (在箭头3) 之前复制下来

复制后的内容类似
```javascript
const mm = {}
  , gm = {
    t: "1641783191890",
    class: "icon",
    viewBox: "0 0 1901 1024",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    "p-id": "2545",
    width: "200",
    height: "200"
}
  , wm = l("path", {
    d: "M146.285714 169.984h1609.142857v707.364571H146.285714z",
    fill: "#FFFFFF",
    "p-id": "2546"
}, null, -1)
  , bm = l("path", {
    class: "level-bg",
    d: "这里太长了 省略了",
    fill: "#C0C0C0",
    "p-id": "2547"
}, null, -1)
  , km = [wm, bm];
```

将他们保存到文件, 这里我保存到了 test.js

然后使用命令就可以愉快的转换等级图标了 owo

```sh
python main.py -i test.js -o test.svg
```

## **碎碎念**
本来做自己主页的评论区时想 `借用(` B站的等级图标

最开始是打算写一个自动生成的项目, 后面我找不到它的字体

然后我去看了看网页版B站发现它这个 SVG 居然不是通过 B站 的 `svg-next` 服务获取的

这个等级SVG好像是写成Vue组件了? 看了下具体的代码大概就是上面 `使用方法` 里面所展示的样子:

可以看到先定义了SVG, 然后通过 `l` 函数构造了 `<path/>` 最后使用 `Q` 函数 渲染上去了?

我本来想直接复制里面的属性的, 但是发现这个 `<path/>` 的 `data` 也太长了, 复制起来好麻烦

然后我就花了2小时写了一个自动解析的小工具 =w=

具体流程:
- 词法分析
- 语法分析
- 解析成SVG

这样的话就很方便的将 等级组件 转换成原始 SVG 了