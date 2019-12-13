import React, {useState} from 'react';
import {
    View,
    Text,
    StyleSheet,
    Button,
    TouchableWithoutFeedback,
    Keyboard,
    Alert,
    Image
} from 'react-native';

import Card from '../components/Card';
import Input from '../components/Input';
import Colors from '../constants/colors';

const MainPage = props => {
    const [enteredValue, setEnteredValue] = useState('');
    const [confirmed, setConfirmed] = useState(false);
    const [selectedName, setName] = useState();

    const nameInputHandler = inputText => {
        setEnteredValue(inputText.replace(/[^A-Za-z]/g, ''));
    };

    const confirmInputHandler = () => {
        const specifiedName = enteredValue;
        if (!isNaN(enteredValue)) {
            Alert.alert(
                'You did not enter anything!',
                'Please input your name.',
                [{text: 'Okay', style: 'destructive'}],
                () => {
                }
            );
            return;
        }
        setConfirmed(true);
        setName(specifiedName);
        setEnteredValue('');
        Keyboard.dismiss();
    };

    let screenOutput;
    if (confirmed) {
        screenOutput = (
            <View style={styles.screen}>
                <Image source={require('../assets/smartProductReco.png')}
                       style={styles.image}
                       resizeMode='cover'
                />
                <Card style={styles.magicContainer}>
                    <View style={styles.productNav}>
                        <Text style={styles.text}>
                            Sometimes you see a nice product!
                        </Text>
                    </View>
                    <View style={styles.productNav}>
                        <Text style={styles.text}>
                            But you don't know where to buy it!
                        </Text>
                    </View>
                    <View style={styles.productNav}>
                        <Button title="Move to Magic"
                                onPress={() => {
                                    props.onMainPageLoad(selectedName)
                                }}
                                color={Colors.primary}
                        />
                    </View>

                </Card>
            </View>
        );
    } else {
        screenOutput = (
            <View style={styles.screen}>
                <Image source={require('../assets/smartProductReco.png')}
                       style={styles.image}
                       resizeMode='cover'
                />
                <Card style={styles.outputContainer}>
                    <Text style={styles.nametext}>Enter Your Name</Text>
                    <Input
                        style={styles.input}
                        blurOnSubmit
                        autoCapitalize="none"
                        autoCorrect={false}
                        keyboardType="default"
                        maxLength={10}
                        onChangeText={nameInputHandler}
                        value={enteredValue}
                    />
                    <View style={styles.buttonContainer}>
                        <View style={styles.button}>
                            <Button
                                title="Confirm"
                                onPress={confirmInputHandler}
                                color={Colors.primary}
                            />
                        </View>
                    </View>
                </Card>
            </View>
        );
    }

    return (
        <TouchableWithoutFeedback
            onPress={() => {
                Keyboard.dismiss();
            }}
        >
            {screenOutput}
        </TouchableWithoutFeedback>
    );
};

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        padding: 10,
        alignItems: 'center'
    },
    title: {
        fontSize: 20,
        marginVertical: 10
    },
    productNav: {
        marginVertical: 20
    },
    outputContainer: {
        margin: 20,
        width: 300,
        maxWidth: '80%',
        alignItems: 'center'
    },
    magicContainer: {
        margin: 20,
        width: 200,
        maxWidth: '80%',
        alignItems: 'center'
    },
    buttonContainer: {
        flexDirection: 'row',
        width: '100%',
        justifyContent: 'space-between',
        paddingHorizontal: 15
    },
    button: {
        width: 200
    },
    input: {
        width: 50,
        textAlign: 'center'
    },
    image: {
        width: '50%',
        height: 150
    },
    text: {
        color: 'black',
        fontSize: 18,
        textAlign: 'center'
    },

});

export default MainPage;
