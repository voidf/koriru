# 在使用koriru.exe或者koriru.py之前记得把学习文件夹放到同一个目录下！

要直接运行py脚本的话，请先安装依赖库：numpy,pillow,requests,progressbar2
# Please download the "学习" Folder to the same directory of koriru!

Please install these packages before running the py script:numpy,pillow,requests,progressbar2

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

A:学习开关是控制koriru在进行正确的验证码识别后是否保存当前已识别数字图片的控件。选择开启会让koriru讲本次识别结果保存至“学习”文件夹，可能会占据少量磁盘空间并且会使下次识别运算变慢。但是足够的样本数据会让koriru识别进行得更精确，目前版本的koriru会在每个数字的样本数量达到10时停止学习。

![study folder](https://github.com/voidf/koriru/blob/master/READMEpic/studyfolder.png)

当然，您也可以直接禁用学习开关。

## 挂机状态窗
![status](https://github.com/voidf/koriru/blob/master/READMEpic/statuswin.png)
