import React from 'react';
import {View, Text, StyleSheet, Button, Image} from 'react-native';

import Card from '../components/Card';
import Colors from '../constants/colors';
const ProductShot = props => {
    // const [cameraMode, setCameraMode] = useState(false);
    return (
        <View style={styles.screen}>
            <Image source={require('../assets/smartProductReco.png')}
                   style={styles.image}
                   resizeMode='cover'
            />
            <Card style={styles.buttonContainer}>
                <Text style={styles.text}>Dear {props.nameOfUser} </Text>
            </Card>

            <Card>
                <Text style={styles.text}>Upload the Picture of Your Favourite Product!</Text>
            </Card>
            <View style={styles.button}>
                <Card style={styles.buttonContainer}>
                    <Button
                        title="Capture Image"
                        onPress={() => {
                            props.onCameraPageClick(true);
                        }}
                        color={Colors.primary}
                    />
                </Card>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        justifyContent: 'space-between',
        padding: 10,
        alignItems: 'center',
        marginBottom: 30
    },
    image: {
        width: '50%',
        height: 150
    },
    buttonContainer: {
        margin: 20,
        flexDirection: 'row',
        justifyContent: 'space-around',
        marginTop: 20,
        width: 600,
        maxWidth: '80%'
    },
    text: {
        color: 'black',
        fontSize: 18,
        paddingVertical: 10
    },
    button: {
        width: 200
    },
});

export default ProductShot;
