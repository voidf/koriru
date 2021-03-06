#分割1时大概会在20~40列，其它数字大概在80~100列

from PIL import Image
import numpy as np
import os,sys,time
import progressbar
import copy as cp
import requests
import json,base64
import tkinter.filedialog
import tkinter as tk
import threading

wid=['[',progressbar.Timer(),']',progressbar.Bar(),'(',progressbar.ETA(),')',]
def check_dot(mmp):#传入一个矩阵，检查里面有没有直径20的圆，返回一个记录这些圆心的矩阵
	aap=cp.deepcopy(mmp)
	for ii in progressbar.progressbar(range(len(mmp)),widgets=wid):
		for jj in range(len(mmp[ii])):
			rou_ctr=0
			if mmp[ii][jj]!=255 and ii>9 and jj>9 and ii<len(mmp)-10 and jj<len(mmp[ii])-10:
				for k in range(ii-10,ii+10):
					for l in range(jj-10,jj+10):
						if mmp[k][l]!=255:
							rou_ctr=rou_ctr+1
			if rou_ctr>=400:
				aap[ii][jj]=255
			else:
				aap[ii][jj]=0
		updatePb(ii,len(mmp))
	return aap

def split_text_on_pic(mmp,cutctr):#从传入矩阵中分割文字，返回两个切开的图
	cut_col=0
	for jj in range(len(mmp[0])):
		color=0
		for ii in range(len(mmp)):
			if mmp[ii][jj]!=0:
				color=1
		if color==0:
			cut_col=jj
			break
	#np.savetxt(os.path.dirname(sys.path[0])+'\\WA.txt',mmp)
	a=Image.fromarray(mmp)
	#a.show()
	#Image.fromarray(mmp).save(os.path.dirname(sys.path[0])+'\\WAA.gif')
	least_color=19260817
	if cut_col>105 or (cut_col==0 and len(mmp[0]))>105:
		
		for jj in range(20,40):
			col_color=0
			for ii in range(len(mmp)):
				if mmp[ii][jj]!=0:
					col_color=col_color+1
			if col_color<least_color:
				least_color=col_color
				cut_col=jj
		for jj in range(80,105):
			col_color=0
			for ii in range(len(mmp)):
				if mmp[ii][jj]!=0:
					col_color=col_color+1
			if col_color<least_color:
				least_color=col_color
				cut_col=jj
	if cut_col==0 and len(mmp[0])>55 and cutctr!=3:
		for jj in range(45,55):
			col_color=0
			for ii in range(len(mmp)):
				if mmp[ii][jj]!=0:
					col_color+=1
			if col_color<least_color:
				least_color=col_color
				if least_color<6:
					cut_col=jj
		#print('leastcolor:%d' % least_color)
	#print('cut_col:%d' % cut_col)
		
	re1=a.crop((0,0,cut_col,len(mmp)))
	re2=a.crop((cut_col+1,0,len(mmp[0]),len(mmp)))
	#if cut_col>102:
		#re1.show()
	#re1.save(os.path.dirname(sys.path[0])+'\\WA'+input('文件名：')+'.gif')
	return re1,re2

def compare_study_and_example(exam_map):
	study_dir=os.path.dirname(sys.path[0])+'\\学习'
	study_list=os.listdir(study_dir)
	source_init=Image.new('L',(250,250))
	source_init_idx=np.array(source_init)
	
	distinguish_text=[]
	is_okay=1
	for repeat4times in range(4):
		
		splited,rest=split_text_on_pic(exam_map,repeat4times)
		#splited.save(os.path.dirname(sys.path[0])+'\\WAc%d.gif' % repeat4times)
		#Image.fromarray(exam_map).show()
		#rest.show()
		arrsplited=np.array(splited)
		if repeat4times==2:
			if splited.size[0]==0:
				distinguish_text[1]=1
				distinguish_text.append('-')
				is_okay=0
				continue
			pix_counter=0
			for ii in range(len(arrsplited)):
				for jj in range(len(arrsplited[ii])):
					if arrsplited[ii][jj]!=0:
						pix_counter=pix_counter+1
			#print(pix_counter)
			if pix_counter>1400:
				distinguish_text.append('+')
				print('+')
			else:
				distinguish_text.append('-')
				print('-')
			
		else:
			
			if repeat4times==3:
				arrsplited=np.array(rest)
			rrr,ccc=center_of_gravity(arrsplited)
			#if repeat4times!=3 and splited.size[0]==0:
				#split_text_on_pic(np.array(chk_before))
			mr=125-rrr
			mc=125-ccc
			
		
			for ii in range(len(arrsplited)):
				for jj in range(len(arrsplited[ii])):
					if ii+mr>=250 or jj-mov_c>=250:
						continue
					source_init_idx[ii+mr][jj+mc]=arrsplited[ii][jj]
			source_init=Image.fromarray(source_init_idx)	
			DistLeaderboard=[]
			TagsLeaderboard=[]
			for sample in study_list:
				file_name=study_dir+'\\'+sample
				#print(file_name)
				now=np.array(Image.open(file_name))
				#print(now)
				study_init=Image.new('L',(250,250))
				study_init_idx=np.array(study_init)
				
				rrr,ccc=center_of_gravity(now)
				mr=125-rrr
				mc=125-ccc

				for ii in range(len(now)):
					for jj in range(len(now[ii])):
						if ii+mr>=250 or jj-mov_c>=250:
							continue
						study_init_idx[ii+mr][jj+mc]=now[ii][jj]*255#如果去掉这个*255了话预览效果会很不好
				#print(study_init)
				study_init=Image.fromarray(study_init_idx)
				DistLeaderboard.append(sum(sum((source_init_idx-study_init_idx)**2)))
				TagsLeaderboard.append(sample[:1])
			
			ranking=np.argsort(DistLeaderboard)
			TagsCounter={}
			for kk in range(3):#knn
				CurrentTag=TagsLeaderboard[ranking[kk]]
				TagsCounter[CurrentTag]=TagsCounter.get(CurrentTag,0)+1

				
			MaxTagCtr=0
			for CurrentTag,Number in TagsCounter.items():
				if Number>MaxTagCtr:
					MaxTagCtr=Number
					ResultTag=CurrentTag
			print(ResultTag)
			#with open(os.path.dirname(sys.path[0])+'\\res.txt','a') as fi:
			#	fi.write(ResultTag+'\n')
			
			distinguish_text.append(ResultTag)
		exam_map=np.array(rest.crop(scan_dark_pixs(rest)))
		chk_before=splited
		#rest.crop(scan_dark_pixs(rest)).save(os.path.dirname(sys.path[0])+'\\Wcropc%d.gif' % repeat4times)
		
	#print(distinguish_text)
	if distinguish_text[2]=='+':
		return int(distinguish_text[0])*10+int(distinguish_text[1])+int(distinguish_text[3]),distinguish_text,is_okay
	else:
		return int(distinguish_text[0])*10+int(distinguish_text[1])-int(distinguish_text[3]),distinguish_text,is_okay

def figure_fst_and_last(mymap):#检查矩阵里面第一个和最后一个白块的行数和列数，用于搭配旋转使用，返回他们的行列
	fst=0
	for ii in range(len(mymap)):
		for jj in range(len(mymap[ii])):
			if mymap[ii][jj]!=0:
				if fst==0:
					fst_raw=ii
					fst_col=jj
					fst=1
				last_raw=ii
				last_col=jj
	return fst_raw,fst_col,last_raw,last_col

def rotate_check(mmp):#检查旋转方法，传入一个矩阵，返回旋转以后摆的最正的图和最优角度
	#print('#####################new img#######################')
	fst=0
	fst_raw,fst_col,last_raw,last_col=figure_fst_and_last(mmp)
	leasthei=last_raw-fst_raw
	
	leastdeg=rotdeg=0
	leastmap=mmp
	if fst_col<last_col:
		for rotdeg in range(1,50):
			tp_map=np.array(Image.fromarray(mmp).rotate(rotdeg))
			fst_raw,fst_col,last_raw,last_col=figure_fst_and_last(tp_map)
			#print('rotdeg:%d,hei:%d,lhei:%d' % (rotdeg,last_raw-fst_raw,leasthei))
			if last_raw-fst_raw<leasthei:
				leasthei=last_raw-fst_raw
				leastmap=tp_map
				leastdeg=rotdeg
			elif last_raw-fst_raw>leasthei:
				break
			
	else:
		for rotdeg in range(0,-50,-1):
			tp_map=np.array(Image.fromarray(mmp).rotate(rotdeg))
			fst_raw,fst_col,last_raw,last_col=figure_fst_and_last(tp_map)
			#print('rotdeg:%d,hei:%d,lhei:%d' % (rotdeg,last_raw-fst_raw,leasthei))
			if last_raw-fst_raw<leasthei:
				leasthei=last_raw-fst_raw
				leastmap=tp_map
				leastdeg=rotdeg
			elif last_raw-fst_raw>leasthei:
				break
			
	return Image.fromarray(leastmap),leastdeg

def shadow_split(arrays):#将图片上的灰边分离，用于寻找重心移动图片，传入原图矩阵，传出灰边矩阵
	w=255
	b=37
	
	zero_one_map=[]
	for col in arrays:
		
		zero_one_map_col=[]
		for single_var in col:
			if single_var!=w and single_var!=b:
				
				zero_one_map_col.append(255)
			else:
				
				zero_one_map_col.append(0)
		
		zero_one_map.append(zero_one_map_col)
	
	#with open(os.path.dirname(sys.path[0])+'\\shadow.gif') as fii:
	#Image.fromarray(np.array(zero_one_map)).show()
	#os.system('pause')
	return np.array(zero_one_map)

def center_of_gravity(map_source):#计算重心，其实这个方法可以合并到上面，传入矩阵，返回重心的行，列
	pctr=sumr=sumc=0
	for rr in range(len(map_source)):
		for cc in range(len(map_source[rr])):
			if map_source[rr][cc]!=0:
				pctr=pctr+1
				sumr=sumr+rr
				sumc=sumc+cc
	#print('another algorithm:%d,%d' % (round(sumr/pctr),round(sumc/pctr)))
	
	nearest_c=round(sumc/pctr)
	nearest_r=round(sumr/pctr)
	
	return nearest_r,nearest_c
	
def scan_dark_pixs(pic):#计算黑边，传入图片，返回一个正好与黑边相切的图的裁切元组
	mmp=np.array(pic)
	hei=len(mmp)
	wid=len(mmp[0])
	hitari=migi=shita=ue=0
	for iii in range(hei):
		for jjj in range(wid):
			if mmp[iii][jjj]!=0:
				ue=iii
				break
		if ue!=0:
			break
	for jjj in range(wid):
		for iii in range(hei):
			if mmp[iii][jjj]!=0:
				hitari=jjj
				break
		if hitari!=0:
			break
	for iii in range(hei-1,-1,-1):
		for jjj in range(wid-1,-1,-1):
			if mmp[iii][jjj]!=0:
				shita=iii+1
				break
		if shita!=0:
			break
	for jjj in range(wid-1,-1,-1):
		for iii in range(hei-1,-1,-1):
			if mmp[iii][jjj]!=0:
				migi=jjj+1
				break
		if migi!=0:
			break
	tur=(hitari-1,ue-1,migi,shita)
	#print(tur)
	return tur

def make_req(ck):
	ac='application/json, text/plain, */*'
	ace='gzip, deflate, sdch, br'
	acl='zh-CN,zh;q=0.8'
	cn='keep-alive'
	
	hst='api.live.bilibili.com'
	ogn='https://live.bilibili.com'
	ref='https://live.bilibili.com/546432'
	ua='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

	
	

	hds={
		'Accept':ac,
		'Accept-Encoding':ace,
		'Accept-Language':acl,
		'Connection':cn,
		'Cookie':ck,
		'Host':hst,
		'Origin':ogn,
		'Referer':ref,
		'User-Agent':ua
	}
	lnk='https://api.live.bilibili.com/lottery/v1/SilverBox/getCaptcha?ts=%d' % int(time.time())
	req=requests.get(lnk,headers=hds)
	
	json_convert=json.loads(req.content)
	pngf=base64.b64decode(json_convert['data']['img'][23:])

	with open(os.path.dirname(sys.path[0])+'\\'+'temp.png','wb') as f:
		f.write(pngf)
	return open(os.path.dirname(sys.path[0])+'\\'+'temp.png','rb')

def getCurrentTask(ck):
	url='https://api.live.bilibili.com/lottery/v1/SilverBox/getCurrentTask'

	hds={
		'Accept':'application/json, text/plain, */*',
		'Accept-Encoding':'gzip, deflate, sdch, br',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'Connection':'keep-alive',
		'Cache-Control':'no-cache',
		'Connection':'keep-alive',
		'Cookie':ck,
		'Host':'api.live.bilibili.com',
		'Origin':'https://live.bilibili.com',
		'Referer':'https://live.bilibili.com/546432',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
	}
	req=requests.get(url,headers=hds)
	jjson=json.loads(req.content)
	# print(jjson['data']['minute'])
	# print(jjson['data']['time_start'])
	# print(jjson['data']['time_end'])
	
	return jjson['data']['time_start'],jjson['data']['time_end']

def getAward(ck,vercode_data,proimg,dislist,istu,iso,timeS,timeE):
	
	lnk='https://api.live.bilibili.com/lottery/v1/SilverBox/getAward?time_start=%d&end_time=%d&captcha=%d' % (timeS,timeE,vercode_data)
	hds={
		'Accept':'application/json, text/plain, */*',
		'Accept-Encoding':'gzip, deflate, sdch, br',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'Connection':'keep-alive',
		'Cache-Control':'no-cache',

		'Cookie':ck,
		'Host':'api.live.bilibili.com',
		'Origin':'https://live.bilibili.com',
		'Referer':'https://live.bilibili.com/1',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
	}
	response_raw=requests.get(lnk,headers=hds)
	#print(response_raw.content)
	convertJson=json.loads(response_raw.content)
	print(convertJson)
	#lbmsg.set(convertJson)
	statusText.config(state=tk.NORMAL)
	#statusText.insert(tk.END,convertJson['msg']+'\n')
	currentTime=time.asctime(time.localtime(time.time()))
	if convertJson['msg']=='ok':
		print('领取成功，获得瓜子：%s，当前瓜子为%s。' % (convertJson['data']['awardSilver'],convertJson['data']['silver']))
		statusText.insert(tk.END,'%s:领取成功，获得瓜子：%s，当前瓜子为%s。\n' % (currentTime,convertJson['data']['awardSilver'],convertJson['data']['silver']))
		study_(proimg,istu,iso)
	statusText.config(state=tk.DISABLED)

def study_(giff,swi,chk):
	if swi==1 and chk==1:
		print('开始学习')
		for studying in range(4):
			matrix_a,matrix_b=split_text_on_pic(giff,studying)
			if studying==3:
				targ=matrix_b
			else:
				targ=matrix_a
			for name_ctr in range(10):
				if studying==2:
					break
				if os.path.exists(os.path.dirname(sys.path[0])+'\\学习\\'+dislist[studying]+'-'+str(name_ctr)+'.gif'):
					continue
				else:
					print(targ)
					targ=targ.crop(scan_dark_pixs(targ))
					targ.save(os.path.dirname(sys.path[0])+'\\学习\\'+dislist[studying]+'-'+str(name_ctr)+'.gif')
					#Image.fromarray(targ).crop(scan_dark_pixs(Image.fromarray(targ))).save(os.path.dirname(sys.path[0])+'\\学习\\'+dislist[studying]+'-'+str(name_ctr)+'.gif')
					print('保存学习文件：'+dislist[studying]+'-'+str(name_ctr)+'.gif')
					statusText.config(state=tk.NORMAL)
					statusText.insert(tk.END,'保存学习文件：'+dislist[studying]+'-'+str(name_ctr)+'.gif\n')
					statusText.config(state=tk.DISABLED)
					break
			giff=np.array(matrix_b.crop(scan_dark_pixs(matrix_b)))
	else:
		print('学习开关已关闭或分割出现问题不能学习')
#init_ck=input('请输入您的cookie【仅用于申请验证码】:')
def statuswin():
	print('GUI线程启动')
	global win
	win=tk.Tk()
	win.title("状态窗")
	win.geometry('600x600')
	# global lbmsg
	# lbmsg=tk.StringVar()
	# lbwin=tk.Label(win,textvariable=lbmsg).pack()
	# lbmsg.set('有状态的话会显示在这里哦')
	global statusText
	statusText=tk.Text(win,width=70,height=40)
	statusText.insert(tk.END,'这里是状态显示栏\n')
	statusText.config(state=tk.DISABLED)
	statusText.pack()
	global cav
	cav=tk.Canvas(win,width=300,height=21,bg="white")
	#x=tk.StringVar()
	outRec=cav.create_rectangle(5,5,300,20,outline="green",width=1)
	global fillRec
	fillRec=cav.create_rectangle(5,5,5,20,outline="",width=0,fill="green")
	cav.pack()
	win.mainloop()

def updatePb(cur,allpro):
	cav.coords(fillRec,(5,5,6+(cur/allpro)*295,20))
	win.update()
	
def update_in_time(ifstu):
	t1=threading.Thread(target=statuswin,args=())
	t2=threading.Thread(target=deathloop,args=(ifstu,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()

def deathloop(is_study):
	init_ck=stv
	while True:
		timeS,timeE=getCurrentTask(init_ck)
		if int(time.time())<timeE:
			print('领取时间戳：%d，当前时间戳：%d，等待%d秒' % (timeE,time.time(),timeE-int(time.time())+1))
			statusText.config(state=tk.NORMAL)
			statusText.insert(tk.END,'领取时间戳：%d，当前时间戳：%d，等待%d秒\n' % (timeE,time.time(),timeE-int(time.time())+1))
			statusText.config(state=tk.DISABLED)
			#lbmsg.set('领取时间戳：%d，当前时间戳：%d，等待%d秒' % (timeE,time.time(),timeE-int(time.time())+1))
			time.sleep(timeE-int(time.time())+1)
		grey_png=Image.open(make_req(init_ck)).convert('L')
		#try:
		arr=np.array(grey_png)
		zomap=shadow_split(arr)
		gc_r,gc_c=center_of_gravity(zomap)
		global mov_c
		global mov_r
		mov_r=gc_r-20
		mov_c=gc_c-60
		new_map=cp.deepcopy(zomap)
		new_png=cp.deepcopy(arr)
		for ii in range(len(new_map)):
			for jj in range(len(new_map[ii])):
				new_map[ii][jj]=0
				new_png[ii][jj]=0
		for ii in range(len(zomap)):
			for jj in range(len(zomap[ii])):
				if ii-mov_r>=40 or jj-mov_c>=120:
					continue
				new_map[ii-mov_r][jj-mov_c]=zomap[ii][jj]
				new_png[ii-mov_r][jj-mov_c]=arr[ii][jj]
			
		ig=Image.fromarray(new_map)
			
		new_map=np.array(ig.resize((960,320)))
		new_img,dg=rotate_check(new_map)
		revis=scan_dark_pixs(new_img)
		revi=new_img.crop(revis)
		processed_gp=Image.fromarray(new_png).resize((960,320)).rotate(dg).crop(revis)
		rou_dot_map=check_dot(np.array(processed_gp))
		rdm_img=Image.fromarray(rou_dot_map).crop(scan_dark_pixs(Image.fromarray(rou_dot_map)))
		global dislist
		distinguish_result,dislist,is_okay=compare_study_and_example(np.array(rdm_img))
		print('识别计算结果为：',end='')
		print(distinguish_result)
		# except:
			# print('程序出错，开始备份错误图片文件')
			# debugi=0
			# for debugi in range(20):
				# if os.path.exists(os.path.dirname(sys.path[0])+'\\BUG_%d' % debugi):
					# continue
				# else:
					# os.system('ren temp.png BUG_%d.png' % debugi)
					# break
			# distinguish_result=39
			# is_okay=0
		getAward(init_ck,distinguish_result,np.array(rdm_img),dislist,is_study,is_okay,timeS,timeE)

#GUI模块
def subm1():
	print(ent)
	global stv
	stv=ent.get('1.0',tk.END)[:-1]
	rt.destroy()
	#print(stv.get())
	global rt2
	rt2=tk.Tk()
	rt2.title("请确认是否开启学习开关")
	rt2.geometry('300x100')
	bb=tk.Button(rt2,text='启用学习开关',width=15,height=2,command=bton).pack()
	bbb=tk.Button(rt2,text='禁用学习开关',width=15,height=2,command=btoff).pack()
	rt2.mainloop()
def bton():
	rt2.destroy()
	update_in_time(1)
def btoff():
	rt2.destroy()
	update_in_time(0)
rt=tk.Tk()
#stv=tk.StringVar()
rt.title("GUI测试：请输入您的cookie【仅用于申请验证码】:")
rt.geometry('400x250')
ent=tk.Text(rt,width=50,height=15)
ent.pack()
bt=tk.Button(rt,text='确定',width=15,height=2,command=subm1).pack()

rt.mainloop()

#is_study=int(input('是否开启学习开关？输入1以开启'))