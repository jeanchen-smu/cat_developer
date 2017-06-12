import React, { PropTypes } from "react";
import Journey from "./Journey";
import { Map, TileLayer } from "react-leaflet";

//a react component that display the routes taken by multiple vehicles on a map

class RouteMap extends React.Component {
	render() {
		const routes = this.props.routes;
		const singapore = [1.36716, 103.80921];

		let journeys = [];
		for (let i = 0; i < routes.length; i++) {
			journeys.push(
				<Journey
					vehicleID={routes[i][0]}
					positions={routes[i][1]}
					key={routes[i][0]}
				/>
			);
		}

		return (
			<Map center={singapore} zoom={12}>
				<TileLayer
					url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
					attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
				/>
				{journeys}
			</Map>
		);
	}
}

RouteMap.propTypes = {
	routes: PropTypes.array
};

export default RouteMap;
