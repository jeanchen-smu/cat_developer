from datetime import *
from config import config
from config import sql
from ForumService import Forum
from TagService import Tag
from TelegramService import Telegram
import random
import subprocess

telegram = Telegram()

class Post(Forum):
    def __init__(self):
        Forum.__init__(self)

    def _pagination(self, post_list):
        pagination_list = []
        while len(post_list)>10:
            pagination_list.append(post_list[:10])
            del post_list[:10]
        pagination_list.append(post_list)
        return pagination_list

    def newPost(self, post, thoughtfulness=None):
        self._init_con()
        user_id = post['userId']
        qacoins = post['qacoins']
        subject = post['subject']
        question = post['question']
        section_id = post['section_id']
        is_qa_bountiful = 1 if qacoins>0 else 0
        time_limit_qa = post['dateTime']
        time_limit_bot = self._date()+" "+self._time()
        self.cur.execute(sql.newPost_sql.format(
            user_id,
            subject,
            question, 
            0, 
            self._date()+" "+self._time(),
            is_qa_bountiful, 
            time_limit_qa, 
            time_limit_bot,
            random.randint(1, 5),
            qacoins,
            random.randint(1, 5),
            post['previous_post_id'],
            section_id))
        self.con.commit()
        post_id = self.cur.lastrowid
        self._insert_tag_ass(post["question"], post_id)
        self._close()
        return post_id
        p = subprocess.Popen(["python telePushMsg.py -i '{}' -q '{}' -t '{}' -c '{}' -w web".format(
                user_id, post_id, subject.replace("\\'", "\'\"\'\"\'"), question.replace("\\'", "\'\"\'\"\'"))
            ], shell=True)


    def replyToPost(self, post):
        self._init_con()
        self.cur.execute(sql.replyToPost_insert_sql.format(
            post['userId'],
            post['answer'],
            post['level'],
            0,
            self._date()+" "+self._time(),
            post['questionId'],
            random.randint(1, 5),
            random.randint(1, 5),
            post['parentId'],
            post['previous_post_id']
        ))
        self.con.commit()
        self._insert_tag_ass(post["answer"], self.cur.lastrowid)
        self._close()

    def getPosts(self, filter):
        self._init_con()
        # if 'topic_id' not in filter:
        #     self.cur.execute(sql.getPosts_sql.format(filter["section_id"]))
        # elif filter['topic_id'] == 0 and filter['section_id'] == 0:
        #     self.cur.execute(sql.getPosts_sql.format(filter["section_id"]))
        # elif filter['section_id'] == 0:
        #     self.cur.execute(sql.getPostsByTopic_sql.format(filter['topic_id'], config.tag_association, filter["section"]))
        # elif filter['topic_id'] == 0:
        #     self.cur.execute(sql.getPostsBySection_sql.format(filter['section_id']))
        # else:
        #     self.cur.execute(sql.getPostsByTopicSection_sql.format(filter['topic_id'], config.tag_association, filter['section_id']))
        if 'topic_id' in filter and filter['topic_id'] !=0 :
            self.cur.execute(sql.getPostsByTopicSection_sql.format(filter['topic_id'], config.tag_association, filter['section_id']))
        else:
            self.cur.execute(sql.getPosts_sql.format(filter["section_id"]))
        
        values = self.cur.fetchall()
        for value in values:
            value['date'] = value['date'].strftime(config.date_format)
        self._close()
        return self._pagination(list(values))

    def getPostsByTopic(self, page, topicSelect):
        cursor = self.cur.execute(sql.getPostsByTopic_sql, topicSelect)
        values = cursor.fetchall()
        l, tmp = len(values), []
        if (page-1)*10 > l: 
            page = int(l/10)+1
        elif page < 1: 
            page = 1
        for i in range(l): 
            tmp.append([values[i+10*(page-1)][0], values[i+10*(page-1)][1]])
        return tmp

    def unreadPosts(self):
        cursor_parent = self.cur.execute(sql.unreadPosts_parentid_sql, self.userid)
        parents = cursor_parent.fetchall()
        cursor = self.cur.execute(sql.unreadPosts_sql, ','.join(str(p) for p in parents))
        values = cursor.fetchall()
        l, tmp = len(values), []
        for i in range(l): 
            tmp.append(values[i][0])
        count = len(tmp)
        return tmp, count

    def Posts(self, questionid):
        cursor = self.cur.execute(sql.Posts_sql, questionid)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(row.keys(), row)))
        return results
    
    def updateThought(self, postid):
        cursor = self.cur.execute(sql.updateThought_select_sql, postid)
        value = cursor.fetchone()
        self.cur.execute(sql.updateThought_update_sql, (value[0],postid))
    
    def updateQA(self, postid):
        cursor_score = self.cur.execute(sql.updateQA_score_sql, postid)
        value_score = cursor_score.fetchone()
        cursor_QAF = self.cur.execute(sql.updateQA_QAF_sql, postid)
        value_QAF = cursor_QAF.fetchone()
        self.cur.execute(sql.updateQA_update_sql,(value_score[0]*value_QAF[0],postid))   

    def _get_tags(self, post_id):
        cursor = self.cur.execute(sql.getTags_sql.format(post_id, config.tag_association))
        return list(self.cur.fetchall())

    def _get_answers(self, avatar_id, post_id):
        cursor = self.cur.execute(sql.getAnswer_sql.format(avatar_id, post_id))
        return self._process_answers(list(self.cur.fetchall()))

    def _process_answers(self, answers):
        for answer in answers:
            answer["reviewed"] = True if answer["reviewed"]=="1" else False
        processed_answers = {}
        answers_left = {}
        appended_answers = {}
        for answer in answers:
            if answer['level'] == 2:
                answer['date'] = answer['date'].strftime(config.date_format)
                answer['subAnswer'] = []
                processed_answers[int(answer['answerId'])] = answer
            else:
                if int(answer['level']) in answers_left.keys():
                    answers_left[int(answer['level'])].append(answer)
                else:
                    answers_left[int(answer['level'])] = [answer]
        level_list = answers_left.keys()
        level_list.sort()
        for level in level_list:
            for answer in answers_left[level]:
                answer['aUserName'] = answer['username']
                answer['postDate'] = answer['date'].strftime(config.date_format)
                answer['content'] = answer['answer']
                if level == 3:
                    processed_answers[int(answer['parent_id'])]['subAnswer'].append(answer)
                    if int(answer['parent_id']) in appended_answers.keys():
                        appended_answers[int(answer['parent_id'])].append(int(answer['answerId']))
                    else:
                        appended_answers[int(answer['parent_id'])] = [int(answer['answerId'])]
                else:
                    for key in appended_answers:
                        if answer['parent_id'] in appended_answers[key]:
                            sorted_subanswer = []
                            for i in processed_answers[key]['subAnswer']:
                                sorted_subanswer.append(i)
                                if i['answerId'] == answer['parent_id']:
                                    sorted_subanswer.append(answer)
                            processed_answers[key]['subAnswer'][:] = sorted_subanswer
                            appended_answers[key].append(int(answer['answerId']))
        return processed_answers.values()

    def _get_question(self, avatar_id, post_id):
        cursor = self.cur.execute(sql.getPost_sql.format(avatar_id, post_id))
        return self.cur.fetchall()[0]

    def get_post(self, avatar_id, post_id):
        result = {}
        self._init_con()
        question = self._get_question(avatar_id, post_id)
        question["reviewed"] = True if question["reviewed"]=="1" else False
        question['tags'] = self._get_tags(post_id)
        answers = self._get_answers(avatar_id, post_id)
        self._close()
        result['question'] = question
        result['answers'] = answers
        return result

    def get_all_tags(self, post_id):
        self._init_con()
        cursor = self.cur.execute(sql.getAllTags_sql.format(config.tag_association,post_id))
        tags = list(self.cur.fetchall())
        self._close()
        return tags

    def _update_tags(self, association, post_tags):
        try:
            self._init_con()
            self.cur.execute(
                sql.updatePostTag_sql.format(
                    association, post_tags['post_id'], post_tags['tag_id']))
            self.con.commit()
            self._close()
            return True
        except:
            return False
    
    def add_tag(self, post_tags):
        return self._update_tags(config.show_tag_association, post_tags)
    
    def delete_tag(self, post_tags):
        return self._update_tags(config.hide_tag_association, post_tags)

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

    def _get_all_user_stat(self, section_id):
        self._init_con()
        self.cur.execute(sql.getStat_sql.format(section_id))
        users = list(self.cur.fetchall())
        self._close()
        ranking = 1
        for user in users:
            user['ranking'] = ranking
            ranking += 1
        return users
        
    def get_user_stat(self, avatar_id, section_id):
        users = self._get_all_user_stat(section_id)
        user_stat = {}
        ranking = []
        count = 0
        ranking_keys = ['username', 'ranking', 'thoughfulness']
        for user in users:
            if count < 10:
                ranking.append({i: user[i] for i in ranking_keys})
            if int(avatar_id) == int(user['avatar_id']):
                user_stat = user
        return {'stat': user_stat, 'rank': ranking}

    def get_ranking(self):
        users = self._get_all_user_stat()
        ranking_keys = ['username', 'ranking', 'thoughfulness']
        ranking = []
        for user in users:
            ranking.append({i: user[i] for i in ranking_keys})
        return ranking

    def get_user_login(self, email):
        self._init_con()
        self.cur.execute(sql.getUser_sql.format(email))
        result = self.cur.fetchall()
        self._close()
        return result

    def get_user_by_id(self, avatar_id):
        self._init_con()
        self.cur.execute(sql.getUserById_sql.format(avatar_id))
        result = self.cur.fetchall()
        self._close()
        return result[0]

    def insert_training_data(self, post):
        self._init_con()
        self.cur.execute(sql.updateReviewed_sql.format(post['post_id']))
        self.con.commit()
        self._close()

    def insert_abandoned_post(self, post):
        self._init_con()
        thoughtfulness = random.randint(1,5)
        subject = "" if post['subject'] == None else post['subject'] 
        insert_sql = sql.insertAbandonedPost_sql.format(subject, post['content'], thoughtfulness)
        self.cur.execute(insert_sql)
        self.con.commit()
        post_id = self.cur.lastrowid
        self._close()
        return {"thoughtfulness": thoughtfulness, "post_id": post_id}        
        
    def delete_abandoned_post(self, post_id):
        self._init_con()
        self.cur.execute(sql.deleteAbandonedPost_sql.format(post_id))
        self.con.commit()
        self._close()
    
    def set_user_name(self, user):
        self._init_con()
        agreed = 1 if user['agreed'] else 0
        self.cur.execute(sql.setUserName_sql.format(user['username'], agreed, user['telegram_account'], user['userId']))
        self.con.commit()
        self._close()

    def get_topics(self):
        self._init_con()
        self.cur.execute(sql.getTopics_sql)
        topics = self.cur.fetchall()
        self._close()
        return list(topics)
            
    def set_vote(self, post_id, avatar_id, vote):
        self._init_con()
        print (sql.vote_sql.format(
            post_id, 
            avatar_id, 
            self._date()+" "+self._time(),
            vote,
            self._date()+" "+self._time(),
            vote))
        self.cur.execute(sql.vote_sql.format(
            post_id, 
            avatar_id, 
            self._date()+" "+self._time(),
            vote,
            self._date()+" "+self._time(),
            vote))
        self.con.commit()
        self._close()

    def get_sessions(self, avatar_id):
        self._init_con()
        self.cur.execute(sql.getSessions_sql.format(avatar_id))
        sessions = self.cur.fetchall()
        self._close()
        return list(sessions)

    def get_new_thoughtfulness(self, post):
        return {"new_thoughtfulness": random.randint(1,5)}   
        
    
    
    