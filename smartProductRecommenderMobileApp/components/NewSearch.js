import React from 'react';
import {Button, StyleSheet,View } from 'react-native';
import Colors from '../constants/colors';

const NewSearch = props => {

  return (<View style={styles.buttonContainer}>
  <View style={styles.button}>
    <Button
        title="New Search"
        onPress={props.onNewSearch}
        color={Colors.primary}
    />
  </View>
  </View>);
};

const styles = StyleSheet.create({
    buttonContainer: {
        marginVertical: 10,
        flexDirection: 'row',
        width: '100%',
        alignItems: 'center',
        justifyContent: 'center'
        
    },
    button: {
        width: 200
    },
});

export default NewSearch;
