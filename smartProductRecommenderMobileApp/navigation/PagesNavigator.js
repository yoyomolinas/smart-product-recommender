import {createStackNavigator} from 'react-navigation' ;

import MainPage from '../screens/MainPage'
import ProductShot from '../screens/ProductShot'


createStackNavigator({
  Main : MainPage,
  Product : ProductPage,
  Camera : CameraPage
});

export default PagesNavigator;
