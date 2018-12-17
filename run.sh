# python 3, annaconda
# source activate learningnms (local-linux-machine)
#CUDA_VISIBLE_DEVICES=0 ipython --pdb train.py -- -c ./experiments/coco_person/conf.yaml
CUDA_VISIBLE_DEVICES=0 ipython --pdb train.py -- -c ./experiments/coco_multiclass/conf.yaml

#CUDA_VISIBLE_DEVICES=0 ipython --pdb test.py -- \
    #./output/coco_person_det.tsv \
    #-c ./experiments/coco_person/conf.yaml \
    #-m ./gnet-1940000
