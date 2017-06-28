import React, { PropTypes } from "react";
import Vehicle from "./Vehicle";
import { Map, TileLayer } from "react-leaflet";
import MarkerClusterGroup from "react-leaflet-markercluster";

//a react component that display the locations of multiple vehicles on a map

class LocationMap extends React.Component {
    render() {
        const data = this.props.data;
        const singapore = [1.36716, 103.80921];
        let vehicles = [];
        let markers = [];
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
        for (let i = 0; i < data.length; i++) {
            markers.push({
                lat: data[i][3],
                lng: data[i][2],
                popup: "Vehicle ID: " + data[i][1] + " Speed: " + data[i][4]
            });
        }

        return (
            <Map center={singapore} zoom={11} maxZoom={19}>
                <TileLayer
                    url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                    attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
                />
                <MarkerClusterGroup
                    markers={markers}
                    wrapperOptions={{ enableDefaultStyle: true }}
                />
            </Map>
        );
    }
}

LocationMap.propTypes = {
    data: PropTypes.array
};

export default LocationMap;
