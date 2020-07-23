'''
@author madhumita
'''

from keras.models import model_from_json
from keras.utils.vis_utils import plot_model
import numpy as np
import scipy.sparse as scp

def x_generator(X, batch_size, shuffle, seed = 1337):
    '''
    Creates batches of data from given input, given a batch size. Returns dense representation of sparse input one batch a time.
    @param X: input features, can be sparse or dense
    @param batch_size: number of instances in each batch
    @param shuffle: If True, shuffle input instances.
    @param seed: fixed seed for shuffling data, for replication
    @return batch of input data, without shuffling
    '''
    number_of_batches = np.ceil(X.shape[0]/batch_size) #ceil function allows for creating last batch off remaining samples
    counter = 0
    sample_index = np.arange(X.shape[0])
    
    if shuffle:
        np.random.seed(seed)
        np.random.shuffle(sample_index)
    
    sparse = False
    if scp.issparse(X):
        sparse = True
        
    while counter < number_of_batches: 
        batch_index = sample_index[batch_size*counter:batch_size*(counter+1)]
        if sparse:
            x_batch = X[batch_index,:].toarray() #converts to dense array
        else:
            x_batch = X[batch_index,:]
        yield x_batch, batch_index
        counter += 1

def save_model(model, out_dir, f_arch = 'model_arch.png', f_model = 'model_arch.json', f_weights = 'model_weights.h5'):
    '''
    Saves a Keras model description and model weights
    @param model: a keras model
    @param out_dir: directory to save model architecture and weights to
    @param f_model: file name for model architecture
    @param f_weights: filename for model weights
    '''
    model.summary()
    plot_model(model, to_file=out_dir+f_arch)
    
    json_string = model.to_json()
    open(out_dir+f_model, 'w').write(json_string)
    
    model.save_weights(out_dir+f_weights, overwrite=True)
    
def load_model(dir_name, f_model = 'model_arch.json', f_weights = 'model_weights.h5' ):
    '''
    Loads a Keras model from disk to memory.
    @param dir_name: directory in which the model architecture and weight files are present
    @param f_model: file name for model architecture
    @param f_weights: filename for model weights
    @return loaded model
    '''
    json_string = open(dir_name + f_model, 'r').read()
    model = model_from_json(json_string)
    
    model.load_weights(f_weights)
    
    return model


def assert_input(n_layers, n_hid, dropout, enc_act, dec_act):
    """
    If the hidden nodes, dropout proportion, encoder activation function or decoder activation function is given,
    it uses the same parameter for all the layers.
    Errors out if there is a size mismatch between number of layers and parameters for each layer.
    """

    if len(n_hid) == 1:
        n_hid = n_hid * n_layers

    if len(dropout) == 1:
        dropout = dropout * n_layers

    if len(enc_act) == 1:
        enc_act = enc_act * n_layers

    if len(dec_act) == 1:
        dec_act = dec_act * n_layers

    assert (n_layers == len(n_hid) == len(dropout) == len(enc_act) == len(
        dec_act)), "Please specify as many hidden nodes, dropout proportion on input, and encoder and decoder " \
                   "activation function, as many layers are there, using list data structure"

    return n_hid, dropout, enc_act, dec_act