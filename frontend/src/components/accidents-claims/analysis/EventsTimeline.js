import React from "react";
import { Card, CardHeader, CardText } from "material-ui/Card";
import {
    ResponsiveContainer,
    ComposedChart,
    Area,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend
} from "recharts";
import axios from "axios";
import {
    cyan600,
    blue600
} from "material-ui/styles/colors";

const styles = {
    card: {
        marginTop: 30
    },
    div: {
        marginLeft: "auto",
        marginRight: "auto",
        width: "90%",
        height: 300,
        paddingTop: 20,
        paddingBottom: 20
    }
};

class EventsTimeline extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.getDefaultState();
    }

    getDefaultState() {
        return {
            graphData: {
                speedEvents: []
            }
        };
    }

    getGraphData() {
        /*var reqObj = {
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
                this.setState({ getGraphData: resp.data });
            })
            .catch(err => {
                this.setState(this.getDefaultState());
            });*/

        this.setState({
            graphData: {
                speedEvents: [
                    { name: "10:05", speed: 60, accelG: 0 },
                    { name: "10:10", speed: 80, accelG: 1 },
                    { name: "10:15", speed: 50, accelG: 0 },
                    { name: "10:20", speed: 50, accelG: 0 },
                    { name: "10:25", speed: 40, accelG: 0 },
                    { name: "10:30", speed: 90, accelG: 1.8 },
                    { name: "10:35", speed: 0, accelG: 3 },
                    { name: "10:40", speed: 0, accelG: 0 }
                ]
            }
        });
    }

    componentDidMount() {
        this.getGraphData();
    }

    componentWillReceiveProps(nextProps) {
        this.getGraphData();
    }

    render() {
        return (
            <Card style={styles.card}>
                <CardHeader
                    title="Max Speed/Harsh Events"
                    subtitle="Max speed and harsh acceleration/braking events before the crash"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    <div style={styles.div}>
                        <ResponsiveContainer>
                            <ComposedChart
                                data={this.state.graphData.speedEvents}
                                margin={{
                                    top: 5,
                                    right: 10,
                                    left: 10,
                                    bottom: 5
                                }}
                            >
                                <XAxis dataKey="name" />
                                <YAxis
                                    yAxisId="left"
                                    orientation="left"
                                    label="Km/Hr"
                                    stroke={cyan600}
                                />
                                <YAxis
                                    yAxisId="right"
                                    orientation="right"
                                    label="G's"
                                    stroke={blue600}
                                />
                                <Tooltip />
                                <Legend />
                                <CartesianGrid stroke="#f5f5f5" />
                                <Area
                                    yAxisId="left"
                                    type="monotone"
                                    dataKey="speed"
                                    fill={cyan600}
                                    stroke={cyan600}
                                />
                                <Bar
                                    yAxisId="right"
                                    dataKey="accelG"
                                    barSize={20}
                                    fill={blue600}
                                />
                            </ComposedChart>
                        </ResponsiveContainer>
                    </div>
                </CardText>
            </Card>
        );
    }
}

export default EventsTimeline;
