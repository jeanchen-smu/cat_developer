import React, { PropTypes } from "react";
import Dialog from 'material-ui/Dialog';

class ErrorVote extends React.Component {

    render() {
        return (
            <Dialog
                modal={false}
                open={this.props.errorVote}
                onRequestClose={this.props.handleClose}
            >
                You have voted for the post.
            </Dialog>
        );
    }
}

ErrorVote.propTypes = {
    errorVote: PropTypes.bool,
    handleClose: PropTypes.func
};

export default ErrorVote;