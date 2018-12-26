export function ErrorVoteOpen(){
    return {type: "ERROR_VOTE_OPEN"}
}

export function ErrorVoteClose(){
    return {type: "ERROR_VOTE_CLOSE"}
}

function VoteClickReqObj(access_token, vote){
    return {
        method: "post",
        url: "/cat/api/vote",
        headers:{
            "Content-Type": "application/json",
            Authorization: "Bearer " + access_token,       
        }, 
        data: {
            vote: vote
        }
    };
}

export function VoteClick(access_token, vote){
    return function(dispatch){
        axios(VoteClickReqObj(access_token, vote))
            .then(response => {
                dispatch ({type: "UPDATE_VOTE_SUCCESSFUL", payload: response.data})
            })
            .catch(err => {
                dispatch ({type: "UPDATE_VOTE_FAIL", payload: err})
            })
    }
}
