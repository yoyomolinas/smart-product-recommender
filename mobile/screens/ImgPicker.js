import React, {useState} from 'react';
import {View, Button, Image, Text, StyleSheet, Alert, Slider} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Permissions from 'expo-permissions';

import colors from '../constants/colors';

const ImgPicker = props => {
    const [pickedImage, setPickedImage] = useState();
    const [imageData, setImageData] = useState();
    const [minPrice, setMinPrice] = useState(10);
    const [maxPrice, setMaxPrice] = useState(500);

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
            aspect: [3, 4],
            base64: true,
            quality: 0.1
        });
        setPickedImage(testImage.uri);
        setImageData(testImage.base64);
    };
    const uploadImageHandler = async () => {
        const testImage = await ImagePicker.launchImageLibraryAsync({
            allowsEditing: true,
            aspect: [3, 4],
            base64: true,
            quality: 0.5
        });
        setPickedImage(testImage.uri);
        setImageData(testImage.base64);
    };

    const resetImageHandler = () => {

        setPickedImage(false);
        setImageData(false);
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
                props.onImageData(imageData, minPrice, maxPrice);
            }
        }
    };
    return (
        <View style={styles.imagePicker}>

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
                <View>
                    <View style={styles.button}>
                        <Button
                            title="Take Image"
                            color={colors.primary}
                            onPress={takeImageHandler}
                        />
                    </View>
                    <View style={styles.button}>
                        <Button
                            title="Upload Image"
                            color={colors.primary}
                            onPress={uploadImageHandler}
                        />
                    </View>
                </View>
            ) : (
                <View>
                    <View style={styles.button}>
                        <Button
                                title="Return Best Matches"
                                color={colors.primary}
                                onPress={saveImageHandler}
                        />
                    </View>
                    <View style={styles.button}>
                        <Button
                                title="Reset Image"
                                color={colors.primary}
                                onPress={resetImageHandler}
                        />
                    </View>
                </View>
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
                    value={10}
                    minimumTrackTintColor = {colors.primary}
                    maximumTrackTintColor = {colors.primary}
                    thumbTintColor={colors.primary}
                    step={10}
                    minimumValue={0}
                    maximumValue={200}
                    onValueChange={val => setMinPrice(val)}
                    onSlidingComplete={val => setMinPrice(val)}
                />
                <Slider
                    style={{width: 300}}
                    value={500}
                    minimumTrackTintColor = {colors.primary}
                    maximumTrackTintColor = {colors.primary}
                    thumbTintColor={colors.primary}
                    step={10}
                    minimumValue={50}
                    maximumValue={1000}
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
        marginVertical : 10,
        width : 300
    },
    imagePreview: {
        marginTop : 20,
        width: '90%',
        height: 350,
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
        marginTop: 20
    },


});

export default ImgPicker;
