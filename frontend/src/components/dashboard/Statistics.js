import React from "react";
import { Card, CardHeader, CardText } from "material-ui/Card";
import StatGraphs from "./StatGraphs";

const styles = {
    card: {
        marginTop: 30
    }
};

class Statistics extends React.Component {
    render() {
        return (
            <Card style={styles.card}>
                <CardHeader
                    title="Statistics"
                    subtitle="Statistics Graphs"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    <StatGraphs />
                </CardText>
            </Card>
        );
    }
}

export default Statistics;
