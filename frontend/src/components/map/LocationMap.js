import React, { PropTypes } from "react";
import Vehicle from "./Vehicle";
import { Map, TileLayer } from "react-leaflet";

//a react component that display the locations of multiple vehicles on a map

class LocationMap extends React.Component {
	render() {
		const data = this.props.data;
		const singapore = [1.36716, 103.80921];
		let vehicles = [];
		for (let i = 0; i < data.length; i++) {
			vehicles.push(
				<Vehicle
					gpsNumber={data[i][0]}
					vehicleId={data[i][1]}
					longitude={data[i][2]}
					latitude={data[i][3]}
					speed={data[i][4]}
					timeStamp={data[i][5]}
					overspeed={data[i][6]}
					key={data[i][0]}
				/>
			);
		}
		return (
			<Map center={singapore} zoom={12}>
				<TileLayer
					url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
					attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
				/>
				{vehicles}
			</Map>
		);
	}
}

LocationMap.propTypes = {
	data: PropTypes.array
};

export default LocationMap;
