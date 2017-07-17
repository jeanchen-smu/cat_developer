import React from "react";
import { Card, CardHeader, CardText } from "material-ui/Card";
import axios from "axios";
import {Tabs, Tab} from "material-ui/Tabs";
import FMBarChart from "../dashboard/charts/FMBarChart";
import FMLineChart from "../dashboard/charts/FMLineChart";
import {
    cyan600,
    pink600,
    purple600,
    orange600,
    red600,
    blue600,
    yellow900
} from "material-ui/styles/colors";

const styles = {
    card: {
        marginTop: 30
    }
};

class MileageStats extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.getDefaultState();
    }

    getDefaultState() {
        return {
            graphData: {
                distanceDistribution: [],
                averageDistance: []
            }
        };
    }

    getStatistics() {
        var reqObj = {
            method: "post",
            url: "/api/mileage",
            headers:{
				"Content-Type": "application/json",
				Authorization: "Bearer " + localStorage.getItem("access_token")            
			}, 
            data: {
                month: this.props.month
            }
        };
        axios(reqObj)
            .then(resp => {
                console.log(resp.data);
                this.setState({ graphData: resp.data });
            })
            .catch(err => {
                this.setState(this.getDefaultState());
            });
    }

    componentDidMount() {
        this.getStatistics();
    }

    componentWillReceiveProps(nextProps){
        this.getStatistics();
    }

    render() {
        return (
            <Card style={styles.card}>
                <CardHeader
                    title="Mileage Statistics"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    <Tabs>
                        {/* <Tab label="Mileage Distribution">
                            <FMBarChart
                                headerColor={orange600}
                                title="Driving Distance Distribution"
                                data={this.state.graphData.distanceDistribution}
                                color={blue600}
                            />
                        </Tab> */}
                        <Tab label="Average Distance">
                            <FMLineChart
                                headerColor={pink600}
                                title="Average Driving Distance"
                                data={this.state.graphData.averageDistance}
                                color={purple600}
                            />
                        </Tab>
                    </Tabs>
                </CardText>
            </Card>
        );
    }
}

export default MileageStats;
