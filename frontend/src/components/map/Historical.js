import React, { PropTypes } from "react";
import RouteMap from "./RouteMap";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import Data from "../../data";

class Historical extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			tripData: [] //array of [vehicleID, coordinates]
		};
		axios
			.get("/api/historical", {
				Accept: "application/json",
				"Content-Type": "application/json"
			})
			.then(resp => {
				this.setState({ tripData: resp.data });
			})
			.catch(err => {
				this.setState({ tripData: [] });
				alert("Fetch error in Historical: " + err);
			});
	}

	componentWillMount() {
		axios
			.get("/api/historical", {
				Accept: "application/json",
				"Content-Type": "application/json"
			})
			.then(resp => {
				this.setState({ tripData: resp.data });
			})
			.catch(err => {
				this.setState({ tripData: [] });
				alert("Fetch error in Historical: " + err);
			});
	}

	render() {
		let routes = this.state.tripData.slice(0, 1);
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
