# 贡献指南

欢迎纠正书目信息、报告失效链接、改进公开指南和修复文档问题。

## 可以提交

- 书名、作者、出版社、ISBN和分类纠错；
- 站内页面链接失效；
- Kindle、电子书格式和阅读器指南修正；
- 透明度文档中的事实或表达问题；
- 不包含个人信息的使用问题。

## 不要提交

- 电子书文件、压缩包、网盘直链或下载令牌；
- 账号、邮箱、订单、IP、访问日志或其他个人信息；
- 权利证明和未公开的安全问题；
- 未经核验的精确馆藏数字或“永久有效”等承诺；
- 与本仓库公开资料无关的生产代码和配置。

## 提交方式

1. 优先使用对应的 Issue 模板；或
2. Fork 后发起 Pull Request。

书目链接必须指向知海图书馆站内书籍页面，格式为：

```text
https://www.zhihailib.com/book/〈post_id〉?utm_source=github
```

每条书目使用一行Markdown表格：

```text
书名 | 作者 | [查看《书名》](站内书籍页面)
```

提交前运行：

```text
python scripts/check_public_docs.py
```

权利投诉请阅读 [CONTENT-POLICY.md](CONTENT-POLICY.md)，安全问题请阅读 [SECURITY.md](SECURITY.md)。
