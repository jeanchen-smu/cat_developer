import React from "react";
import {
    cyan600,
    pink600,
    purple600,
    orange600,
    red600,
    blue600
} from "material-ui/styles/colors";
import { Card, CardHeader, CardText } from "material-ui/Card";
import DirectionsCar from "material-ui/svg-icons/maps/directions-car";
import SwapCalls from "material-ui/svg-icons/communication/swap-calls";
import Alarm from "material-ui/svg-icons/action/alarm";
import Gesture from "material-ui/svg-icons/content/gesture";
import Hotel from "material-ui/svg-icons/maps/hotel";
import Warning from "material-ui/svg-icons/alert/warning";
import InfoBox from "./InfoBox";
import axios from "axios";

class Kpi extends React.Component {
    constructor(props) {
        super(props);
        this.state = this.getDefaultState();
    }

    getDefaultState() {
        return {
            activeVehicles: 0,
            totalDistance: 0,
            longestRideTime: 0,
            longestRideDistance: 0,
            totalIdling: 0,
            lowestScore: 0
        };
    }

    getKpi() {
        var reqObj = {
            method: "post",
            url: "/api/kpi",
            headers: {
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
                this.setState({
                    activeVehicles: resp.data.activeVehicles,
                    totalDistance: resp.data.totalDistance,
                    longestRideTime: resp.data.longestRideTime,
                    longestRideDistance: resp.data.longestRideDistance,
                    totalIdling: resp.data.totalIdling,
                    lowestScore: resp.data.lowestScore
                });
            })
            .catch(err => {
                this.setState(this.getDefaultState());
            });
    }

    componentDidMount() {
        this.getKpi();
    }

    componentWillReceiveProps(nextProps){
        this.getKpi();
    }

    render() {
        return (
            <Card initiallyExpanded={true}>
                <CardHeader
                    title="KPI"
                    subtitle="Key Performance Indicators"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    <div className="row">
                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={DirectionsCar}
                                color={pink600}
                                title="Active Vehicles"
                                value={this.state.activeVehicles.toString()}
                            />
                        </div>

                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={SwapCalls}
                                color={cyan600}
                                title="Total Distance"
                                value={this.state.totalDistance.toFixed(0) + " km"}
                            />
                        </div>

                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={Alarm}
                                color={purple600}
                                title="Longest Ride Time"
                                value={this.state.longestRideTime.toFixed(2) + " h"}
                            />
                        </div>

                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={Gesture}
                                color={orange600}
                                title="Longest Ride Distance"
                                value={this.state.longestRideDistance.toFixed(0) + " km"}
                            />
                        </div>

                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={Hotel}
                                color={blue600}
                                title="Total Idling"
                                value={this.state.totalIdling.toFixed(2) + " h"}
                            />
                        </div>

                        <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                            <InfoBox
                                Icon={Warning}
                                color={red600}
                                title="Lowest Score"
                                value={(this.state.lowestScore.toFixed(2)*100).toString()}
                            />
                        </div>
                    </div>
                </CardText>
            </Card>
        );
    }
}

export default Kpi;
