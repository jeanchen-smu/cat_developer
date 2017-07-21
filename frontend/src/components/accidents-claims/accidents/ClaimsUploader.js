import React from "react";
import Paper from "material-ui/Paper";
import Subheader from "material-ui/Subheader";
import TextField from "material-ui/TextField";
import RaisedButton from "material-ui/RaisedButton";

const styles = {
    div:{
        marginLeft:30,
        paddingBottom:30
    }, 

    button: {
        margin: 12
    },
    fileOpen: {
        cursor: "pointer",
        position: "absolute",
        top: 0,
        bottom: 0,
        right: 0,
        left: 0,
        width: "100%",
        opacity: 0
    }
};
class ClaimsUploader extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.getDefaultState();
    }

    getDefaultState() {
        return {
            fileName: ""
        };
    }

    render() {
        return (
            <Paper>
                <Subheader>Upload Claims File</Subheader>
                <div style={styles.div}>
                    <TextField hintText="Please select file name" style={{ width: 400 }} />
                    <RaisedButton
                        primary={true}
                        label="Upload"
                        labelPosition="before"
                        style={styles.button}
                        containerElement="label"
                    >
                        <input type="file" style={styles.fileOpen} />
                    </RaisedButton>
                </div>
            </Paper>
        );
    }
}

export default ClaimsUploader;
