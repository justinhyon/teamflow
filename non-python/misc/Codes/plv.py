def plv(raw, segment, blocksize, fsample, numblocks):
    import numpy as np
    import mne
    from mne.connectivity import spectral_connectivity

    print("\nCalculating PLV:")

    E, simlen = generate_sim_events(raw, segment, blocksize, fsample, numblocks)  # Replaces events with equally spaced dummy events to calculate PLV
    epochs = mne.Epochs(raw, E, tmin=-(simlen/fsample)/2, tmax=(simlen/fsample)/2)

    # con, freqs, times, n_epochs, n_tapers = spectral_connectivity(epochs, method='plv', sfreq=self.fSamp, fmin=13.,
    #                                                               fmax=50., n_jobs=6)
    con, freqs, times, n_epochs, n_tapers = spectral_connectivity(epochs, method='plv', sfreq=fsample, fmin=13.,
                                                                  fmax=50., n_jobs=1)

    con = con.mean(axis=2)
    print('Connectivity Matrix dimensions: {}'.format(con.shape))
    # np.delete(con, 257, axis=1)
    # np.delete(con, 257, axis=0)
    # print('Connectivity Matrix dimensions: {}'.format(con.shape))

    intra1 = con[0:int(con.shape[0] / 2), 0:int(con.shape[1] / 2)]
    inter = con[int(con.shape[0] / 2):int(con.shape[0] / 2) * 2, 0:int(con.shape[1] / 2)]
    intra2 = con[int(con.shape[0] / 2):int(con.shape[0] / 2) * 2, int(con.shape[1] / 2):int(con.shape[1] / 2) * 2]
    plv1, plv2, plv3 = [], [], []

    plv2.append(np.mean(inter[0, :-1]))  # 2 triangular sections have no first row, while rectangular section does
    idx = 1
    while idx < int(con.shape[0] / 2):
        plv1.append(np.mean(intra1[idx, 0:idx]))
        plv2.append(np.mean(inter[idx, :]))
        plv3.append(np.mean(intra2[idx, 0:idx]))
        idx += 1
    plv1_mean = np.nanmean(plv1)
    plv2_mean = np.nanmean(plv2)
    plv3_mean = np.nanmean(plv3)

    print("PLV value for intra-brain subject 1: ", plv1_mean)
    print("PLV value for inter-brain: ", plv2_mean)
    print("PLV value for intra-brain subject 2: ", plv3_mean)

    return plv1_mean, plv2_mean, plv3_mean

def generate_sim_events(raw, segment, blocksize, fsample, numblocks):
    import numpy as np
    import math
    import mne
    from mne.io import RawArray

    # Length of a simulated event
    sim_len = math.floor(blocksize / numblocks)
    # Index at which to start the simulated events
    sim_start = sim_len / 2
    stim = []
    stim_idxs = np.arange(sim_start, blocksize, sim_len)
    for idx in np.arange(blocksize):
        if idx in stim_idxs:
            stim.append(1.)
        else:
            stim.append(0.)

    # seg = blocksize / blocksize_sec - 1
    print('Generating {0} simulated events {1} samples apart...'.format(numblocks, sim_len))

    info_stim = mne.create_info(['PLVstim'], sfreq=fsample, ch_types=['stim'])
    raw_stim = RawArray(np.asarray(stim).reshape(1, len(stim)), info_stim)
    PLV_raw = raw.add_channels([raw_stim], force_update_info=True)
    E = mne.find_events(PLV_raw, stim_channel='PLVstim')
    print("Simulated events in segment {0}: {1}".format(segment, E))

    return E, sim_len

    # if self.plotpref != 'none':
    #     self.plv_plot(con)

# def plv_plot(self, data):
#     self.ax[1, 0].cla()  # clears the axes to prepare for new data
#     self.ax[1, 1].cla()
#     self.ax[1, 2].cla()
#     self.ax[1, 3].cla()
#
#     # connectivity matrix
#     self.ax[1, 0].axvline(x=data.shape[0] / 2, color='red')  # horizontal and vertical lines for quadrants
#     self.ax[1, 0].hlines(int(data.shape[0] / 2), 0, data.shape[0], color='red')
#     self.ax[1, 0].imshow(data)  # plots the data
#
#     # average PLV indexes
#     x = np.arange(1, len(self.PLV_intra1) + 1)
#     self.ax[1, 1].bar(x, self.PLV_intra1, width=0.4, color='red')  # index for plv intra 1
#     self.ax[1, 2].bar(x, self.PLV_inter, width=0.4, color='blue')  # index for plv inter
#     self.ax[1, 3].bar(x, self.PLV_intra2, width=0.4, color='green')  # index for plv intra 2
#
#     for i, v in enumerate(self.PLV_intra1):  # adds labels to bars
#         if v != 0.:
#             self.ax[1, 1].text(i + 1 - .2, v, str(round(v, 2)))
#     for i, v in enumerate(self.PLV_inter):
#         if v != 0.:
#             self.ax[1, 2].text(i + 1 - .2, v, str(round(v, 2)))
#     for i, v in enumerate(self.PLV_intra2):
#         if v != 0.:
#             self.ax[1, 3].text(i + 1 - .2, v, str(round(v, 2)))
#
#     self.ax[1, 0].set(title='Connectivity Matrix', xlabel='Channel #', ylabel='Channel #')
#     self.ax[1, 1].set(title='PLV values for Subject 1', xlabel='Segment #', ylabel='PLV Value', ylim=(0, 1))
#     self.ax[1, 2].set(title='PLV Values for Inter-Brain', xlabel='Segment #', ylabel='PLV Value', ylim=(0, 1))
#     self.ax[1, 3].set(title='PLV Values for subject 2', xlabel='Segment #', ylabel='PLV Value', ylim=(0, 1))