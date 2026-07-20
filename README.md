# Govee 项目文档

产品需求文档与交互原型的 GitHub Pages 静态站点。

## 在线访问

**文档首页：** https://lindamapotato-cpu.github.io/govee/docs/

### Adyen 卡支付 · 一键复购

| 页面 | URL |
|------|-----|
| PRD 全文 | https://lindamapotato-cpu.github.io/govee/docs/Adyen-NTO卡支付一键复购-PRD.html |
| Checkout 交互原型 | https://lindamapotato-cpu.github.io/govee/docs/Adyen-checkout-UI交互图.html |

### 美国站 · 部分退款发票

| 页面 | URL |
|------|-----|
| PRD 全文 | https://lindamapotato-cpu.github.io/govee/docs/us-govee-部分退款发票更新-PRD.html |

## 仓库结构

```
.
├── Adyen-NTO卡支付一键复购-PRD.md          # Adyen PRD 源文件
├── us-govee-部分退款发票更新-PRD-v0.2.md   # 发票 PRD 源文件
├── assets/
│   ├── export-adyen-prd-html.py            # Adyen PRD → HTML
│   └── export-prd-html.py                  # 发票 PRD → HTML
└── docs/                                   # GitHub Pages 发布目录
    ├── index.html
    ├── Adyen-NTO卡支付一键复购-PRD.html
    ├── Adyen-checkout-UI交互图.html
    └── us-govee-部分退款发票更新-PRD.html
```

## 重新生成 HTML

修改 Adyen PRD 后：

```bash
python3 assets/export-adyen-prd-html.py
```

修改发票 PRD 后：

```bash
python3 assets/export-prd-html.py
```

## GitHub Pages

将 `docs/` 目录设为 Pages 源目录（Settings → Pages → Deploy from branch → `/docs` on `main`）。
