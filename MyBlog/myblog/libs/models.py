#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import math


class GetDBdata(object):
	def get_sortpost(self,orderbase,count):
		posts = self.db.query("SELECT * FROM posts ORDER BY %s DESC LIMIT %s",orderbase,int(count))
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
		total_post = self.db.get("SELECT * FROM classify WHERE classifyid=%s",classifyid)
		total_record = math.ceil(total_post.record/5)
		return total_record

	def get_current_record_post_by_classify(self,current_record,step,classify):
		start = (int(current_record)-1)*step
		end = step
		posts = self.db.query("SELECT * FROM posts WHERE classify=%s ORDER BY published LIMIT %s,%s",classify,start,end)
		return posts

	def get_current_record_post(self,current_record,step):
		start = (int(current_record)-1)*step
		end = step
		posts = self.db.query("SELECT * FROM posts ORDER BY published LIMIT %s,%s",start,end)
		return posts

	def delete_post_record(self,article):
		self.db.execute("DELETE FROM posts WHERE id=%s",article["id"])
		self.db.execute("UPDATE authors SET record = record-1 WHERE id = %s",int(1))
		self.db.execute("UPDATE classify SET record = record-1 WHERE classifyid =%s",int(article["classifyid"]))

	def add_post_record(self,article):
		self.db.execute("INSERT INTO posts (author_id,title,markdown,html,published,classify) VALUES (%s,%s,%s,%s,UTC_TIMESTAMP(),%s)",int(1),article["title"],article["content"],article["html"],int(article["classifyid"]))
		self.db.execute("UPDATE authors SET record = record+1 WHERE id = %s",int(1))
		self.db.execute("UPDATE classify SET record = record+1 WHERE classifyid = %s",int(article["classifyid"]))

	def change_post_record(self,article):
		oldclassifyid = self.db.get("SELECT classify FROM posts WHERE id=%s",int(article["id"]))
		#oldclassifyid = oldclassify.classify
		if oldclassifyid["classify"] != article["classifyid"]:
			self.db.execute("UPDATE classify SET record = record+1 WHERE classifyid = %s",article["classifyid"])
			self.db.execute("UPDATE classify SET record = record-1 WHERE classifyid = %s",oldclassifyid["classify"])
		self.db.execute("UPDATE posts SET title=%s,markdown=%s,html=%s,published=UTC_TIMESTAMP(),classify=%s WHERE id=%s",article["title"],article["content"],article["html"],article["classifyid"],article["id"])

	def get_classifyname(self,classifyid):
		classifyname = self.db.get("SELECT classifyname FROM classify WHERE classifyid=%s",classifyid)
		return classifyname["classifyname"]
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






