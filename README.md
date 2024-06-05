# AI Mysticism

## AI 算命，占卜 功能

- [x] 塔罗牌
- [x] 生辰八字
- [x] 姓名五格
- [x] 周公解梦
- [x] 起名
- [x] 梅花易数
- [x] 姻缘 [@alongLFB](https://github.com/alongLFB)



## Deploy by docker

```yaml

```

```bash
docker-compose down
docker-compose up --build
```

## Local Run

创建 `.env` 文件，填入如下内容, `api_key` 为必填项, 其余为可选项

```bash
api_key=sk-xxxx
api_base=https://api.openai.com/v1
github_client_id=xxx
github_client_secret=xxx
ad_client=ca-pub-xxx
ad_slot=123
```

RUN

```bash
# 后端服务器
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
# 前端
cd D:\ai-mysticism\frontend
npm run dev
```

## Reference
[chatgpt-tarot-divination](https://github.com/dreamhunter2333/chatgpt-tarot-divination)
