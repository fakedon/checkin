# checkin

## Hostloc刷分脚本

前贴：[https://www.hostloc.com/thread-505027-1-1.html](https://www.hostloc.com/thread-505027-1-1.html)

源码地址：[https://github.com/fakedon/checkin](https://github.com/fakedon/checkin)

最近loc开启防cc，原来的脚本基本都没设置时间间隔，很容易被判定cc而导致ip被封
更新下脚本，每个操作都添加1-5秒的时间间隔，每个账号间等待3分钟，travis效果看下图

## 快捷链接
- [本地或者服务器运行](#本地或者服务器运行)
- [部署到travis](#部署到travis)
- [部署到腾讯云无服务器云函数](#部署到腾讯云无服务器云函数)

## 特点
* 多账号
* 支持代理（http, https, socks5)
* 避免被判定cc
* 跨系统
* 日志保存

## 本地或者服务器运行
* 安装python3
* 运行python -V查看python版本，如果不是3版本，尝试运行python3 -V
* `git clone https://github.com/fakedon/checkin`
* 上面是python就运行pip，是python3就运行pip3
* `pip3 install -r requirements.txt`
* 上面是python就运行python，是python3就运行python3
* `python3 run.py`

**添加账号方式有三种：**
* 运行python run.py时指定-c参数  
   查看hostloc文件夹下hostloc.cfg，每个账号需添加代码如下
   ```python
   [username1]
   username=username1
   password=password1
   http_proxy=http1
   https_proxy=https1
   ```
   [username1] 这里原则上是可以任意指定的，最好同下方的username1

   username=username1 修改username1为当前用户名

   password=password1 修改password1为当前密码

   http_proxy=http1 这里设置http代理，没有删除此行，代理格式：http://127.0.0.1:1080，socks5://127.0.0.1:1080

   https_proxy=https1 这里设置http代理，没有删除此行，代理格式：http://127.0.0.1:1080，socks5://127.0.0.1:1080

   可添加多个账号，hostloc.cfg中多余的请删除  
   
* 设置环境变量
   linux下运行
   ```
   export hostloc_username_1=username1 \
   hostloc_password_1=password1 \
   hostloc_http_1=http1 \
   hostloc_https_1=https1 \
   hostloc_username_2=username2 \
   hostloc_password_2=password2
   ```
   windows下运行
   ```
   set hostloc_username_1=username1
   set hostloc_password_1=password1
   set hostloc_http_1=http1
   set hostloc_https_1=https1
   set hostloc_username_2=username2
   set hostloc_password_2=password2
   ```
   各项设置规则同上
* 直接添加在hostloc/hostloc.py文件(不建议)
accounts 字典中添加账号即可，规则如1

   以上3种方式可同时存在  
* 之后运行`python3 run.py -c hostloc/hostloc.cfg`

## 部署到travis
* fork我的项目，下一步
   或者上传你自己的签到脚本到github，需要有.travis.yml文件，并在文件内设置运行签到的命令
* 注册[https://travis-ci.org/](https://travis-ci.org/)，可通过github一键注册
* 访问[https://travis-ci.org/account/repositories](https://travis-ci.org/account/repositories)，Repositories里找到你的项目，x点成√
* 点settings，Environment Variables下Name填hostloc_username_1和hostloc_password_1，Value 填帐号和密码，有代理添加代理，Name填代理方式hostloc_http_1或hostloc_https_1，Value填上述提到的代理，多账号以此类推
* Cron Jobs 设置成 daily

PS. 用户名/密码是填在travis-ci的环境变量里，并不会暴露密码，github中并没有密码信息  
因为签到任务依托于travis-ci，任务调用并不是定时执行，可以在一天中的任何时候，这个取决于网站的任务调配，有时两次执行间隔差不多有48个小时, 但是都在48小时之内。

Travis运行效果图：

![](/docs/img/hostloc_autocheck_travis.jpg)


## 部署到腾讯云无服务器云函数
* 访问[https://console.cloud.tencent.com/scf/list](https://console.cloud.tencent.com/scf/list)
* 新建函数服务，创建方式：空白函数，函数名称：任意，如hostloc，运行环境：Python3.6，下一步
   ![](/docs/img/hostloc_tencent1.jpg)
* 执行方法：index.main_handler(不用改)，提交方式：在线编辑，复制[https://github.com/fakedon/checkin/blob/master/hostloc/hostloc.py](https://github.com/fakedon/checkin/blob/master/hostloc/hostloc.py)内代码到编辑框里，完成
   ![](/docs/img/hostloc_tencent12.jpg)
* 由于腾讯云有一定的免费时间额度，这里我默认把每个账号完成后等待时间改为60秒，如果你要改的话，修改下图172行interval=60的数字60为你想要的等待时间，单位秒
   ![](/docs/img/hostloc_tencent13.jpg)
* 编辑函数配置，超时时间：300，添加环境变量，key填hostloc_username_1和hostloc_password_1，value填帐号和密码，有代理添加代理，Name填代理方式hostloc_http_1或hostloc_https_1，Value填上述提到的代理，多账号以此类推  
   示例图为我添加的小号（Alita）
   ![](/docs/img/hostloc_tencent14.jpg)
* 添加触发方式，触发方式：定时触发，触发周期：每天，填入参数：否，立即启用，保存
   ![](/docs/img/hostloc_tencent4.jpg)
* 函数代码测试如下图
   ![](/docs/img/hostloc_tencent15.jpg)
