#!/usr/bin/env python
# coding: utf-8

# In[10]:


def word_seq(seq, k, stride=1):
    i = 0
    words = []
    while i <= len(seq) - k:
        words.append(seq[i: i + k])
        i += stride
    return words


# In[11]:


def create_dict(nucleotides):
    vec_dict = {}
    perms = k_len_perms(nucleotides, 3)
    perms.sort()
    for idx, seq in enumerate(perms):
        hot_vec = [ 0 for i in range(0, len(perms))]
        hot_vec[idx] = 1
        vec_dict[seq] = hot_vec
    return vec_dict


# In[12]:


def k_len_perms(letters, k):
    n = len(letters)
    perms = []
    k_len_perms_hlpr(perms, letters, "", n, k)
    return perms


# In[13]:


def k_len_perms_hlpr(perms, letters, prefix, n, k):
    if (k == 0):
        perms.append(prefix)
        return
    for i in range(0, n):
        newPrefix = prefix + letters[i]
        k_len_perms_hlpr(perms, letters, newPrefix, n, k - 1)


# In[14]:


def create_rep_mat(words, hot_vec_dict, r_size):
    mat_len = len(words) - r_size + 1
    mat = [[] for i in range(0, mat_len)]
    i = 0
    while i < mat_len:
        j = i
        while j < i + r_size:
            mat[i].append(hot_vec_dict[words[j]])
            j += 1
        i += 1
    return mat


# In[15]:


def get_rep_mat(seq, hot_vec_dict, k=3, r_size=2):
    words = word_seq(seq, k)
    rep_mat = create_rep_mat(words, hot_vec_dict, r_size)
    return rep_mat


# In[16]:


def get_rep_mats(seqs):
    rep_mats = []
    hot_vec_dict = create_dict('ACGT')
    for seq in seqs:
        rep_mat = get_rep_mat(seq, hot_vec_dict, k=3, r_size=1)
        rep_mats.append(rep_mat)
    return rep_mats


# In[17]:


def conv_labels(labels, dataset='splice'):
    converted = []
    for label in labels:
        if dataset == 'splice':
            if label == 'EI':
                converted.append(0)
            elif label == 'IE':
                converted.append(1)
            elif label == 'N':
                converted.append(2)
        elif dataset == 'promoter':
            if label =='+':
                converted.append(0)
            elif label == '-':
                converted.append(1)
    return converted


# In[18]:


if __name__ == "__main__":
    # running on a test sequence matching example in paper
    seq = 'ACCGATTATGCA'
    words = word_seq(seq, 3)
    hot_vec_dict = create_dict('ACGT')
    rep_mat = create_rep_mat(words, hot_vec_dict, 2)

