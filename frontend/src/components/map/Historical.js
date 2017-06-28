import React, { PropTypes } from "react";
import RouteMap from "./RouteMap";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import Data from "../../data";

class Historical extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			mapData: [] //array of [vehicleID, positions]
		};
	}

	getMapData() {
        var reqObj = {
            method: "post",
            url: "/api/historical",
            headers: {
                "Content-Type": "application/json"
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
                this.setState({ mapData: [] });
            });
    }

	componentWillMount() {
		this.getMapData();
	}

	render() {
		let routes = this.state.mapData.slice(0, 1);
		{/*let routes = this.state.tripData;*/}
		return (
			<div>
				<RouteMap routes={routes} />
			</div>
		);
	}
}

Historical.propTypes = {
	filterObj: PropTypes.object
};

export default Historical;
