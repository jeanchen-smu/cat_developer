###Avatar###
getStat_sql = """SELECT IFNULL(qa_gain-qa_lost, 0) AS qacoins, section_id, username, thoughfulness, s0.avatar_id FROM
((SELECT a.avatar_id, a.avatar_name AS username, IFNULL(SUM(qa_coin_basic),0) AS qa_gain, a.section_id as section_id,
IFNULL(SUM(thoughtfulness_score),0) AS thoughfulness FROM avatar a LEFT JOIN post p ON a.avatar_id = p.avatar_id GROUP BY a.avatar_id) s0
LEFT JOIN (SELECT avatar_id, IFNULL(SUM(qa_coin_bounty),0) AS qa_lost FROM post WHERE time_limit_qa<CURDATE() GROUP BY avatar_id) s1
on s0.avatar_id = s1.avatar_id) WHERE section_id='{}' ORDER BY thoughfulness DESC"""

setUserName_sql = """UPDATE avatar SET avatar_name='{}', agreed={}, telegram_account='{}' WHERE avatar_id={}"""

getUser_sql = """SELECT * FROM avatar WHERE email='{}' and expiry_date > CURDATE()"""

getUserById_sql = """SELECT * FROM avatar WHERE avatar_id={} and expiry_date > CURDATE()"""

newUser_sql = """INSERT INTO avatar (avatar_id, avatar_name, icon, avatar_qa_coin, avatar_thoughtfulness_score, section_id, is_bot)
                VALUES (%s, %s, %s, 0, 0, %s, 0)"""

userData_sql = "SELECT * FROM avatar WHERE avatar_id = %s"

profUserData_sql = "SELECT * FROM avatar WHERE section_id = %s"

updateUserQA_select_sql = "SELECT qa_coins FROM avatar_qa_coin WHERE avatar_id = %s ORDER BY `timestamp` DESC"

updateUserQA_update_sql = "UPDATE avatar SET avatar_qa_coin = %s WHERE avatar_id = %s"

updateUserThought_select_sql = "SELECT thoughtfulness_score FROM avatar_thoughtfulness_score WHERE avatar_id = %s ORDER BY `timestamp` DESC"

updateUserThought_update_sql = "UPDATE avatar SET avatar_thoughtfulness_score = %s WHERE avatar_id = %s"

userUnreadCount_select_sql = "SELECT post_id FROM post WHERE avatar_id = %s"

userUnreadCount_count_sql = "SELECT COUNT(*) FROM post WHERE parent_id IN ('+','.join(map(str,%s))+')"

_idOfName_sql = "SELECT avatar_id FROM avatar WHERE avatar_name = %s"

changeName_sql = "UPDATE avatar SET avatar_name = %s WHERE avatar_id = %s"

changeIcon_sql = "UPDATE avatar SET icon = %s WHERE avatar_id = %s"


###Post###
newPost_sql = """INSERT INTO post (avatar_id, post_subject, 
                post_content, level, is_question, is_bot, `timestamp`, 
                is_qa_bountiful, time_limit_qa, time_limit_bot, qa_coin_basic,
                qa_coin_bounty, thoughtfulness_score, previous_id, section_id)
                VALUES ({}, '{}', '{}', 1, 1, {}, '{}', {}, '{}', '{}', {}, {}, {}, {}, '{}')"""

replyToPost_select_sql = "SELECT level FROM post WHERE post_id = %s"

replyToPost_insert_sql = """INSERT INTO post (avatar_id, post_content, level, is_question,
                            is_bot, `timestamp`, question_id, qa_coin_basic, 
                            thoughtfulness_score, parent_id, previous_id)
                            VALUES ({}, '{}', {}, 0, {}, '{}', {}, {}, {}, {}, {})"""

getPosts_sql = """SELECT post_id as 'key', post_subject as subject, 
                qa_coin_bounty as qacoins, timestamp as date, 
                (select count(*) from post	where question_id = p.post_id) as commentCounts,
                (select count(*) from post where (isnull(reviewed) or reviewed=0) and 
                (post_id=p.post_id or question_id=p.post_id)) as reviewCounts,
                avatar_name as username FROM post p, avatar a 
                WHERE is_question = 1 and p.avatar_id = a.avatar_id and 
                p.section_id='{}'
                ORDER BY `timestamp` DESC"""

getPost_sql = """SELECT post_id AS questionId, avatar_name AS username, p.avatar_id as userId,
                timestamp AS date, post_subject As subject, post_content AS question,
                reviewed, thoughtfulness_score, 
                (select ifnull((select upvotes from (select post_id, count(*) as upvotes from vote where vote=1 group by post_id)  uv where  uv.post_id=p.post_id), 0)) as upvotes,
                (select ifnull((select downvotes from (select post_id, count(*) as downvotes from vote where vote=2 group by post_id)  dv where  dv.post_id=p.post_id), 0)) as downvotes,
                (select ifnull((select vote from vote where post_id=p.post_id and avatar_id={}),0) ) as uservote
                FROM post p, avatar a WHERE p.avatar_id = a.avatar_id AND post_id = {}"""

getAnswer_sql = """SELECT post_id AS answerId, parent_id, level, avatar_name AS username, 
                (SELECT avatar_name FROM avatar WHERE avatar_id = 
                (SELECT avatar_id FROM post WHERE post_id = p.parent_id)) AS pUserName,
                timestamp AS date, post_content AS answer, reviewed, thoughtfulness_score,
                (select ifnull((select upvotes from (select post_id, count(*) as upvotes from vote where vote=1 group by post_id)  uv where  uv.post_id=p.post_id), 0)) as upvotes,
                (select ifnull((select downvotes from (select post_id, count(*) as downvotes from vote where vote=2 group by post_id)  dv where  dv.post_id=p.post_id), 0)) as downvotes,
                (select ifnull((select vote from vote where post_id=p.post_id and avatar_id={}),0) ) as uservote 
                FROM post p, avatar a 
                WHERE p.avatar_id = a.avatar_id AND question_id = {}"""

updateReviewed_sql = """UPDATE post SET reviewed=1 WHERE post_id={}"""

getPostsByTopic_sql = """SELECT post_id as 'key', post_subject as subject, 
                qa_coin_bounty as qacoins, timestamp as date, 
                (select count(*) from post	where question_id = p.post_id) as commentCounts,
                (select count(*) from post where (isnull(reviewed) or reviewed=0) and 
                (post_id=p.post_id or question_id=p.post_id)) as reviewCounts,
                avatar_name as username FROM post p, avatar a 
                WHERE is_question = 1 and p.avatar_id = a.avatar_id and post_id in (select post_id from post_tag where tag_id in (select tag_id from 
                tag_topic where topic_id ={}) and association > {}) and 
                p.section={}
                ORDER BY `timestamp` DESC"""

unreadPosts_parentid_sql = """SELECT post_id FROM post WHERE avatar_id = %s"""

unreadPosts_sql = """SELECT post_content FROM post WHERE is_question = 0 AND parent_id IN (%s) AND read = 0 ORDER BY `timestamp` DESC"""

Posts_sql = "SELECT * FROM post WHERE question_id = %s"

updateThought_select_sql = "SELECT thoughtfulness_score FROM thoughtfulness WHERE posi_id = %s"

updateThought_update_sql = "UPDATE post SET thoughtfulness_score = %s WHERE posi_id = %s"

updateQA_score_sql = "SELECT thoughtfulness_score FROM thoughtfulness WHERE posi_id = %s"

updateQA_QAF_sql = "SELECT qaf FROM qaf WHERE posi_id = %s"

updateQA_update_sql = "UPDATE post SET qa_coin_basic = %s WHERE posi_id = %s"

###Thoughtfulness###
contentOfPost_sql = "SELECT post_content FROM post WHERE post_id = %s"

###vote###
newUpvote_sql = """INSERT INTO vote(avatar_id, post_id, upvote, `timestamp`)
                VALUES(%s, %s, 1, %s)"""

newDownvote_sql = """INSERT INTO vote(avatar_id, post_id, downvote, `timestamp`)
                VALUES(%s, %s, 1, %s)"""

###QAcin###
newUserQA_select_sql = "SELECT SUM(qa_coin_basic), MAX(`timestamp`) FROM post WHERE avatar_id = %s GROUP BY avatar_id"

newUserQA_insert_sql = "INSERT INTO avatar_qa_coin(`timestamp`, qa_coins, avatar_id)VALUES(%s, %s, %s)"

###ThoughtfulnessScore###
newUserThought_select_sql = """SELECT SUM(thoughtfulness_score), MAX(`timestamp`) FROM post
                            WHERE avatar_id = %s GROUP BY avatar_id"""

newUserThought_insert_sql = """INSERT INTO avatar_thoughtfulness_score(`timestamp`, thoughtfulness_score, avatar_id)
                            VALUES(%s, %s, %s)"""

###QAF###
newQAF_select_sql = "SELECT MAX(post_id), MAX(`timestamp`), COUNT(post_id) FROM post WHERE avatar_id = %s GROUP BY avatar_id"

newQAF_insert_sql = "INSERT INTO qaf(avatar_id, post_id, qaf, `timestamp`)VALUES(%s, %s, %s, %s)"

###Tag###
newTag_sql = """INSERT INTO post_tag(tag_id, post_id, association) 
                VALUES {}"""

getTags_sql = """SELECT tag_id AS 'key', tag AS label FROM tag WHERE tag_id IN 
            (SELECT tag_id FROM post_tag WHERE post_id = {} 
            AND association >= {})"""

getAllTags_sql = """SELECT * FROM tag where tag_id in (select tag_id from post_tag where 
                association<={} and post_id={})"""

updatePostTag_sql = """UPDATE post_tag SET association={} WHERE post_id={} and tag_id={}"""

###abandoned_post###
insertAbandonedPost_sql = """INSERT INTO abandoned_post(post_subject, post_content, thoughtfulness_score)
VALUES ('{}','{}',{})"""

deleteAbandonedPost_sql = """DELETE FROM abandoned_post WHERE post_id={}"""

getTopics_sql = "SELECT * FROM topic"

getChatId_sql = """SELECT chat_id from avatar where """

teleNewPost_sql = """INSERT INTO post (avatar_id, post_subject, 
                post_content, level, is_question, is_bot, `timestamp`, 
                is_qa_bountiful, time_limit_qa, time_limit_bot, qa_coin_basic,
                qa_coin_bounty, thoughtfulness_score)
                VALUES ((SELECT avatar_id from avatar where chat_id={}), 
                '{}', '{}', 1, 1, {}, '{}', {}, '{}', '{}', {}, {}, {})"""

teleGetChatId = """select * from avatar where not isnull(chat_id) and
                    chat_id != '' and 
                    section_id=(select section_id from avatar where 
                    chat_id='{}')"""

webGetChatId = """select * from avatar where not isnull(chat_id) and 
                    chat_id != '' and 
                    section_id=(select section_id from avatar where 
                    avatar_id={})"""

teleReplyToPost_insert_sql = """INSERT INTO post (avatar_id, post_content, level, is_question,
                            is_bot, `timestamp`, question_id, qa_coin_basic, 
                            thoughtfulness_score, parent_id)
                            VALUES ((SELECT avatar_id from avatar where chat_id={}),
                             '{}', {}, 0, {}, '{}', {}, {}, {}, {})"""

upsertChatId_sql = """UPDATE avatar SET chat_id='{}' where telegram_account='{}'"""

teleGetStat_sql = """SELECT (qa_gain-qa_lost) AS qacoins, section_id, username, thoughfulness, s0.avatar_id FROM
((SELECT p.avatar_id, a.avatar_name AS username, IFNULL(SUM(qa_coin_basic),0) AS qa_gain, a.section_id,
IFNULL(SUM(thoughtfulness_score),0) AS thoughfulness FROM avatar a, post p WHERE a.avatar_id = p.avatar_id GROUP BY p.avatar_id) s0
JOIN (SELECT avatar_id, IFNULL(SUM(qa_coin_bounty),0) AS qa_lost FROM post WHERE time_limit_qa<CURDATE() and 
avatar_id=(SELECT avatar_id from avatar where chat_id='{}')GROUP BY avatar_id) s1
on s0.avatar_id = s1.avatar_id) ORDER BY thoughfulness DESC """

vote_sql = """INSERT INTO vote (post_id, avatar_id, timestamp, vote) VALUES ({}, {}, '{}', {})
            ON DUPLICATE KEY UPDATE timestamp='{}', vote={}"""

getSessions_sql = """select section_id from ((select avatar_id, section_id from avatar) 
                    union (select avatar_id, section as section_id from a_section) ) 
                     as T where avatar_id ={}"""

getPostsBySection_sql = """SELECT post_id as 'key', post_subject as subject, 
                qa_coin_bounty as qacoins, timestamp as date, 
                (select count(*) from post	where question_id = p.post_id) as commentCounts,
                (select count(*) from post where (isnull(reviewed) or reviewed=0) and 
                (post_id=p.post_id or question_id=p.post_id)) as reviewCounts,
                avatar_name as username FROM post p, avatar a 
                WHERE is_question = 1 and p.avatar_id = a.avatar_id and 
                (section_id='{}')
                ORDER BY `timestamp` DESC"""

getPostsByTopicSection_sql = """SELECT post_id as 'key', post_subject as subject, 
                qa_coin_bounty as qacoins, timestamp as date, 
                (select count(*) from post	where question_id = p.post_id) as commentCounts,
                (select count(*) from post where (isnull(reviewed) or reviewed=0) and 
                (post_id=p.post_id or question_id=p.post_id)) as reviewCounts,
                avatar_name as username FROM post p, avatar a 
                WHERE is_question = 1 and p.avatar_id = a.avatar_id and post_id in (select post_id from post_tag where tag_id in (select tag_id from 
                tag_topic where topic_id ={}) and association > {}) and 
                (p.section_id='{}')
                ORDER BY `timestamp` DESC"""