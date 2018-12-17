import os
import os.path as op
import json

def ensure_directory(path):
    if path == '' or path == '.':
        return
    if path != None and len(path) > 0:
        if not os.path.exists(path) and not op.islink(path):
            try:
                os.makedirs(path)
            except OSError as e:
                if e.errno == errno.EEXIST and os.path.isdir(folder_location):
                    # another process has done makedir
                    pass
                else:
                    raise

def tsv_writer(values, tsv_file_name, sep='\t'):
    ensure_directory(os.path.dirname(tsv_file_name))
    tsv_lineidx_file = os.path.splitext(tsv_file_name)[0] + '.lineidx'
    idx = 0
    tsv_file_name_tmp = tsv_file_name + '.tmp'
    tsv_lineidx_file_tmp = tsv_lineidx_file + '.tmp'
    with open(tsv_file_name_tmp, 'w') as fp, open(tsv_lineidx_file_tmp, 'w') as fpidx:
        assert values is not None
        for value in values:
            assert value
            v = sep.join(map(lambda v: str(v) if type(v) is not str else v, value)) + '\n'
            fp.write(v)
            fpidx.write(str(idx) + '\n')
            idx = idx + len(v)
    os.rename(tsv_file_name_tmp, tsv_file_name)
    os.rename(tsv_lineidx_file_tmp, tsv_lineidx_file)

def save_imdb_to_tsv(imdb, pred_file, gt_file):
    roidb, classes = imdb['roidb'], imdb['classes']
    def gen_gt_rows():
        for roi in roidb:
            rects = []
            for rect, c_idx in zip(roi['gt_boxes'], roi['gt_classes']):
                c = classes[c_idx]
                rect = list(map(float, rect))
                rects.append({'class': c, 'rect': rect})
            yield roi['id'], json.dumps(rects)
    tsv_writer(gen_gt_rows(), gt_file)

    def gen_pred_rows():
        for roi in roidb:
            rects = []
            for rect, c_idx, s in zip(roi['dets'], roi['det_classes'],
                    roi['det_scores']):
                c = classes[c_idx]
                rect = list(map(float, rect))
                s = float(s)
                rects.append({'class': c, 'rect': rect, 'conf': s})
            yield roi['id'], json.dumps(rects)
    tsv_writer(gen_pred_rows(), pred_file)

