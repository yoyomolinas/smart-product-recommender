import React, {useState} from 'react';
import {View, Button, Image, Text, StyleSheet, Alert, Slider} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Permissions from 'expo-permissions';

import colors from '../constants/colors';

const ImgPicker = props => {
    const [pickedImage, setPickedImage] = useState();
    const [imageData, setImageData] = useState();
    const [minPrice, setMinPrice] = useState();
    const [maxPrice, setMaxPrice] = useState();

    const verifyPermissions = async () => {
        const result = await Permissions.askAsync(Permissions.CAMERA_ROLL);
        if (result.status !== 'granted') {
            Alert.alert(
                'Insufficient permissions!',
                'You need to grant camera permissions to use this app.',
                [{text: 'Okay'}]
            );
            return false;
        }
        return true;
    };
    const takeImageHandler = async () => {
        const hasPermission = await verifyPermissions();
        if (!hasPermission) {
            return;
        }
        const testImage = await ImagePicker.launchCameraAsync({
            allowsEditing: true,
            aspect: [4, 3],
            base64: true,
            quality: 0.5
        });
        console.log(testImage.height);
        console.log(testImage.width);
        console.log(testImage.size);
        setPickedImage(testImage.uri);
        setImageData(testImage.base64);
    };
    const priceRangeHandler = () => {
        if (maxPrice < minPrice) {
            Alert.alert(
                'Wrong Price Range',
                'You specified a wrong price range.',
                [{text: 'Okay', style: 'destructive'}],
                () => {
                }
            );
            return false;
        }
        return true;
    };

    const saveImageHandler = () => {
        if (pickedImage && maxPrice && minPrice) {
            if (priceRangeHandler()) {
                props.onSetMax(maxPrice);
                props.onSetMin(minPrice);
                props.onImageData(imageData,minPrice,maxPrice);


            }
        }
    };
    return (
        <View style={styles.imagePicker}>
            <Image source={require('../assets/smartProductReco.png')}
                   style={styles.icon}
                   resizeMode='cover'
            />
            <View style={styles.imagePreview}>
                {!pickedImage ? (
                        <Text style={styles.text}>
                            No image picked yet.</Text>
                    )
                    : (
                        <Image style={styles.image} source={{uri: pickedImage}}/>
                    )
                }
            </View>
            {!pickedImage ? (
                <Button
                    title="Take Image"
                    color={colors.primary}
                    onPress={takeImageHandler}
                />) : (
                <Button style={{width: 200}}
                        title="Return Best Matches"
                        color={colors.primary}
                        onPress={saveImageHandler}
                />
            )
            }
            <View style={styles.sliderContainer}>
                <Text style={styles.text}>
                    Specify Minimum Price
                </Text>
                <Text>
                    {minPrice}
                </Text>

                <Slider
                    style={{width: 300}}
                    step={20}
                    minimumValue={20}
                    maximumValue={200}
                    value={minPrice}
                    onValueChange={val => setMinPrice(val)}
                    onSlidingComplete={val => setMinPrice(val)}
                />
                <Slider
                    style={{width: 300}}
                    step={20}
                    minimumValue={100}
                    maximumValue={1000}
                    value={maxPrice}
                    onValueChange={val => setMaxPrice(val)}
                    onSlidingComplete={val => setMaxPrice(val)}
                />
                <Text>
                    {maxPrice}
                </Text>
                <Text>
                    Specify Maximum Price
                </Text>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    imagePicker: {
        alignItems: 'center'
    },
    sliderContainer: {
        alignItems: 'center'
    },
    button: {
        width: 300
    },
    imagePreview: {
        width: '100%',
        height: 200,
        justifyContent: 'center',
        alignItems: 'center',
        borderColor: '#ccc',
        borderWidth: 5
    },
    image: {
        width: '100%',
        height: '100%'
    },
    icon: {
        width: 200,
        height: 200
    },
    text: {
        marginTop: 50
    },
    slider: {
        marginTop: 50
    }

});

export default ImgPicker;
