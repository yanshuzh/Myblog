#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import math


class GetDBdata(object):

	def get_sortpostby_published(self,count):
		posts = self.db.query("SELECT * FROM posts ORDER BY published DESC LIMIT %s",int(count))
		return posts
	def get_sortpostby_readcount(self,count):
		posts = self.db.query("SELECT * FROM posts ORDER BY readcount DESC LIMIT %s",int(count))
		return posts

	def get_post_by_id(self,postid):
		post = self.db.get("SELECT * FROM posts WHERE id = %s",int(postid))
		return post

	def get_post_by_title(self,posttitle):
		post = self.db.get("SELECT * FROM posts WHERE title = %s",posttitle)
		return post

	def get_total_record(self,authorid,step):
		total_post = self.db.get("SELECT * FROM authors WHERE id = %s",int(authorid))
		total_record = math.ceil(total_post.record/step)
		return	total_record

	def get_total_record_by_classify(self,classifyid):
		total_post = self.db.query("SELECT * FROM posts WHERE classifyid=%s",classifyid)
		total_record = math.ceil(len(total_post)/5)
		return total_record

	def get_current_record_post_by_classify(self,current_record,step,classifyid):
		start = (int(current_record)-1)*step
		end = step
		posts = self.db.query("SELECT * FROM posts WHERE classifyid=%s ORDER BY published LIMIT %s,%s",classifyid,start,end)
		return posts

	def get_current_record_post(self,current_record,step):
		start = (int(current_record)-1)*step
		end = step
		posts = self.db.query("SELECT * FROM posts ORDER BY published LIMIT %s,%s",start,end)
		return posts

	def delete_post_record(self,article):
		self.db.execute("DELETE FROM posts WHERE id=%s",article["id"])
		self.db.execute("UPDATE authors SET record = record-1 WHERE id = %s",int(1))

	def add_post_record(self,article):
		classifyid = int(article["classifyid"])
		classify = self.db.get("SELECT * FROM classify WHERE classifyid=%s",classifyid)

		self.db.execute("INSERT INTO posts (author_id,title,markdown,html,published,classifyid,classifyname) VALUES (%s,%s,%s,%s,UTC_TIMESTAMP(),%s,%s)",int(1),article["title"],article["content"],article["html"],classifyid,classify.classifyname)
		self.db.execute("UPDATE authors SET record = record+1 WHERE id = %s",int(1))

	def change_post_record(self,article):
		classifyid = int(article["classifyid"])
		classify = self.db.get("SELECT * FROM classify WHERE classifyid=%s",classifyid)
		self.db.execute("UPDATE posts SET title=%s,markdown=%s,html=%s,published=UTC_TIMESTAMP(),classifyid=%s,classifyname=%s WHERE id=%s",article["title"],article["content"],article["html"],classifyid,classify.classifyname,article["id"])

class GetMoodDBData(object):

	def get_total_moodrecord(self,authorid,step):
		total_post = self.db.get("SELECT * FROM authors WHERE id = %s",int(authorid))
		total_record = math.ceil(total_post.moodrecord/step)
		return	total_record

	def get_current_record_moodpost(self,current_moodrecord,step):
		start = (int(current_moodrecord)-1)*step
		end = step
		posts = self.db.query("SELECT * FROM moodlist ORDER BY published LIMIT %s,%s",start,end)
		return posts
	def delete_moodpost_record_by_id(self,moodid):
		self.db.execute("DELETE FROM moodlist WHERE id=%s",moodid)
		self.db.execute("UPDATE authors SET moodrecord = moodrecord-1 WHERE id = %s",int(1))

	def add_mood_record(self,mood):
		self.db.execute("INSERT INTO moodlist (author_id,content,published) VALUES (%s,%s,UTC_TIMESTAMP())",int(1),mood["content"])
		self.db.execute("UPDATE authors SET moodrecord = moodrecord+1 WHERE id = %s",int(1))


class GetUserData(object):
	def get_user_by_id(self,userid):
		user = self.db.get("SELECT * FROM authors WHERE id = %s",int(userid))
		return user
	def get_user_by_email(self,email):
		user = self.db.get("SELECT * FROM authors WHERE email = %s", email)
		return user

	def set_user_aboutme(self,userid,aboutme_markdown):
		self.db.execute("UPDATE authors SET aboutme = %s WHERE id = %s", aboutme_markdown,int(userid))
		user = self.get_user_by_id(userid)
		return user

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