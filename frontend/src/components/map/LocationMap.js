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
                    vehicleId={data[i].VehicleID}
                    longitude={data[i].Lon}
                    latitude={data[i].Lat}
                    speed={data[i].Speed}
                    timeStamp={data[i].DeviceTS}
                    overspeed={0}
                    key={data[i].VehicleID}
                />
            );
        }
        for (let i = 0; i < data.length; i++) {
            markers.push({
                lat: data[i].Lat,
                lng: data[i].Lon,
                popup: "Vehicle ID: " + data[i].VehicleID + " Speed: " + data[i].Speed
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
