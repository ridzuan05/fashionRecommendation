def get_ndcg(scores_pos, scores_neg, nr_tuples_pos, nr_tuples_neg,
			 fn_out='', tuples_pos=None, tuples_neg=None, nr_return=0):
	"""
	- nr_tuples_pos[ui]: the number of positive outfits for user ui
	- nr_tuples_neg[ui]: the number of negative(neutral) outfits for user ui
	
	- scores_pos: scores for positive outfits. 
				  scores_pos[0:nr_tuples_pos[0]] are the scores for the first user.
				  scores_pos[nr_tuples_pos[0]:nr_tuples_pos[0]+nr_tuples_pos[1]] are the scores for the second user.
				
	- scores_neg: scores for negative outfits. 
				  scores_neg[0:nr_tuples_neg[0]] are the scores for the first user.
				  scores_neg[nr_tuples_neg[0]:nr_tuples_neg[0]+nr_tuples_neg[1]] are the scores for the second user.
	"""
	if fn_out != '':
            fid_out = open(fn_out, 'w')

	m = 10
	ndcg_ct = np.zeros(m)
	ndcg_at = np.zeros(m)
	mean_ndcg = 0
	s_ind_pos = 0
	s_ind_neg = 0
	nr_users = len(nr_tuples_pos) # user number
	for ui in range(nr_users): # for each user
		count_q = nr_tuples_pos[ui] + nr_tuples_neg[ui] # total outfits (both posi & neutral) number of this user
		label = np.zeros(nr_tuples_pos[ui]+nr_tuples_neg[ui])
		label[:nr_tuples_pos[ui]] = 1
		target = np.empty(nr_tuples_pos[ui]+nr_tuples_neg[ui]) # scores for all outfits (both posi & neutral)
		target[:nr_tuples_pos[ui]] = scores_pos[s_ind_pos:s_ind_pos+nr_tuples_pos[ui]]
		target[nr_tuples_pos[ui]:] = scores_neg[s_ind_neg:s_ind_neg+nr_tuples_neg[ui]]
		if fn_out != '':
			tuples = np.hstack((tuples_pos[:,s_ind_pos:s_ind_pos+nr_tuples_pos[ui]],
								tuples_neg[:,s_ind_neg:s_ind_neg+nr_tuples_neg[ui]]))
		s_ind_pos += nr_tuples_pos[ui]
		s_ind_neg += nr_tuples_neg[ui]

		ndcg_size = min(m, count_q)
		ideal_dcg = np.empty(count_q)
		dcg = np.empty(count_q)
		ndcg = 0
		order = np.argsort(-label)
		ideal_dcg[0] = pow(2.0, label[order[0]]) - 1
		for i in range(1, count_q):
			ideal_dcg[i] = ideal_dcg[i-1]+(pow(2.0, label[order[i]])
										   - 1)*np.log(2.0)/np.log(i+1.0)
		order = np.argsort(-target)
		dcg[0] = pow(2.0, label[order[0]]) - 1
		for i in range(1, count_q):
			dcg[i] = dcg[i-1]+(pow(2.0, label[order[i]])
							   - 1)*np.log(2.0)/np.log(i+1.0)
		if ideal_dcg[0] > 0:
			for i in range(count_q):
				ndcg += dcg[i] / ideal_dcg[i]
			for i in range(ndcg_size):
				ndcg_ct[i] += 1
				ndcg_at[i] += dcg[i] / ideal_dcg[i]
		else:
			ndcg = 0
		m_ndcg = ndcg / count_q
		mean_ndcg += m_ndcg

		if fn_out != '':
			fid_out.write('%f\n' % m_ndcg)
			n_out = min(count_q, nr_return)
			for i in range(n_out):
				fid_out.write('%d ' % label[order[i]])
				for jj in range(tuples.shape[0]):
					fid_out.write('%d ' % tuples[jj, order[i]])
				fid_out.write('\n')

	mean_ndcg /= nr_users
	for i in range(m):
		ndcg_at[i] /= ndcg_ct[i]

	if fn_out != '':
		fid_out.close()

	return (mean_ndcg, ndcg_at)