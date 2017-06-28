import React from 'react';
import Assessment from 'material-ui/svg-icons/action/assessment';
import GpsFixed from 'material-ui/svg-icons/device/gps-fixed';
import GridOn from 'material-ui/svg-icons/image/grid-on';
import Grade from 'material-ui/svg-icons/action/grade';
import PermIdentity from 'material-ui/svg-icons/action/perm-identity';
//import Web from 'material-ui/svg-icons/av/web';
import {cyan600, pink600, purple600} from 'material-ui/styles/colors';
import ExpandLess from 'material-ui/svg-icons/navigation/expand-less';
import ExpandMore from 'material-ui/svg-icons/navigation/expand-more';
import ChevronRight from 'material-ui/svg-icons/navigation/chevron-right';

const data = {
  menus: [
    { text: 'Overview', key:1, icon: <Assessment/>, link: '/home/dashboard', submenu:[] },
    { text: 'Tracking', key:2, icon: <GpsFixed/>, link: '/home/form', submenu:[
      { text: 'History', key:1, icon: <GpsFixed/>, link: '/home/form', submenu:[] },
      { text: 'Real Time', key:2, icon: <GpsFixed/>, link: '/home/form', submenu:[] },    
    ] },
    { text: 'Rank', key:1, icon: <Grade/>, link: '/home/rank', submenu:[] }
  ],
  tablePage: {
    items: [
      {id: 1, name: 'Product 1', price: '$50.00', category: 'Category 1'},
      {id: 2, name: 'Product 2', price: '$150.00', category: 'Category 2'},
      {id: 3, name: 'Product 3', price: '$250.00', category: 'Category 3'},
      {id: 4, name: 'Product 4', price: '$70.00', category: 'Category 4'},
      {id: 5, name: 'Product 5', price: '$450.00', category: 'Category 5'},
      {id: 6, name: 'Product 6', price: '$950.00', category: 'Category 6'},
      {id: 7, name: 'Product 7', price: '$550.00', category: 'Category 7'},
      {id: 8, name: 'Product 8', price: '$750.00', category: 'Category 8'}
    ]
  },
  dashBoardPage: {
    scoreDistribution: [
      {name: 'Jan', value: 3700},
      {name: 'Feb', value: 3000},
      {name: 'Mar', value: 2000},
      {name: 'Apr', value: 2780},
      {name: 'May', value: 2000},
      {name: 'Jun', value: 1800},
      {name: 'Jul', value: 2600},
      {name: 'Aug', value: 2900},
      {name: 'Sep', value: 3500},
      {name: 'Oct', value: 3000},
      {name: 'Nov', value: 2400},
      {name: 'Dec', value: 2780}
    ],
    averageScore: [
      {name: 'Nov', value: 2400},
      {name: 'Nov', value: 1398},
      {name: 'Nov', value: 9800},
      {name: 'Nov', value: 3908},
      {name: 'Nov', value: 4800},
      {name: 'Nov', value: 3490},
      {name: 'Nov', value: 4300}
    ],
    averageDistance: [
      {name: 'Nov', value: 2400},
      {name: 'Nov', value: 1398},
      {name: 'Nov', value: 9800},
      {name: 'Nov', value: 3908},
      {name: 'Nov', value: 4800},
      {name: 'Nov', value: 3490},
      {name: 'Nov', value: 4300},
      {name: 'Nov', value: 4300},
      {name: 'Nov', value: 4300},
      {name: 'Nov', value: 4300},
      {name: 'Nov', value: 4300}
    ]
  }
};

export default data;
