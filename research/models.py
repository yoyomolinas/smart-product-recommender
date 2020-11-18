import tensorflow as tf
from tensorflow import keras
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Activation, Convolution2D, Dropout, Conv2D
from tensorflow.keras.layers import AveragePooling2D, BatchNormalization
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import SeparableConv2D
from tensorflow.keras.layers import Multiply, Average
from tensorflow.keras.regularizers import l2
from tensorflow.keras.utils import Sequence
from tensorflow.keras import layers

def bigxception(input_shape = (256, 256, 3)):
    regularization = l2(0.01)
    input_tensor = Input(input_shape)
    x = Conv2D(32, (3, 3), strides=(2, 2), use_bias=False)(input_tensor)
    x = BatchNormalization(name='block1_conv1_bn')(x)
    x = Activation('relu', name='block1_conv1_act')(x)
    x = Conv2D(64, (3, 3), use_bias=False)(x)
    x = BatchNormalization(name='block1_conv2_bn')(x)
    x = Activation('relu', name='block1_conv2_act')(x)

    residual = Conv2D(128, (1, 1), strides=(2, 2),
                      padding='same', use_bias=False)(x)
    residual = BatchNormalization()(residual)

    x = SeparableConv2D(128, (3, 3), padding='same', use_bias=False)(x)
    x = BatchNormalization(name='block2_sepconv1_bn')(x)
    x = Activation('relu', name='block2_sepconv2_act')(x)
    x = SeparableConv2D(128, (3, 3), padding='same', use_bias=False)(x)
    x = BatchNormalization(name='block2_sepconv2_bn')(x)

    x = MaxPooling2D((3, 3), strides=(2, 2), padding='same')(x)
    x = layers.add([x, residual])

    residual = Conv2D(256, (1, 1), strides=(2, 2),
                      padding='same', use_bias=False)(x)
    residual = BatchNormalization()(residual)

    x = SeparableConv2D(256, (3, 3), padding='same', use_bias=False)(x)
    x = BatchNormalization(name='block3_sepconv1_bn')(x)
    x = Activation('relu', name='block3_sepconv2_act')(x)
    x = SeparableConv2D(256, (3, 3), padding='same', use_bias=False)(x)
    x = BatchNormalization(name='block3_sepconv2_bn')(x)

    x = MaxPooling2D((3, 3), strides=(2, 2), padding='same')(x)
    x = layers.add([x, residual])

    residual = Conv2D(256, (1, 1), strides=(2, 2),
                      padding='same', use_bias=False)(x)
    residual = BatchNormalization()(residual)

    x = SeparableConv2D(256, (3, 3), padding='same', use_bias=False)(x)
    x = BatchNormalization(name='block4_sepconv1_bn')(x)
    x = Activation('relu', name='block4_sepconv2_act')(x)
    x = SeparableConv2D(256, (3, 3), padding='same', use_bias=False)(x)
    x = BatchNormalization(name='block4_sepconv2_bn')(x)
    map_out = K.mean(x, axis = -1)
    cat_x = SeparableConv2D(50, (32, 32), strides = (1, 1), activation = 'softmax')(x)
    cat_out = Flatten(name = 'categories')(cat_x)
    attr_x = SeparableConv2D(1000, (32, 32), strides = (1, 1), activation = 'sigmoid')(x)
    attr_out = Flatten(name = 'attributes')(attr_x)
    model = keras.models.Model(inputs = input_tensor, outputs = [cat_out, attr_out]) 
    return model

def pretrained_mobilenetv1(input_shape = (256, 256, 3)):
    mobil = keras.applications.mobilenet.MobileNet(input_shape=input_shape, include_top=False, weights='imagenet', pooling='avg')
    x = mobil.outputs[0]
    cat = keras.layers.Dense(50,name='categories', activation='softmax')(x)
    attr = keras.layers.Dense(1000,name='attributes', activation='sigmoid')(x)
    model = keras.models.Model(inputs = mobil.inputs[0], outputs = [cat, attr])
    return model

def pretrained_vgg16(input_shape = (256, 256, 3)):
    mobil = keras.applications.vgg16.VGG16(input_shape=input_shape, include_top=False, weights='imagenet', pooling='avg')
    x = mobil.outputs[0]
    cat = keras.layers.Dense(50,name='categories', activation='softmax')(x)
    attr = keras.layers.Dense(1000,name='attributes', activation='sigmoid')(x)
    model = keras.models.Model(inputs = mobil.inputs[0], outputs = [cat, attr])
    return model

def pretrained_resnet50(input_shape = (256, 256, 3)):
    mobil = keras.applications.resnet50.ResNet50(input_shape=input_shape, include_top=False, weights='imagenet', pooling='avg')
    x = mobil.outputs[0]
    cat = keras.layers.Dense(50,name='categories', activation='softmax')(x)
    attr = keras.layers.Dense(1000,name='attributes', activation='sigmoid')(x)
    model = keras.models.Model(inputs = mobil.inputs[0], outputs = [cat, attr])
    return model


ENUM_MODELS_DICT = {
    0: bigxception,
    1: pretrained_mobilenetv1,
    2: pretrained_vgg16,
    3: pretrained_resnet50}
