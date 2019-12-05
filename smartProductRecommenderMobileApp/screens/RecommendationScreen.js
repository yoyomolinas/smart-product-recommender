import React from 'react';
import {Linking, FlatList, View, Text, StyleSheet, Image} from 'react-native';
import Card from '../components/Card';
import products from '../demo.json';

const RecommendationScreen = props => {

    if (props.useDemo == true) {
        return (
            <FlatList
                keyExtractor={products => products.name}
                data={products}
                renderItem={({item}) => {
                    return (<View>
                            <Card style={styles.outputContainer}>
                                <Text style={styles.textStyle}>{item.name}</Text>
                                <Image source={{uri: item.image}}
                                       style={styles.image}
                                       resizeMode='cover'
                                />
                                <Text style={styles.textStyle}>Price: {item.price}</Text>
                                <Text style={{color: 'blue'}}
                                      onPress={() => Linking.openURL(item.product_url)}>
                                    Get Product
                                </Text>
                            </Card>
                        </View>
                    )
                }}
            />
        );
    } else {
        return (
            <FlatList
                keyExtractor={matching_data => matching_data.id}
                data={props.imageData}
                renderItem={({item}) => {
                    if (item.matching_id == props.productId) {
                        return (<View>
                                <Card style={styles.outputContainer}>
                                    {/*<Text style={styles.textStyle}>{item.name}</Text>*/}
                                    <Image source={{uri: item.imageUrl}}
                                           style={styles.image}
                                           resizeMode='cover'
                                    />
                                    <Text style={styles.textStyle}>Price: {item.price}</Text>
                                    <Text style={{color: 'blue'}}
                                          onPress={() => Linking.openURL(item.productUrl)}>
                                        Get Product
                                    </Text>
                                </Card>
                            </View>
                        )
                    }
                }}
            />
        );
    }
};
// const products = require('https://s5.aconvert.com/convert/p3r68-cdx67/mtx3i-k338b.json');


// constructor(props) {
//     super(props);
//     this.state = {
//         isLoading: true,
//         dataSource: []
//     }
// }

const styles = StyleSheet.create({

    image: {
        width: '70%',
        height: 250
    },
    textStyle: {
        color: 'black',
        fontSize: 18,
        paddingVertical: 10
    },
    outputContainer: {
        margin: 35,
        width: 400,
        maxWidth: '80%',
        alignItems: 'center'
    },
    button: {
        width: 200
    },
});


export default RecommendationScreen;