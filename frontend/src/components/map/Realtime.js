import React, { PropTypes } from "react";
import LocationMap from "./LocationMap";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import Data from "../../data";

class Realtime extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			data: []
		};
		
	}

	componentWillMount() {
		this.updateData();
	}

	componentDidMount() {
		this.timerID = setInterval(this.updateData.bind(this), 30000);
	}

	componentWillUnmount(){
		clearInterval(this.timerID);
	}

	updateData() {
		axios
			.get("/api/realtime", {
				Accept: "application/json",
				"Content-Type": "application/json"
			})
			.then(resp => {
				console.log(resp.data);
				this.setState({ data: resp.data });
			})
			.catch(err => {
				this.setState({ data: [] });
				alert("Fetch error in Realtime: " + err);
			});
	}

	render() {
		let { data } = this.state;
		return (
			<div>
				<LocationMap data={data} />
			</div>
		);
	}
}

Realtime.propTypes = {
	vehicleList: PropTypes.array
};

export default Realtime;
