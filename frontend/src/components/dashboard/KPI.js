import React from 'react';
import {cyan600, pink600, purple600, orange600, red600, blue600} from 'material-ui/styles/colors';
import {Card, CardHeader, CardText} from 'material-ui/Card'; 
import DirectionsCar from 'material-ui/svg-icons/maps/directions-car';
import SwapCalls from 'material-ui/svg-icons/communication/swap-calls';
import Alarm from 'material-ui/svg-icons/action/alarm';
import Gesture from 'material-ui/svg-icons/content/gesture';
import Hotel from 'material-ui/svg-icons/maps/hotel';
import Warning from 'material-ui/svg-icons/alert/warning';
import InfoBox from './InfoBox';  

class KPI extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            coordinates: [] //array of [Lat, Long, Speed] 
        };
        axios.get("/api/overview", {
			Accept: "application/json",
			"Content-Type": "application/json",
            params: {
                vehicleList: this.props.filterObj.vehicleList,
                startDate: this.props.filterObj.startDate,
                endDate: this.props.filterObj.endDate
            }
		})
        .then((resp) =>{
            this.setState({ coordinates: resp.data });
        })
        .catch(
            function(err) {
                this.setState({ coordinates: [] });
                alert("Fetch error: " + err);
            }.bind(this)
        );
    }
    
    render(){
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
                    <InfoBox Icon={DirectionsCar}
                            color={pink600}
                            title="Active Vehicles"
                            value="1500"
                    />
                </div>

                <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                    <InfoBox Icon={SwapCalls}
                            color={cyan600}
                            title="Total Distance"
                            value="4231km"
                    />
                </div>

                <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                    <InfoBox Icon={Alarm}
                            color={purple600}
                            title="Longest Time"
                            value="4.60h"
                    />
                </div>

                <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                    <InfoBox Icon={Gesture}
                            color={orange600}
                            title="Longest Distance"
                            value="248km"
                    />
                </div>

                <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                    <InfoBox Icon={Hotel}
                            color={blue600}
                            title="Total Idling"
                            value="1.2h"
                    />
                </div>

                <div className="col-xs-12 col-sm-6 col-md-4 col-lg-4 m-b-15 ">
                    <InfoBox Icon={Warning}
                            color={red600}
                            title="Lowest Score"
                            value="74/100"
                    />
                </div>
                </div>
                </CardText>
            </Card>
        );
    };
};

export default KPI;
