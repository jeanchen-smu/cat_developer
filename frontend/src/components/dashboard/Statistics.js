import React from "react";
import { Card, CardHeader, CardText } from "material-ui/Card";
import StatGraphs from "./StatGraphs";
import axios from "axios";

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
            graphData: {
                scoreDistribution: [],
                averageScore: [],
                averageDistance: []
            }
        };
    }

    getStatistics() {
        var reqObj = {
            method: "post",
            url: "/api/stats",
            headers:{
				"Content-Type": "application/json",
				Authorization: "Bearer " + localStorage.getItem("access_token")            
			}, 
            data: {
                startDate: this.props.filterObj.startDate,
                endDate: this.props.filterObj.endDate,
                vehicleList: this.props.filterObj.vehicleList
            }
        };
        axios(reqObj)
            .then(resp => {
                this.setState({ graphData: resp.data });
            })
            .catch(err => {
                this.setState(this.getDefaultState());
            });
    }

    componentWillMount() {
        this.getStatistics();
    }

    componentWillReceiveProps(nextProps){
        this.getStatistics();
    }

    render() {
        return (
            <Card style={styles.card}>
                <CardHeader
                    title="Statistics"
                    subtitle="Distribution & Trends"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    <StatGraphs data={this.state.graphData} />
                </CardText>
            </Card>
        );
    }
}

export default Statistics;
