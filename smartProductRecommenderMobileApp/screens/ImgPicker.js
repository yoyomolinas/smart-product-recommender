import React, {useState} from 'react';
import { View, Button, Image, Text, StyleSheet, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Permissions from 'expo-permissions';

import colors from './constants/colors';

const ImgPicker = props => {
  const [pickedImage , setPickedImage] = useState();
  const verifyPermissions = async () => {
    const result = await Permissions.askAsync(Permissions.CAMERA_ROLL);
    if (result.status !== 'granted') {
      Alert.alert(
        'Insufficient permissions!',
        'You need to grant camera permissions to use this app.',
        [{ text: 'Okay' }]
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
      aspect : [4,3],
      quality : 0.5
    });
    setPickedImage(testImage.uri);
  };

  const saveImageHandler = () => {
    console.log("The image is sent to the server!");
  }
  return (
    <View style={styles.imagePicker}>
    <Image source= {require('../assets/smartProductReco.png')}
          style ={styles.icon}
          resizeMode = 'cover'
    />
      <View style={styles.imagePreview}>
      {!pickedImage ? (
        <Text style={styles.text}>
        No image picked yet.</Text>
      )
      :(
        <Image style={styles.image} source={{uri:pickedImage}}/>
      )
      }
      </View>
      {!pickedImage ? (
        <Button
        title="Take Image"
        color={colors.primary}
        onPress={takeImageHandler}
          />) : (
          <Button
          title="Save Image"
          color={colors.primary}
          onPress={saveImageHandler}
          />
        )
      }
    </View>
  );
};

const styles = StyleSheet.create({
  imagePicker: {
    alignItems: 'center'
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
  icon : {
    width: 200,
    height: 200
  },
  text: {
    marginTop: 50
  }

});

export default ImgPicker;
