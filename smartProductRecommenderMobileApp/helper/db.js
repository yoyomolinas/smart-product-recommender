import * as SQLite from 'expo-sqlite';

const db =SQLite.openDatabase('products.db');

export const init = () => {
    return new Promise((resolve, reject) => {
        db.transaction(tx => {
            tx.executeSql(
                'CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY NOT NULL, imageUri TEXT NOT NULL,maxPrice INTEGER NOT NULL, minPrice INTEGER NOT NULL);',
                [],
                () => {
                    resolve();
                },
                (_, err) => {
                    reject(err);
                }
            );
        });
    });
};

export const insertProduct = (imageUri, maxPrice, minPrice) => {
    return new Promise((resolve, reject) => {
        db.transaction(tx => {
            tx.executeSql(
                `INSERT INTO products (imageUri, maxPrice, minPrice) VALUES (?, ?, ?);`,
                [imageUri, maxPrice, minPrice],
                (_, result) => {
                    resolve(result);
                },
                (_, err) => {
                    reject(err);
                }
            );
        });
    });
};

export const fetchProduct = () => {
    return new Promise((resolve, reject) => {
        db.transaction(tx => {
            tx.executeSql(
                'SELECT * FROM products', //right now for testing purposes I assigned this table to products. In the future it will be results.
                [],
                (_, result) => {
                    resolve(result);
                },
                (_, err) => {
                    reject(err);
                }
            );
        });
    });
};


