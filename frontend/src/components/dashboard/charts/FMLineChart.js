import React, {PropTypes} from 'react';
import Paper from 'material-ui/Paper';
import {white} from 'material-ui/styles/colors';
import {LineChart, Line, ResponsiveContainer, XAxis, YAxis, CartesianGrid, Tooltip} from 'recharts';
import {typography} from 'material-ui/styles';

const FMLineChart = (props) => {

  const styles = {
    div: {
      marginLeft: 'auto',
      marginRight: 'auto',
      width: '90%',
      height: 500,
      paddingTop: 40,
      paddingBottom: 20
    },
    header: {
      fontSize: 24,
      fontWeight: typography.fontWeightLight,
      color: white,
      backgroundColor: props.headerColor,
      padding: 10,
    }
  };

  return (
    <Paper>
      {/*<div style={{...styles.header}}>{props.title}</div>*/}
      <div style={styles.div}>
        <ResponsiveContainer >
          <LineChart data={props.data}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <XAxis dataKey='name'/>
            <YAxis />
            <CartesianGrid strokeDasharray="3 3" />
            <Tooltip />
            <Line type="monotone" dataKey="pv" stroke={props.color} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Paper>
  );
};

FMLineChart.propTypes = {
    headerColor: PropTypes.string,
    title: PropTypes.string,
    data: PropTypes.array,
    color: PropTypes.string
};

export default FMLineChart;
