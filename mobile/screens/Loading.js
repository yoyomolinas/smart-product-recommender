import React from "react";
import {Image,Text, StyleSheet, View} from "react-native";



const Loading = props => {
    return (
        <View style={styles.screen}>
            <Image source={require('../assets/smartProductReco.png')}
                   style={styles.image}
                   resizeMode='cover'
            />
            <Text style={styles.text}>{props.output}</Text>
        </View>
    );
};

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        padding: 10,
        alignItems: 'center'
    },
    image: {
        width :'50%',
        height : 150,
        marginTop : 200
    },
    text: {
        color: 'black',
        fontSize: 18
    }
});
export default Loading;