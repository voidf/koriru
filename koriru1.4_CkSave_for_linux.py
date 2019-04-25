#分割1时大概会在20~40列，其它数字大概在80~100列

from PIL import Image
import platform as pf
import numpy as np
import os,sys,time,random
import progressbar
import copy as cp
import requests
import json,base64
import tkinter.filedialog
import tkinter as tk
import threading
import traceback
def combinePATH(*p):
	pr=''
	if pf.system()=="Windows":
		for i in p:
			pr+=i+"\\"
	elif pf.system()=="Linux":
		for i in p:
			pr+=i+"/"
	else:
		for i in p:
			pr+=i+"/"
	return pr[:-1]
def loadIMG(imgName):
	if pf.system()=="Windows":
		return Image.fromarray(imgName)
	elif pf.system()=="Linux":
		return Image.fromarray(np.uint8(imgName))
	else:
		return Image.fromarray(np.uint8(imgName))

def dosign(ck):
	hds={
			'Accept':'application/json, text/plain, */*',
			'Accept-Encoding':'gzip, deflate, sdch, br',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Connection':'keep-alive',
			'Cookie':ck,
			'Host':'api.live.bilibili.com',
			'Origin':'https://live.bilibili.com',
			'Referer':'https://live.bilibili.com/1',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
		}
	print(json.loads(requests.get('https://api.live.bilibili.com/sign/doSign',headers=hds).content))

def resource_path(relative_path):
	if pf.system()=="Windows":
		p=sys.argv[0]
		p=p[:p.rfind('\\')+1]
		return p+relative_path
	elif pf.system()=="Linux":
		relative_path=relative_path.replace("\\","/")
		return sys.path[0]+relative_path
	else:
		relative_path=relative_path.replace("\\","/")
		return sys.path[0]+relative_path
	# if hasattr(sys,'_MEIPASS'):
		# base_path = sys._MEIPASS
	# else:
		# base_path = os.path.abspath('.')
	# return os.path.join(base_path,relative_path)

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

	a=loadIMG(mmp)

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

	re1=a.crop((0,0,cut_col,len(mmp)))
	re2=a.crop((cut_col+1,0,len(mmp[0]),len(mmp)))

	return re1,re2

def compare_study_and_example(exam_map):
	study_dir=resource_path('\\学习')
	#print(study_dir)
	study_list=os.listdir(study_dir)
	source_init=Image.new('L',(250,250))
	source_init_idx=np.array(source_init)
	
	distinguish_text=[]
	is_okay=1
	for repeat4times in range(4):
		
		splited,rest=split_text_on_pic(exam_map,repeat4times)

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

			mr=125-rrr
			mc=125-ccc
			
		
			for ii in range(len(arrsplited)):
				for jj in range(len(arrsplited[ii])):
					if ii+mr>=250 or jj-mov_c>=250:
						continue
					source_init_idx[ii+mr][jj+mc]=arrsplited[ii][jj]
			source_init=loadIMG(source_init_idx)
			DistLeaderboard=[]
			TagsLeaderboard=[]
			#print(study_list)
			for sample in study_list:
				file_name=combinePATH(study_dir,sample)
				#print(file_name)
				now=np.array(Image.open(file_name))

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

				study_init=loadIMG(study_init_idx)
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

			distinguish_text.append(ResultTag)
		exam_map=np.array(rest.crop(scan_dark_pixs(rest)))
		chk_before=splited

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
			tp_map=np.array(loadIMG(mmp).rotate(rotdeg))
			fst_raw,fst_col,last_raw,last_col=figure_fst_and_last(tp_map)
			if last_raw-fst_raw<leasthei:
				leasthei=last_raw-fst_raw
				leastmap=tp_map
				leastdeg=rotdeg
			elif last_raw-fst_raw>leasthei:
				break
			
	else:
		for rotdeg in range(0,-50,-1):
			tp_map=np.array(loadIMG(mmp).rotate(rotdeg))
			fst_raw,fst_col,last_raw,last_col=figure_fst_and_last(tp_map)
			if last_raw-fst_raw<leasthei:
				leasthei=last_raw-fst_raw
				leastmap=tp_map
				leastdeg=rotdeg
			elif last_raw-fst_raw>leasthei:
				break
			
	return loadIMG(leastmap),leastdeg

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
	return np.array(zero_one_map)

def center_of_gravity(map_source):#计算重心，其实这个方法可以合并到上面，传入矩阵，返回重心的行，列
	pctr=sumr=sumc=0
	for rr in range(len(map_source)):
		for cc in range(len(map_source[rr])):
			if map_source[rr][cc]!=0:
				pctr=pctr+1
				sumr=sumr+rr
				sumc=sumc+cc
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
	with open(resource_path(r'\temp.png'),'wb') as f:
		f.write(pngf)
	return open(resource_path(r'\temp.png'),'rb')

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

	currentTime=time.asctime(time.localtime(time.time()))
	if convertJson['msg']=='ok':
		print('领取成功，获得瓜子：%s，当前瓜子为%s。' % (convertJson['data']['awardSilver'],convertJson['data']['silver']))
		study_(proimg,istu,iso)


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
				if os.path.exists(resource_path('\\学习\\'+dislist[studying]+'-'+str(name_ctr)+'.gif')):
					continue
				else:
					print(targ)
					targ=targ.crop(scan_dark_pixs(targ))
					targ.save(resource_path('\\学习\\'+dislist[studying]+'-'+str(name_ctr)+'.gif'))
					print('保存学习文件：'+dislist[studying]+'-'+str(name_ctr)+'.gif')

					break
			giff=np.array(matrix_b.crop(scan_dark_pixs(matrix_b)))
	else:
		print('学习开关已关闭或分割出现问题不能学习')


def deathloop(is_study):
	init_ck=cur_ck
	while True:
		try:
			timeS,timeE=getCurrentTask(init_ck)
			if int(time.time())<timeE:
				print('领取时间戳：%d，当前时间戳：%d，等待%d秒' % (timeE,time.time(),timeE-int(time.time())+1))
				
				time.sleep(timeE-int(time.time())+1)
			grey_png=Image.open(make_req(init_ck)).convert('L')
		except KeyError:
			print('收到抛出的KeyError异常')
			print('领取完成，正在等待次日启动')
			
			slpt=int(time.strftime('%X',time.localtime(time.time()))[:2])*3600+int(time.strftime('%X',time.localtime(time.time()))[3:5])*60+int(time.strftime('%X',time.localtime(time.time()))[6:8])
			slpt=86400-slpt
			slpt=slpt+random.randint(0,10800)
			print('阻塞%d秒'%slpt)
			
			time.sleep(slpt)
			dosign(init_ck)
			continue
		try:
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
				
			ig=loadIMG(new_map)
				
			new_map=np.array(ig.resize((960,320)))
			new_img,dg=rotate_check(new_map)
			revis=scan_dark_pixs(new_img)
			revi=new_img.crop(revis)
			processed_gp=loadIMG(new_png).resize((960,320)).rotate(dg).crop(revis)
			rou_dot_map=check_dot(np.array(processed_gp))
			rdm_img=loadIMG(rou_dot_map).crop(scan_dark_pixs(loadIMG(rou_dot_map)))
			global dislist
			distinguish_result,dislist,is_okay=compare_study_and_example(np.array(rdm_img))
			print('识别计算结果为：',end='')
			print(distinguish_result)
		except Exception as e:
			traceback.print_exc(e)
			print('程序出错，开始备份错误图片文件')
			debugi=0
			for debugi in range(20):
				if os.path.exists(resource_path(r'\BUG_%d' % debugi)):
					continue
				else:
					os.system('ren temp.png BUG_%d.png' % debugi)
					break
			distinguish_result=39
			is_okay=0
		getAward(init_ck,distinguish_result,np.array(rdm_img),dislist,is_study,is_okay,timeS,timeE)


try:
	ckf=open(resource_path('LastCK.ck'),'r')
	conf1=input("使用上次的Cookie？[Use previous cookie?](Y/n)")
	if conf1!="n" or conf1!="N" or conf1!="no" or conf1!="No" or conf1!="NO" or conf1!="oN":
		for i in ckf:
			cur_ck=i
		ckf.close()
	else:
		raise NameError("Manual Cookie")
except:
	cur_ck=input("Cookie:")
	conf1=input("保存Cookie吗?[Save cookie?](Y/n)")

	if conf1!="n" or conf1!="N" or conf1!="no" or conf1!="No" or conf1!="NO" or conf1!="oN":
		with open(resource_path('LastCK.ck'),'w') as ckf:
			ckf.write(cur_ck)

conf1=input("学习开关?[Enable auto study?](y/N)")
if conf1!="y" or conf1!="Y":
	enable_study=0
else:
	enable_study=1

deathloop(enable_study)