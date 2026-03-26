import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path
   
mu0 = 1.25663706e-6
a = 0.005
    
def dipole_model(x, m):
    return mu0 * m / (2 * np.pi * (a**2 + x**2)**(3/2))

def main():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    figures_dir = base_dir / "figures"
    figures_dir.mkdir(exist_ok=True)
    
    hall_x, hv1, hv2, hv3 = np.loadtxt( 
        data_dir / 'hall-probe-data.csv',
        delimiter=',',
        skiprows=1,
        unpack=True
    )
    
    phone_x, b1, b2, b3 = np.loadtxt(
        data_dir / 'iphone-data.csv',
        delimiter=',',
        skiprows=1,
        unpack=True
    ) 
    
    hall_mean_v = (hv1 + hv2 + hv3) / 3
    hall_std_v = np.std([hv1, hv2, hv3], axis=0, ddof=1)
    hall_sem_v = hall_std_v / np.sqrt(3)

    phone_baseline = 12.4e-6
    phone_mean_b = ((b1 - phone_baseline) + (b2 - phone_baseline) + (b3 - phone_baseline)) / 3
    phone_std_b = np.std([b1 - phone_baseline, b2 - phone_baseline, b3 - phone_baseline], axis=0, ddof=1)
    phone_sem_b = phone_std_b / np.sqrt(3)
    
    sensitivity = 50
    hall_b = hall_mean_v / sensitivity
    hall_sem_b = hall_sem_v / sensitivity
    mask_hall = hall_x >= 0.015 # where model is valid
    
    guess = [0.01]
    
    popt_hall, pcov_hall = curve_fit(
        dipole_model,
        hall_x[mask_hall],
        hall_b[mask_hall],
        p0=guess,
        sigma=hall_sem_b[mask_hall],
        absolute_sigma=True
    )
    
    m_hall = popt_hall[0]
    dm_hall = np.sqrt(np.diag(pcov_hall))[0]
    
    popt_phone, pcov_phone = curve_fit(
        dipole_model,
        phone_x,
        phone_mean_b,
        p0=guess,
        sigma=phone_sem_b,
        absolute_sigma=True
    )
    
    m_phone = popt_phone[0]
    dm_phone = np.sqrt(np.diag(pcov_phone))[0]
    
    hall_fit = dipole_model(hall_x[mask_hall], m_hall)
    hall_res = hall_b[mask_hall] - hall_fit
    hall_ss_res = np.sum(hall_res**2)
    hall_ss_tot = np.sum((hall_b[mask_hall] - np.mean(hall_b[mask_hall]))**2)
    hall_r2 = 1 - hall_ss_res / hall_ss_tot
    
    phone_fit = dipole_model(phone_x, m_phone)
    phone_res = phone_mean_b - phone_fit
    phone_ss_res = np.sum(phone_res**2)
    phone_ss_tot = np.sum((phone_mean_b - np.mean(phone_mean_b))**2)
    phone_r2 = 1 - phone_ss_res / phone_ss_tot
    
    xfit_hall = np.linspace(np.min(hall_x[mask_hall]), np.max(hall_x[mask_hall]), 300)
    xfit_phone = np.linspace(np.min(phone_x), np.max(phone_x), 300)
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    
    axs[0].errorbar(
        hall_x,
        hall_b,
        yerr=hall_sem_b,
        fmt='o',
        label='Hall probe data',
        color='tab:purple',
        markersize=4,
        capsize=3,
        ecolor='black',
        elinewidth=2,
        capthick=2
    )
    
    axs[0].plot(
        xfit_hall,
        dipole_model(xfit_hall, m_hall),
        label='Dipole fit (x ≥ 0.015 m)',
        color='tab:purple'
    )
    
    axs[0].set_xlabel('Distance (m)')
    axs[0].set_ylabel('Magnetic field (T)')
    axs[0].set_title('Hall Probe')
    axs[0].legend()
    
    axs[1].errorbar(
        phone_x,
        phone_mean_b,
        yerr=phone_sem_b,
        fmt='o',
        label='iPhone data',
        color='tab:blue',
        markersize=4,
        capsize=3,
        ecolor='black',
        elinewidth=2,
        capthick=2
    )
    axs[1].plot(xfit_phone, dipole_model(xfit_phone, m_phone), label='Dipole fit')
    
    axs[1].set_xlabel('Distance (m)')
    axs[1].set_ylabel('Magnetic field (T)')
    axs[1].set_title('iPhone Magnetometer')
    axs[1].legend()
    
    plt.tight_layout()
    plt.savefig(figures_dir / "magnetic_field_analysis.png", dpi=300)
    plt.show()
    
    print(f"Hall probe magnetic moment: {m_hall:.2e} ± {dm_hall:.1e} A m^2")
    print(f"Hall probe R^2: {hall_r2:.4f}")
    
    print(f"iPhone magnetic moment: {m_phone:.2e} ± {dm_phone:.1e} A m^2")
    print(f"iPhone R^2: {phone_r2:.4f}")

if __name__ == "__main__":
    main()
