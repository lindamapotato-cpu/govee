# Govee US — 部分退款发票 PRD

美国站（us.govee.com）部分退款场景下的发票更新产品需求文档，及 GitHub Pages 静态展示。

## 在线访问

| 页面 | URL |
|------|-----|
| 文档首页 | https://mashulin05.github.io/govee-Risk-control-system/ |
| PRD 全文 | https://mashulin05.github.io/govee-Risk-control-system/us-govee-部分退款发票更新-PRD.html |

## 仓库结构

```
.
├── us-govee-部分退款发票更新-PRD-v0.2.md   # PRD 源文件（内容版本 v0.5）
├── assets/
│   ├── export-prd-html.py                  # Markdown → HTML 导出脚本
│   └── us-govee-部分退款发票更新-PRD-展示页.html
└── docs/                                   # GitHub Pages 发布目录
    ├── index.html
    └── us-govee-部分退款发票更新-PRD.html
```

## 重新生成 HTML

修改 Markdown 后，运行：

```bash
python3 assets/export-prd-html.py
```

脚本会读取 `us-govee-部分退款发票更新-PRD-v0.2.md`，生成：

- `assets/us-govee-部分退款发票更新-PRD-展示页.html`
- `docs/us-govee-部分退款发票更新-PRD.html`
- `docs/index.html`

## PRD 概要

- **范围**：仅美国站，不含税定价（tax-exclusive）
- **ERP 流程**：运营录入退款金额 → 自动算税 → 触发 Shopify 退款 → SKU 级台账
- **发票**：用户手动下载；完整行项目 + `Refunded (incl. tax)` + Payment Details
- **合计**：`Total = Subtotal + Total tax + Shipping − Refunded`（Total tax 保持原订单税额）

## GitHub Pages

将 `docs/` 目录设为 Pages 源目录（`/docs` on `main` branch）即可发布。
