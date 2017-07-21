import React, { PropTypes } from "react";
import { Card, CardHeader, CardText } from "material-ui/Card";
//import axios from "axios";

const styles = {
    card: {
        marginTop: 30
    },
    image: {
        height: '100px',
        width: '150px'
    }
};

class Reconstruction extends React.Component {

    render() {
        return (
            <Card style={styles.card}>
                <CardHeader
                    title="Accident Reconstruction"
                    subtitle="Possible impact region on the vehicle"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    <div>
                        <img src={require("../../../images/collision_image.jpg")} />
                    </div>
                </CardText>
            </Card>
        );
    }
}

export default Reconstruction;