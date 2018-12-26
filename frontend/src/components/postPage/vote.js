import React, { PropTypes } from "react";
import ThumbsDown from 'react-icons/lib/fa/thumbs-o-down'; 
import ThumbsUp from 'react-icons/lib/fa/thumbs-o-up'; 
import FaThumbsUp from 'react-icons/lib/fa/thumbs-up';
import FaThumbsDown from 'react-icons/lib/fa/thumbs-down';
import {blue400} from "material-ui/styles/colors";
import IconButton from "material-ui/IconButton";
import {VoteClick, NeedImprovementOpenClick} from './../../actions/questionAction';
import {connect} from 'react-redux';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import Dialog from 'material-ui/Dialog';

class Vote extends React.Component {
    voteObj(post_id, vote) {
        return {
            questionId: this.props.questionId,
            post_id: post_id,
            avatar_id: this.props.userId,
            vote: vote
        }
    }

    upVoteClick() {
        if (this.props.uservote==1){
            this.props.voteClick(
            sessionStorage.getItem("access_token"),
            this.voteObj(this.props.post_id, 0)
        )
    }
        else if(!this.props.uservote){
            this.props.voteClick(
            sessionStorage.getItem("access_token"),
            this.voteObj(this.props.post_id, 1)
        )
        }
    
    }

    downVoteClick() {
        console.log(this.props.post_id)
        this.props.voteClick(
            sessionStorage.getItem("access_token"),
            this.voteObj(this.props.impPostId, 2)
        )
        this.props.needImprovementOpenClick();
    }

    render() {
        return (
            <span style={{paddingRight: 15, marginBottom: 30}}>
                <span style={{paddingRight: 15}}>
                    <IconButton 
                        iconStyle={{paddingBottom: 15}}
                        onClick={()=>{this.upVoteClick()}}
                        disabled={this.props.uservote == 2}
                    >
                        {
                            this.props.uservote == 1?
                            <FaThumbsUp color={blue400} size={25} />:
                            <ThumbsUp color={blue400} size={25} />       
                        }
                    </IconButton>
                    <span>
                    {this.props.upvotes}
                    </span>
                </span>
                <span style={{paddingRight: 15}}>
                    <RaisedButton 
                        label={this.props.uservote == 2?
                            "Improvement Sent ("+this.props.downvotes+")":
                            "Need Impovement ("+this.props.downvotes+")"}
                        disabled={this.props.uservote == 2|this.props.uservote == 1}
                        onClick={()=>this.props.needImprovementOpenClick(this.props.post_id)}
                    />
                    {this.props.qaCoins>=125?
                    <Dialog
                        title="Suggest Improvement"
                        actions={
                        [<FlatButton
                            label="Yes"
                            primary={true}
                            keyboardFocused={true}
                            onClick={()=>this.downVoteClick()}
                        />,
                        <FlatButton
                            label="No"
                            primary={true}
                            onClick={()=>this.props.needImprovementOpenClick()}
                        />]}
                        modal={false}
                        open={this.props.needImp}
                    >
                        By clicking on "Yes", it will cost you 1 QA coin.
                        Are you sure to proceed?
                    </Dialog>:
                    <Dialog
                        title="Insufficient QA Coins"
                        modal={false}
                        open={this.props.needImp}
                    >
                        You do not have sufficient QA coins.
                    </Dialog>
                    }
                </span>
            </span>
        );
    }
}

Vote.propTypes = {
    upvotes: PropTypes.any,
    downvotes: PropTypes.any,
    uservote: PropTypes.any,
    post_id: PropTypes.any
};

const mapStateToProps = (state) => {
  return {
	  errorVote: state.nav.errorVote,
      questionId: state.ques.post.question.questionId,
      userId: state.login.user.userId,
      needImp: state.ques.needImp,
      qaCoins: state.stat.stat.qacoins,
      impPostId: state.ques.impPostId
  };
};

const mapDispatchToProps = (dispatch) => {
    return {
        voteClick: (access_token, vote) => {
            dispatch(VoteClick(access_token, vote))
        },
        needImprovementOpenClick: (post_id) => {
            dispatch(NeedImprovementOpenClick(post_id))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Vote);