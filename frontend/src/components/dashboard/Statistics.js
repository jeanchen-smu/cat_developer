import React from "react";
import { Card, CardHeader, CardText } from "material-ui/Card";
import StatGraphs from "./StatGraphs";
import Data from "../../data";

const styles = {
    card: {
        marginTop: 30
    }
};

class Statistics extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.getDefaultState();
    }

    getDefaultState() {
        return {
            graphData: Data.dashBoardPage
        };
    }

    getStatistics() {
        var reqObj = {
            method: "post",
            url: "/api/stats",
            headers: {
                "Content-Type": "application/json"
            },
            data: {
                startDate: this.props.startDate,
                endDate: this.props.endDate,
                vehicleList: this.props.vehicleList
            }
        };
        axios(reqObj)
            .then(resp => {
                this.setState({
                    graphData: resp.data
                });
            })
            .catch(err => {
                this.setState(this.getDefaultState());
            });
    }

    componentWillMount() {
        this.getStatistics();
    }

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
                    <StatGraphs data={Data.dashBoardPage}/>
                </CardText>
            </Card>
        );
    }
}

export default Statistics;
