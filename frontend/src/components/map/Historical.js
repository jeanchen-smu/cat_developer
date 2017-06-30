import React, { PropTypes } from "react";
import RouteMap from "./RouteMap";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import Data from "../../data";

class Historical extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			//{vehicle_id:[{Lat:##, Lon:##, Speed:##, OverSpeed:##, DeviceTS:##},]}
			mapData: {} 
		};
	}

	getMapData() {
        var reqObj = {
            method: "post",
            url: "/api/historical",
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
                this.setState({ mapData: resp.data });
            })
            .catch(err => {
                this.setState({ mapData: {} });
            });
    }

	componentDidMount() {
		this.getMapData();
	}

	componentWillReceiveProps(nextProps){
        this.getMapData();
    }

	render() {
		return (
			<div>
				<RouteMap routes={this.state.mapData} />
			</div>
		);
	}
}

Historical.propTypes = {
	filterObj: PropTypes.object
};

export default Historical;
