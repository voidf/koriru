# 在使用koriru.exe或者koriru.py之前记得把学习文件夹放到同一个目录下！

要直接运行py脚本的话，请先安装依赖库：numpy,pillow,requests,progressbar2
# Please download the "学习" Folder to the same directory of koriru!

Please install these packages before running the py script:numpy,pillow,requests,progressbar2

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# koriru是用于bilibili直播间自动领取银瓜子的脚本程序。

# 界面展示：

## 等待cookie输入
![preview](https://github.com/voidf/koriru/blob/master/READMEpic/askck.png)

Q：如何获取我的cookie？

A：如果您使用chrome内核的浏览器，进入哔哩哔哩直播任一房间后按下F12启动开发人员工具，如图所示：
![vick](https://github.com/voidf/koriru/blob/master/READMEpic/viewck.png)

然后切换到Network选项卡，按下F5刷新以重新抓包，选择第一个包：
![cpck](https://github.com/voidf/koriru/blob/master/READMEpic/copyck.png)

将图中所圈划字段中cookie：后面所有字符复制下来，粘贴进cookie输入框即可。注意输入完不要敲回车，要点击确定或者输入并保存按钮。

## 学习开关
![swi](https://github.com/voidf/koriru/blob/master/READMEpic/studyswitch.png)

Q:学习开关有什么用？

A:学习开关是控制koriru在进行正确的验证码识别后是否保存当前已识别数字图片的控件。选择开启会让koriru将本次识别结果保存至“学习”文件夹，可能会占据少量磁盘空间并且会使下次识别运算变慢。但是足够的样本数据会让koriru识别进行得更精确，目前版本的koriru会在每个数字的样本数量达到10时停止学习。

![study folder](https://github.com/voidf/koriru/blob/master/READMEpic/studyfolder.png)

当然，您也可以直接禁用学习开关。

## 挂机状态窗
![status](https://github.com/voidf/koriru/blob/master/READMEpic/statuswin.png)

底下的绿色进度条如果没动或者卡住了可能是发生了BUG。另外Dev版本的命令行如果显示“程序出错，开始备份图像文件”则是发生图片计算错误，请携带当前系统版本，运行环境和所备份错误图片至Issues区进行报告（如果您愿意的话）。

验证码错误是正常情况。

## 如果您对开发不感兴趣，那么本README应该到这里就足够您使用了

## 请转至Releases区下载已经预编译好的exe程序，如有任何问题可转至Issues区讨论

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 
 
# 下面是对koriru工作原理和内部代码的一些说明

打开koriru.py，会发现所有方法都给打在这一个文件里了，所以koriru是一个单文件脚本。~~其实是因为我不会打多文件~~

先介绍用二级标题的不太重要的方法，比较核心的方法用一级标题在后面说明。

## dosign

这是一个最简单的方法，用来进行**每日签到**。

![doSign](https://github.com/voidf/koriru/blob/master/READMEpic/dosign.jpg)

hds里面装的东西其实都是用来模拟用户登录操作签到的一系列请求头文件。这些信息可以从chrome浏览器的开发工具Network选项卡里面抓到。

值得注意的是这里必须用到ck，也就是用户的**cookie**，所以这里传入了一个ck。另外直播签到的地址这里留一下，是：https://api.live.bilibili.com/sign/doSign

这个方法其实在1.0版本就已经写好，但是现在1.4的时候才考虑加了进去。**不是核心算法。**

## resource_path

这个方法用来给pyinstaller打包成exe文件的时候用，但最近发现好像也直接兼容脚本运行。

它返回传入资源的**绝对路径**，虽然看起来短小但是维持程序运行异常重要。**不是核心算法。**

*这个方法之后费解的一行是给progressbar用的网上抄的代码，请不要在意。*

## make_req

做请求，从 https://api.live.bilibili.com/lottery/v1/SilverBox/getCaptcha 下载验证码图片，并且保存在程序工作目录下。**不是核心算法。**

## getCurrentTask

获取当前瓜子**领取状态**，返回可以领取的时间戳。

屑站直播的银瓜子领取系统通过time_start值来记录你上次成功领取的时间，并且只有等到time_end的时间才能进行领取。每天第一次进入直播间时会取这个时候的时间作为time_start。然后每次领取瓜子后会取当前时间更新time_start。time_start数值上等于time_end-当前瓜子箱子等待秒数。

本方法**不是核心算法。**

## getAward

发送程序识别的结果，用来**领取瓜子**，并把领取结果写入GUI记录窗格和命令行中。**不是核心算法。**

## statuswin

显示程序运行状态的日志窗格，不可编辑。以下所有提到GUI模块的都是1.2版本新加入的。**GUI模块的一部分，不是核心算法。**

## updatePb

用来实时更新显示识别算法的进度的进度条的方法。**GUI模块的一部分，不是核心算法。**

## update_in_time

让GUI和脚本主程序**并行**执行的一个方法，用到多线程模块threading。**GUI模块的一部分，不是核心算法。**

## subm1

程序执行第二个跳出来问你要不要启用学习开关的窗口。**GUI模块的一部分，不是核心算法。**

## restoreck

1.4版本加入的懒人功能，用于从保存的ck文件中恢复上次使用的cookie。**不是核心算法。**

## saveck

1.4版本加入的懒人功能，保存输入到输入框的cookie到工作目录的Lastck.ck文件中。值得注意的是这个文件是**明文**保存cookie的，为了安全起见请不要将该文件泄露给他人。**不是核心算法。**

## bton

响应激活学习开关的方法。**GUI模块的一部分，不是核心算法。**

## btoff

响应禁用学习开关的方法。**GUI模块的一部分，不是核心算法。**

*此方法以下几行代码用于创建初始化cookie输入窗格，为了方便没有用方法装起来。*

*至此非核心方法介绍完毕，接下来按照运行顺序介绍核心算法。*

# 核心算法————将验证码图片上的数字和运算符转成字符

