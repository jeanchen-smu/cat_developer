import React, {PropTypes} from 'react';
import Paper from 'material-ui/Paper';
import {white} from 'material-ui/styles/colors';
import {BarChart, Bar, ResponsiveContainer, XAxis, YAxis, CartesianGrid, Tooltip} from 'recharts';
import GlobalStyles from '../../../styles';

const FMBarChart = (props) => {

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
      color: white,
      backgroundColor: props.headerColor,
      padding: 10
    }
  };

  return (
    <Paper>
      {/*<div style={{...GlobalStyles.title, ...styles.header}}>{props.title}</div>*/}
      <div style={styles.div}>
        <ResponsiveContainer>
          <BarChart data={props.data}>
            <XAxis dataKey="name"/>
            <YAxis />
            <CartesianGrid strokeDasharray="3 3" />
            <Tooltip />
            <Bar dataKey="uv" fill={props.color} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Paper>
  );
};

FMBarChart.propTypes = {
  headerColor: PropTypes.string,
  title: PropTypes.string,
  data: PropTypes.array,
  color: PropTypes.string
};

export default FMBarChart;
