# BUAA 博雅课程小助手

简体中文 | [English](https://github.com/Eadral/buaa-bykc/blob/master/README-en.md)


## 功能

- 自动抢博雅课程
- 设置目标类型（讲座）
- 设置目标课程
- 设置轮询间隔时间
- 设置最大抢课数量
- 支持钉钉机器人提醒

## 依赖

- 北航校园网环境
- selenium~=3.141.0
- requests~=2.23.0

##### 安装依赖
```bash
pip install -r requirements.txt
```


## 用法

命令行运行后交互式输入密码，即可开始抢博雅。

##### 简单使用

默认用法，自动抢所有**讲座**类型博雅，每秒轮询1次。

```bash
python bykc.py 用户名 
```
```bash
Password:
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
```
