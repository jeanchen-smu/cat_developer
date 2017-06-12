import React, {PropTypes} from 'react';
import {Polyline, CircleMarker, Popup, Tooltip} from 'react-leaflet';


class Journey extends React.Component{
  render() {
    let positions = this.props.positions; //an array of position, [lat, long, speed, timestamp]
    let vehicle = this.props.vehicleID;
    
    let pointList = [];
    let latlngList = [];

    for (let i = 0; i < positions.length; i++) {
      let latlng = [positions[i][0], positions[i][1]];
      latlngList.push(latlng);
      pointList.push( 
        <CircleMarker center= {latlng} radius = {3} color="blue" key={i}>
          <Popup>
            <p>
              <b>Time: </b>{positions[i][3]}<br/>
              <b>Speed: </b>{positions[i][2]}
            </p>
          </Popup>
        </CircleMarker>
      );
    }

    return (
      <div>
        <Polyline positions = {latlngList}>
          <Tooltip>{vehicle}</Tooltip>
        </Polyline>
        {pointList}
      </div>
    );
  } 
}

Journey.propTypes = {
	positions: PropTypes.array,
  vehicleID: PropTypes.string,
};

export default Journey;