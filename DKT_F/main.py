import argparse
import torch
import torch.optim as optim

from data_loader import DATA
from model import MODEL
from run import train, test

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', type=int, default=0)
    parser.add_argument('--max_iter', type=int, default=30, help='number of iterations')
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
    parser.add_argument('--max_grad_norm', type=float, default=3.0, help='maximum gradient norm')
    parser.add_argument('--hidden_dim', type=int, default=64, help='hidden layer dimension')
    parser.add_argument('--n_hidden', type=int, default=2, help='hidden numbers')
    parser.add_argument('--dataset', type=str, default='assist2009_updated')
    parser.add_argument('--batch_size', type=int, default=32, help='the batch size')
    parser.add_argument('--qa_embed_dim', type=int, default=200, help='answer and question embedding dimensions')
    parser.add_argument('--dropout_rate', type=float, default=0.6)


    if parser.parse_args().dataset == 'assist2009_updated':
        # parser.add_argument('--batch_size', type=int, default=32, help='the batch size')
        # parser.add_argument('--qa_embed_dim', type=int, default=200, help='answer and question embedding dimensions')
        parser.add_argument('--n_question', type=int, default=110, help='the number of unique questions in the dataset')
        parser.add_argument('--seqlen', type=int, default=200, help='the allowed maximum length of a sequence')
        parser.add_argument('--data_dir', type=str, default='../dataset/assist2009_updated', help='data directory')
        parser.add_argument('--data_name', type=str, default='assist2009_updated', help='data set name')
        parser.add_argument('--load', type=str, default='assist2009_updated', help='model file to load')
        parser.add_argument('--save', type=str, default='assist2009_updated', help='path to save model')

    elif parser.parse_args().dataset == 'assist2015':
        # parser.add_argument('--batch_size', type=int, default=32, help='the batch size')
        # parser.add_argument('--qa_embed_dim', type=int, default=200, help='answer and question embedding dimensions')
        parser.add_argument('--n_question', type=int, default=100, help='the number of unique questions in the dataset')
        parser.add_argument('--seqlen', type=int, default=200, help='the allowed maximum length of a sequence')
        parser.add_argument('--data_dir', type=str, default='../dataset/assist2015', help='data directory')
        parser.add_argument('--data_name', type=str, default='assist2015', help='data set name')
        parser.add_argument('--load', type=str, default='assist2015', help='model file to load')
        parser.add_argument('--save', type=str, default='assist2015', help='path to save model')

    elif parser.parse_args().dataset == 'STATICS':
        # parser.add_argument('--batch_size', type=int, default=32, help='the batch size')
        # parser.add_argument('--qa_embed_dim', type=int, default=100, help='answer and question embedding dimensions')
        parser.add_argument('--n_question', type=int, default=1223,
                            help='the number of unique questions in the dataset')
        parser.add_argument('--seqlen', type=int, default=200, help='the allowed maximum length of a sequence')
        parser.add_argument('--data_dir', type=str, default='../dataset/STATICS', help='data directory')
        parser.add_argument('--data_name', type=str, default='STATICS', help='data set name')
        parser.add_argument('--load', type=str, default='STATICS', help='model file to load')
        parser.add_argument('--save', type=str, default='STATICS', help='path to save model')

    elif parser.parse_args().dataset == 'synthetic':
        # parser.add_argument('--batch_size', type=int, default=32, help='the batch size')
        # parser.add_argument('--qa_embed_dim', type=int, default=100, help='answer and question embedding dimensions')
        parser.add_argument('--n_question', type=int, default=50,
                            help='the number of unique questions in the dataset')
        parser.add_argument('--seqlen', type=int, default=200, help='the allowed maximum length of a sequence')
        parser.add_argument('--data_dir', type=str, default='../dataset/synthetic', help='data directory')
        parser.add_argument('--data_name', type=str, default='synthetic', help='data set name')
        parser.add_argument('--load', type=str, default='synthetic', help='model file to load')
        parser.add_argument('--save', type=str, default='synthetic', help='path to save model')

    elif parser.parse_args().dataset == 'assist2017':
        # parser.add_argument('--batch_size', type=int, default=32, help='the batch size')
        # parser.add_argument('--qa_embed_dim', type=int, default=100, help='answer and question embedding dimensions')
        parser.add_argument('--n_question', type=int, default=102,
                            help='the number of unique questions in the dataset')
        parser.add_argument('--seqlen', type=int, default=200, help='the allowed maximum length of a sequence')
        parser.add_argument('--data_dir', type=str, default='../dataset/assist2017/train_valid_test', help='data directory')
        parser.add_argument('--data_name', type=str, default='assist2017', help='data set name')
        parser.add_argument('--load', type=str, default='assist2017', help='model file to load')
        parser.add_argument('--save', type=str, default='assist2017', help='path to save model')

    params = parser.parse_args()
    params.lr = params.init_lr

    print(params)

    dat = DATA(n_question=params.n_question, seqlen=params.seqlen, separate_char=',')
    if params.dataset != 'synthetic':
        train_data_path = params.data_dir + "/" + params.data_name + "_train1.csv"
        valid_data_path = params.data_dir + "/" + params.data_name + "_valid1.csv"
        test_data_path = params.data_dir + "/" + params.data_name + "_test.csv"
    else:
        train_data_path = params.data_dir + "/" + "naive_c5_q50_s4000_v0_train1.csv"
        valid_data_path = params.data_dir + "/" + "naive_c5_q50_s4000_v0_valid1.csv"
        test_data_path = params.data_dir + "/" + "naive_c5_q50_s4000_v0_test.csv"

    train_q_data, train_q_t_data, train_answer_data, train_repeated_time_gap, train_past_trail_counts,\
    train_seq_time_gap = dat.load_data(train_data_path)
    valid_q_data, valid_q_t_data, valid_answer_data, valid_repeated_time_gap, valid_past_trail_counts,\
    valid_seq_time_gap  = dat.load_data(valid_data_path)
    test_q_data, test_q_t_data, test_answer_data, test_repeated_time_gap, test_past_trail_counts,\
    test_seq_time_gap = dat.load_data(test_data_path)

    model = MODEL(batch_size=params.batch_size,
                  seqlen=params.seqlen,
                  n_question=params.n_question,
                  hidden_dim=params.hidden_dim,
                  x_embed_dim=params.qa_embed_dim,
                  hidden_layers=params.n_hidden,
                  dropout_rate=params.dropout_rate,
                  gpu=params.gpu)

    model.init_embeddings()
    model.init_params()
    optimizer = optim.Adam(params=model.parameters(), lr=params.lr, betas=(0.9, 0.9))

    if params.gpu >= 0:
        print('device: ' + str(params.gpu))
        torch.cuda.set_device(params.gpu)
        model.cuda()

    # all_train_loss = {}
    # all_train_accuracy = {}
    # all_train_auc = {}
    # all_valid_loss = {}
    # all_valid_accuracy = {}
    # all_valid_auc = {}
    # all_test_loss = {}
    # all_test_accuracy = {}
    # all_test_auc = {}
    best_valid_auc = 0
    cur_test_auc = 0
    cur_train_auc = 0

    for idx in range(params.max_iter):
        train_loss, train_accuracy, train_auc = train(model, params, optimizer, train_q_data, train_q_t_data,
                                                      train_answer_data, train_repeated_time_gap,\
                                                      train_past_trail_counts, train_seq_time_gap)
        print('Epoch %d/%d, loss : %3.5f, auc : %3.5f, accuracy : %3.5f' % (
            idx + 1, params.max_iter, train_loss, train_auc, train_accuracy))
        valid_loss, valid_accuracy, valid_auc = test(model, params, optimizer, valid_q_data, valid_q_t_data,
                                                     valid_answer_data, valid_repeated_time_gap,\
                                                     valid_past_trail_counts, valid_seq_time_gap)
        print('Epoch %d/%d, valid auc : %3.5f, valid accuracy : %3.5f' % (
            idx + 1, params.max_iter, valid_auc, valid_accuracy))
        test_loss, test_accuracy, test_auc = test(model, params, optimizer, test_q_data, test_q_t_data,
                                                  test_answer_data, test_repeated_time_gap,
                                                  test_past_trail_counts, test_seq_time_gap)
        print('Epoch %d/%d, test auc : %3.5f, test accuracy : %3.5f' % (
            idx + 1, params.max_iter, test_auc, test_accuracy))

        # all_train_auc[idx + 1] = train_auc
        # all_train_accuracy[idx + 1] = train_accuracy
        # all_train_loss[idx + 1] = train_loss
        # all_valid_loss[idx + 1] = valid_loss
        # all_valid_accuracy[idx + 1] = valid_accuracy
        # all_valid_auc[idx + 1] = valid_auc
        # all_test_loss[idx + 1] = test_loss
        # all_test_accuracy[idx + 1] = test_accuracy
        # all_test_auc[idx + 1] = test_auc

        if valid_auc > best_valid_auc:
            print('%3.4f to %3.4f' % (best_valid_auc, valid_auc))
            best_valid_auc = valid_auc
            cur_test_auc = test_auc
            cur_train_auc = train_auc

    print('DATASET: {}, TRAIN AUC: {}, BEST VALID AUC: {}, TEST AUC: {}'.format(params.data_name, cur_train_auc, \
                                                                                best_valid_auc, cur_test_auc))


if __name__ == "__main__":
    main()
