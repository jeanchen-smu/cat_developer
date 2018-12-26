import React, { PropTypes } from "react";
import Avatar from 'material-ui/Avatar';
import Subheader from 'material-ui/Subheader';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
import AnswerReply from './answerReply';
import {connect} from 'react-redux';
import {AnswerReplyOpen, AnswerReplyClose} from './../../actions/navAction';
import SubAnswer from "./subAnswerList";
import QuestionThoughtfulness from "./questionThoughtfulness";
import NewPostDialog from "./../newPostDialog";
import Vote from "./vote";

class AnswerCard extends React.Component {
    handleAnswerReply(answer) {
        if (this.props.nav.answerReply==answer.answerId){
            this.props.answerReplyClose();
        }else{
            this.props.answerReplyOpen(answer);
        }
    }

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
            answerCard: {
                marginTop: 5,
                paddingBottom: (this.props.nav.answerReply==this.props.answerId)?35:0
            }
        }
        
    return (
      <Card 
        style={styles.answerCard}
        key={this.props.key}
      >
        <CardHeader
            title={this.props.username}
            subtitle={this.props.date}
            avatar={<Avatar>{this.getShortForm(this.props.username)}</Avatar>}
            />
        <CardText>
            {this.props.answer}
        </CardText>
        <CardActions style={{float: "right"}}>
            <div>
            <span>
            <Vote 
                upvotes={this.props.upvotes} 
                downvotes={this.props.downvotes} 
                uservote={this.props.uservote}
                post_id={this.props.answerId}/>
            </span>
            <span>
            <RaisedButton 
                label={this.props.nav.answerReply == this.props.answerId?"Cancel":"Reply"}
                onClick={()=>this.handleAnswerReply(
                    {
                        answerId: this.props.answerId,
                        level: this.props.level
                    }
                )}
            />
            </span>
            </div>
            
        </CardActions>
        <NewPostDialog />
        {this.props.nav.answerReply == this.props.answerId?
            <CardText style={{marginTop:40}}>
                <AnswerReply />
            </CardText>:null
        }
        {
            this.props.isTeacher?<QuestionThoughtfulness post={{
            post_id: this.props.answerId,
            thoughtfulness_score: this.props.thoughtfulness_score,
            reviewed: this.props.reviewed
            }}/>:null
        }
        <CardText style={{marginTop:30}}>
        {this.props.nav.answerReply == this.props.answerId?
            null:<SubAnswer
                subAnswer={this.props.subAnswer}
            />
        }
        </CardText>  
    </Card>
    )
    }
};

AnswerCard.propTypes = {
    key: PropTypes.any,
    username: PropTypes.string,
    date: PropTypes.string,
    answer: PropTypes.string,
    answerId: PropTypes.any,
    subAnswer: PropTypes.array,
    level: PropTypes.any,
    thoughtfulness_score: PropTypes.any,
    reviewed: PropTypes.any,
    upvotes: PropTypes.any,
    downvotes: PropTypes.any,
    uservote: PropTypes.any
};

const mapStateToProps = (state) => {
  return {
	  nav: state.nav,
      isTeacher: state.login.user.is_teacher
  };
};

const mapDispatchToProps = (dispatch) => {
    return {
        answerReplyOpen: (answerId) => {
            dispatch(AnswerReplyOpen(answerId))
        },
        answerReplyClose: () => {
            dispatch(AnswerReplyClose())
        }
        
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(AnswerCard);