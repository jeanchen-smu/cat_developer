import React, { PropTypes } from "react";
import { Map, TileLayer, LayersControl, FeatureGroup, Marker, CircleMarker, Circle, Popup } from "react-leaflet";
import { Card, CardHeader, CardText } from "material-ui/Card";
import "leaflet/dist/leaflet.css";
import Journey from "../../map/Journey";
import axios from "axios";

const styles = {
    card: {
        marginTop: 30
    }
};

const events = {
        "Harsh Braking": [
            {
                "Lat": 1.3174356628542145, 
                "Long": 103.78553891365623, 
                "DeviceTS": "2017-07-20 11:29:50",
                "Speed": 0,
                "Severity": 3,
                "color": "yellow" 
            }
        ],
        "Harsh Acceleration": [
            {                
                "Lat": 1.2887929297178298, 
                "Long": 103.8390107728446, 
                "DeviceTS": "2017-07-21 07:00:30", 
                "Speed": 90,
                "Severity": 1.8,
                "color": "green"
            }, 
            {   
                "Lat": 1.282119690277941, 
                "Long": 103.83310014023004, 
                "DeviceTS": "2017-07-20 10:25:29", 
                "Speed": 80,
                "Severity": 1,
                "color": "green"
            }
        ]
    };

class TripRoute extends React.Component {

    constructor(props) {
        super(props);
        this.state = this.getDefaultState();
    }

    getDefaultState() {
        return {
          coordinates: [],
          events: {}
        }
    };

    getMapData() { 
        
		    var reqObj = {
            method: "post",
            url: "/api/historical",
            //url: "/api/accident".
            headers:{
              "Content-Type": "application/json",
              Authorization: "Bearer " + localStorage.getItem("access_token")            
            }, 
            data: {/*
              startDate: this.props.filterObj.startDate,
              endDate: this.props.filterObj.endDate,
              vehicleList: this.props.filterObj.vehicleList */
              startDate: "Thu Jul 20 2017 00:00:00 GMT+0800 (Malay Peninsula Standard Time)",
              endDate: "Thu Jul 20 2017 00:00:00 GMT+0800 (Malay Peninsula Standard Time)",
              vehicleList: [32396]
            }
        };
		  axios(reqObj)
			.then(resp => {
				this.setState({ coordinates: resp.data });
        this.setState({ events: events });
			})
			.catch(err => {
				this.setState( this.getDefaultState() );
       });
        
      
    }

    getTrip() {
        //const coordinates = this.state.coordinates;
        //const vehicleID = this.props.vehicleList[0];
        const vehicleID = "32396";
        const coordinates = this.state.coordinates["32396"];

        return (
            <Journey 
                vehicleID={vehicleID} 
                positions={coordinates}
            />);
    }

    getEventFilters() {
        let events = this.state.events;
        let eventFilters = []
        for (var eventType in events) {
            eventFilters.push(
                <LayersControl.Overlay name={eventType} checked key={eventType}>
                    <FeatureGroup color="purple">
                        {events[eventType].map((event)=>(
                            <CircleMarker center={[event.Lat, event.Long]} 
                                    radius={event.Severity*5} 
                                    weight={0}
                                    fill={true} 
                                    fillOpacity={0.9} 
                                    fillColor={event.color} 
                                    key={event.DeviceTS}>
                                <Popup>
                                    <p>
                                        <b>Time: </b>{event.DeviceTS}<br/>
                                        <b>Speed: </b>{event.Speed}<br/>
                                        <b>Event: </b>{eventType}
                                    </p>
                                </Popup>
                            </CircleMarker>))}
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
                      {this.getTrip()}
                        <LayersControl>
                            <TileLayer
                                url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                                attribution="&copy; <a href=http://osm.org/copyright>OpenStreetMap</a> contributors"
                            />
                            {this.getEventFilters()}
                        </LayersControl>
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

