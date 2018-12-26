import telegram
from config import config
from config import sql
from ForumService import Forum
from TagService import Tag
import random



class Telegram(Forum):
    def __init__(self):
        Forum.__init__(self)
        self.bot = telegram.Bot(token=config.bot_token)
    
    def _bot_message(self, chat_id, username, question_id, title, content):
        self.bot.send_message(chat_id=chat_id, 
        text="""{} has a new post:
                \nquestion_id:{}
                 \ntitle: {}
                 \ncontent: {}
                 \nplease key in /reply to reply the question""".format(username, question_id, title, content))

    def _process_tag_sim(self, sim, post_id):
        sim_strs = ["({}, {}, {})".format(i, post_id, j) for j, i in sim]
        return " ,".join(sim_strs)

    def _insert_tag_ass(self, post, post_id):
        tag_service = Tag(post)
        tag_service.newTag()
        self.cur.execute(sql.newTag_sql.format(
            self._process_tag_sim(tag_service.sim, post_id)
        ))
        self.con.commit()
    
    def newPost(self, post, thoughtfulness=None):
        self._init_con()
        chat_id = post['chat_id']
        qacoins = post['qacoin']
        subject = post['title']
        question = post['content']
        is_qa_bountiful = 1 if qacoins>0 else 0
        time_limit_qa = post['timelimit']
        time_limit_bot = self._date()+" "+self._time()
        self.cur.execute(sql.teleNewPost_sql.format(
            chat_id,
            self._process_string(subject),
            self._process_string(question), 
            0, 
            self._date()+" "+self._time(),
            is_qa_bountiful, 
            time_limit_qa, 
            time_limit_bot,
            random.randint(1, 5),
            qacoins,
            random.randint(1, 5)))
        self.con.commit()
        question_id = self.cur.lastrowid
        self._insert_tag_ass(post["content"], question_id)
        self._close()
        return question_id

    def tele_push_message(self, chat_id, question_id, title, content):
        self._init_con()
        self.cur.execute(sql.teleGetChatId.format(chat_id))
        user_list = self.cur.fetchall()
        self._close()
        for user in user_list:
            try:
                self._bot_message(
                    user['chat_id'],
                    user['avatar_name'],
                    question_id,
                    title,
                    content
                )
            except:
                continue

    def web_push_message(self, userId, question_id, title, content):
        self._init_con()
        self.cur.execute(sql.webGetChatId.format(userId))
        user_list = self.cur.fetchall()
        self._close()
        for user in user_list:
            try:
                self._bot_message(
                    user['chat_id'],
                    user['avatar_name'],
                    question_id, 
                    title,
                    content
                )
            except:
                continue

    def replyToPost(self, post):
        self._init_con()
        self.cur.execute(sql.teleReplyToPost_insert_sql.format(
            post['chat_id'],
            post['answer'],
            2,
            0,
            self._date()+" "+self._time(),
            post['question_id'],
            random.randint(1, 5),
            random.randint(1, 5),
            post['question_id']
        ))
        self.con.commit()
        self._insert_tag_ass(post["answer"], self.cur.lastrowid)
        self._close()

    def _process_string(self, string):
        return string.replace("'", "\\'")

    def upsert_chat_id(self, chat_id, username):
        self._init_con()
        self.cur.execute(sql.upsertChatId_sql.format(chat_id, self._process_string(username)))
        self.con.commit()
        self._close()
            
    def verify_telgram(self, username):
        self._init_con()
        self.cur.execute("select * from avatar where telegram_account='{}'".format(self._process_string(username)))
        user = self.cur.fetchall()
        self._close()
        return len(user)>0

    def get_user_qacoins(self, chat_id):
        self._init_con()
        self.cur.execute(sql.teleGetStat_sql.format(chat_id))
        qacoin = self.cur.fetchall()
        self._close()
        return qacoin[0]['qacoins']