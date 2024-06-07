# AI Mysticism

## AI 算命，占卜 功能
### 占卜功能
- [x] 塔罗牌
  - [ ] 塔罗牌（不同玩法）
  - [ ] 塔罗牌（自己抽牌）
  - [ ] 利用多Agent占卜
  - [ ] 用户填入自己的api-key
- [x] 测名
- [x] 宝宝起名
- [x] 周公解梦
- [x] 梅花易数
- [x] 测姻缘指数

### 记录功能
- [x] 记录占卜对话（云数据库）


## Deploy by docker

根目录新建一个`docer-compose.yml`文件
```yaml
version: '3.11'

services:
  ai-mysticism:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ai-mysticism
    restart: always
    ports:
      - "8000:8000"
    environment:
      - api_key=<your api key>          # 必填
      - api_base=<your api base>        # 必填
      - github_client_id=xxx
      - github_client_secret=xxx
      - jwt_secret=secret
      - ad_client=ca-pub-xxx
      - ad_slot=123
      - database_url=<your database url> # 必填
```

```bash
docker-compose down
docker-compose up --build
```

## Local Run

根目录创建 `.env` 文件，填入如下内容, `api_key` `api_base` `database_url` 为必填项, 其余为可选项

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


## 效果展示
<!-- <img src="frontend\public\index_without_login.png" alt="主页（未登录）" title="主页（未登录）">
<img src="frontend\public\index_conversation_without_login.png" alt="主页对话（未登录）" title="主页对话（未登录）">
<img src="frontend\public\login.png" alt="登录/注册页" title="登录/注册页">
<img src="frontend\public\login_after.png" alt="登录后的个人主页" title="登陆后的个人主页">
<img src="frontend\public\index_login.png" alt="主页（已登录）" title="主页（已登录）">
<img src="frontend\public\dark_mode.png" alt="暗亮色切换" title="暗亮色切换"> -->

![主页（未登录）](frontend\public\index_without_login.png)
*主页（未登录）*

![主页对话（未登录）](frontend\public\index_conversation_without_login.png)
*主页对话（未登录）*

![登录/注册页](frontend\public\login.png)
*登录/注册页*

![登录后的个人主页](frontend\public\login_after.png)
*登录后的个人主页*

![主页（已登录）](frontend\public\index_login.png)
*主页（已登录）*

![暗亮色切换](frontend\public\dark_mode.png)
*暗亮色切换*


## Reference
因为本人是小白，所以大部分参考了[chatgpt-tarot-divination](https://github.com/dreamhunter2333/chatgpt-tarot-divination)项目，非常感谢！
- 修改了UI部分
- 增加了登录模块
- 修改了部分占卜prompt
