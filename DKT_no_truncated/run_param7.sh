python -u main.py --dataset assist2009_updated --batch_size 128 --init_lr 0.001 --dropout_rate 0.5 --hidden_dim 200 --qa_embed_dim 100
python -u main.py --dataset assist2015 --batch_size 128 --init_lr 0.001 --dropout_rate 0.5 --hidden_dim 200 --qa_embed_dim 100
python -u main.py --dataset assist2017 --batch_size 32--init_lr 0.001 --dropout_rate 0.5 --hidden_dim 200 --qa_embed_dim 100
python -u main.py --dataset STATICS --batch_size 32--init_lr 0.001 --dropout_rate 0.5 --hidden_dim 200 --qa_embed_dim 100
python -u main.py --dataset synthetic --batch_size 128 --init_lr 0.001 --dropout_rate 0.5 --hidden_dim 200 --qa_embed_dim 100
