import React, { PropTypes } from "react";
import { Map, TileLayer, LayersControl, FeatureGroup, Marker, Popup } from "react-leaflet";
import { Card, CardHeader, CardText } from "material-ui/Card";
import "leaflet/dist/leaflet.css";
import Journey from "../../map/Journey";
import axios from "axios";

const styles = {
    card: {
        marginTop: 30
    }
};

const data = {
    coordinates: [{
      "DeviceTS": "2017-07-19T15:25:14.000000+08:00", 
      "Lat": 1.3718202438102371, 
      "Lon": 103.89909170019982, 
      "OverSpeed": 0, 
      "Speed": 0, 
      "VehicleID": 32455
    }, 
    {
      "DeviceTS": "2017-07-19T17:06:45.000000+08:00", 
      "Lat": 1.3718202438102371, 
      "Lon": 103.89909170019982, 
      "OverSpeed": 0, 
      "Speed": 0, 
      "VehicleID": 32455
    }, 
    {
      "DeviceTS": "2017-07-19T17:07:04.000000+08:00", 
      "Lat": 1.3718202438102371, 
      "Lon": 103.89909170019982, 
      "OverSpeed": 0, 
      "Speed": 0, 
      "VehicleID": 32455
    }, 
    {
      "DeviceTS": "2017-07-19T17:07:24.000000+08:00", 
      "Lat": 1.3718202438102371, 
      "Lon": 103.89909170019982, 
      "OverSpeed": 0, 
      "Speed": 0, 
      "VehicleID": 32455
    }, 
    {
      "DeviceTS": "2017-07-19T17:07:44.000000+08:00", 
      "Lat": 1.3718202438102371, 
      "Lon": 103.89909170019982, 
      "OverSpeed": 0, 
      "Speed": 0, 
      "VehicleID": 32455
    }, 
    {
      "DeviceTS": "2017-07-19T17:07:45.000000+08:00", 
      "Lat": 1.3718202438102371, 
      "Lon": 103.89909170019982, 
      "OverSpeed": 0, 
      "Speed": 0, 
      "VehicleID": 32455
    }, 
    {
      "DeviceTS": "2017-07-19T17:08:04.000000+08:00", 
      "Lat": 1.3718202438102371, 
      "Lon": 103.89909170019982, 
      "OverSpeed": 0, 
      "Speed": 0, 
      "VehicleID": 32455
    }, 
    {
      "DeviceTS": "2017-07-19T17:08:20.000000+08:00", 
      "Lat": 1.3730967937777887, 
      "Lon": 103.90001874591235, 
      "OverSpeed": -42, 
      "Speed": 8, 
      "VehicleID": 32455
    }, 
    {
      "DeviceTS": "2017-07-19T17:08:24.000000+08:00", 
      "Lat": 1.3731581002618678, 
      "Lon": 103.89993910477882, 
      "OverSpeed": -31, 
      "Speed": 19, 
      "VehicleID": 32455
    }, 
    {
      "DeviceTS": "2017-07-19T17:08:25.000000+08:00", 
      "Lat": 1.3731581002618678, 
      "Lon": 103.89993910477882, 
      "OverSpeed": -31, 
      "Speed": 19, 
      "VehicleID": 32455
    }, 
    {
      "DeviceTS": "2017-07-19T17:08:28.000000+08:00", 
      "Lat": 1.3731581002618678, 
      "Lon": 103.89993910477882, 
      "OverSpeed": -31, 
      "Speed": 19, 
      "VehicleID": 32455
    }, 
    {
      "DeviceTS": "2017-07-19T17:08:44.000000+08:00", 
      "Lat": 1.373531668744293, 
      "Lon": 103.89953115882868, 
      "OverSpeed": 0, 
      "Speed": 0, 
      "VehicleID": 32455
    }],
    events: {
        "Harsh Braking": [
            {
                "Lat": 1.373531668744293, 
                "Long": 103.89953115882868, 
                "DeviceTS": "2017-07-19 15:59:54",
                "Speed": 1 
            }
        ],
        "Harsh Acceleration": [
            {                
                "Lat": 1.3718202438102371, 
                "Long": 103.89909170019982, 
                "DeviceTS": "2017-07-19 17:06:45", 
                "Speed": 0
            }, 
        ]
    }
};

class TripRoute extends React.Component {

    constructor(props) {
        super(props);
        this.state = this.getDefaultState();
    }

    getDefaultState() {
        return {
            accidentData: {
                coordinates: [],
                events: {}
			}
        };
    }

    getMapData() { 
        /*
		var reqObj = {
            method: "post",
            url: "/api/accident",
			headers:{
				"Content-Type": "application/json",
				Authorization: "Bearer " + localStorage.getItem("access_token")            
			}, 
			data: {
				startDate: this.props.filterObj.startDate,
				endDate: this.props.filterObj.endDate,
                vehicleList: this.props.filterObj.vehicleList
			}
        };
		axios(reqObj)
			.then(resp => {
				this.setState({ accidentData: resp.data });
			})
			.catch(err => {
				this.setState( this.getDefaultState() );
            });
        */
        this.setState({ accidentData: data });
    }

    getTrip() {
        const coordinates = this.state.accidentData.coordinates;
        //const vehicleID = this.props.vehicleList[0];
        const vehicleID = "32455";

        return (
            <Journey 
                vehicleID={vehicleID} 
                positions={coordinates}
            />);
    }

    getEventFilters() {
        let events = this.state.accidentData.events;
        let eventFilters = []
        for (var eventType in events) {
            eventFilters.push(
                <LayersControl.Overlay name={eventType} checked key={eventType}>
                    <FeatureGroup color="purple">
                        {events[eventType].map((event)=>(
                            <Marker position={[event.Lat, event.Long]} key={event.DeviceTS}>
                                <Popup>
                                    <p>
                                        <b>Time: </b>{event.DeviceTS}<br/>
                                        <b>Speed: </b>{event.Speed}<br/>
                                        <b>Event: </b>{eventType}
                                    </p>
                                </Popup>
                            </Marker>))}
                    </FeatureGroup>
                </LayersControl.Overlay>
            );
        }
        return eventFilters;
    }

    componentDidMount() {
        this.getMapData();
    }

    componentWillReceiveProps(nextProps) {
        this.getMapData();
    }

    render() {
        const singapore = [1.36716, 103.80921];
        return (
            <Card style={styles.card}>
                <CardHeader
                    title="Trip Details"
                    subtitle="Route taken by the vehicle on the day of accident"
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    <Map center={singapore} zoom={11} maxZoom={19}>
                        <LayersControl>
                            <TileLayer
                                url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                                attribution="&copy; <a href=http://osm.org/copyright>OpenStreetMap</a> contributors"
                            />
                            {this.getEventFilters()}
                        </LayersControl>
                        {this.getTrip()}
                    </Map>
                </CardText>
            </Card>
        );
    }
}

TripRoute.propTypes = {
    coordinates: PropTypes.array,
    events: PropTypes.object,
    vehicle: PropTypes.string
};

export default TripRoute;