import numpy as np
from scipy.signal import welch

from .models import EEGRecord


class ReportService:
    def __init__(self):
        self.sf = 125

        self.bands = {
            "delta": (0.5, 4),
            "theta": (4, 8),
            "alpha": (8, 13),
            "beta": (13, 30),
            "gamma": (30, 45),
        }

        self.channel_names = ["O1", "T3", "Fp1", "Fp2", "T4", "O2"]

    def bandpower(self, data, band):
        nperseg = int(4 * self.sf)
        freqs, psd = welch(data, self.sf, nperseg=nperseg)
        idx_band = np.logical_and(freqs >= band[0], freqs <= band[1])
        power = np.trapz(psd[idx_band], freqs[idx_band])
        return power

    def calc_indexes(self, EEG_data):
        channels = dict(zip(self.channel_names, EEG_data))

        alpha_powers = {
            ch: self.bandpower(data, self.bands["alpha"])
            for ch, data in channels.items()
        }
        beta_powers = {
            ch: self.bandpower(data, self.bands["beta"])
            for ch, data in channels.items()
        }
        theta_powers = {
            ch: self.bandpower(data, self.bands["theta"])
            for ch, data in channels.items()
        }

        arousal_values = []
        for ch in self.channel_names:
            alpha = alpha_powers[ch]
            beta = beta_powers[ch]
            arousal_values.append(beta / (alpha + 1e-6))
        arousal = np.mean(arousal_values)

        valence = alpha_powers["Fp2"] - alpha_powers["Fp1"]

        relaxation = (alpha_powers["O1"] + alpha_powers["O2"]) / (
            beta_powers["O1"] + beta_powers["O2"] + 1e-6
        )

        drowsiness = (theta_powers["Fp1"] + theta_powers["Fp2"]) / (
            beta_powers["Fp1"] + beta_powers["Fp2"] + 1e-6
        )

        stress = (beta_powers["Fp1"] + beta_powers["Fp2"]) / (
            theta_powers["Fp1"] + theta_powers["Fp2"] + 1e-6
        )

        beta_sum = (
            beta_powers["Fp1"]
            + beta_powers["Fp2"]
            + beta_powers["T3"]
            + beta_powers["T4"]
        )
        alpha_sum = (
            alpha_powers["Fp1"]
            + alpha_powers["Fp2"]
            + alpha_powers["T3"]
            + alpha_powers["T4"]
        )
        concentration = beta_sum / (alpha_sum + 1e-6)

        return {
            "arousal": arousal,
            "valence": valence,
            "relaxation": relaxation,
            "drowsiness": drowsiness,
            "stress": stress,
            "concentration": concentration,
        }

    def aggregate_indexes(self, employee_ids):
        eeg_data_list = []
        for emp_id in employee_ids:
            eeg_record = (
                EEGRecord.objects.filter(employee_id=emp_id).order_by("-id").first()
            )
            if eeg_record:
                eeg_data_list.append(eeg_record.channel_data)

        inds_by_employees = [self.calc_indexes(data) for data in eeg_data_list]

        aggregated = {}
        keys = inds_by_employees[0].keys()
        for k in keys:
            aggregated[k] = sum(d[k] for d in inds_by_employees) / len(
                inds_by_employees
            )
        return aggregated
