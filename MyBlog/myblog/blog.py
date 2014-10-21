#!/usr/bin/env python
import markdown
import os.path
import re
import torndb
import unicodedata
import tornado.web
from .libs.models import GetDBdata,GetUserData,GetMoodDBData,ClassifyData


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    def get_current_user(self):
        user_email = self.get_secure_cookie("blog_user")
        if not user_email: return None
        return self.db.get("SELECT * FROM authors WHERE email = %s",user_email)

class HomeHandler(BaseHandler,GetDBdata):
    def get(self):
        newestposts = self.get_sortpostby_published(5)
        bestposts = self.get_sortpostby_readcount(5)
        if not newestposts or not bestposts:pass
            #self.redirect("/compose")
            #return
        self.render("home.html", newestposts=newestposts,bestposts=bestposts)

class AboutHandler(BaseHandler,GetUserData):
    def get(self):
        user = self.get_user_by_id(1)
        self.render("about.html",aboutme=user.aboutme)

class LifeHandler(BaseHandler,GetDBdata,ClassifyData):
    def get(self,current_record):
        classify = self.get_classify();
        total_record = self.get_total_record(1,5)
        posts = self.get_current_record_post(int(current_record),5)
        before_record = 1 if int(current_record)<=1 else (int(current_record)-1)
        after_record = int(total_record) if int(current_record)+1 > total_record else (int(current_record)+1)
        record = [before_record,int(current_record),after_record]
        if not posts:pass
            #self.redirect("/compose")
            #return
        self.render("newlist.html",posts=posts,total_record=int(total_record),record=record,classify=classify)
        #self.render("test.html",classify=classify)
class ClassifyHandler(BaseHandler,GetDBdata,ClassifyData):
    def get(self,classifyid,current_record):
        classify = self.get_classify();
        total_record = self.get_total_record_by_classify(classifyid)

        posts = self.get_current_record_post_by_classify(int(current_record),5,classifyid)
        before_record = 1 if int(current_record)<=1 else (int(current_record)-1)
        after_record = int(total_record) if int(current_record)+1 > total_record else (int(current_record)+1)
        record = [before_record,int(current_record),after_record]

        newestposts = self.get_sortpostby_published(5)
        bestposts = self.get_sortpostby_readcount(5)
        allposts = {"posts":posts,"newestposts":newestposts,"bestposts":bestposts}
        self.render("classify.html",allposts=allposts,total_record=int(total_record),record=record,classify=classify)
        #self.render("test.html",total_record=total_record)


class MoodHandler(BaseHandler,GetMoodDBData):
    def get(self,current_moodrecord):
        total_moodrecord = self.get_total_moodrecord(1,5)
        moodposts = self.get_current_record_moodpost(int(current_moodrecord),5)
        before_moodrecord = 1 if int(current_moodrecord)<=1 else (int(current_moodrecord)-1)
        after_moodrecord = total_moodrecord if int(current_moodrecord)+1 > total_moodrecord else (int(current_moodrecord)+1)
        moodrecord = [before_moodrecord,int(current_moodrecord),after_moodrecord]
        if not moodposts:pass
            #self.redirect("/compose")
            #return
        self.render("moodlist.html",moodposts=moodposts,total_moodrecord=int(total_moodrecord),moodrecord=moodrecord)


class DetailedHandler(BaseHandler,GetDBdata,ClassifyData):
    def get(self,postid):
        classify = self.get_classify();
        post = self.get_post_by_id(int(postid))
        if not post:return
        beforepost = self.get_post_by_id(int(postid)-1)
        afterpost = self.get_post_by_id(int(postid)+1)
        bestposts = self.get_sortpostby_readcount(5)
        self.render("detailed.html",post=post,beforepost=beforepost,afterpost=afterpost,bestposts=bestposts,classify=classify)

#admin!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class AuthLoginHandler(BaseHandler,GetUserData):
    def get(self):
        self.render("admin/login.html")
    def post(self):

        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        self.set_secure_cookie("blog_user",email)
        if (not email) or (not password):
            self.redirect("/admin/login")
            return
        user = self.get_user_by_email(email)
        if not user:
            #access_log.error("Login Error for email: %s" % email)
            self.redirect("/admin/login")
            return

        if password==user.passwd:
            
            self.redirect(self.get_argument("next", "/admin/about"))
            return
        else:
            self.redirect("/admin/login")

        return
class AuthLogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("blog_user")
        self.redirect(self.get_argument("next", "/admin/login"))

class AuthAboutHandler(BaseHandler,GetUserData):
    @tornado.web.authenticated
    def get(self):
        user = self.get_user_by_id(1)
        self.render("admin/about.html",aboutme_markdown=user.aboutme)
    @tornado.web.authenticated
    def post(self):
        aboutme_text = self.get_argument("aboutme_text",None)
        aboutme_markdown = markdown.markdown(aboutme_text)
        user = self.set_user_aboutme(1,aboutme_markdown)
        self.redirect("/admin/about")

class AuthClassifyHandler(BaseHandler,ClassifyData):
    @tornado.web.authenticated
    def get(self):
        classify = self.get_classify()
        self.render("admin/classify.html",classify=classify)
    @tornado.web.authenticated
    def post(self):
        classify = self.get_arguments("classify",None)
        self.set_classify(classify)
        self.render("admin/classify.html",classify=classify)

class AuthArticleHandler(BaseHandler,GetDBdata):
    @tornado.web.authenticated
    def get(self,current_record):
        total_record = self.get_total_record(1,10)
        posts = self.get_current_record_post(int(current_record),10)
        before_record = 1 if int(current_record)<=1 else (int(current_record)-1)
        after_record = total_record if int(current_record)+1 > total_record else (int(current_record)+1)
        record = [before_record,int(current_record),after_record]
        self.render("admin/article.html",posts=posts,total_record=int(total_record),record=record)
    @tornado.web.authenticated
    def post(self):
        title = self.get_argument("search_title",None)
        post = self.get_post_by_title(title)
        if not post:
            self.render("admin/article.html") 
            return
        self.render("admin/newarticle.html") 

class AuthMoodHandler(BaseHandler,GetMoodDBData):
    @tornado.web.authenticated
    def get(self,current_moodrecord):
        total_moodrecord = self.get_total_moodrecord(1,10)
        moodposts = self.get_current_record_moodpost(int(current_moodrecord),10)
        before_moodrecord = 1 if int(current_moodrecord)<=1 else (int(current_moodrecord)-1)
        after_moodrecord = total_moodrecord if int(current_moodrecord)+1 > total_moodrecord else (int(current_moodrecord)+1)
        moodrecord = [before_moodrecord,int(current_moodrecord),after_moodrecord]
        self.render("admin/mood.html",moodposts=moodposts,total_moodrecord=int(total_moodrecord),moodrecord=moodrecord)
    @tornado.web.authenticated
    def post(self,current_moodrecord):
        mycheckbox=self.get_arguments("checkbox")
        #self.render("admin/test.html",mycheckbox=mycheckbox)
        for moodid in mycheckbox:
            self.delete_moodpost_record_by_id(int(moodid))
        self.redirect("/admin/mood/1")

class AuthNewArticleHandler(BaseHandler,GetDBdata):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/newarticle.html")
    @tornado.web.authenticated
    def post(self):
        article = {}
        article["title"] = self.get_argument("articletitle",None)
        article["content"] = self.get_argument("articlecontent",None)
        article["classifyid"] = self.get_argument("articleclassifyid",None)
        article["html"] = markdown.markdown(article["content"])
        self.add_post_record(article)
        self.redirect("/admin/newarticle")
        #self.render("admin/test.html",classify=article["classify"])

class AuthMoodNewHandler(BaseHandler,GetMoodDBData):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/newmood.html")
    @tornado.web.authenticated
    def post(self):
        mood = {}
        mood["content"] = self.get_argument("moodcontent",None)
        self.add_mood_record(mood)
        self.redirect("/admin/moodnew")

class AuthResultArticleHandler(BaseHandler,GetDBdata,ClassifyData):
    @tornado.web.authenticated
    def get(self,articleid):
        classify = self.get_classify()
        post = self.get_post_by_id(articleid)
        self.render("admin/resultarticle.html",post=post,classify=classify)
    @tornado.web.authenticated
    def post(self,articleid):
        classify = self.get_classify()
        buttonsubmit = self.get_argument("buttonsubmit",None)
        buttondelete = self.get_argument("buttondelete",None)
        article = {}
        article["id"]=self.get_argument("articleid",None)
        article["title"] = self.get_argument("articletitle",None)
        article["content"] = self.get_argument("articlecontent",None)
        article["html"] = markdown.markdown(article["content"])
        article["classifyid"] = self.get_argument("articleclassifyid",None)
        if buttonsubmit=="Submit":
            self.change_post_record(article)
            post = self.get_post_by_id(article["id"])
            self.render("admin/resultarticle.html",post=post,classify=classify)
            #self.render("admin/test.html",articleid=article["id"])
            return
        elif buttondelete=="Delete":
            self.delete_post_record(article)
        else:pass
        self.redirect("/admin/article/1")

class AuthSearchHandler(BaseHandler,GetDBdata):
    @tornado.web.authenticated
    def post(self):
        articletitle = self.get_argument("search_title",None)
        if not articletitle:
            self.redirect("/admin/article/1")
            return
        post = self.get_post_by_title(articletitle)
        if not post:
            self.redirect("/admin/article/1")
            return
        self.render("admin/resultarticle.html",post=post)


handlers = [
    (r"/", HomeHandler),
    (r"/about", AboutHandler),
    (r"/newlist/(\d+)", LifeHandler),
    (r"/classify/(\d+)/(\d+)", ClassifyHandler),    
    (r"/moodlist/(\d+)", MoodHandler),
    (r"/detailed/(\d+)", DetailedHandler),
    (r"/admin/login", AuthLoginHandler),
    (r"/admin/about",AuthAboutHandler),
    (r"/admin/classify",AuthClassifyHandler),
    (r"/admin/article/(\d+)",AuthArticleHandler),
    (r"/admin/mood/(\d+)",AuthMoodHandler),
    (r"/admin/moodnew",AuthMoodNewHandler),   
    (r"/admin/newarticle",AuthNewArticleHandler),
    (r"/admin/resultarticle/(\d+)",AuthResultArticleHandler),
    (r"/admin/search",AuthSearchHandler),
    (r"/admin/logout", AuthLogoutHandler),
]

