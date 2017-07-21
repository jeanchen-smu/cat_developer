import React from "react";
import { Card, CardHeader, CardText } from "material-ui/Card";
import TextField from "material-ui/TextField";
import RaisedButton from "material-ui/RaisedButton";

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
            <Card  expanded={true} style={{marginTop:30, width:"60%"}}>
                <CardHeader title="Upload Claims File" style={{fontWeight:"normal"}}/>
                <CardText expandable={true}>
                    <div>
                        <TextField hintText="Please select file name" style={{width:"80%"}}/>
                        <RaisedButton label="Upload" primary={true} style={{ margin: 10 }} />
                    </div>
                </CardText>
            </Card>
        );
    }
}

export default ClaimsUploader;
