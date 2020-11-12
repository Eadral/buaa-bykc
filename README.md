# BUAA 博雅课程小助手

简体中文 | [English](https://github.com/Eadral/buaa-bykc/blob/master/README-en.md)


## 功能

- 自动抢博雅课程
- 设置目标类型（讲座）
- 设置目标课程
- 设置轮询间隔时间
- 支持钉钉机器人提醒

## 依赖

- selenium~=3.141.0

##### 安装依赖
```bash
pip install -r requirements.txt
```


## 用法

##### 简单使用
```bash
python bykc.py 用户名 密码
count: 0
从巴黎到图卢兹：在原创中发展的欧洲航空航天企业 400/400 博雅课程-讲座-人文 True
“博识杯”知识竞赛决赛 300/300 博雅课程-学校/院文化素质教育活动 False
count: 1
从巴黎到图卢兹：在原创中发展的欧洲航空航天企业 400/400 博雅课程-讲座-人文 True
“博识杯”知识竞赛决赛 300/300 博雅课程-学校/院文化素质教育活动 False

```

##### 帮助
```bash
python bykc.py -h
usage: bykc.py [-h] [--driver_path DRIVER_PATH] [--interval INTERVAL] [--target TARGET [TARGET ...]] [--type TYPE]
               [--dingding_url DINGDING_URL] [--dingding_secret DINGDING_SECRET]
               [--dingding_phone_number DINGDING_PHONE_NUMBER]
               username password

北航博雅小助手

positional arguments:
  username              统一认证用户名
  password              统一认证密码

optional arguments:
  -h, --help            show this help message and exit
  --driver_path DRIVER_PATH, -d DRIVER_PATH
                        webdriver地址 默认: http://10.128.63.245:4444/wd/hub
  --interval INTERVAL, -i INTERVAL
                        轮询间隔时间(ms)
  --target TARGET [TARGET ...], -t TARGET [TARGET ...]
                        目标课程
  --type TYPE           目标课程类型 默认：讲座
  --dingding_url DINGDING_URL
                        dingding机器人url
  --dingding_secret DINGDING_SECRET
                        dingding机器人secret
  --dingding_phone_number DINGDING_PHONE_NUMBER
                        dingding机器人at手机号

```
