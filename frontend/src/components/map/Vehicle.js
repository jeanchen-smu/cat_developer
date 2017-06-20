import React, {PropTypes} from "react";
import { Marker, Popup, CircleMarker } from "react-leaflet";

class Vehicle extends React.Component {
	render() {
		const position = [this.props.latitude, this.props.longitude];
		const overspeed = this.props.overspeed > 0;

		return (
			<div>
				<Marker position={position} title={this.props.vehicleId}>
					<Popup>
						<p>
							<b>Vehicle ID: </b>{this.props.vehicleId}<br />
							<b>Time: </b>{this.props.timeStamp}<br />
							<b>Speed: </b>{this.props.speed}
						</p>
					</Popup>
				</Marker>
				{overspeed &&
					<CircleMarker
						center={position}
						radius={5}
						fillOpacity={0.3}
						opacity={0.0}
						color="red"
					/>}
			</div>
		);
	}
}

Vehicle.propTypes = {
	latitude: PropTypes.number,
	longitude: PropTypes.number,
	overspeed: PropTypes.number,
	vehicleId: PropTypes.string,
	timeStamp: PropTypes.string,
	speed: PropTypes.number
};

export default Vehicle;
