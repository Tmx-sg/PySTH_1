#!/usr/bin/env python3

# -*- coding: utf-8 -*-
from rich.console import Console
from tabulate import tabulate
import os
import load
# 创建 Console 对象
console = Console()
# 主菜单
def display_main_menu():
    """
    显示主界面菜单
    """
    print("---------------------------------------------------------------------")
    print("+------------------- Main Menu -------------------+")
    print("|  Welcome to the PySTH Toolkit! Choose an option |")
    print("|  below to explore the computational utilities.  |")
    print("+-------------------------------------------------+")
    print("This program allows you to calculate the solar-to-hydrogen (STH)")
    print("conversion efficiency for 4 types of photocatalytic materials.")
    print("Additionally, the program provides visualizations of the calculated ")
    print("efficiency and related parameters, helping you better understand")
    print("and analyze the results.")
    print("=========================== PySTH Toolkit ===========================")
    print(" 1) Conventional photocatalysts    ")
    print(" 2) Janus materials                ")
    print(" 3) Z-scheme systems              ")
    print(" 4) Janus Z-scheme heterojunctions ")
    print("---------------------------------------------------------------------")
    # print("=========================== Cor-functions ===========================")
    # print(" 11) Calculate efficiency    -  For conventional photocatalysts")
    # print(" 12) Generate contour map           ")
    # print()
    # print(" 21) Calculate efficiency    -  For janus materials")
    # print(" 22) Generate contour map            ")
    # print()
    # print(" 31) Calculate efficiency    -  For Z-scheme systems")
    # print(" 32) Generate contour map            ")
    # print()
    # print(" 41) Calculate efficiency    -  For janus Z-scheme heterojunctions")
    # print(" 42) Generate contour map            ")
    # print("----------------------------------------------------------------------")
    print(" 0) Quit")
    print("---------------------------------------------------------------------")

def display_sub_menu():
    print("==================== Sub-functions ====================")
    print(" 11) Calculate efficiency          -  For conventional systems")
    print(" 12) Generate Contour Map          ")
    print()
    print(" 21) Calculate Efficiency          -  For Janus materials")
    print(" 22) Generate Contour Map          ")
    print()
    print(" 31) Calculate Efficiency          -  For Z-scheme systems")
    print(" 32) Generate Contour Map          ")
    print()
    print(" 41) Calculate Efficiency          -  For Janus Z-scheme heterojunctions")
    print(" 42) Generate Contour Map          ")
    print("-------------------------------------------------------")
    print(" 0) Quit")
    print(" 9) Back")
    print("-------------------------------------------------------")
def display_sub_menu_1():
    print("=========================== Cor-functions ===========================")
    print("                   conventional photocatalysts                   ")
    print(" 11) Calculate STH efficiency    ")
    print(" 12) Generate STH efficiency map          ")
    print("---------------------------------------------------------------------")
    print(" 9) Back")
    print(" 0) Quit")
    print("---------------------------------------------------------------------")
def display_sub_menu_2():
    print("=========================== Cor-functions ===========================")
    print("                         janus materials                         ")
    print(" 21) Calculate STH efficiency    ")
    print(" 22) Generate STH efficiency map          ")
    print("---------------------------------------------------------------------")
    print(" 9) Back")
    print(" 0) Quit")
    print("---------------------------------------------------------------------")
def display_sub_menu_3():
    print("=========================== Cor-functions ===========================")
    print("                        Z-scheme systems                         ")
    print(" 31) Calculate STH efficiency   ")
    print(" 32) Generate STH efficiency map          ")
    print("---------------------------------------------------------------------")
    print(" 9) Back")
    print(" 0) Quit")
    print("---------------------------------------------------------------------")

def display_sub_menu_3_A():
    print("=========================== Cor-functions ===========================")
    print("                        Z-scheme systems                         ")
    print(" 311) The first calculation function (maximum Eg) ")
    print(" 312) The second calculation function (considering xh and xo) ")
    print("---------------------------------------------------------------------")
    print(" 9) Back")
    print(" 0) Quit")
    print("---------------------------------------------------------------------")
def display_sub_menu_4():
    print("========================= Cor-functions =============================")
    print("              janus Z-scheme heterojunctions                     ")
    print(" 41) Calculate STH efficiency   ")
    print(" 42) Generate STH efficiency map        ")
    print("---------------------------------------------------------------------")
    print(" 9) Back")
    print(" 0) Quit")
    print("---------------------------------------------------------------------")
def display_sub_menu_2_main():
    print("=========================== Cor-functions ===========================")
    print("                         janus materials                         ")
    print(" 1) xo remains unchanged (ΔΦ > 0) Figure 2 above in the paper")
    print(" 0) xo changes (ΔΦ > 0) Figure 2 below in the paper")
    print("---------------------------------------------------------------------")
    print(" 9) Back")
    print("---------------------------------------------------------------------")
def display_sub_menu_2_A():
    print("=========================== Cor-functions ===========================")
    print("                         janus materials                         ")
    print(" 211) monolayer(ΔΦ>0)    ")
    print(" 212) Heterostructure_Ⅰtype(ΔΦ > 0)          ")
    print(" 213) Heterostructure_Ⅱ type(ΔΦ > 0)          ")
    print("---------------------------------------------------------------------")
    print(" 9) Back")
    print(" 0) Quit")
    print("---------------------------------------------------------------------")


def display_sub_menu_2_B():
    print("=========================== Cor-functions ===========================")
    print("                         janus materials                         ")
    print(" 211) monolayer(ΔΦ < 0)    ")
    print(" 212) Heterostructure_Ⅰtype(ΔΦ < 0)          ")
    print(" 213) Heterostructure_Ⅱ type(ΔΦ < 0)          ")
    print("---------------------------------------------------------------------")
    print(" 9) Back")
    print(" 0) Quit")
    print("---------------------------------------------------------------------")
def display_sub_menu_4_A():
    print("=========================== Cor-functions ===========================")
    print("                        Z-scheme systems                         ")
    print(" 411) Janus_Z_systems(ΔΦ > 0)  Figure 3 (b) right in the paper ")
    print(" 412) Janus_Z_systems(ΔΦ < 0)  Figure 3 (b) left in the paper    ")
    print("---------------------------------------------------------------------")
    print(" 9) Back")
    print(" 0) Quit")
    print("---------------------------------------------------------------------")

def main():
    """
    主程序：用户交互逻辑
    """
    while True:
        # 显示主界面
        display_main_menu()
        # 获取用户输入
        try:
            choice = int(input(">>>> "))
        except ValueError:
            print("Invalid input! Please enter a number from the menu.")
            continue

        # 根据用户选择执行相应功能
        if choice == 0:
            print("Thank you for using the PySTH Toolkit. Goodbye!")
            break
        elif choice == 9:
            print("Returning to the previous menu...")
            continue
        elif choice == 1:
            while True:
                display_sub_menu_1()
                try:
                    choice1 = int(input(">>>> "))
                except ValueError:
                    print("Invalid input! Please enter a number from the menu.")
                    continue
                if choice1 in [11, 12]:
                    handle_sub_function(choice1)
                    break
                elif choice1 == 0:
                    exit(0)
                elif choice1 == 9:
                    break
                else:
                    print("Invalid choice! Please select a valid option from the menu.")
        elif choice == 2:
            while True:
                display_sub_menu_2()
                try:
                    choice1 = int(input(">>>>"))
                except ValueError:
                    print("Invalid input! Please enter a number from the menu.")
                    continue
                if choice1 in [21, 22]:
                    handle_sub_function(choice1)
                    break
                elif choice1 == 0:
                    exit(0)
                elif choice1 == 9:
                    break
                else:
                    print("Invalid choice! Please select a valid option from the menu.")
        elif choice == 3:
            while True:
                display_sub_menu_3()
                try:
                    choice1 = int(input("Enter your choice: "))
                except ValueError:
                    print("Invalid input! Please enter a number from the menu.")
                    continue
                if choice1 in [31, 32]:
                    handle_sub_function(choice1)
                    break
                elif choice1 == 0:
                    exit(0)
                elif choice1 == 9:
                    break
                else:
                    print("Invalid choice! Please select a valid option from the menu.")
        elif choice == 4:
            while True:
                display_sub_menu_4()
                try:
                    choice1 = int(input("Enter your choice: "))
                except ValueError:
                    print("Invalid input! Please enter a number from the menu.")
                    continue
                if choice1 in [41, 42]:
                    handle_sub_function(choice1)
                    break
                elif choice1 == 0:
                    exit(0)
                elif choice1 == 9:
                    break
                else:
                    print("Invalid choice! Please select a valid option from the menu.")
        elif choice in [11, 12, 21, 22, 31, 32, 41, 42]:
            handle_sub_function(choice)
            break
        else:
            print("Invalid choice! Please select a valid option from the menu.")


def handle_sub_function(choice):
    """
    处理子功能逻辑
    """
    if choice == 11:

        choice_Conventional(1)
        # 在此处调用实际的效率计算函数
    elif choice == 12:

        choice_Conventional(2)
        # 在此处调用等高线图生成函数
    elif choice == 21:
        display_sub_menu_2_main()
        choice1 = input(">>>>")
        if choice1 == '1':
            display_sub_menu_2_A()
            choice = input(">>>>")
            choice_Janus(choice,1)
        elif choice1 == '0':
            display_sub_menu_2_B()
            choice = input(">>>>")
            choice_Janus(choice,0)
        elif choice1 == '9':
            return
        # 在此处调用实际的效率计算函数
    elif choice == 22:

        choice_Janus('222',1)
        # 在此处调用等高线图生成函数
    elif choice == 31:
        display_sub_menu_3_A()

        choice1 = input(">>>>")
        if choice1 == '311':
            choice_Z(11)

        elif choice1 == '312':
            choice_Z(12)
        elif choice1 == '9':
            return
        elif choice1 == '0':
            exit(0)



        # 在此处调用实际的效率计算函数
    elif choice == 32:
        choice_Z(2)
        # 在此处调用等高线图生成函数
    elif choice == 41:
        display_sub_menu_4_A()
        choice1 = input(">>>>")
        if choice1 == '411':
            choice_Janus_Z(choice1,1)
        elif choice1 == '412':
            choice_Janus_Z(choice1,0)
        elif choice1 == '9':
            return
        elif choice1 == '0':
            exit(0)
        # 在此处调用实际的效率计算函数
    elif choice == 42:
        choice_Janus_Z('421', 0)
        # 在此处调用等高线图生成函数
    else:
        print("Invalid sub-function choice!")






def choice_Conventional(choice):
    Load = load.Conventional_photocatalysts(r'1.xls')
    s = "Conventional photocatalysts"

    console.print("[bold yellow]You selected: Conventional photocatalysts calculate[/bold yellow]")


    if choice == 1:
        print('Please enter the following parameters for conventional photocatalysts:')
        CBM = float(input('- Conduction Band Minimum (CBM) in eV:'))
        VBM = float(input('- -  Valence Band Maximum (VBM) in eV:'))
        xh = CBM + 4.44
        xo = -5.67 - VBM
        Eg = xh + xo + 1.23
        if xh < 0 or xo < 0:
            print("When the pH is 0, water cannot be split!")
            return
        flag1 = 0
        for ph in range(15):
            xh1 = xh - (ph * 0.059)
            xo1 = xo + (ph * 0.059)
            if xh1 >= 0 and xo1 >= 0:
                flag1 = 1
                D, E, F = Load.calculate(xh, xo, Eg, 0)
                break
        if flag1 == 0:
            print('And water cannot be split at any pH value!')
            return
        elif flag1 == 1:
            print('In the following pH range, photocatalytic materials can split water')
            if E[0] == E[-1]:
                print("Water can be split at pH:", E[0])
            else:
                print("pH:", E[0], "-", E[-1])
        if not os.path.exists(s):
            os.makedirs(s)
        full_path = os.path.join(s, 'STH Efficiency vs pH.png')
        print(tabulate(D, headers='firstrow', tablefmt='simple', floatfmt=".2f"))
        Load.plot(E, F, full_path)
        # 在这里添加 Conventional photocatalysts 的逻辑
        console.print("[bold yellow]The data and images have been saved to the current folder.[/bold yellow]")
        return "1"
    elif choice == 2:
        print('Please enter the following parameters for conventional photocatalysts:')
        CBM = float(input('- Conduction Band Minimum (CBM) in eV:'))
        VBM = float(input('- -  Valence Band Maximum (VBM) in eV:'))
        xh = CBM + 4.44
        xo = -5.67 - VBM
        Eg = xh + xo + 1.23
        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        D, E, F = Load.calculate(xh, xo, Eg, 0)
        if not os.path.exists(s):
            os.makedirs(s)
        #plot
        x_h, x_o, sth = Load.coSTH(0,xh,xo,s,E)
        Load.Save_coSTH(x_h,x_o,sth,s,0)
        #date
        cbm,vbm,sth = Load.CBM_VBM(0,CBM,VBM,s,0)
        Load.Save_CBM_VBM(cbm,vbm,sth,s,0)
        console.print("[bold yellow]The data and images have been saved to the current folder.[/bold yellow]")
        return "2"
        # 在这里添加 Janus materials 的逻辑
    elif choice == 0:
        console.print("[bold red]Exiting... Goodbye![/bold red]")
        exit(0)
    elif choice == 9:
        return "9"
        # 在这里添加 Z-scheme heterojunctions 的逻辑
    else:
        console.print("[bold red]Invalid choice! Please try again.[/bold red]")


def choice_Janus(choice,fa):
    Load = load.Janus_materials(r'1.xls')
    s = "Janus materials"
    console.print("[bold yellow]You selected: Janus materials calculate[/bold yellow]")

    print('ok')
    if choice == '211' or '213' and fa == 1:
        print('Please enter the following parametersfor Janus materials:')
        CBM = float(input('- Conduction Band Minimum (CBM) in eV:'))
        VBM = float(input('- -  Valence Band maximum (VBM) in eV:'))
        VLC = float(input('- -Vacuum Level Difference (ΔΦ) in eV:'))
        Eg = abs(CBM - VBM)
        xh = CBM + 4.44 + VLC
        xo = -5.67 - VBM

        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        flag1 = 0
        for ph in range(15):
            xh1 = xh - (ph * 0.059)
            xo1 = xo + (ph * 0.059)
            if xh1 >= 0 and xo1 >= 0:
                flag1 = 1
                D, E, F = Load.calculate(xh, xo, Eg, VLC)
                break
        if flag1 == 0:
            print('And water cannot be split at any pH value!')
            return
        elif flag1 == 1:
            print('In the following pH range, photocatalytic materials can split water')
            if E[0] == E[-1]:
                print("Water can be split at pH:", E[0])
            else:
                print("pH:", E[0], "-", E[-1])
        if not os.path.exists(s):
            os.makedirs(s)
        full_path = os.path.join(s, 'STH Efficiency vs pH.png')
        print(tabulate(D, headers='firstrow', tablefmt='simple', floatfmt=".2f"))
        Load.plot(E, F, full_path)
        return "1"
    elif choice == '212' and fa == 1:
        print('Please enter the following parametersfor Janus materials:')
        CBM = float(input('- Conduction Band Minimum (CBM) in eV:'))
        VBM = float(input('- -  Valence Band maximum (VBM) in eV:'))
        VLC = float(input('- -Vacuum Level Difference (ΔΦ) in eV:'))
        Eg = abs(CBM - VBM)
        xh = CBM + 4.44
        xo = -5.67 - VBM

        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        flag1 = 0
        for ph in range(15):
            xh1 = xh - (ph * 0.059)
            xo1 = xo + (ph * 0.059)
            if xh1 >= 0 and xo1 >= 0:
                flag1 = 1
                D, E, F = Load.calculate(xh, xo, Eg, VLC)
                break
        if flag1 == 0:
            print('And water cannot be split at any pH value!')
            return
        elif flag1 == 1:
            print('In the following pH range, photocatalytic materials can split water')
            if E[0] == E[-1]:
                print("Water can be split at pH:", E[0])
            else:
                print("pH:", E[0], "-", E[-1])
        if not os.path.exists(s):
            os.makedirs(s)
        full_path = os.path.join(s, 'STH Efficiency vs pH.png')
        print(tabulate(D, headers='firstrow', tablefmt='simple', floatfmt=".2f"))
        Load.plot(E, F, full_path)
        return "1"
    if choice == '221' or '223' and fa == 1:
        print('Please enter the following parametersfor Janus materials:')
        CBM = float(input('- Conduction Band Minimum (CBM) in eV:'))
        VBM = float(input('- -  Valence Band maximum (VBM) in eV:'))
        VLC = float(input('- -Vacuum Level Difference (ΔΦ) in eV:'))
        Eg = abs(CBM - VBM)
        xh = CBM + 4.44 + VLC
        xo = -5.67 - VBM

        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        D, E, F = Load.calculate(xh, xo, Eg, VLC)
        if not os.path.exists(s):
            os.makedirs(s)
        console.print("[bold yellow]You selected: Janus materials Plot[/bold yellow]")
        # plot
        x_h, x_o, sth = Load.coSTH(VLC, xh, xo, s, E)
        de, eg, sth = Load.Delta_Eg(s)
        C, V, sth = Load.CBM_VBM_J(VLC, CBM, VBM, s)
        # date
        Load.Save_coSTH(x_h, x_o, sth, s, VLC)
        Load.Save_CBM_VBM(C, V, sth, s, VLC)
        Load.Save_Delta_Eg(de, eg, sth, s)

        console.print("[bold yellow]The data and images have been saved to the current folder.[/bold yellow]")
        return "2"
    # 在这里添加 Conventional photocatalysts 的逻辑
    elif choice == '222' and fa == 1:
        print('Please enter the following parametersfor Janus materials:')
        CBM = float(input('- Conduction Band Minimum (CBM) in eV:'))
        VBM = float(input('- -  Valence Band maximum (VBM) in eV:'))
        VLC = float(input('- -Vacuum Level Difference (ΔΦ) in eV:'))
        Eg = abs(CBM - VBM)
        xh = CBM + 4.44
        xo = -5.67 - VBM

        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        D, E, F = Load.calculate(xh, xo, Eg, VLC)
        if not os.path.exists(s):
            os.makedirs(s)
        console.print("[bold yellow]You selected: Janus materials Plot[/bold yellow]")
        #plot
        x_h, x_o, sth = Load.coSTH(VLC, xh, xo, s, E)
        de, eg, sth = Load.Delta_Eg(s)
        C,V,sth = Load.CBM_VBM_J(VLC,CBM,VBM,s)
        #date
        Load.Save_coSTH(x_h, x_o, sth, s, VLC)
        Load.Save_CBM_VBM(C, V, sth, s,VLC)
        Load.Save_Delta_Eg(de, eg, sth, s)

        console.print("[bold yellow]The data and images have been saved to the current folder.[/bold yellow]")
        return "2"
    if choice == '211' or '213' and fa == 0:
        print('Please enter the following parametersfor Janus materials:')
        CBM = float(input('- Conduction Band Minimum (CBM) in eV:'))
        VBM = float(input('- -  Valence Band maximum (VBM) in eV:'))
        VLC = float(input('- -Vacuum Level Difference (ΔΦ) in eV:'))
        Eg = abs(CBM - VBM)
        xh = CBM + 4.44
        xo = -5.67 - VBM - VLC

        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        flag1 = 0
        for ph in range(15):
            xh1 = xh - (ph * 0.059)
            xo1 = xo + (ph * 0.059)
            if xh1 >= 0 and xo1 >= 0:
                flag1 = 1
                D, E, F = Load.calculate(xh, xo, Eg, VLC)
                break
        if flag1 == 0:
            print('And water cannot be split at any pH value!')
            return
        elif flag1 == 1:
            print('In the following pH range, photocatalytic materials can split water')
            if E[0] == E[-1]:
                print("Water can be split at pH:", E[0])
            else:
                print("pH:", E[0], "-", E[-1])
        if not os.path.exists(s):
            os.makedirs(s)
        full_path = os.path.join(s, 'STH Efficiency vs pH.png')
        print(tabulate(D, headers='firstrow', tablefmt='simple', floatfmt=".2f"))
        Load.plot(E, F, full_path)
        return "1"
        # 在这里添加 Conventional photocatalysts 的逻辑
    elif choice == '212' and fa == 0:
        print('Please enter the following parametersfor Janus materials:')
        CBM = float(input('- Conduction Band Minimum (CBM) in eV:'))
        VBM = float(input('- -  Valence Band maximum (VBM) in eV:'))
        VLC = float(input('- -Vacuum Level Difference (ΔΦ) in eV:'))
        Eg = abs(CBM - VBM)
        xh = CBM + 4.44 + VLC
        xo = -5.67 - VBM - VLC

        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        flag1 = 0
        for ph in range(15):
            xh1 = xh - (ph * 0.059)
            xo1 = xo + (ph * 0.059)
            if xh1 >= 0 and xo1 >= 0:
                flag1 = 1
                D, E, F = Load.calculate(xh, xo, Eg, VLC)
                break
        if flag1 == 0:
            print('And water cannot be split at any pH value!')
            return
        elif flag1 == 1:
            print('In the following pH range, photocatalytic materials can split water')
            if E[0] == E[-1]:
                print("Water can be split at pH:", E[0])
            else:
                print("pH:", E[0], "-", E[-1])
        if not os.path.exists(s):
            os.makedirs(s)
        full_path = os.path.join(s, 'STH Efficiency vs pH.png')
        print(tabulate(D, headers='firstrow', tablefmt='simple', floatfmt=".2f"))
        Load.plot(E, F, full_path)
        return "1"
    if choice == '221' or '223' and fa == 0:
        print('Please enter the following parametersfor Janus materials:')
        CBM = float(input('- Conduction Band Minimum (CBM) in eV:'))
        VBM = float(input('- -  Valence Band maximum (VBM) in eV:'))
        VLC = float(input('- -Vacuum Level Difference (ΔΦ) in eV:'))
        Eg = abs(CBM - VBM)
        xh = CBM + 4.44
        xo = -5.67 - VBM - VLC

        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        D, E, F = Load.calculate(xh, xo, Eg, VLC)
        if not os.path.exists(s):
            os.makedirs(s)
        console.print("[bold yellow]You selected: Janus materials Plot[/bold yellow]")
        # plot
        x_h, x_o, sth = Load.coSTH(VLC, xh, xo, s, E)
        de, eg, sth = Load.Delta_Eg(s)
        C, V, sth = Load.CBM_VBM_J(VLC, CBM, VBM, s)
        # date
        Load.Save_coSTH(x_h, x_o, sth, s, VLC)
        Load.Save_CBM_VBM(C, V, sth, s, VLC)
        Load.Save_Delta_Eg(de, eg, sth, s)

        console.print("[bold yellow]The data and images have been saved to the current folder.[/bold yellow]")
        return "2"
    # 在这里添加 Conventional photocatalysts 的逻辑
    elif choice == '222' and fa == 0:
        print('Please enter the following parametersfor Janus materials:')
        CBM = float(input('- Conduction Band Minimum (CBM) in eV:'))
        VBM = float(input('- -  Valence Band maximum (VBM) in eV:'))
        VLC = float(input('- -Vacuum Level Difference (ΔΦ) in eV:'))
        Eg = abs(CBM - VBM)
        xh = CBM + 4.44 + VLC
        xo = -5.67 - VBM - VLC

        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        D, E, F = Load.calculate(xh, xo, Eg, VLC)
        if not os.path.exists(s):
            os.makedirs(s)
        console.print("[bold yellow]You selected: Janus materials Plot[/bold yellow]")
        # plot
        x_h, x_o, sth = Load.coSTH(VLC, xh, xo, s, E)
        de, eg, sth = Load.Delta_Eg(s)
        C, V, sth = Load.CBM_VBM_J(VLC, CBM, VBM, s)
        # date
        Load.Save_coSTH(x_h, x_o, sth, s, VLC)
        Load.Save_CBM_VBM(C, V, sth, s, VLC)
        Load.Save_Delta_Eg(de, eg, sth, s)

        console.print("[bold yellow]The data and images have been saved to the current folder.[/bold yellow]")
        return "2"
        # 在这里添加 Janus materials 的逻辑
    elif choice == '0':
        console.print("[bold red]Exiting... Goodbye![/bold red]")
        exit(0)
    elif choice == '9':
        return
        # 在这里添加 Z-scheme heterojunctions 的逻辑
    else:
        console.print("[bold red]Invalid choice! Please try again.[/bold red]")




def choice_Z(choice):
    Load = load.Z_scheme_systems(r'1.xls')
    s = "Z-scheme systems"
    console.print("[bold yellow]You selected: Z-scheme systems Calculate[/bold yellow]")


    if choice == 11:
        print('Please enter the following parametersfor Z-scheme systems:')
        Eg1 = float(input('--The first single-layer bandgap (Eg1) in eV:'))
        Eg2 = float(input('-The second single-layer bandgap (Eg2) in eV:'))
        xh  = float(input('- - - - - -Hydrogen evolution reaction in eV:'))
        xo  = float(input('- - - - - - -Oxygen evolution reaction in eV:'))

        if Eg1 + Eg2 < 1.23 or xh <0 or xo <0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        STH = Load.calculate_1(Eg1, Eg2)

        console.print("The STH efficiency is :","%.2f" % (STH),"%")
        return "1"
    if choice == 12:
        print('Please enter the following parametersfor Z-scheme systems:')
        Eg1 = float(input('--The first single-layer bandgap (Eg1) in eV:'))
        Eg2 = float(input('-The second single-layer bandgap (Eg2) in eV:'))
        xh = float(input('- - - - - -Hydrogen evolution reaction in eV:'))
        xo = float(input('- - - - - - -Oxygen evolution reaction in eV:'))

        if Eg1 + Eg2 < 1.23 or xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        D, E, F = Load.calculate_2(Eg1, Eg2,xh,xo)

        if not os.path.exists(s):
            os.makedirs(s)
        full_path = os.path.join(s, 'STH Efficiency vs pH.png')
        print(tabulate(D, headers='firstrow', tablefmt='simple', floatfmt=".2f"))
        Load.plot(E, F, full_path)
        return "1"

        # 在这里添加 Conventional photocatalysts 的逻辑
    elif choice == 2:
        print('Please enter the following parametersfor Z-scheme systems:')
        Eg1 = float(input('--The first single-layer bandgap (Eg1) in eV:'))
        Eg2 = float(input('-The second single-layer bandgap (Eg2) in eV:'))
        xh = float(input('- - - - - -Hydrogen evolution reaction in eV:'))
        xo = float(input('- - - - - - -Oxygen evolution reaction in eV:'))

        if Eg1 + Eg2 < 1.23:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        STH = Load.calculate_2(Eg1, Eg2,xh,xo)
        console.print("[bold yellow]You selected: Z-scheme systems Mapjp[/bold yellow]")
        if not os.path.exists(s):
            os.makedirs(s)
        #plot
        Eg1,Eg2,Z = Load.Z_STH(s)

        #date
        Load.Save_Z(Eg1,Eg2,Z,s)

        console.print("[bold yellow]The data and images have been saved to the current folder.[/bold yellow]")
        return "2"
        # 在这里添加 Janus materials 的逻辑
    elif choice == 0:
        console.print("[bold red]Exiting... Goodbye![/bold red]")
        return "0"
    elif choice == 9:
        return "9"
        # 在这里添加 Z-scheme heterojunctions 的逻辑
    else:
        console.print("[bold red]Invalid choice! Please try again.[/bold red]")


def choice_Janus_Z(choice,fa):
    Load = load.Janus_Z_scheme_heterojunctions(r'1.xls')
    s = "Janus Z-scheme"
    if not os.path.exists(s):
        os.makedirs(s)
    console.print("[bold yellow]You selected: Janus Z-scheme calculate[/bold yellow]")


    if choice == '411' and fa == 1:
        print('Please enter the following parametersfor Janus Z-scheme:')
        Eg1 = float(input('- -The first single-layer bandgap in eV:'))
        Eg2 = float(input('- The second single-layer bandgap in eV:'))
        VLC = float(input('- - -Vacuum level difference (ΔΦ) in eV:'))
        xh = float(input('- - - -Hydrogen evolution reaction in eV:'))
        xo = float(input('- - - - -Oxygen evolution reaction in eV:'))
        Eg = max(Eg1, Eg2)
        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        flag1 = 0
        for ph in range(15):
            xh1 = xh - (ph * 0.059) + VLC
            xo1 = xo + (ph * 0.059)
            if xh1 >= 0 and xo1 >= 0:
                flag1 = 1
                D, E, F = Load.calculate_max(xh, xo, Eg, VLC)
                break
        if flag1 == 0:
            print('And water cannot be split at any pH value!')
            return
        elif flag1 == 1:
            print('In the following pH range, photocatalytic materials can split water')
            if E[0] == E[-1]:
                print("Water can be split at pH:", E[0])
            else:
                print("pH:", E[0], "-", E[-1])
        full_path = os.path.join(s, 'STH Efficiency vs pH.png')
        print(tabulate(D, headers='firstrow', tablefmt='simple', floatfmt=".2f"))
        Load.plot(E, F, full_path)
        return "1"
        # 在这里添加 Conventional photocatalysts 的逻辑
    elif choice == '412' and fa == 0:
        print('Please enter the following parametersfor Janus Z-scheme:')
        Eg1 = float(input('- -The first single-layer bandgap in eV:'))
        Eg2 = float(input('- The second single-layer bandgap in eV:'))
        VLC = float(input('- - -Vacuum level difference (ΔΦ) in eV:'))
        xh = float(input('- - - -Hydrogen evolution reaction in eV:'))
        xo = float(input('- - - - -Oxygen evolution reaction in eV:'))
        Eg = max(Eg1, Eg2)
        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        flag1 = 0
        for ph in range(15):
            xh1 = xh - (ph * 0.059)
            xo1 = xo + (ph * 0.059) - VLC
            if xh1 >= 0 and xo1 >= 0:
                flag1 = 1
                D, E, F = Load.calculate_min(xh, xo, Eg, VLC)
                break
        if flag1 == 0:
            print('And water cannot be split at any pH value!')
            return
        elif flag1 == 1:
            print('In the following pH range, photocatalytic materials can split water')
            if E[0] == E[-1]:
                print("Water can be split at pH:", E[0])
            else:
                print("pH:", E[0], "-", E[-1])
        full_path = os.path.join(s, 'STH Efficiency vs pH.png')
        print(tabulate(D, headers='firstrow', tablefmt='simple', floatfmt=".2f"))
        Load.plot(E, F, full_path)
        return "1"

    if choice == '421' and fa == 1:
        print('Please enter the following parametersfor Janus Z-scheme:')
        Eg1 = float(input('- - - - - -The first single-layer bandgap in eV:'))
        Eg2 = float(input('- - - - - The second single-layer bandgap in eV:'))
        VLC = float(input('- - - - - - -Vacuum Level Difference (ΔΦ) in eV:'))
        xh = float(input('-Hydrogen evolution reaction overpotential in eV:'))
        xo = float(input('- -Oxygen evolution reaction overpotential in eV:'))
        Eg = max(Eg1, Eg2)
        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        D, E, F = Load.calculate(xh, xo, Eg, VLC)
        console.print("[bold yellow]You selected: Janus Z-scheme heterojunctions Mapjp[/bold yellow]")
        Eg1, Eg2, Z = Load.Janus_Z_STH(s, VLC, xh, xo)

        Load.Save_JanusZ(Eg1, Eg2, Z, s)
        console.print("[bold yellow]The data and images have been saved to the current folder.[/bold yellow]")
        return "2"
        # 在这里添加 Conventional photocatalysts 的逻辑
    elif choice == '421' and fa == 0:
        print('Please enter the following parametersfor Janus Z-scheme:')
        Eg1 = float(input('- - - - - -The first single-layer bandgap in eV:'))
        Eg2 = float(input('- - - - - The second single-layer bandgap in eV:'))
        VLC = float(input('- - - - - - -Vacuum Level Difference (ΔΦ) in eV:'))
        xh = float(input('-Hydrogen evolution reaction overpotential in eV:'))
        xo = float(input('- -Oxygen evolution reaction overpotential in eV:'))
        Eg = max(Eg1, Eg2)
        if xh < 0 or xo < 0:
            console.print("[bold yellow]No  NO  NO[/bold yellow]")
            return
        # D, E, F = Load.calculate(xh, xo, Eg, VLC)
        console.print("[bold yellow]You selected: Janus Z-scheme heterojunctions Mapjp[/bold yellow]")
        Eg1, Eg2, Z = Load.Janus_Z_STH(s, VLC, xh, xo)

        Load.Save_JanusZ(Eg1, Eg2, Z, s)
        console.print("[bold yellow]The data and images have been saved to the current folder.[/bold yellow]")
        return "2"
        # 在这里添加 Janus materials 的逻辑
    elif choice == 0:
        console.print("[bold red]Exiting... Goodbye![/bold red]")
        return "0"
    elif choice == 9:
        return "9"
        # 在这里添加 Z-scheme heterojunctions 的逻辑
    else:
        console.print("[bold red]Invalid choice! Please try again.[/bold red]")



if __name__ == "__main__":
    main()