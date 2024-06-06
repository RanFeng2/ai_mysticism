# AI Mysticism

## AI 算命，占卜 功能

- [x] 塔罗牌
- [ ] 塔罗牌（自己抽牌）
- [x] 测名
- [x] 宝宝起名
- [x] 周公解梦
- [x] 梅花易数
- [x] 测姻缘指数

## Deploy by docker

```yaml

```

```bash
docker-compose down
docker-compose up --build
```

## Local Run

创建 `.env` 文件，填入如下内容, `api_key` `api_base` `database_url` 为必填项, 其余为可选项

```bash
# 后端变量
api_key=xxx
api_base=xxx
github_client_id=xxx
github_client_secret=xxx
ad_client=ca-pub-xxx
ad_slot=123
database_url = xxxx  # 云数据库连接
```

```bash
# 启动后端服务器
cd D:\ai-mysticism\frontend
# pnpm install
pnpm build --emptyOutDir
cd ..
rm -r dist
cp -r frontend/dist/ dist
# python -m venv venv
.\venv\Scripts\activate
# pip install -r requirements.txt
python main.py

```

```bash
# 启动前端
cd D:\ai-mysticism\frontend
npm run dev
```

## Reference
因为本人是小白，所以大部分参考了[chatgpt-tarot-divination](https://github.com/dreamhunter2333/chatgpt-tarot-divination)项目，非常感谢！
- 修改了UI部分
- 增加了登录模块
- 修改了部分占卜prompt
