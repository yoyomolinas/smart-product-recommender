import React from 'react';
import { Text, StyleSheet , View, Button, TouchableOpacity, FlatList} from 'react-native';

const companies = [
    {name: 'LC-Waikiki'},
    {name: 'Boyner'}
];
    


const RecommendationScreen = () => {
       return <FlatList
       keyExtractor = {companies => companies.name}
       data = {companies}
       renderItem={({item}) => {
        return <Text style={styles.textStyle}>{item.name}</Text>
       
       }}
       /> 
};

const styles = StyleSheet.create({
    textStyle: {
        marginVertical: 20
    }

});


export default RecommendationScreen;