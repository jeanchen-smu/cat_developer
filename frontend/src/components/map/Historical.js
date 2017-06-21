import React, { PropTypes } from "react";
import RouteMap from "./RouteMap";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import Data from "../../data";

class Historical extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			tripData: [] //array of [vehicleID, positions]
		};
	}

	componentWillMount() {
		axios
			.get("/api/historical", {
				Accept: "application/json",
				"Content-Type": "application/json",
				params: {
					vehicleList: this.props.filterObj.vehicleList,
					startDate: this.props.filterObj.startDate,
					endDate: this.props.filterObj.endDate
				}
			})
			.then(resp => {
				console.log(resp.data)
				this.setState({ tripData: resp.data });
			})
			.catch(err => {
				this.setState({ tripData: [] });
				alert("Fetch error in Historical: " + err);
			});
	}

	render() {
		let routes = this.state.tripData.slice(0, 1);
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
