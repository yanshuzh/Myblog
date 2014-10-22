#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import math

#文章信息数据库posts处理类
class GetDBdata(object):
	#获取最新发表的文章，数量为count
	def get_sortpostby_published(self,count):
		posts = self.db.query("SELECT * FROM posts ORDER BY published DESC LIMIT %s",int(count))
		return posts
	#获取点击量最多的文章，数量为count
	def get_sortpostby_readcount(self,count):
		posts = self.db.query("SELECT * FROM posts ORDER BY readcount DESC LIMIT %s",int(count))
		return posts
	#获取id为postid的文章
	def get_post_by_id(self,postid):
		post = self.db.get("SELECT * FROM posts WHERE id = %s",int(postid))
		return post
	#获取title为posttitle的文章
	def get_post_by_title(self,posttitle):
		post = self.db.get("SELECT * FROM posts WHERE title = %s",posttitle)
		return post
	#获取文章页数,每页为step篇
	def get_total_record(self,step):
		total_post = self.db.get("SELECT * FROM authors WHERE id = %s",1)
		total_record = math.ceil(total_post.record/step)
		return	total_record
	#获取当前页数的step篇的文章	
	def get_current_record_post(self,current_record,step):
		start = (int(current_record)-1)*step
		end = step
		posts = self.db.query("SELECT * FROM posts ORDER BY published LIMIT %s,%s",start,end)
		return posts
	#获取特定分类的文章页数，每页为step篇
	def get_total_record_by_classify(self,classifyid,step):
		total_post = self.db.get("SELECT COUNT(*) FROM posts WHERE classifyid=%s",classifyid)
		total_record = math.ceil(total_post['COUNT(*)']/step)
		return total_record
	#获取当前页数的step篇特定分类的文章
	def get_current_record_post_by_classify(self,current_record,step,classifyid):
		start = (int(current_record)-1)*step
		end = step
		posts = self.db.query("SELECT * FROM posts WHERE classifyid=%s ORDER BY published LIMIT %s,%s",classifyid,start,end)
		return posts
	#删除文章
	def delete_post_record(self,article):
		self.db.execute("DELETE FROM posts WHERE id=%s",article["id"])
		self.db.execute("UPDATE authors SET record = record-1 WHERE id = %s",int(1))
	#添加文章
	def add_post_record(self,article):
		classifyid = int(article["classifyid"])
		#获取文章类别id对应的类别名称
		classify = self.db.get("SELECT * FROM classify WHERE classifyid=%s",classifyid)
		#添加文章信息到posts数据库，作者发表文章数量加一
		self.db.execute("INSERT INTO posts (author_id,title,markdown,html,published,classifyid,classifyname) VALUES (%s,%s,%s,%s,UTC_TIMESTAMP(),%s,%s)",int(1),article["title"],article["content"],article["html"],classifyid,classify.classifyname)
		self.db.execute("UPDATE authors SET record = record+1 WHERE id = %s",int(1))
	#修改文章
	def change_post_record(self,article):
		classifyid = int(article["classifyid"])
		#获取修改后的文章类别id对应的类别名称
		classify = self.db.get("SELECT * FROM classify WHERE classifyid=%s",classifyid)
		#更新文章信息到posts数据库
		self.db.execute("UPDATE posts SET title=%s,markdown=%s,html=%s,published=UTC_TIMESTAMP(),classifyid=%s,classifyname=%s WHERE id=%s",article["title"],article["content"],article["html"],classifyid,classify.classifyname,article["id"])
	#某文章被点击阅读后点击量加一
	def add_readcount_by_id(self,articleid):
		self.db.execute("UPDATE posts set readcount=readcount+1 WHERE id=%s",articleid)

#心情状态数据库moodlistt处理类
class GetMoodDBData(object):
	#获取心情状态页数,每页为step条
	def get_total_moodrecord(self,step):
		total_post = self.db.get("SELECT * FROM authors WHERE id = %s",1)
		total_record = math.ceil(total_post.moodrecord/step)
		return	total_record
	#获取当前心情状态为step条
	def get_current_record_moodpost(self,current_moodrecord,step):
		start = (int(current_moodrecord)-1)*step
		end = step
		posts = self.db.query("SELECT * FROM moodlist ORDER BY published LIMIT %s,%s",start,end)
		return posts
	#删除心情状态
	def delete_moodpost_record_by_id(self,moodid):
		self.db.execute("DELETE FROM moodlist WHERE id=%s",moodid)
		self.db.execute("UPDATE authors SET moodrecord = moodrecord-1 WHERE id = %s",int(1))
	#添加心情状态
	def add_mood_record(self,mood):
		self.db.execute("INSERT INTO moodlist (author_id,content,published) VALUES (%s,%s,UTC_TIMESTAMP())",int(1),mood["content"])
		self.db.execute("UPDATE authors SET moodrecord = moodrecord+1 WHERE id = %s",int(1))

#用户数据库信息处理类
class GetUserData(object):

	def get_user_by_id(self,userid):
		user = self.db.get("SELECT * FROM authors WHERE id = %s",int(userid))
		return user
	def get_user_by_email(self,email):
		user = self.db.get("SELECT * FROM authors WHERE email = %s", email)
		return user
	#个人简介设置
	def set_user_aboutme(self,userid,aboutme_markdown):
		self.db.execute("UPDATE authors SET aboutme = %s WHERE id = %s", aboutme_markdown,int(userid))
		user = self.get_user_by_id(userid)
		return user

#文章类别处理类，主要是获取、修改类别信息
class ClassifyData(object):
	def set_classify(self,classify):
		index=1;
		for classifyname in classify:
			self.db.execute("UPDATE classify SET classifyname =%s WHERE id = %s",classifyname,index)	
			self.db.execute("UPDATE posts SET classifyname =%s WHERE classifyid = %s",classifyname,index)
			index=index+1
	def get_classify(self):
		classify = self.db.query("SELECT * FROM classify")
		classifynamelist = [classify[0].classifyname,classify[1].classifyname,classify[2].classifyname,classify[3].classifyname,] 
		return classifynamelist