import React from 'react';
import { View, Text, StyleSheet ,Image} from 'react-native';

import Colors from '../constants/colors';
const Header = props => {
  return (
    <View style={styles.header}>
     
        <Image source= {require('../assets/Koc_University_logo.jpg')}
              style ={styles.headerImage}
              resizeMode = 'contain' 
        />

    </View>
  );
};

const styles = StyleSheet.create({

  header: {
    width: '100%',
    height: 100,
    paddingTop: 36,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center'
  },
  headerImage: {
    width: '30%',
    height: 50
  }
});

export default Header;
