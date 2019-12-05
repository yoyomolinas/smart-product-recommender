import tensorflow.keras.backend as K

def triplet_loss(y_true, y_pred, alpha = 0.4):
    """
    Triplet loss implementation. loss = max(sum(square(anchor - positive)) - sum(square(anchor - negative)) + alpha, 0).
    The idea is to minimize distance to between anchor and positive example, while expanding distance between anchor and 
    negative example at least alpha units.
    :param y_true: true labels, dummy in this function
    :param y_pred: python list of anchor, positive, and negative feature embeddings
    :return loss: loss that will be backpropagated by the network
    """
    
    total_lenght = y_pred.shape.as_list()[-1]
#     print('total_lenght=',  total_lenght)
#     total_lenght =12
    
    anchor = y_pred[:,0:int(total_lenght*1/3)]
    positive = y_pred[:,int(total_lenght*1/3):int(total_lenght*2/3)]
    negative = y_pred[:,int(total_lenght*2/3):int(total_lenght*3/3)]

    # distance between the anchor and the positive
    pos_dist = K.sum(K.square(anchor-positive),axis=1)

    # distance between the anchor and the negative
    neg_dist = K.sum(K.square(anchor-negative),axis=1)

    # compute loss
    basic_loss = pos_dist-neg_dist+alpha
    loss = K.maximum(basic_loss,0.0)
 
    return loss

def triplet_cosine_loss(y_true, y_pred, alpha = 0.4):
    """
    Implementation of the triplet loss function
    Arguments:
    y_true -- true labels, required when you define a loss in Keras, you don't need it in this function.
    y_pred -- python list containing three objects:
            anchor -- the encodings for the anchor data
            positive -- the encodings for the positive data (similar to anchor)
            negative -- the encodings for the negative data (different from anchor)
    Returns:
    loss -- real number, value of the loss
    """
    # print('y_pred.shape = ',y_pred)
    cosine_loss = tf.keras.losses.CosineSimilarity(axis = 1)    
    total_lenght = y_pred.shape.as_list()[-1]
    
    anchor = y_pred[:,0:int(total_lenght*1/3)]
    positive = y_pred[:,int(total_lenght*1/3):int(total_lenght*2/3)]
    negative = y_pred[:,int(total_lenght*2/3):int(total_lenght*3/3)]

    # positive loss
    pos_dist = K.sum(K.square(anchor-positive),axis=1)
    pos_loss = 1 - K.abs(cosine_loss(anchor, positive))

    # negative loss
    neg_loss = K.abs(cosine_loss(anchor, negative))

    # compute loss
    loss = pos_loss + neg_loss
 
    return loss