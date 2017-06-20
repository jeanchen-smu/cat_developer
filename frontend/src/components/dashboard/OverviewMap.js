
import React, {PropTypes} from 'react';
import {Map, TileLayer, LayersControl, FeatureGroup} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import HeatmapLayer from 'react-leaflet-heatmap-layer';
import MarkerClusterGroup from 'react-leaflet-markercluster';
import axios from 'axios';


class OverviewMap extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            coordinates: [] //array of [Lat, Long, Speed] 
        };
        axios.get("/api/overview", {
			Accept: "application/json",
			"Content-Type": "application/json",
            params: {
                vehicleList: this.props.filterObj.vehicleList,
                startDate: this.props.filterObj.startDate,
                endDate: this.props.filterObj.endDate
            }
		})
        .then((resp) =>{
            this.setState({ coordinates: resp.data });
        })
        .catch(
            function(err) {
                this.setState({ coordinates: [] });
                alert("Fetch error: " + err);
            }.bind(this)
        );
    }

    render() {
        const singapore = [1.36716,103.80921];
        
        let markers = [];
        const coordinates = this.state.coordinates;
        for (let i = 0; i < coordinates.length; i++) {
            markers.push({
                lat: coordinates[i][0], 
                lng: coordinates[i][1], 
                popup: 'Vehicle ID: ' + coordinates[i][3] + ' Speed: ' + coordinates[i][2]});
        }
        console.log(markers);
        
        return (
            <div>
                <Map center={singapore} zoom={11} maxZoom={19}>
                    <LayersControl>
                        <LayersControl.BaseLayer name="Base" checked>
                            <TileLayer
                            url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                            attribution="&copy; <a href=http://osm.org/copyright>OpenStreetMap</a> contributors"
                            />
                        </LayersControl.BaseLayer>
                        <LayersControl.Overlay name="Heatmap" checked>
                            <FeatureGroup color="purple">
                            <HeatmapLayer
                                points={coordinates}
                                longitudeExtractor={m => m[1]}
                                latitudeExtractor={m => m[0]}
                                intensityExtractor={m => parseFloat(m[2])}
                            />
                            </FeatureGroup>
                        </LayersControl.Overlay>
                        <LayersControl.Overlay name="Markers">
                            <FeatureGroup color="purple">
                            <MarkerClusterGroup
                                markers={markers}
                                wrapperOptions={{enableDefaultStyle: true}}
                            />
                            </FeatureGroup>
                        </LayersControl.Overlay>
                    </LayersControl>
                </Map>
            </div>
        );
    }

}

OverviewMap.propTypes = {
	filterObj: PropTypes.object
};

export default OverviewMap;