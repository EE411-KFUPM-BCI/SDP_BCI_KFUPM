import tensorflow as tf
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt


MODEL_NAME = "new_models/88.12-acc-64x3-batch-norm-6epoch-1668593073-loss-0.71.model"


CLIP = False  # if your model was trained with np.clip to clip  values
CLIP_VAL = 10  # if above, what was the value +/-

model = tf.keras.models.load_model(MODEL_NAME)

VALDIR = 'validation_data'
ACTIONS = ['left', 'none', 'right','bite']
PRED_BATCH = 32


def get_val_data(valdir, action, batch_size):

    argmax_dict = {0: 0, 1: 0, 2: 0, 3: 0}
    raw_pred_dict = {0: 0, 1: 0, 2: 0, 3: 0}

    action_dir = os.path.join(valdir, action)
    for session_file in os.listdir(action_dir):
        filepath = os.path.join(action_dir, session_file)
        if CLIP:
            data = np.clip(np.load(filepath), -CLIP_VAL, CLIP_VAL) / CLIP_VAL
        else:
            data = np.load(filepath)

        preds = model.predict([data.reshape(-1, 16, 50)],
                              batch_size=batch_size)

        for pred in preds:
            argmax = np.argmax(pred)
            argmax_dict[argmax] += 1
            for idx, value in enumerate(pred):
                raw_pred_dict[idx] += value

    argmax_pct_dict = {}

    for i in argmax_dict:
        total = 0
        correct = argmax_dict[i]
        for ii in argmax_dict:
            total += argmax_dict[ii]

        argmax_pct_dict[i] = round(correct/total, 3)

    return argmax_dict, raw_pred_dict, argmax_pct_dict


def make_conf_mat(left, none, right, bite):

    action_dict = {"left": left, "none": none, "right": right,"bite":bite}
    action_conf_mat = pd.DataFrame(action_dict)
    actions = [i for i in action_dict]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.matshow(action_conf_mat, cmap=plt.cm.RdYlGn)
    ax.set_xticklabels([""]+actions)
    ax.set_yticklabels([""]+actions)

    print("__________")
    print(action_dict)
    for idx, i in enumerate(action_dict):
        print('tf', i)
        for idx2, ii in enumerate(action_dict[i]):
            print(i, ii)
            print(action_dict[i][ii])
            ax.text(
                idx, idx2, f"{round(float(action_dict[i][ii]),2)}", va='center', ha='center')
    plt.title("Action done")
    plt.ylabel("Predicted Action")
    plt.show()


left_argmax_dict, left_raw_pred_dict, left_argmax_pct_dict = get_val_data(
    VALDIR, "left", PRED_BATCH)
none_argmax_dict, none_raw_pred_dict, none_argmax_pct_dict = get_val_data(
    VALDIR, "none", PRED_BATCH)
right_argmax_dict, right_raw_pred_dict, right_argmax_pct_dict = get_val_data(
    VALDIR, "right", PRED_BATCH)
bite_argmax_dict, bite_raw_pred_dict, bite_argmax_pct_dict = get_val_data(
    VALDIR, "bite", PRED_BATCH)

make_conf_mat(left_argmax_pct_dict, none_argmax_pct_dict,
              right_argmax_pct_dict, bite_argmax_pct_dict)
