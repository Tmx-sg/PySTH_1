import os
import xlwt
import xlrd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FixedLocator, FixedFormatter


# ͨ�ú���
def load_data(file_path):
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_name("Sheet1")
    l = sheet.col_values(2)[1:]
    f = sheet.col_values(3)[1:]
    h = sheet.col_values(4)[1:]
    n = sheet.col_values(5)[1:]
    return l, f, h, n


def calculate_STH(l, f, h, n, Eg, E, VLC):
    Emax = max(l)
    emax = max(h)
    DEmin = min(np.gradient(l))
    dEmin = min(np.gradient(h))

    Eintp = np.arange(Eg, DEmin + Emax, DEmin)
    eintp = np.arange(E, emax + dEmin, dEmin)
    Jintp = np.interp(Eintp, l, f)
    jintp = np.interp(eintp, h, n)
    fintp = np.interp(Eintp, h, n)

    Egg = np.trapz(Jintp, Eintp)
    Eh = np.trapz(jintp, eintp)
    Ef = np.trapz(fintp, Eintp)

    nabs = Egg / 1000.37
    ncu = Eh * 1.23 / Egg
    STH = nabs * ncu
    correctedSTH = STH * 1000.37 / (1000.37 + VLC * Ef)

    return Egg,Eh,Ef
def calculate_STH_Z(l, f, h, n, E):
    Emax = max(l)
    emax = max(h)
    DEmin = min(np.gradient(l))
    dEmin = min(np.gradient(h))
    eintp = np.arange(E, emax + dEmin, dEmin)
    jintp = np.interp(eintp, h, n)
    Eh = np.trapz(jintp, eintp)
    STH = 1.23 * Eh / 1000.37 / 2 * 100
    return STH

def calculate_STH_JanusZ(l, f, h, n, Eg,E,VLC):
    Emax = max(l)
    emax = max(h)
    DEmin = min(np.gradient(l))
    dEmin = min(np.gradient(h))

    Eintp = np.arange(Eg, DEmin + Emax, DEmin)
    eintp = np.arange(E, emax + dEmin, dEmin)
    Jintp = np.interp(Eintp, l, f)
    jintp = np.interp(eintp, h, n)
    fintp = np.interp(Eintp, h, n)

    Egg = np.trapz(Jintp, Eintp)
    Eh = np.trapz(jintp, eintp)
    Ef = np.trapz(fintp, Eintp)

    nabs = Egg / 1000.37
    ncu = Eh * 1.23 / Egg
    STH = nabs * ncu
    correctedSTH = STH * 1000.37 / (1000.37 + VLC * Ef)


    return Egg,Eh,Ef


# General ����Conversion and Janus material
class General:
    def __init__(self, file_path):
        self.l, self.f, self.h, self.n = load_data(file_path)

    def calculate(self, xh, xo, Eg, VLC):
        PH = []
        STH1 = []
        C = []
        title_0 = ["pH", '\u03c7(H2) (eV)', '\u03c7(O2) (eV)', "\u03B7abs (%)", "\u03B7cu (%)", "\u03B7STH (%)"]
        title_1 = ["pH", '\u03c7(H2) (eV)', '\u03c7(O2) (eV)', "\u03B7abs (%)", "\u03B7cu (%)", "\u03B7STH (%)",
                   '\u03B7\u2032STH (%)']
        if VLC == 0:
            C.append(title_0)
        else:
            C.append(title_1)
        for pH in range(0, 15):
            Xh9 = xh - (pH * 0.059)
            Xo9 = xo + (pH * 0.059)
            if Xh9 >= 0 and Xo9 >= 0:
                PH.append(pH)
                E = self.get_E(Xh9, Xo9, Eg)
                Egg,Eh,Ef = calculate_STH(self.l, self.f, self.h, self.n, Eg, E, VLC)
                nabs = Egg / 1000.37
                ncu = Eh * 1.23 / Egg
                STH = nabs * ncu
                correctedSTH = STH * 1000.37 / (1000.37 + VLC * Ef)
                STH1.append(correctedSTH * 100)
                nabs2 = "%.2f" % (nabs * 100)
                ncu2 = "%.2f" % (ncu * 100)
                STH2 = "%.2f" % (STH * 100)
                STH3 = "%.2f" % (correctedSTH * 100)
                Xh2 = "%.2f" % Xh9
                Xo2 = "%.2f" % Xo9
                if VLC == 0:
                    B = [pH, Xh2, Xo2, nabs2, ncu2, STH2]  # Ҫ�����ֵ
                else:
                    B = [pH, Xh2, Xo2, nabs2, ncu2, STH2,STH3]  # Ҫ�����ֵ
                C.append(B)
        return C,PH, STH1

    def get_E(self, Xh9, Xo9, Eg):
        if Xh9 >= 0.2 and Xo9 >= 0.6:
            E = Eg
        elif Xh9 < 0.2 and Xo9 >= 0.6:
            E = Eg + 0.2 - Xh9
        elif Xh9 >= 0.2 and Xo9 < 0.6:
            E = Eg + 0.6 - Xo9
        elif Xh9 < 0.2 and Xo9 < 0.6:
            E = Eg + 0.8 - Xh9 - Xo9
        return max(E, 0.31)

    def plot(self, PH, STH1, save_path):
        plt.figure(figsize=(10, 6))
        plt.plot(PH, STH1, marker='o')
        plt.xlabel('pH')
        plt.ylabel('STH (%)')
        plt.title('Conversion Photocatalysts STH vs pH')
        plt.savefig(save_path)
        plt.show()

    def coSTH(self,VLC, xh, xo, s, E):
        # print(len(E))
        len1 = int(len(E))
        if VLC >= 1.72:
            Xh = np.linspace(0, 2, 201)
            Xo = np.linspace(0, 2, 201)
        elif VLC < 1.72:
            Xh = np.linspace(0, 1, 101)
            Xo = np.linspace(0, 1, 101)
            # Xh = np.linspace(0, 2, 201)
            # Xo = np.linspace(0, 2, 201)

        # VLC = 0
        t0 = E[0]
        xh0 = xh - (t0 * 0.059)
        xo0 = xo + (t0 * 0.059)
        xh = round(xh, 2)
        xo = round(xo, 2)
        t1 = E[-1]

        xh1 = xh - (t1 * 0.059)
        xo1 = xo + (t1 * 0.059)

        xh1 = round(xh1, 2)
        xo1 = round(xo1, 2)

        X, Y = np.meshgrid(Xh, Xo)
        Eg = X + Y + 1.23 - VLC


        Emax = np.max(self.l)
        emax = np.max(self.h)
        # ����С�ݶ�
        DEmin = np.min(np.gradient(self.l))
        dEmin = np.min(np.gradient(self.h))
        r = []
        Z = []
        max = 0
        min = 1000
        for i, Eg0 in zip(Xo, Eg):
            for j, Eg1 in zip(Xh, Eg0):
                if Eg1 < 0:
                    r.append(np.nan)
                    continue
                if j >= 0.2 and i >= 0.6:
                    if Eg1 < 0.31:
                        Eg1 = 0.31
                    E = Eg1
                elif j < 0.2 and i >= 0.6:
                    E = Eg1 + 0.2 - j
                    if E < 0.31:
                        E = 0.31
                    if Eg1 < 0.31:
                        Eg1 = 0.31
                elif j >= 0.2 and i < 0.6:
                    E = Eg1 + 0.6 - i
                    if E < 0.31:
                        E = 0.31
                    if Eg1 < 0.31:
                        Eg1 = 0.31
                elif j < 0.2 and i < 0.6:
                    E = Eg1 + 0.8 - i - j
                    if E < 0.31:
                        E = 0.31
                    if Eg1 < 0.31:
                        Eg1 = 0.31
                Eintp = np.arange(Eg1, DEmin + Emax, DEmin)
                eintp = np.arange(E, emax + dEmin, dEmin)
                Jintp = np.interp(Eintp, self.l, self.f)
                jintp = np.interp(eintp, self.h, self.n)
                fintp = np.interp(Eintp, self.h, self.n)
                Egg = np.trapz(Jintp, Eintp)
                Eh = np.trapz(jintp, eintp)
                Ef = np.trapz(fintp, Eintp)
                nabs = Egg / 1000.37
                ncu = Eh * 1.23 / Egg
                STH = nabs * ncu
                correctedSTH = STH * 1000.37 / (1000.37 + VLC * Ef)
                if xh == round(j, 2) and xo == round(i, 2):
                    ans = correctedSTH * 100
                if xh1 == round(j, 2) and xo1 == round(i, 2):
                    ans1 = correctedSTH * 100
                if correctedSTH >= max:
                    max = correctedSTH
                    xhh = round(j, 2)
                    xoo = round(i, 2)
                if correctedSTH < min:
                    min = correctedSTH
                r.append(correctedSTH * 100)
            Z.append(r)
            r = []

        max = max * 100
        min = min * 100

        mpl.rcParams.update(mpl.rcParamsDefault)
        plt.close('all')
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.set_size_inches(12, 10)
        for spine in ax.spines.values():
            spine.set_linewidth(3)
        colors = ["#86190d", "#dc0105", "#ffad0d", "#edfc1b", "#8efd72", "#1ffee1", "#03bffe", "#0c08ed"]
        # colors = ["#0000ff", "#00ffff", "#00ff00", "#ffff00", "#da0300","#7e0004"]
        colors.reverse()
        cmap = LinearSegmentedColormap.from_list("custom_rainbow", colors)
        cmap_reversed = cmap.reversed()
        norm = mpl.colors.Normalize(vmin=min, vmax=max)
        # mpl.rc('font', size=33,  weight='bold')
        mpl.rc('font', size=40, family='Times New Roman', weight='bold')

        C = ax.contour(X, Y, Z, colors='black', linewidths=0)

        cs = ax.contourf(X, Y, Z, 6, cmap=cmap)  # �����ȸ�ͼ

        x_val, y_val = np.where(np.isclose(Z, max))

        ax.scatter(xh, xo, marker='*', c='black', s=300)
        # #���colorbar
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)  # ��colorbar�Ĵ�С��������
        # ticks = [5, 15, 25, 35]  # �̶�ֵ���������ֵ
        # tick_labels = ['5', '15', '25', '35']  # ��Ӧ�Ŀ̶ȱ�ǩ

        # ticks = [25,30,35]  # �̶�ֵ���������ֵ
        # tick_labels = ['25','30','35']  # ��Ӧ�Ŀ̶ȱ�ǩ
        # cbar.set_ticks(ticks)
        # cbar.set_ticklabels(tick_labels)
        #
        # # ʹ��FixedLocator��FixedFormatter
        # cbar.locator = FixedLocator(ticks)
        # cbar.formatter = FixedFormatter(tick_labels)

        cbar.ax.invert_yaxis()

        cbar.update_ticks()  # ��ʾcolorbar�Ŀ̶�ֵ

        font3 = {'family': 'Times New Roman',
                 'weight': 'bold',
                 'size': 40,
                 }
        ax.set_xlabel('\u03c7(H\u2082) (eV)', font3)
        ax.set_ylabel('\u03c7(O\u2082) (eV)', font3)
        # �������̶ȵı�ǩ�� �������̶���ת�ǶȺ������С����
        if VLC >= 1.72:
            ax.set_xticks([0, 0.4, 0.8, 1.2, 1.6, 2])
            ax.set_xticklabels(['0', '0.4', '0.8', '1.2', '1.6', '2'], fontsize=35, weight='bold',
                               family='Times New Roman')
            ax.set_yticks([0, 0.4, 0.8, 1.2, 1.6, 2])
            ax.set_yticklabels(['', '0.4', '0.8', '1.2', '1.6', '2'], fontsize=35, weight='bold',
                               family='Times New Roman')

            cbar.ax.tick_params(width=3, length=8)
            ax.set_xticks([0.2, 0.4, 1, 1.4, 1.8], minor=True)
            ax.set_yticks([0.2, 0.4, 1, 1.4, 1.8], minor=True)
            ax.tick_params(direction='in', which='both')
            ax.tick_params(axis='x', which='major', width=3, length=8)
            ax.tick_params(axis='x', which='minor', width=2, length=4)
            ax.tick_params(axis='y', which='major', width=3, length=8)
            ax.tick_params(axis='y', which='minor', width=2, length=4)
        elif VLC < 1.72:
            ax.set_xticks([0, 0.2,  0.4, 0.6,0.8,1])
            ax.set_xticklabels(['', '0.2', '0.4','0.6', '0.8', '1'], fontsize=35, weight='bold', family='Times New Roman')
            ax.set_yticks([0,  0.2,  0.4,0.6,0.8,1])
            ax.set_yticklabels(['', '0.2', '0.4','0.6','0.8', '1'], fontsize=35, weight='bold', family='Times New Roman')

            cbar.ax.tick_params(width=3, length=8)
            ax.set_xticks([0.1, 0.3, 0.5, 0.7, 0.9], minor=True)
            ax.set_yticks([0.1, 0.3, 0.5, 0.7, 0.9], minor=True)
            ax.tick_params(direction='in', which='both')
            ax.text(-0.02, -0.02, '0', fontsize=35, weight='bold', family='Times New Roman', ha='right', va='top')
            ax.yaxis.set_tick_params(pad=10)  # ��������ֿ��Ը�����Ҫ����
            ax.xaxis.set_tick_params(pad=10)  # ��������ֿ��Ը�����Ҫ����
            ax.tick_params(axis='x', which='major', width=3, length=8)
            ax.tick_params(axis='x', which='minor', width=2, length=4)
            ax.tick_params(axis='y', which='major', width=3, length=8)
            ax.tick_params(axis='y', which='minor', width=2, length=4)

            # ax.set_xticks([0, 0.4, 0.8, 1.2, 1.6, 2])
            # ax.set_xticklabels(['', '0.4', '0.8', '1.2', '1.6', ''], fontsize=35, weight='bold',
            #                    family='Times New Roman')
            # ax.set_yticks([0, 0.4, 0.8, 1.2, 1.6, 2])
            # ax.set_yticklabels(['', '0.4', '0.8', '1.2', '1.6', '2'], fontsize=35, weight='bold',
            #                    family='Times New Roman')
            # ax.text(-0.02, -0.02, '0', fontsize=35, weight='bold', family='Times New Roman', ha='right', va='top')
            # cbar.ax.tick_params(width=3, length=8)
            # ax.yaxis.set_tick_params(pad=10)  # ��������ֿ��Ը�����Ҫ����
            # ax.xaxis.set_tick_params(pad=10)  # ��������ֿ��Ը�����Ҫ����
            # ax.set_xticks([0.2, 0.4, 1, 1.4, 1.8], minor=True)
            # ax.set_yticks([0.2, 0.4, 1, 1.4, 1.8], minor=True)
            # ax.tick_params(direction='in', which='both')
            # ax.tick_params(axis='x', which='major', width=3, length=8)
            # ax.tick_params(axis='x', which='minor', width=2, length=4)
            # ax.tick_params(axis='y', which='major', width=3, length=8)
            # ax.tick_params(axis='y', which='minor', width=2, length=4)

        # plt.rcParams['figure.figsize']=(6,4)
        plt.rcParams['savefig.dpi'] = 300  # ͼƬ����
        plt.rcParams['figure.dpi'] = 300  # �ֱ���
        # plt.gcf().subplots_adjust(left=0.05, top=0.91, bottom=0.09)
        plt.tight_layout()
        #
        file_path = os.path.join(s, "STH Efficiency vs HER and OER.png")
        fig.savefig(file_path)
        plt.show()
        mpl.rcParams.update(mpl.rcParamsDefault)
        plt.close('all')

        return Xh, Xo, Z

    def Delta_Eg(self,s):
        # Emin = np.min(l)
        Emax = np.max(self.l)
        # emin = min(h)
        emax = np.max(self.l)
        # ����С�ݶ�
        DEmin = np.min(np.gradient(self.l))
        dEmin = np.min(np.gradient(self.h))
        Vlc = np.arange(0, 5.1, 0.01)
        Eg = np.arange(0, 3.1, 0.01)
        X, Y = np.meshgrid(Vlc, Eg)
        r = []
        Z = []
        max = 0
        max1 = 0
        min = 1000
        flag = 1
        for Eg1 in Eg:
            for i in Vlc:
                flag = 1
                for xh in np.arange(0, 1, 0.1):
                    xo = Eg1 - 1.23 + i - xh
                    correctedSTH = 0
                    if xo < 0 and flag == 1:
                        correctedSTH = np.nan
                        max = np.nan
                        break
                    elif xo < 0:
                        break
                    else:
                        if xh >= 0.2 and xo >= 0.6:
                            E = Eg1
                        elif xh < 0.2 and xo >= 0.6:
                            E = Eg1 + 0.2 - xh
                        elif xh >= 0.2 and xo < 0.6:
                            E = Eg1 + 0.6 - xo
                        elif xh < 0.2 and xo < 0.6:
                            E = Eg1 + 0.8 - xh - xo
                        # ��ֵ����
                        Eintp = np.arange(Eg1, DEmin + Emax, DEmin)
                        eintp = np.arange(E, emax + dEmin, dEmin)
                        Jintp = np.interp(Eintp, self.l, self.f)
                        jintp = np.interp(eintp, self.h, self.n)
                        fintp = np.interp(Eintp, self.h, self.n)
                        Egg = np.trapz(Jintp, Eintp)
                        Eh = np.trapz(jintp, eintp)
                        Ef = np.trapz(fintp, Eintp)
                        nabs = Egg / 1000.37
                        ncu = Eh * 1.23 / Egg
                        STH = nabs * ncu
                        correctedSTH = STH * 1000.37 / (1000.37 + i * Ef)
                        flag = 0
                    if correctedSTH * 100 > max:
                        max = correctedSTH * 100
                if max1 < max:
                    max1 = max
                if max < min:
                    min = max

                r.append(max)
                max = 0
            Z.append(r)
            r = []

        max = max1
        min = min
        fig, ax = plt.subplots()
        # plt.figure(figsize=(12, 8))
        fig.set_size_inches(14, 8)
        for spine in ax.spines.values():
            spine.set_linewidth(3)
        colors = ["#86190d", "#dc0105", "#ffad0d", "#edfc1b", "#8efd72", "#1ffee1", "#03bffe", "#0c08ed"]
        # colors = ["#0000ff", "#00ffff", "#00ff00", "#ffff00", "#da0300","#7e0004"]
        colors.reverse()
        cmap = LinearSegmentedColormap.from_list("custom_rainbow", colors)
        cmap_reversed = cmap.reversed()
        norm = mpl.colors.Normalize(vmin=min, vmax=max)
        # ax.rc('font', size=12, family='serif')
        mpl.rc('font', size=30, family='Times New Roman', weight='bold')
        # ��ͼ��text����,(0.68,0.35),(0.72,0.45),(0.61,0.21),
        # lev = [40,36,32,28,24,20,16,12]
        # lev.reverse()
        # manual_locations = [(1.7,0.8),(2,1.2),(2.2,1.4),(2.6,1.8),(3,2.2),(3.5,2.6)](1.5,0.6),
        manual_locations = [(1.7, 0.8), (1.95, 1.1), (2.15, 1.2), (2.4, 1.7), (2.6, 1.8), (2.8, 2.2), (2.8, 2.7)]
        C = ax.contour(X, Y, Z, colors='black', linewidths=0)
        labels = ax.clabel(C, inline=True, fontsize=35, manual=manual_locations)
        for label in labels:
            # label.set_position((label.get_position()[0], label.get_position()[1])-0.03)
            x, y = label.get_position()
            label.set_position((x, y - 0.01))
        #
        cs = ax.contourf(X, Y, Z, 7, cmap=cmap)  # �����ȸ�ͼ
        #
        x_val, y_val = np.where(np.isclose(Z, max))

        # �ڵȸ�ͼ�ϻ�����Щ�㣬ʹ�����η���

        # ��ͼ�б��ZֵΪ0.5�ĵ�
        for i in range(len(x_val)):
            # plt.annotate('*', (X[x_val[i], y_val[i]], Y[x_val[i], y_val[i]]), fontsize=20)
            ax.scatter(X[x_val[i], y_val[i]], Y[x_val[i], y_val[i]], marker='*', c='white', s=300)
            # plt.annotate(f'$\eta^{{max}}_{{STH}}={max:.2f}\%$', (X[x_val[i], y_val[i]], Y[x_val[i], y_val[i]]), textcoords="offset points", xytext=(0, -20),
            #          ha='center', fontsize=20)

        # ax.colorbars(label='correctSTH')
        # #���colorbar
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)  # ��colorbar�Ĵ�С��������
        ticks = [5, 10, 15, 20, 25, 30, 35, 40]  # �̶�ֵ���������ֵ
        tick_labels = ['5', '10', '15', '20', '25', '30', '35', '40']  # ��Ӧ�Ŀ̶ȱ�ǩ

        cbar.set_ticks(ticks)
        cbar.set_ticklabels(tick_labels)
        cbar.ax.invert_yaxis()
        # ʹ��FixedLocator��FixedFormatter
        cbar.locator = FixedLocator(ticks)
        cbar.formatter = FixedFormatter(tick_labels)

        # cbar.set_ticks([10,15,20,25,30,35,max])
        # cbar.set_ticklabels(['10', '15', '20', '25', '30','35','38.18'])
        # cbar.ax.set_title('�ǡ�$_{STH}$ $\%$',fontsize=40,weight='bold', family='Times New Roman',pad=15)
        cbar.update_ticks()  # ��ʾcolorbar�Ŀ̶�ֵ
        # ticks = cbar.get_ticks()  # ��ȡ��ǰ�Ŀ̶ȱ�ǩ
        # new_ticks = ticks +0  # �����ƶ�2����λ
        # cbar.set_ticks(new_ticks)  # �����µĿ̶ȱ�ǩ

        font3 = {'family': 'Times New Roman',
                 'weight': 'bold',
                 'size': 40,
                 }
        ax.set_xlabel('\u0394\u03A6 (eV)', font3)
        ax.set_ylabel('Band gap (eV)', font3)
        # �������̶ȵı�ǩ�� �������̶���ת�ǶȺ������С����
        ax.set_xticks([0, 1, 2, 3, 4, 5])
        ax.set_xticklabels(['0', '1', '2', '3', '4', '5'], fontsize=35, weight='bold', family='Times New Roman')
        ax.set_yticks([0, 0.5, 1, 1.5, 2, 2.5, 3])
        ax.set_yticklabels(['', '0.5', '1', '1.5', '2', '2.5', '3'], fontsize=35, weight='bold',
                           family='Times New Roman')

        ax.tick_params(direction='in', which='both')
        ax.tick_params(axis='x', which='major', width=3, length=8)
        ax.tick_params(axis='y', which='major', width=3, length=8)
        # plt.rcParams['figure.figsize']=(6,4)
        plt.rcParams['savefig.dpi'] = 300  # ͼƬ����
        plt.rcParams['figure.dpi'] = 300  # �ֱ���
        # plt.gcf().subplots_adjust(left=0.05, top=0.91, bottom=0.09)
        plt.tight_layout()
        file_path = os.path.join(s, "BandGap_Map.png")
        fig.savefig(file_path)
        #
        plt.show()
        mpl.rcParams.update(mpl.rcParamsDefault)
        # fig.savefig(r'D:\tu\python\myplot_Eg.png')

        return Vlc, Eg, Z

    def CBM_VBM(self,VLC, C, V, s, t1):

        C = round(C, 2)
        V = round(V, 2)

        # print(names1)
        emax = np.max(self.h)
        # ����С�ݶ�
        DEmin = np.min(np.gradient(self.l))
        dEmin = np.min(np.gradient(self.h))
        r = []
        Z = []
        max = 0
        min = 1000
        CBM = np.arange(-4.44, -3.44, 0.01)
        VBM = np.arange(-6.67, -5.66, 0.01)
        X, Y = np.meshgrid(CBM, VBM)
        Eg = X - Y
        ans = 0
        for i, Eg0 in zip(VBM, Eg):
            for j, Eg1 in zip(CBM, Eg0):
                # print(i,j,Eg1)
                xh = j + 4.44 + VLC - (t1 * 0.059)
                xo = -5.67 - i + (t1 * 0.059)
                if (xh < 0 or xo < 0) or Eg1 < 1.23:
                    r.append(np.nan)
                    continue
                if xh >= 0.2 and xo >= 0.6:
                    E = Eg1

                elif xh < 0.2 and xo >= 0.6:
                    E = Eg1 + 0.2 - xh

                elif xh >= 0.2 and xo < 0.6:
                    E = Eg1 + 0.6 - xo

                elif xh < 0.2 and xo < 0.6:
                    E = Eg1 + 0.8 - xh - xo

                Eintp = np.arange(Eg1, DEmin + emax, DEmin)  # �޳�
                eintp = np.arange(E, emax + dEmin, dEmin)  # �г�
                Jintp = np.interp(Eintp, self.l, self.f)
                jintp = np.interp(eintp, self.h, self.n)
                fintp = np.interp(Eintp, self.h, self.n)
                Egg = np.trapz(Jintp, Eintp)
                Eh = np.trapz(jintp, eintp)
                Ef = np.trapz(fintp, Eintp)

                nabs = Egg / 1000.37

                ncu = Eh * 1.23 / Egg
                # STH = Eh * 1.23 / 1000.37
                STH = nabs * ncu
                correctedSTH = STH * 1000.37 / (1000.37 + VLC * Ef)
                if C == round(j, 2) and V == round(i, 2):
                    ans = correctedSTH * 100
                if correctedSTH >= max:
                    max = correctedSTH
                if correctedSTH < min:
                    min = correctedSTH

                r.append(correctedSTH * 100)
            Z.append(r)
            r = []

        max = max * 100
        min = min * 100
        fig, ax = plt.subplots(figsize=(10, 8))
        # plt.figure(figsize=(10, 8))
        fig.set_size_inches(12, 10)
        for spine in ax.spines.values():
            spine.set_linewidth(3)
        colors = ["#86190d", "#dc0105", "#ffad0d", "#edfc1b", "#8efd72", "#1ffee1", "#03bffe", "#0c08ed"]
        # colors = ["#0000ff", "#00ffff", "#00ff00", "#ffff00", "#da0300","#7e0004"]
        colors.reverse()
        cmap = LinearSegmentedColormap.from_list("custom_rainbow", colors)
        cmap_reversed = cmap.reversed()
        norm = mpl.colors.Normalize(vmin=min, vmax=max)
        # ax.rc('font', size=12, family='serif')
        mpl.rc('font', size=40, family='Times New Roman', weight='bold')
        cs = ax.contourf(X, Y, Z, cmap=cmap)  # �����ȸ�ͼ

        x_val, y_val = np.where(np.isclose(Z, max))
        # print(x_val)
        # print(y_val)

        # ��ͼ�б��ZֵΪ0.5�ĵ�\u2032
        # title = ["pH", '\u03c7h', '\u03c7o', "\u03B7abs", "\u03B7cu", "\u03B7STH", '\u03B7\u2032STH']
        # plt.annotate(f'({C:.2f}, {V:.2f})', (C, V), textcoords="offset points", xytext=(0, -20),#����
        #              ha='center', fontsize=20)
        if VLC == 0:

            pass
            # plt.annotate(f'$\eta_{{STH}}={ans:.2f}\%$', (C, V), textcoords="offset points", xytext=(0, 10),
            #          ha='center', fontsize=25)
        #
        else:
            plt.annotate(f'{ans:.2f}%', (C, V), textcoords="offset points", xytext=(30, 10),
                         ha='center', fontsize=25)
        if VLC == 0:
            for i in range(len(x_val)):
                ax.scatter(X[x_val[i], y_val[i]], Y[x_val[i], y_val[i]], marker='*', c='black', s=1)
                cc = X[x_val[i], y_val[i]]
                vv = Y[x_val[i], y_val[i]]
            # plt.annotate(f'$\eta^{{max}}_{{STH}}={max:.2f}\%$', (-4.3, -6.4),
            #              textcoords="offset points", xytext=(60, -10), ha='center', fontsize=25, c='black')
        else:
            for i in range(len(x_val)):
                ax.scatter(X[x_val[i], y_val[i]], Y[x_val[i], y_val[i]], marker='*', c='black', s=100)
            # plt.annotate(f'$\eta^{{max}}_{{STH}}={max:.2f}\%$', (X[x_val[-1], y_val[-1]], Y[x_val[-1], y_val[-1]]),
            #              textcoords="offset points", xytext=(60, 20), ha='center', fontsize=25, c='black')
            # plt.annotate('*', (X[x_val[i], y_val[i]], Y[x_val[i], y_val[i]]), fontsize=20)

        if C >= -4.44 and C < -2.23 and V >= -7.3 and V < -4.66:
            ax.scatter(C, V, marker='*', c='black', s=300)
            # plt.annotate(f'pH={0}', (C, V), textcoords="offset points", xytext=(0, -30),
            #              ha='center', fontsize=25)

        # ax.colorbars(label='correctSTH')
        # #���colorbar
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)  # ��colorbar�Ĵ�С��������
        # ticks = [1, 3, 6, 9, 12, 15]  # �̶�ֵ���������ֵ
        # tick_labels = ['1', '3', '6', '9', '12', '15']  # ��Ӧ�Ŀ̶ȱ�ǩ
        # cbar.set_ticks(ticks)
        # cbar.set_ticklabels(tick_labels)
        #
        # # ʹ��FixedLocator��FixedFormatter
        # cbar.locator = FixedLocator(ticks)
        # cbar.formatter = FixedFormatter(tick_labels)
        cbar.ax.invert_yaxis()
        # cbar.set_ticks([10,15,20,25,30,35,max])
        # cbar.set_ticklabels(['10', '15', '20', '25', '30','35','38.18'])
        # cbar.ax.set_title('�ǡ�$_{STH}$ $\%$',fontsize=40,weight='bold', family='Times New Roman',pad=15)
        cbar.update_ticks()  # ��ʾcolorbar�Ŀ̶�ֵ
        # ticks = cbar.get_ticks()  # ��ȡ��ǰ�Ŀ̶ȱ�ǩ
        # new_ticks = ticks +0  # �����ƶ�2����λ
        # cbar.set_ticks(new_ticks)  # �����µĿ̶ȱ�ǩ

        font3 = {'family': 'Times New Roman',
                 'weight': 'bold',
                 'size': 40,
                 }
        ax.set_xlabel('CBM (eV)', font3)
        ax.set_ylabel('VBM (eV)', font3)
        # �������̶ȵı�ǩ�� �������̶���ת�ǶȺ������С����
        ax.set_xticks([-4.44, -4.24, -4.04, -3.84, -3.64, -3.44])
        ax.set_xticklabels(['-4.44', '-4.24', '-4.04', '-3.84', '-3.64', '-3.44'], fontsize=35, weight='bold',
                           family='Times New Roman')
        ax.set_yticks([-6.67, -6.27, -5.97, -5.67])
        ax.set_yticklabels([ '', '-6.27', '-5.97', '-5.67'], fontsize=35, weight='bold',
                           family='Times New Roman')
        ax.yaxis.set_tick_params(pad=10)  # ��������ֿ��Ը�����Ҫ����
        ax.xaxis.set_tick_params(pad=10)  # ��������ֿ��Ը�����Ҫ����
        cbar.ax.tick_params(width=3, length=8)
        # ax.set_xticks([0.2, 0.4, 1, 1.4, 1.8], minor=True)
        # ax.set_yticks([0.2, 0.4, 1, 1.4, 1.8], minor=True)
        ax.tick_params(direction='in', which='both')
        ax.tick_params(axis='x', which='major', width=3, length=8)
        # ax.tick_params(axis='x', which='minor', width=2, length=4)
        ax.tick_params(axis='y', which='major', width=3, length=8)
        # ax.tick_params(axis='y', which='minor', width=2, length=4)
        # plt.rcParams['figure.figsize']=(6,4)
        plt.rcParams['savefig.dpi'] = 300  # ͼƬ����
        plt.rcParams['figure.dpi'] = 300  # �ֱ���
        # plt.gcf().subplots_adjust(left=0.05, top=0.91, bottom=0.09)

        plt.tight_layout()
        file_path = os.path.join(s, "STH Efficiency vs CBM and VBM.png")
        fig.savefig(file_path)
        #
        plt.show()
        mpl.rcParams.update(mpl.rcParamsDefault)
        plt.close('all')
        # fig.savefig(r'D:\tu\python\CBM_VBM_0.png')
        return CBM, VBM, Z

    def CBM_VBM_J(self,VLC, C, V, s):
        emax = np.max(self.h)
        # ����С�ݶ�
        DEmin = np.min(np.gradient(self.l))
        dEmin = np.min(np.gradient(self.h))
        r = []
        Z = []
        max = 0
        min = 1000
        CBM = np.arange(-5.44, -3.42, 0.01)
        VBM = np.arange(-7.66, -5.66, 0.01)
        X, Y = np.meshgrid(CBM, VBM)
        Eg = X - Y
        ans = 0
        for i, Eg0 in zip(VBM, Eg):
            for j, Eg1 in zip(CBM, Eg0):
                # print(i,j,Eg1)
                xh = j + 4.44 + VLC
                xo = -5.67 - i
                if (xh < 0 or xo < 0):
                    r.append(np.nan)
                    continue
                if xh >= 0.2 and xo >= 0.6:
                    if Eg1 < 0.31:
                        Eg1 = 0.31
                    E = Eg1

                elif xh < 0.2 and xo >= 0.6:
                    if Eg1 < 0.31:
                        Eg1 = 0.31
                    E = Eg1 + 0.2 - xh
                    if E < 0.31:
                        E = 0.31

                elif xh >= 0.2 and xo < 0.6:
                    if Eg1 < 0.31:
                        Eg1 = 0.31
                    E = Eg1 + 0.6 - xo
                    if E < 0.31:
                        E = 0.31
                elif xh < 0.2 and xo < 0.6:
                    if Eg1 < 0.31:
                        Eg1 = 0.31
                    E = Eg1 + 0.8 - xh - xo
                    if E < 0.31:
                        E = 0.31

                Eintp = np.arange(Eg1, DEmin + emax, DEmin)  # �޳�
                eintp = np.arange(E, emax + dEmin, dEmin)  # �г�
                Jintp = np.interp(Eintp, self.l, self.f)
                jintp = np.interp(eintp, self.h, self.n)
                fintp = np.interp(Eintp, self.h, self.n)
                Egg = np.trapz(Jintp, Eintp)
                Eh = np.trapz(jintp, eintp)
                Ef = np.trapz(fintp, Eintp)

                nabs = Egg / 1000.37

                ncu = Eh * 1.23 / Egg
                # STH = Eh * 1.23 / 1000.37
                STH = nabs * ncu
                correctedSTH = STH * 1000.37 / (1000.37 + VLC * Ef)
                if C == round(j, 2) and V == round(i, 2):
                    ans = correctedSTH * 100

                if correctedSTH >= max:
                    max = correctedSTH
                if correctedSTH < min:
                    min = correctedSTH

                r.append(correctedSTH * 100)
            Z.append(r)
            r = []

        max1 = max * 100
        min1 = min * 100
        print(max1)
        print(min1)
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.set_size_inches(12, 10)
        for spine in ax.spines.values():
            spine.set_linewidth(3)
        colors = ["#86190d", "#dc0105", "#ffad0d", "#edfc1b", "#8efd72", "#1ffee1", "#03bffe", "#0c08ed"]
        # colors = ["#0000ff", "#00ffff", "#00ff00", "#ffff00", "#da0300","#7e0004"]
        colors.reverse()
        cmap = LinearSegmentedColormap.from_list("custom_rainbow", colors)
        cmap_reversed = cmap.reversed()
        norm = mpl.colors.Normalize(vmin=min1, vmax=max1)
        # ax.rc('font', size=12, family='serif')
        mpl.rc('font', size=40, family='Times New Roman', weight='bold')
        cs = ax.contourf(X, Y, Z, 6, cmap=cmap)  # �����ȸ�ͼ

        x_val, y_val = np.where(np.isclose(Z, max1))

        ax.scatter(C, V, marker='*', c='white', s=500)
        #
        # ax.colorbars(label='correctSTH')
        # #���colorbar
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)  # ��colorbar�Ĵ�С��������
        ticks = [5, 15, 25, 35]  # �̶�ֵ���������ֵ
        tick_labels = ['5', '15', '25', '35']  # ��Ӧ�Ŀ̶ȱ�ǩ

        # ticks = [25,30,35]  # �̶�ֵ���������ֵ
        # tick_labels = ['25','30','35']  # ��Ӧ�Ŀ̶ȱ�ǩ
        cbar.set_ticks(ticks)
        cbar.set_ticklabels(tick_labels)

        # ʹ��FixedLocator��FixedFormatter
        cbar.locator = FixedLocator(ticks)
        cbar.formatter = FixedFormatter(tick_labels)

        # cbar.ax.invert_xaxis()

        cbar.ax.invert_yaxis()
        # cbar.set_ticks([10,15,20,25,30,35,max])
        # cbar.set_ticklabels(['10', '15', '20', '25', '30','35','38.18'])
        # cbar.ax.set_title('�ǡ�$_{STH}$ $\%$',fontsize=40,weight='bold', family='Times New Roman',pad=15)
        cbar.update_ticks()  # ��ʾcolorbar�Ŀ̶�ֵ
        # ticks = cbar.get_ticks()  # ��ȡ��ǰ�Ŀ̶ȱ�ǩ
        # new_ticks = ticks +0  # �����ƶ�2����λ
        # cbar.set_ticks(new_ticks)  # �����µĿ̶ȱ�ǩ

        font3 = {'family': 'Times New Roman',
                 'weight': 'bold',
                 'size': 40,
                 }
        ax.set_xlabel('CBM (eV)', font3)
        ax.set_ylabel('VBM (eV)', font3)
        # �������̶ȵı�ǩ�� �������̶���ת�ǶȺ������С����
        ax.set_xticks([-4.44, -4.94, -4.44, -3.94, -3.44])
        ax.set_xticklabels(['-4.44', '-4.94', '-4.44', '-3.94', ''], fontsize=35, weight='bold',
                           family='Times New Roman')
        ax.set_yticks([ -6.67, -6.17, -5.67])
        ax.set_yticklabels([ '', '-6.17', '-5.67'], fontsize=35, weight='bold',
                           family='Times New Roman')

        ax.set_xticks([-5.19, -4.69, -4.19, -3.69], minor=True)
        ax.set_yticks([-7.42, -6.92, -6.42, -5.92], minor=True)
        ax.tick_params(direction='in', which='both')
        ax.tick_params(axis='x', which='major', width=3, length=8)
        ax.tick_params(axis='x', which='minor', width=2, length=4)
        ax.tick_params(axis='y', which='major', width=3, length=8)
        ax.tick_params(axis='y', which='minor', width=2, length=4)

        ax.yaxis.set_tick_params(pad=10)  # ��������ֿ��Ը�����Ҫ����
        ax.xaxis.set_tick_params(pad=10)  # ��������ֿ��Ը�����Ҫ����
        cbar.ax.tick_params(width=3, length=8)
        # ax.set_xticks([0.2, 0.4, 1, 1.4, 1.8], minor=True)
        # ax.set_yticks([0.2, 0.4, 1, 1.4, 1.8], minor=True)
        ax.tick_params(direction='in', which='both')
        ax.tick_params(axis='x', which='major', width=3, length=8)
        # ax.tick_params(axis='x', which='minor', width=2, length=4)
        ax.tick_params(axis='y', which='major', width=3, length=8)
        # ax.tick_params(axis='y', which='minor', width=2, length=4)
        # plt.rcParams['figure.figsize']=(6,4)
        plt.rcParams['savefig.dpi'] = 300  # ͼƬ����
        plt.rcParams['figure.dpi'] = 300  # �ֱ���
        # plt.gcf().subplots_adjust(left=0.05, top=0.91, bottom=0.09)

        plt.tight_layout()
        file_path = os.path.join(s, "STH Efficiency vs CBM and VBM.png")
        fig.savefig(file_path)
        #
        plt.show()
        mpl.rcParams.update(mpl.rcParamsDefault)
        plt.close('all')
        # fig.savefig(r'D:\tu\python\CBM_VBM_0.png')
        return CBM, VBM, Z

    def Save_coSTH(self,xh, xo, sth, s, g):



        # ����һά�б��һ����ά�б�
        list1 = [1, 2, 3]
        list2 = ['a', 'b', 'c']
        list3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        # �����ݱ��浽dat�ļ�

        # title = ["pH", '\u03c7h', '\u03c7o', "\u03B7abs", "\u03B7cu", "\u03B7STH", '\u03B7\u2032STH']
        # �����ݱ��浽���ļ����е�dat�ļ�
        file_path = os.path.join(s, "STH Efficiency vs HER and OER.dat")
        with open(file_path, "w") as file:
            # "{:<5}".format
            if g == 0:
                file.write("{:<10}{:<10}{:<10}\n".format('\u03c7(h) (eV)', '\u03c7(o) (eV)', '\u03B7STH (%)'))
            elif g == 1:
                file.write("{:<10}{:<10}{:<10}\n".format('\u03c7(h) (eV)', '\u03c7(o) (eV)', '\u03B7\u2032STH (%)'))
            # file.write(f"Xh\t\t\t\tXo\t\t\t\tSTH%\n")
            for i, j, k in zip(xh, xo, sth):
                i = float(i)
                j = float(j)
                file.write("{:<10.2f}{:<10.2f}".format(i, j))
                for k1 in k:
                    k1 = float(k1)
                    file.write("{:<10.2f}".format(k1))
                file.write('\n')

    def Save_CBM_VBM(self,C, V, Z, s, g):

        # �����ݱ��浽���ļ����е�dat�ļ�
        file_path = os.path.join(s, "STH Efficiency vs CBM and VBM.dat")
        with open(file_path, "w") as file:
            if g == 0:

                file.write("{:<10}{:<10}{:<10}\n".format('CBM', 'VBM', '\u03B7STH (%)'))

            elif g == 1:
                file.write("{:<10}{:<10}{:<10}\n".format('CBM', 'VBM', '\u03B7\u2032STH (%)'))
            for i, j, k in zip(C, V, Z):
                file.write("{:<10.2f}{:<10.2f}".format(i, j))
                for k1 in k:
                    file.write("{:<10.2f}".format(k1))
                file.write('\n')

        pass

    def Save_Delta_Eg(self,VLC, Eg, STH, s):

        # �����ݱ��浽���ļ����е�dat�ļ�
        file_path = os.path.join(s, "STH Efficiency vs Eg and $\Delta\Phi$.dat")
        with open(file_path, "w") as file:
            # file.write(f"VLC\t\t\tEg\t\t\tSTH%\n")
            file.write("{:<10}{:<10}{:<10}\n".format('\u0394\u03C6', 'Eg', '\u03B7\u2032STH (%)'))
            for i, j, k in zip(VLC, Eg, STH):
                file.write("{:<10.2f}{:<10.2f}".format(i, j))
                for k1 in k:
                    file.write("{:<10.2f}".format(k1))
                file.write('\n')


# Janus ����

# Heterojunction_Z ����
class Heterojunction_Z:
    def __init__(self, file_path):
        self.l, self.f, self.h, self.n = load_data(file_path)

    def calculate(self, Eg1, Eg2):
        E1 = max(Eg1, Eg2)
        if E1 < 0.615:
            E1 = 0.615
        STH = calculate_STH_Z(self.l, self.f, self.h, self.n, E1)
        return STH

    def plot(self, save_path):
        # Heterojunction_Z ���͵ĳ�ͼ�߼�
        pass

    def Z_STH(self,s):
        emax = np.max(self.h)
        # ����С�ݶ�
        DEmin = np.min(np.gradient(self.l))
        dEmin = np.min(np.gradient(self.h))
        mpl.rcParams.update(mpl.rcParamsDefault)
        plt.close('all')
        Eg1 = np.linspace(0, 3, 301)
        Eg2 = np.linspace(0, 3, 301)
        Y, X = np.meshgrid(Eg1, Eg2)
        dEmin = np.min(np.gradient(self.l))
        E11 = 1.9
        E22 = 1.39
        r = []
        Z = []
        maxx = []
        ans = 0
        max1 = 0
        min1 = 1000
        for i in Eg1:
            for j in Eg2:
                if i + j < 1.23:
                    r.append(np.nan)
                else:

                    E1 = max(i, j)
                    if E1 < 0.615:
                        E1 = 0.615
                    # Eintp = np.arange(Eg1 , DEmin+Emax,DEmin)#�޳�
                    eintp = np.arange(E1, emax + dEmin, dEmin)  # �г�
                    # Jintp = np.interp(Eintp, l, f)
                    jintp = np.interp(eintp, self.h, self.n)
                    # fintp = np.interp(Eintp, h, n)
                    # Egg = np.trapz(Jintp, Eintp)
                    Eh = np.trapz(jintp, eintp)
                    # Ef = np.trapz(fintp, Eintp)
                    # nabs = Egg/1000.37
                    # ncu = Eh*1.23/Egg
                    STH = 1.23 * Eh / 1000.37 / 2 * 100
                    # if e1 == round(i,2) and e2 == round(j,2):
                    #     print(STH)
                    if STH >= max1:
                        max1 = STH
                    if STH < min1:
                        min1 = STH
                    r.append(STH)

            Z.append(r)
            r = []

        fig, ax = plt.subplots()
        # fig.set_size_inches(8, 10)
        fig.set_size_inches(12, 10)

        for spine in ax.spines.values():
            spine.set_linewidth(3)
        # colors = ["#86190d","#86190d","#dc0105","#ffad0d","#edfc1b","#8efd72","#1ffee1","#03bffe","#0c08ed"]
        colors = ["#86190d", "#dc0105", "#ffad0d", "#edfc1b", "#8efd72", "#1ffee1", "#03bffe", "#0c08ed"]
        # colors = ["#0000ff", "#00ffff", "#00ff00", "#ffff00", "#da0300","#7e0004"]"#0c08ed",
        colors.reverse()
        cmap = LinearSegmentedColormap.from_list("custom_rainbow", colors)
        cmap_reversed = cmap.reversed()
        norm = mpl.colors.Normalize(vmin=min1, vmax=max1)
        # ax.rc('font', size=12, family='serif')
        mpl.rc('font', size=33, family='Times New Roman', weight='bold')

        manual_locations = [(0.22, 0.63), (0.35, 0.7), (0.5, 0.8), (0.8, 0.83), (0.9, 0.9)]

        C = ax.contour(X, Y, Z, colors='black', linewidths=0)

        cs = ax.contourf(X, Y, Z, 5, cmap=cmap)  # �����ȸ�ͼ

        x_val, y_val = np.where(np.isclose(Z, max1))
        # for i in range(len(x_val)):
        # ax.scatter(X[x_val[-1], y_val[-1]], Y[x_val[-1], y_val[-1]], marker='*', c='black', s=500)

        # ax.scatter(Eg_1, Eg_2, marker='*', c='white', s=500)

        x_val, y_val = np.where(np.isclose(Z, max1))

        points = []
        # ��ͼ�б��ZֵΪ0.5�ĵ�
        for i in range(len(x_val)):
            ax.scatter(X[x_val[i], y_val[i]], Y[x_val[i], y_val[i]], marker='*', c='black', s=20)

        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)

        ticks = [5, 10, 15, 20, 25, 30, 35]  # �̶�ֵ���������ֵ
        tick_labels = ['5', '10', '15', '20', '25', '30', '35']  # ��Ӧ�Ŀ̶ȱ�ǩ

        # ticks = [25,30,35]  # �̶�ֵ���������ֵ
        # tick_labels = ['25','30','35']  # ��Ӧ�Ŀ̶ȱ�ǩ
        cbar.set_ticks(ticks)
        cbar.set_ticklabels(tick_labels)

        # ʹ��FixedLocator��FixedFormatter
        cbar.locator = FixedLocator(ticks)
        cbar.formatter = FixedFormatter(tick_labels)

        # cbar.ax.invert_xaxis()

        cbar.ax.invert_yaxis()

        cbar.update_ticks()  # ��ʾcolorbar�Ŀ̶�ֵ

        font3 = {'family': 'Times New Roman',
                 'weight': 'bold',
                 'size': 40,
                 }
        ax.set_xlabel('Eg\u2081 (eV)', font3)
        ax.set_ylabel('Eg\u2082 (eV)', font3)

        ax.set_xticks([0, 1, 2, 3])
        ax.set_xticklabels(['0', '1', '2', '3'], fontsize=35, weight='bold', family='Times New Roman')
        ax.set_yticks([0, 1, 2, 3])
        ax.set_yticklabels(['', '1', '2', '3'], fontsize=35, weight='bold', family='Times New Roman')
        cbar.ax.tick_params(width=3, length=8)
        ax.set_xticks([0.5, 1.5, 2.5], minor=True)
        ax.set_yticks([0.5, 1.5, 2.5], minor=True)
        ax.tick_params(direction='in', which='both')
        ax.tick_params(axis='x', which='major', width=3, length=8)
        ax.tick_params(axis='x', which='minor', width=2, length=4)
        ax.tick_params(axis='y', which='major', width=3, length=8)
        ax.tick_params(axis='y', which='minor', width=2, length=4)

        plt.rcParams['savefig.dpi'] = 300  # ͼƬ����
        plt.rcParams['figure.dpi'] = 300  # �ֱ���
        # plt.gcf().subplots_adjust(left=0.05, top=0.91, bottom=0.09)
        plt.tight_layout()
        #
        plt.show()
        file_path = os.path.join(s, "STH Efficiency vs Eg1 and Eg2.png")
        fig.savefig(file_path)
        return Eg1,Eg2,Z

    def Save_Z(self,Eg1, Eg2, Z, s):

        # �����ݱ��浽���ļ����е�dat�ļ�
        file_path = os.path.join(s, "STH Efficiency vs Eg1 and Eg2.dat")
        with open(file_path, "w") as file:


            file.write("{:<10}{:<10}{:<10}\n".format('Eg1', 'Eg2', '\u03B7STH (%)'))

            for i, j, k in zip(Eg1, Eg2, Z):
                file.write("{:<10.2f}{:<10.2f}".format(i, j))
                for k1 in k:
                    file.write("{:<10.2f}".format(k1))
                file.write('\n')

        pass

# Janus_Z ����
class Janus_Z:
    def __init__(self, file_path):
        self.l, self.f, self.h, self.n = load_data(file_path)

    def calculate(self, xh, xo, Eg, VLC):
        title_1 = ["pH", '\u03c7(H2) (eV)', '\u03c7(O2) (eV)', "\u03B7abs (%)", "\u03B7cu (%)", "\u03B7STH (%)",
                   '\u03B7\u2032STH (%)']
        PH = []
        STH1 = []
        C = []
        C.append(title_1)
        for pH in range(0, 15):
            Xh9 = xh - (pH * 0.059) + VLC
            Xo9 = xo + (pH * 0.059)
            if Xh9 >= 0 and Xo9 >= 0:
                PH.append(pH)
                E = self.get_E(Xh9, Xo9, Eg)
                Egg,Eh,Ef = calculate_STH_JanusZ(self.l, self.f, self.h, self.n, Eg, E, VLC)
                nabs = Egg / 1000.37/2
                ncu = Eh * 1.23 / Egg
                STH = nabs * ncu
                correctedSTH = STH * 1000.37 / (1000.37 + VLC * Ef)
                STH1.append(correctedSTH * 100)
                nabs2 = "%.2f" % (nabs * 100)
                ncu2 = "%.2f" % (ncu * 100)
                STH2 = "%.2f" % (STH * 100)
                STH3 = "%.2f" % (correctedSTH * 100)
                Xh2 = "%.2f" % Xh9
                Xo2 = "%.2f" % Xo9
                B = [pH, Xh2, Xo2, nabs2, ncu2, STH2, STH3]  # Ҫ�����ֵ

                C.append(B)
        return C,PH,STH1
    def get_E(self, Xh9, Xo9, Eg):
        if Xh9 >= 0.2 and Xo9 >= 0.6:
            E = Eg
        elif Xh9 < 0.2 and Xo9 >= 0.6:
            E = Eg + 0.2 - Xh9
        elif Xh9 >= 0.2 and Xo9 < 0.6:
            E = Eg + 0.6 - Xo9
        elif Xh9 < 0.2 and Xo9 < 0.6:
            E = Eg + 0.8 - Xh9 - Xo9
        return max(E, 0.31)
    def plot(self, save_path):
        # Janus_Z ���͵ĳ�ͼ�߼�
        pass
    def Janus_Z_STH(self,s,VLC,xh,xo):
        emax = np.max(self.h)
        # ����С�ݶ�
        DEmin = np.min(np.gradient(self.l))
        dEmin = np.min(np.gradient(self.h))
        Emax = np.max(self.l)
        emax = np.max(self.h)
        # ����С�ݶ�
        DEmin = np.min(np.gradient(self.l))
        dEmin = np.min(np.gradient(self.h))
        mpl.rcParams.update(mpl.rcParamsDefault)
        plt.close('all')
        Eg1 = np.linspace(0, 3, 301)
        Eg2 = np.linspace(0, 3, 301)
        Y, X = np.meshgrid(Eg1, Eg2)
        dEmin = np.min(np.gradient(self.l))
        E11 = 1.9
        E22 = 1.39
        r = []
        Z = []
        maxx = []
        ans = 0
        max1 = 0
        min1 = 1000
        for i in zip(Eg1):
            for j in zip(Eg2):
                if i+j < 1.23:
                    r.append(np.nan)
                    continue
                if j >= 0.2 and i >= 0.6:
                    if Eg < 0.31:
                        Eg = 0.31
                    E = Eg
                elif j < 0.2 and i >= 0.6:
                    E = Eg + 0.2 - j
                    if E < 0.31:
                        E = 0.31
                    if Eg < 0.31:
                        Eg = 0.31
                elif j >= 0.2 and i < 0.6:
                    E = Eg + 0.6 - i
                    if E < 0.31:
                        E = 0.31
                    if Eg < 0.31:
                        Eg = 0.31
                elif j < 0.2 and i < 0.6:
                    E = Eg + 0.8 - i - j
                    if E < 0.31:
                        E = 0.31
                    if Eg < 0.31:
                        Eg = 0.31
                Eintp = np.arange(Eg, DEmin + Emax, DEmin)
                eintp = np.arange(E, emax + dEmin, dEmin)
                Jintp = np.interp(Eintp, self.l, self.f)
                jintp = np.interp(eintp, self.h, self.n)
                fintp = np.interp(Eintp, self.h, self.n)
                Egg = np.trapz(Jintp, Eintp)
                Eh = np.trapz(jintp, eintp)
                Ef = np.trapz(fintp, Eintp)
                nabs = Egg / 1000.37
                ncu = Eh * 1.23 / Egg
                STH = nabs * ncu
                correctedSTH = STH * 1000.37 / (1000.37 + VLC * Ef)
                if xh == round(j, 2) and xo == round(i, 2):
                    ans = correctedSTH * 100
                if correctedSTH >= max:
                    max = correctedSTH
                    xhh = round(j, 2)
                    xoo = round(i, 2)
                if correctedSTH < min:
                    min = correctedSTH
                r.append(correctedSTH * 100)
            Z.append(r)
            r = []

        fig, ax = plt.subplots()
        # fig.set_size_inches(8, 10)
        fig.set_size_inches(12, 10)

        for spine in ax.spines.values():
            spine.set_linewidth(3)
        # colors = ["#86190d","#86190d","#dc0105","#ffad0d","#edfc1b","#8efd72","#1ffee1","#03bffe","#0c08ed"]
        colors = ["#86190d", "#dc0105", "#ffad0d", "#edfc1b", "#8efd72", "#1ffee1", "#03bffe", "#0c08ed"]
        # colors = ["#0000ff", "#00ffff", "#00ff00", "#ffff00", "#da0300","#7e0004"]"#0c08ed",
        colors.reverse()
        cmap = LinearSegmentedColormap.from_list("custom_rainbow", colors)
        cmap_reversed = cmap.reversed()
        norm = mpl.colors.Normalize(vmin=min1, vmax=max1)
        # ax.rc('font', size=12, family='serif')
        mpl.rc('font', size=33, family='Times New Roman', weight='bold')

        manual_locations = [(0.22, 0.63), (0.35, 0.7), (0.5, 0.8), (0.8, 0.83), (0.9, 0.9)]

        C = ax.contour(X, Y, Z, colors='black', linewidths=0)

        cs = ax.contourf(X, Y, Z, 5, cmap=cmap)  # �����ȸ�ͼ

        x_val, y_val = np.where(np.isclose(Z, max1))
        # for i in range(len(x_val)):
        # ax.scatter(X[x_val[-1], y_val[-1]], Y[x_val[-1], y_val[-1]], marker='*', c='black', s=500)

        # ax.scatter(Eg_1, Eg_2, marker='*', c='white', s=500)

        x_val, y_val = np.where(np.isclose(Z, max1))

        points = []
        # ��ͼ�б��ZֵΪ0.5�ĵ�
        for i in range(len(x_val)):
            ax.scatter(X[x_val[i], y_val[i]], Y[x_val[i], y_val[i]], marker='*', c='black', s=20)

        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)

        ticks = [5, 10, 15, 20, 25, 30, 35]  # �̶�ֵ���������ֵ
        tick_labels = ['5', '10', '15', '20', '25', '30', '35']  # ��Ӧ�Ŀ̶ȱ�ǩ

        # ticks = [25,30,35]  # �̶�ֵ���������ֵ
        # tick_labels = ['25','30','35']  # ��Ӧ�Ŀ̶ȱ�ǩ
        cbar.set_ticks(ticks)
        cbar.set_ticklabels(tick_labels)

        # ʹ��FixedLocator��FixedFormatter
        cbar.locator = FixedLocator(ticks)
        cbar.formatter = FixedFormatter(tick_labels)

        # cbar.ax.invert_xaxis()

        cbar.ax.invert_yaxis()

        cbar.update_ticks()  # ��ʾcolorbar�Ŀ̶�ֵ

        font3 = {'family': 'Times New Roman',
                 'weight': 'bold',
                 'size': 40,
                 }
        ax.set_xlabel('Eg\u2081 (eV)', font3)
        ax.set_ylabel('Eg\u2082 (eV)', font3)

        ax.set_xticks([0, 1, 2, 3])
        ax.set_xticklabels(['0', '1', '2', '3'], fontsize=35, weight='bold', family='Times New Roman')
        ax.set_yticks([0, 1, 2, 3])
        ax.set_yticklabels(['', '1', '2', '3'], fontsize=35, weight='bold', family='Times New Roman')
        cbar.ax.tick_params(width=3, length=8)
        ax.set_xticks([0.5, 1.5, 2.5], minor=True)
        ax.set_yticks([0.5, 1.5, 2.5], minor=True)
        ax.tick_params(direction='in', which='both')
        ax.tick_params(axis='x', which='major', width=3, length=8)
        ax.tick_params(axis='x', which='minor', width=2, length=4)
        ax.tick_params(axis='y', which='major', width=3, length=8)
        ax.tick_params(axis='y', which='minor', width=2, length=4)

        plt.rcParams['savefig.dpi'] = 300  # ͼƬ����
        plt.rcParams['figure.dpi'] = 300  # �ֱ���
        # plt.gcf().subplots_adjust(left=0.05, top=0.91, bottom=0.09)
        plt.tight_layout()
        #
        plt.show()
        file_path = os.path.join(s, "STH Efficiency vs Eg1 and Eg2.png")
        fig.savefig(file_path)
        return Eg1,Eg2,Z

    def Save_JanusZ(self, Eg1, Eg2, Z, s):

        # �����ݱ��浽���ļ����е�dat�ļ�
        file_path = os.path.join(s, "STH Efficiency vs Eg1 and Eg2.dat")
        with open(file_path, "w") as file:

            file.write("{:<10}{:<10}{:<10}\n".format('Eg1', 'Eg2', '\u03B7\u2032STH (%)'))

            for i, j, k in zip(Eg1, Eg2, Z):
                file.write("{:<10.2f}{:<10.2f}".format(i, j))
                for k1 in k:
                    file.write("{:<10.2f}".format(k1))
                file.write('\n')

        pass