# Используемые библиотеки
from __future__ import unicode_literals 
import csv
import youtube_dl
import pandas as pd
from itertools import chain
import datetime
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import copy

from vosk import Model, KaldiRecognizer
import sys
import wave
import subprocess

import numpy as np

from gensim.models.keyedvectors import KeyedVectors
import gensim 

import scipy.spatial as spatial

import json
from pymystem3 import Mystem

import cv2
import fast_colorthief

import time

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
russian_stopwords = stopwords.words("russian")

import subprocess
import pickle

class Video:
    def __init__(self, start_time, end_time, text, top_colors, keywords):
        self.start_time = start_time
        self.end_time = end_time
        self.text = text  
        self.top_colors = top_colors
        self.keywords = keywords

class Videos:
    def __init__(self, videos):
        self.videos = videos

def chunk_video(from_filepath, start_time, end_time, to_filepath):
    ffmpeg_extract_subclip(from_filepath, start_time, end_time, targetname=to_filepath)

#TEXT EXTRACTION
#!wget https://alphacephei.com/vosk/models/vosk-model-small-ru-0.15.zip
#!unzip vosk-model-small-ru-0.15.zip
#!mv vosk-model-small-ru-0.15 model

sample_rate=16000
model = Model("model")

def extract_text(name):
  rec = KaldiRecognizer(model, sample_rate)
  process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet', '-i', name,'-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                           stdout=subprocess.PIPE)
  while True:
    data = process.stdout.read(4000)
    if len(data) == 0:
         break
    rec.AcceptWaveform(data)
  return eval(rec.FinalResult())['text']

#TEXT PROCESSING
# загрузка модели word2vec
wv = KeyedVectors.load_word2vec_format('model.bin', binary=True)

mystem_to_vec = {'A':'ADJ', 'ADV':'ADV', 'ADVPRO':'x', 'ANUM':'ADJ', 'APRO':'x', 'COM':'x',
                'CONJ':'x', 'INTI':'x', 'NUM':'NUM', 'PART':'x', 'PR':'x', 'S':'NOUN',
                 'SPRO':'x', 'V':'VERB'}
mystem = Mystem()
def vector_value(word):
    part = 'unknown'
    word_found = True

    global mystem
    error = True
    while error:
        try:
            word_analysis = mystem.analyze(word)[0]
            error = False
        except BrokenPipeError:
            mystem = Mystem()
            error = True
    try:
        part = word_analysis[u'analysis'][0][u'gr'].split(',')[0]
        try:
            part = part.split('=')[0]
            part = mystem_to_vec[part]
            value = wv[word + u'_' + part]
            return word_found, value
        except:
            part = word_analysis[u'analysis'][0][u'gr'].split(',')[0]
            part = mystem_to_vec[part]
            request = word + u'_' + part
            value = wv[request]
            return word_found, value
    except:
        word_found = False
        return word_found, [int(0) for i in range(300)]

def safe_mystem_lemmatize(text):
    global mystem
    error = True
    while error:
        try:
            return mystem.lemmatize(text)
        except BrokenPipeError:
            mystem = Mystem()
            continue

def lemmatize(text): 
    return [lemma for lemma in safe_mystem_lemmatize(text) 
            if lemma.strip() != '']  

def is_good_word(word):
    global mystem
    error = True
    while error:
        try:
            word_analysis = mystem.analyze(word)[0]
            error = False
        except BrokenPipeError:
            mystem = Mystem()
            error = True
    try:
        part = word_analysis[u'analysis'][0][u'gr'].split(',')[0]
    except:
        return False
    if '=' not in part and part in mystem_to_vec:
        return mystem_to_vec[part] != 'x'
    if '=' in part:
        part = part.split('=')[0]
        if part in mystem_to_vec:
            return mystem_to_vec[part] != 'x'
    return False

def remove_bad_tokens(tokens):
    return [token for token in tokens if is_good_word(token) 
            and token not in russian_stopwords and len(token) > 1]

def get_text(filename):
    text = extract_text(filename)
    lemmas = lemmatize(text)
    lemmas = remove_bad_tokens(lemmas)
    return lemmas

#COLORS
def get_frame(vidcap, sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
    success, image = vidcap.read()
    return success, image

def get_frames(filepath):
    vidcap = cv2.VideoCapture(filepath)
    sec = 0
    success, image = get_frame(vidcap, sec)
    frames = []
    while success:
        frames.append(image)
        sec += 1
        success, image = get_frame(vidcap, sec)
    return frames

def save_frames(folderpath, frames):
    for i in range(len(frames)):
        print(folderpath+"frame%d.jpg" % i)
        print(cv2.imwrite("./frame%d.jpg" % i, frames[i]))

def save_frame(frame):
    cv2.imwrite("./tmp/image.jpg", frame)

def get_top_colors(filepath):
    frames = get_frames(filepath)
    frames_all_in_one = frames[0]
    for i in range(1, len(frames)):
        frames_all_in_one = np.append(frames_all_in_one, frames[i], axis=0)
    frames_all_in_one = cv2.cvtColor(frames_all_in_one, cv2.COLOR_RGB2RGBA)
    palette = fast_colorthief.get_palette(frames_all_in_one,color_count=5, quality=10)
    palette = [(r/255, g/255, b/255) for r, g, b in palette]
    return palette

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def save_ad_info(from_filepath, to_filepath, keywords=[], share_info=False):
    if share_info != False:
        share_info("Извлекаем текст")
    text = get_text(from_filepath)
    if share_info != False:
        share_info("Извлекаем цвета")
    top_colors = get_top_colors(from_filepath)
    vid_obj = Video(0, 30, text, top_colors, keywords)
    videos = [vid_obj]
    videos_obj = Videos(videos)
    with open(to_filepath + ".pkl", "wb") as f:
        pickle.dump(videos_obj, f)
    if share_info != False:
        share_info("Обработка завершена")
    
def save_video_info(from_filepath, to_filepath, share_info=False):
    vid_duration = get_length(from_filepath)
    videos = []
    for start_time in range(0, int(vid_duration), 30):
        if share_info != False:
            share_info("Фрагмент:" + str(time.strftime('%H:%M:%S', time.gmtime(start_time))))
        end_time = start_time + 30 if start_time + 30 < vid_duration else vid_duration
        if share_info != False:
            share_info("Обрезаем фрагмент")
        chunk_video(from_filepath, start_time, end_time, "./tmp/vid." + from_filepath.split('.')[-1])
        if share_info != False:
            share_info("Извлекаем текст")
        text = get_text("./tmp/vid." + from_filepath.split('.')[-1])
        if share_info != False:
            share_info("Извлекаем цвета")
        top_colors = get_top_colors("./tmp/vid." + from_filepath.split('.')[-1])
        vid_obj = Video(start_time, end_time, text, top_colors, [])
        videos.append(vid_obj)

    videos_obj = Videos(videos)
    with open(to_filepath + "_" + str(start_time) + ".pkl", "wb") as f:
        pickle.dump(videos_obj, f)
    if share_info != False:
        share_info("Обработка завершена")

def download_video(filepath, link):
    link_video=[link]
    ydl_opts = {'format': 'best[height<=720]',
                'outtmpl': os.path.join(filepath, '%(title)s.%(ext)s'),
                'sleep_interval': 30,
                'max_sleep_interval': 40
                }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(link_video)

def make_dict_of_words(swapdict):
    word_id_dict = dict()
    for index, words in swapdict.items():
        for word in words:
            if word in word_id_dict.keys():
                word_id_dict[word].add(index)
            else:
                word_id_dict[word] = set()
                word_id_dict[word].add(index)
    return word_id_dict

def make_query(word_id_dict, query_words_list):
    id_set = set()
    not_all_query_words = False
    new_query_words_list = []
    for word in query_words_list:
        if word not in word_id_dict:
            not_all_query_words = True
        else:
            new_query_words_list.append(word)
    
    query_words_list = new_query_words_list

    if (len(query_words_list) > 0):
        id_set = word_id_dict[query_words_list[0]]
    
    for word in query_words_list[1:]:
        id_set = set.intersection(id_set, word_id_dict[word])
    
    return id_set, not_all_query_words

# TEXT ESTIMATION
def mid_rel_vid_text_dict_vect(ad_words_v_list, vid_tree, vid_words_v_list, word_id_values, 
                          words, mid_rel_freq_dict, radius=3.3):
    mid_rel_vid_dict = dict()
    id_used_words_dict = dict()
    q = vid_tree.query_ball_point(ad_words_v_list, radius)
    for i, query in enumerate(q):
        for word_id in query:
            r_est = 1 - np.linalg.norm(ad_words_v_list[i]-vid_words_v_list[word_id]) / radius
            for vid_id in word_id_values[words[word_id]]:
                if vid_id not in id_used_words_dict:
                    id_used_words_dict[vid_id] = dict()
                if word_id not in id_used_words_dict[vid_id]:
                    id_used_words_dict[vid_id][word_id] = r_est
                else:
                    cur_r = id_used_words_dict[vid_id][word_id]
                    id_used_words_dict[vid_id][word_id] = max(cur_r, r_est)
    for vid_id, used_words in id_used_words_dict.items():
        vid_estimate = 0
        for word_id, rad in used_words.items():
            vid_estimate += rad * mid_rel_freq_dict[vid_id][words[word_id]]
        #vid_estimate /= len(mid_rel_text_dict[vid_id])
        mid_rel_vid_dict[vid_id] = vid_estimate
    return mid_rel_vid_dict

def mid_rel_vid_text_dict_non_vect(ad_words, word_id_values, mid_rel_freq_dict):
    mid_rel_vid_dict = dict()
    id_used_words_dict = dict()
    for word in ad_words:
        if word not in word_id_values:
            continue
        for ID in word_id_values[word]:
            if ID not in id_used_words_dict:
                id_used_words_dict[ID] = list()
            id_used_words_dict[ID].append(word)
    for vid_id, words in id_used_words_dict.items():
        vid_estimate = 0
        for word in words:
            vid_estimate += mid_rel_freq_dict[vid_id][word]
        mid_rel_vid_dict[vid_id] = vid_estimate
    return mid_rel_vid_dict

def get_mid_rel_vid_text_dict(vect_dict, non_vect_dict, mid_rel_text_dict):
    mid_rel_vid_dict = dict()
    for ID, estimation in vect_dict.items():
        mid_rel_vid_dict[ID] = estimation
    for ID, estimation in non_vect_dict.items():
        if ID not in mid_rel_vid_dict:
            mid_rel_vid_dict[ID] = 0
        mid_rel_vid_dict[ID] += estimation
    for ID in mid_rel_vid_dict.keys():
        mid_rel_vid_dict[ID] /= len(mid_rel_text_dict[ID])
    return mid_rel_vid_dict

def get_freq_dict(textdict):
    freq_dict = dict()
    for vid_id, words in textdict.items():
        freq_dict[vid_id] = dict()
        for word in words:
            if word not in freq_dict[vid_id]:
                freq_dict[vid_id][word] = 1
            else:
                freq_dict[vid_id][word] += 1
    return freq_dict

def tokens_to_vec(tokens):
    vectors = []
    for token in tokens:
        word_found, *vect = vector_value(token)
        if word_found:
            vectors.append(*vect)
    return vectors

def get_text_estimate(ad_words, ad_words_v_list, vid_tree, vid_words_v_list, word_id_values, 
                      words, mid_rel_freq_dict, mid_rel_text_dict):
    vect_dict = mid_rel_vid_text_dict_vect(ad_words_v_list, vid_tree, vid_words_v_list, word_id_values, 
                words, mid_rel_freq_dict)
    non_vect_dict = mid_rel_vid_text_dict_non_vect(ad_words, word_id_values, mid_rel_freq_dict)
    final_dict = get_mid_rel_vid_text_dict(vect_dict, non_vect_dict, mid_rel_text_dict)
    final_dict = {key : value for key, value in final_dict.items() if value > 0}
    return final_dict

#COLOR ESTIMATION 
def mid_rel_vid_color_dict_vect(ad_colors_v_list, vid_tree, vid_colors_v_list, color_id_values, 
                                vid_colors, radius=0.13):
    mid_rel_vid_dict = dict()
    id_used_colors_dict = dict()
    q = vid_tree.query_ball_point(ad_colors_v_list, radius)
    for i, query in enumerate(q):
        for color_id in query:
            r_est = 1 - np.linalg.norm(np.array(ad_colors_v_list[i])-np.array(vid_colors_v_list[color_id])) / radius
            for vid_id in color_id_values[vid_colors[color_id]]:
                if vid_id not in id_used_colors_dict:
                    id_used_colors_dict[vid_id] = dict()
                if color_id not in id_used_colors_dict[vid_id]:
                    id_used_colors_dict[vid_id][color_id] = r_est
                else:
                    cur_r = id_used_colors_dict[vid_id][color_id]
                    id_used_colors_dict[vid_id][color_id] = max(cur_r, r_est)
    for vid_id, used_colors in id_used_colors_dict.items():
        vid_estimate = 0
        for color_id, rad in used_colors.items():
            vid_estimate += rad
        vid_estimate /= 5
        mid_rel_vid_dict[vid_id] = vid_estimate
    return mid_rel_vid_dict

def get_color_estimate(ad_colors_v_list, vid_tree, vid_colors_v_list, color_id_values, 
                        vid_colors):
    vect_dict = mid_rel_vid_color_dict_vect(ad_colors_v_list, vid_tree, vid_colors_v_list, color_id_values, 
                                            vid_colors)
    final_dict = {key : value for key, value in vect_dict.items() if value > 0}
    return final_dict

def get_one_ad_estimate(text_dict, color_dict, high_rel_ids, video_names, videos):
    whole_estimate_dict = {key:2*value for key, value in text_dict.items()}
    for key, value in color_dict.items():
        if key not in whole_estimate_dict:
            whole_estimate_dict[key] = 0
        whole_estimate_dict[key] += value

    estimate_list = []

    for key, value in whole_estimate_dict.items():
        text_estimate = text_dict[key] if key in text_dict else 0
        color_estimate = color_dict[key] if key in color_dict else 0
        start_time = str(time.strftime('%H:%M:%S', time.gmtime(videos[key].start_time)))
        
        if key in high_rel_ids:
            estimate_list.append((video_names[key], start_time, 'high_rel', value/3, text_estimate, color_estimate))
        else:
            estimate_list.append((video_names[key], start_time, 'mid_rel', value/3, text_estimate, color_estimate))

    estimate_list = sorted(estimate_list, key=lambda x: x[3], reverse=True)
    return estimate_list


def get_estimate(ads, videos, video_names):
    ad_words_v_lists = [tokens_to_vec(set(tokens)) for tokens in [ad.text for ad in ads]]
    mid_rel_text_dict = {i:video.text for i, video in enumerate(videos)}
    words = list(set([token for tokens in mid_rel_text_dict.values() for token in tokens if vector_value(token)[0]]))
    vid_words_v_list = [vector_value(token)[1:][0] for token in words]
    vid_tree = spatial.cKDTree(vid_words_v_list)
    word_id_values = make_dict_of_words(mid_rel_text_dict)
    mid_rel_freq_dict = get_freq_dict(mid_rel_text_dict)
    ad_non_vect_words = [[token for token in tokens if is_good_word(token) and not vector_value(token)[0]
                                                            and token not in russian_stopwords and len(token) > 1] 
                            for tokens in [ad.text for ad in ads]]

    ad_colors_v_lists = [colors_v for colors_v in [ad.top_colors for ad in ads]]
    mid_rel_colors_dict = {i:video.top_colors for i, video in enumerate(videos)}
    vid_colors = list(set([color for colors in mid_rel_colors_dict.values() for color in colors]))
    vid_colors_v_list = [color_v for color_v in vid_colors]
    vid_color_tree = spatial.cKDTree(vid_colors_v_list)
    color_id_values = make_dict_of_words(mid_rel_colors_dict)

    estimations_list = []
    for i in range(len(ad_words_v_lists)):
        text_estimate = get_text_estimate(ad_non_vect_words[i], ad_words_v_lists[i], vid_tree, vid_words_v_list, word_id_values, 
                        words, mid_rel_freq_dict, mid_rel_text_dict)
        color_estimate = get_color_estimate(ad_colors_v_lists[i], vid_color_tree, vid_colors_v_list, color_id_values, 
                                            vid_colors)
        high_rel_ids, all_words_used = make_query(word_id_values, ads[i].keywords)
        estimations_list.append(get_one_ad_estimate(text_estimate, color_estimate, high_rel_ids, video_names, videos))
    return estimations_list
