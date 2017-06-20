import React, {PropTypes} from 'react';
import {Polyline, Circle, Popup} from 'react-leaflet';


class Journey extends React.Component{
  render() {
    let positions = this.props.positions; //an array of position, [lat, long, overspeed, speed, timestamp]
    let vehicle = this.props.vehicleID;
    
    let pointList = [];
    let latlngList = [];

    for (let i = 0; i < positions.length; i++) {
      let latlng = [positions[i][0], positions[i][1]];
      latlngList.push(latlng);
      let overspeed = positions[i][2];
      let color = overspeed > 0 ? "red":"blue";
      pointList.push( 
        (overspeed>0)&&
        <Circle center= {latlng} radius = {8} opacity= {0.7} fill ={true} fillOpacity = {1} color={color} key={i}>
          <Popup>
            <p>
              <b>Time: </b>{positions[i][4]}<br/>
              <b>Speed: </b>{positions[i][3]}
            </p>
          </Popup>
        </Circle>
      );
    }

    return (
      <div>
        <Polyline weight = {5} positions = {latlngList}>
          <Popup>
            <p>
              <b>Vehicle: </b>{vehicle}
            </p>
          </Popup>
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