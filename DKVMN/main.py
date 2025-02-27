import torch

import argparse
from model import MODEL
from run import train, test
import numpy as np
import torch.optim as optim

from data_loader import DATA


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', type=int, default=0, help='the gpu will be used, e.g "0,1,2,3"')
    parser.add_argument('--max_iter', type=int, default=50, help='number of iterations')
    parser.add_argument('--decay_epoch', type=int, default=20, help='number of iterations')
    parser.add_argument('--test', type=bool, default=False, help='enable testing')
    parser.add_argument('--train_test', type=bool, default=True, help='enable testing')
    parser.add_argument('--show', type=bool, default=True, help='print progress')
    parser.add_argument('--init_std', type=float, default=0.1, help='weight initialization std')
    parser.add_argument('--init_lr', type=float, default=0.01, help='initial learning rate')
    parser.add_argument('--lr_decay', type=float, default=0.75, help='learning rate decay')
    parser.add_argument('--final_lr', type=float, default=1E-5,
                        help='learning rate will not decrease after hitting this threshold')
    parser.add_argument('--momentum', type=float, default=0.9, help='momentum rate')
    parser.add_argument('--max_grad_norm', type=float, default=50.0, help='maximum gradient norm')
    # parser.add_argument('--final_fc_dim', type=float, default=110, help='hidden state dim for final fc layer')
    parser.add_argument('--dataset', type=str, default='assist2009_updated')
    parser.add_argument('--train_set', type=int, default=1)

    parser.add_argument('--memory_size', type=int, default=20, help='memory size')
    parser.add_argument('--q_embed_dim', type=int, default=50, help='question embedding dimensions')
    parser.add_argument('--qa_embed_dim', type=int, default=200, help='answer and question embedding dimensions')
    
    if parser.parse_args().dataset == 'assist2009_updated':
        # memory_size: 20, q_embed_dim: 50, qa_embed_dim: 200
        parser.add_argument('--batch_size', type=int, default=128, help='the batch size')
        parser.add_argument('--n_question', type=int, default=110, help='the number of unique questions in the dataset')
        parser.add_argument('--seqlen', type=int, default=200, help='the allowed maximum length of a sequence')
        parser.add_argument('--data_dir', type=str, default='../dataset/assist2009_updated', help='data directory')
        parser.add_argument('--data_name', type=str, default='assist2009_updated', help='data set name')
        parser.add_argument('--load', type=str, default='assist2009_updated', help='model file to load')
        parser.add_argument('--save', type=str, default='assist2009_updated', help='path to save model')
        parser.add_argument('--final_fc_dim', type=float, default=110, help='hidden state dim for final fc layer')
    
    elif parser.parse_args().dataset == 'assist2015':
        # memory_size: 50, q_embed_dim: 50, qa_embed_dim: 200
        parser.add_argument('--batch_size', type=int, default=128, help='the batch size')
        parser.add_argument('--n_question', type=int, default=100, help='the number of unique questions in the dataset')
        parser.add_argument('--seqlen', type=int, default=200, help='the allowed maximum length of a sequence')
        parser.add_argument('--data_dir', type=str, default='../dataset/assist2015', help='data directory')
        parser.add_argument('--data_name', type=str, default='assist2015', help='data set name')
        parser.add_argument('--load', type=str, default='assist2015', help='model file to load')
        parser.add_argument('--save', type=str, default='assist2015', help='path to save model')
        parser.add_argument('--final_fc_dim', type=float, default=100, help='hidden state dim for final fc layer')
   
    elif parser.parse_args().dataset == 'assist2017':
        # memory_size: 20, q_embed_dim: 50, qa_embed_dim: 100
        parser.add_argument('--batch_size', type=int, default=32, help='the batch size')
        parser.add_argument('--n_question', type=int, default=102,
                            help='the number of unique questions in the dataset')
        parser.add_argument('--seqlen', type=int, default=200, help='the allowed maximum length of a sequence')
        parser.add_argument('--data_dir', type=str, default='../dataset/assist2017/train_valid_test/', help='data directory')
        parser.add_argument('--data_name', type=str, default='assist2017', help='data set name')
        parser.add_argument('--load', type=str, default='assist2017', help='model file to load')
        parser.add_argument('--save', type=str, default='assist2017', help='path to save model')
        parser.add_argument('--final_fc_dim', type=float, default=102, help='hidden state dim for final fc layer')

    elif parser.parse_args().dataset == 'STATICS':
        # memory_size: 50, q_embed_dim: 50, qa_embed_dim: 100
        parser.add_argument('--batch_size', type=int, default=32, help='the batch size')
        parser.add_argument('--n_question', type=int, default=1223, help='the number of unique questions in the dataset')
        parser.add_argument('--seqlen', type=int, default=200, help='the allowed maximum length of a sequence')
        parser.add_argument('--data_dir', type=str, default='../dataset/STATICS', help='data directory')
        parser.add_argument('--data_name', type=str, default='STATICS', help='data set name')
        parser.add_argument('--load', type=str, default='STATICS', help='model file to load')
        parser.add_argument('--save', type=str, default='STATICS', help='path to save model')
        parser.add_argument('--final_fc_dim', type=float, default=1223, help='hidden state dim for final fc layer')

    elif parser.parse_args().dataset == 'synthetic':
        # memory_size: 20, q_embed_dim: 50, qa_embed_dim: 100
        parser.add_argument('--batch_size', type=int, default=128, help='the batch size')
        parser.add_argument('--n_question', type=int, default=50,
                            help='the number of unique questions in the dataset')
        parser.add_argument('--seqlen', type=int, default=200, help='the allowed maximum length of a sequence')
        parser.add_argument('--data_dir', type=str, default='../dataset/synthetic/', help='data directory')
        parser.add_argument('--data_name', type=str, default='synthetic', help='data set name')
        parser.add_argument('--load', type=str, default='synthetic', help='model file to load')
        parser.add_argument('--save', type=str, default='synthetic', help='path to save model')
        parser.add_argument('--final_fc_dim', type=float, default=50, help='hidden state dim for final fc layer')

    params = parser.parse_args()
    params.lr = params.init_lr
    params.memory_key_state_dim = params.q_embed_dim
    params.memory_value_state_dim = params.qa_embed_dim

    print(params)

    dat = DATA(n_question=params.n_question, seqlen=params.seqlen, separate_char=',')
    if params.dataset != 'synthetic':
        train_data_path = params.data_dir + "/" + params.data_name + "_train" + str(params.train_set) + ".csv"
        valid_data_path = params.data_dir + "/" + params.data_name + "_valid" + str(params.train_set) + ".csv"
        test_data_path = params.data_dir + "/" + params.data_name + "_test.csv"
    else:
        train_data_path = params.data_dir + "/" + "naive_c5_q50_s4000_v0_train" + str(params.train_set) + ".csv"
        valid_data_path = params.data_dir + "/" + "naive_c5_q50_s4000_v0_valid" + str(params.train_set) + ".csv"
        test_data_path = params.data_dir + "/" + "naive_c5_q50_s4000_v0_test.csv"

    train_q_data, train_qa_data = dat.load_data(train_data_path)
    valid_q_data, valid_qa_data = dat.load_data(valid_data_path)
    test_q_data, test_qa_data = dat.load_data(test_data_path)

    params.memory_key_state_dim = params.q_embed_dim
    params.memory_value_state_dim = params.qa_embed_dim

    model = MODEL(n_question=params.n_question,
                  batch_size=params.batch_size,
                  q_embed_dim=params.q_embed_dim,
                  qa_embed_dim=params.qa_embed_dim,
                  memory_size=params.memory_size,
                  memory_key_state_dim=params.memory_key_state_dim,
                  memory_value_state_dim=params.memory_value_state_dim,
                  final_fc_dim=params.final_fc_dim)


    model.init_embeddings()
    model.init_params()
    # optimizer = optim.SGD(params=model.parameters(), lr=params.lr, momentum=params.momentum)
    optimizer = optim.Adam(params=model.parameters(), lr=params.lr, betas=(0.9, 0.9))

    if params.gpu >= 0:
        print('device: ' + str(params.gpu))
        torch.cuda.set_device(params.gpu)
        model.cuda()

    best_valid_auc = 0
    correspond_train_auc = 0
    correspond_test_auc = 0

    for idx in range(params.max_iter):
        train_loss, train_accuracy, train_auc = train(model, params, optimizer, train_q_data, train_qa_data)
        print('Epoch %d/%d, loss : %3.5f, auc : %3.5f, accuracy : %3.5f' % (idx + 1, params.max_iter, train_loss, train_auc, train_accuracy))
        valid_loss, valid_accuracy, valid_auc = test(model, params, optimizer, valid_q_data, valid_qa_data)
        print('Epoch %d/%d, valid auc : %3.5f, valid accuracy : %3.5f' % (idx + 1, params.max_iter, valid_auc, valid_accuracy))
        test_loss, test_accuracy, test_auc = test(model, params, optimizer, test_q_data, test_qa_data)
        print('Epoch %d/%d, test auc : %3.5f, test accuracy : %3.5f' % (idx + 1, params.max_iter, test_auc, test_accuracy))

        # output the epoch with the best validation auc
        if valid_auc > best_valid_auc:
            print('%3.4f to %3.4f' % (best_valid_auc, valid_auc))
            best_valid_auc = valid_auc
            correspond_train_auc = train_auc
            correspond_test_auc = test_auc

    print("DATASET: {}, MEMO_SIZE: {}, Q_EMBED_SIZE: {}, QA_EMBED_SIZE: {}, LR: {}".format(params.data_name, params.memory_size, params.q_embed_dim, params.qa_embed_dim, params.init_lr))
    print("BEST VALID AUC: {}, CORRESPOND TRAIN AUC: {}, CORRESPOND TEST AUC: {}".format(best_valid_auc, correspond_train_auc, correspond_test_auc))

if __name__ == "__main__":
    main()
