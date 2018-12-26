import React, { PropTypes } from "react";
import Avatar from 'material-ui/Avatar';
import Subheader from 'material-ui/Subheader';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
import Tag from './tag';
import QuestionReply from './questionReply';
import {connect} from 'react-redux';
import {QuestionReplyOpen} from './../../actions/navAction';
import {DeleteTag} from './../../actions/questionAction';
import NewPostDialog from "./../newPostDialog";
import Vote from "./vote";

class QuestionCard extends React.Component {
    getShortForm(username){
        if(username){
            var fields = username.split(" ");
            var sf_username = fields[0][0].toUpperCase()
            if (fields.length > 1){
            sf_username = sf_username + fields[1][0].toUpperCase()
            }
            return sf_username
        }
        return username
    }
    
    render(){
        const styles = {
            questionCard: {
                paddingBottom: this.props.nav.questionReply?40:60
            }
        }
        return (
            <Card style={styles.questionCard}>
                <CardHeader
                    title={this.props.username}
                    subtitle={this.props.date}
                    avatar={<Avatar>{this.getShortForm(this.props.username)}</Avatar>}
                    />
                <CardTitle title={this.props.subject} />
                    <CardText>
                        {this.props.question}
                    </CardText>
                    <CardText>
                        <Tag
                            tags={this.props.tags}
                            isUser={false}
                            onRequestDelete={this.props.deleteTag}
                            questionId={this.props.questionId}
                            userId={this.props.userId}
                        />
                    </CardText>
                <CardActions style={{float:"right"}}>
                    <div>
                    <span>
                    <Vote 
                        upvotes={this.props.upvotes} 
                        downvotes={this.props.downvotes} 
                        uservote={this.props.uservote}
                        post_id={this.props.questionId}/>
                    </span>
                    <span>
                    <RaisedButton 
                        label={this.props.nav.questionReply?"Cancle":"Reply"}
                        onClick={()=>this.props.questionReplyOpen()}
                    />
                    </span>
                    </div>
                </CardActions>
                <NewPostDialog />
                {this.props.nav.questionReply?
                    <CardText style={{marginTop: 50}}>
                        <QuestionReply />
                    </CardText>:null
                }
            </Card>
        )}
};

QuestionCard.propTypes = {
    username: PropTypes.string,
    date: PropTypes.string,
    subject: PropTypes.string,
    question: PropTypes.string,
    tags: PropTypes.array,
    showReply: PropTypes.func,
    isUser: PropTypes.bool,
    upvotes: PropTypes.any,
    downvotes: PropTypes.any,
    uservote: PropTypes.any
};

const mapStateToProps = (state) => {
  return {
	  nav: state.nav,
      questionId: state.ques.post.question.questionId,
      userId: state.login.user.userId
  };
};

const mapDispatchToProps = (dispatch) => {
    return {
        questionReplyOpen: () => {
            dispatch(QuestionReplyOpen())
        },
        deleteTag: (access_token, post) => {
            dispatch(DeleteTag(access_token, post))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(QuestionCard);